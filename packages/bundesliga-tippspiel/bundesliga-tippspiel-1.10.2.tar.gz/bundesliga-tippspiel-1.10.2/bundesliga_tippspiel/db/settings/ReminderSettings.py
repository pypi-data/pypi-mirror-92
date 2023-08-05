"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of bundesliga-tippspiel.

bundesliga-tippspiel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

bundesliga-tippspiel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""


from flask import render_template
from typing import List
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
from smtplib import SMTPAuthenticationError
from jerrycan.base import app, db
from jerrycan.db.ModelMixin import ModelMixin
from jerrycan.db.TelegramChatId import TelegramChatId
from puffotter.smtp import send_email
from jerrycan.db.User import User
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.enums import ReminderType
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.db.match_data.Match import Match


class ReminderSettings(ModelMixin, db.Model):
    """
    Database model that keeps track of reminder settings
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "reminder_settings"
    """
    The name of the table
    """

    __table_args__ = (
        db.UniqueConstraint(
            "reminder_type",
            "user_id",
            name="unique_reminder_settings"
        ),
    )
    """
    Makes sure that each user can  only have one reminder setting of one type
    """

    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    """
    The ID of the user associated with this setting
    """

    user: User = db.relationship(
        "User",
        backref=db.backref("reminder_settings", cascade="all, delete")
    )
    """
    The user associated with this setting
    """

    reminder_type = db.Column(db.Enum(ReminderType), nullable=False)
    """
    The type of reminder
    """

    active = db.Column(db.Boolean, nullable=False, default=True)
    """
    Whether the reminder is active or not
    """

    reminder_time: int = db.Column(db.Integer, nullable=False, default=86400)
    """
    The time before the next unbet match when the reminder message
    will be sent.
    Unit: seconds
    """

    last_reminder: str = db.Column(db.String(19), nullable=False,
                                   default="1970-01-01:01-01-01")
    """
    The time when the last reminder was sent. Format in the form
    %Y-%m-%d:%H-%M-%S
    """

    @property
    def reminder_time_delta(self) -> timedelta:
        """
        :return: The 'reminder_time' parameter as a datetime timedelta
        """
        return timedelta(seconds=self.reminder_time)

    @property
    def last_reminder_datetime(self) -> datetime:
        """
        :return: The 'last_reminder' parameter as a datetime object
        """
        return datetime.strptime(self.last_reminder, "%Y-%m-%d:%H-%M-%S")

    def set_reminder_time(self, reminder_time: int):
        """
        Sets the reminder time and resets the time stored as the last reminder
        :param reminder_time: the new reminder time
        :return: None
        """
        self.reminder_time = reminder_time
        self.last_reminder = "1970-01-01:01-01-01"
        db.session.commit()

    def get_due_matches(self) -> List[Match]:
        """
        Checks if the reminder is due and returns a list of matches that the
        user still needs to bet on.
        :return: The matches for which the reminder is due
        """
        app.logger.debug("Checking for due reminders for user {}."
                         .format(self.user.username))

        now = datetime.utcnow()
        start = max(now, self.last_reminder_datetime)
        start_str = start.strftime("%Y-%m-%d:%H-%M-%S")
        then = now + self.reminder_time_delta
        then_str = then.strftime("%Y-%m-%d:%H-%M-%S")

        due_matches = Match.query \
            .filter_by(season=Config.season()) \
            .filter(start_str < Match.kickoff) \
            .filter(Match.kickoff < then_str) \
            .all()

        user_bets = Bet.query \
            .filter_by(user_id=self.user_id) \
            .join(Match) \
            .filter(Match.season == Config.season()) \
            .all()
        betted_matches = list(map(lambda x: x.match_id, user_bets))

        to_remind = list(filter(
            lambda x: x.id not in betted_matches,
            due_matches
        ))

        app.logger.debug("Matches to remind: {}.".format(to_remind))

        return to_remind

    def send_reminder(self):
        """
        Sends a reminder message if it's due
        :return: None
        """
        due = self.get_due_matches()
        if len(due) < 1:
            app.logger.debug("No due reminders found")
            return
        else:
            app.logger.debug("Sending reminder to {}.".format(self.user.email))
            message = render_template(
                "email/reminder.html",
                user=self.user,
                matches=due,
                hours=int(self.reminder_time / 3600)
            )
            self.send_reminder_message(message)
            last_match = max(due, key=lambda x: x.kickoff)
            self.last_reminder = last_match.kickoff
            db.session.commit()

    def send_reminder_message(self, message: str):
        """
        Sends a reminder message using the appropriate method of delivery
        :param message: The message to send
        :return: None
        """
        if self.reminder_type == ReminderType.EMAIL:
            try:
                send_email(
                    self.user.email,
                    "Tippspiel Erinnerung",
                    message,
                    Config.SMTP_HOST,
                    Config.SMTP_ADDRESS,
                    Config.SMTP_PASSWORD,
                    Config.SMTP_PORT
                )
            except SMTPAuthenticationError:
                app.logger.error("Invalid SMTP settings, failed to send email")
        elif self.reminder_type == ReminderType.TELEGRAM:
            telegram = TelegramChatId.query.filter_by(user=self.user).first()
            if telegram is not None:
                message = BeautifulSoup(message, "html.parser").text
                message = "\n".join([x.strip() for x in message.split("\n")])
                telegram.send_message(message)
