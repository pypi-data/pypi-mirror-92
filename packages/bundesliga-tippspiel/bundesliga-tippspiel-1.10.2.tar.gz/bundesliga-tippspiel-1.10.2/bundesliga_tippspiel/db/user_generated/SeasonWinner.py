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

from jerrycan.base import db
from jerrycan.db.User import User
from jerrycan.db.ModelMixin import ModelMixin
from bundesliga_tippspiel.Config import Config


class SeasonWinner(ModelMixin, db.Model):
    """
    Model that describes the 'season_winners' SQL table
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "season_winners"
    """
    The name of the table
    """

    season: int = db.Column(db.Integer, unique=True, nullable=False)
    """
    The season for which this is the winner
    """

    user_id: int = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    """
    The ID of the user that won the competition
    """

    user: User = db.relationship(
        "User", backref=db.backref("season_winners", cascade="all, delete")
    )
    """
    The user that won the competition
    """

    @property
    def season_string(self) -> str:
        """
        :return: The season string, e.g. 2019/20
        """
        return Config.season_string(self.season)
