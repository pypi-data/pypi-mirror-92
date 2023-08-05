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

from typing import Dict, Any, Optional, List
from jerrycan.base import db
from jerrycan.db.User import User
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.Config import Config


class LeaderboardAction(Action):
    """
    Action that allows fetching a sorted leaderboard
    """

    def __init__(
            self,
            matchday: Optional[int] = None,
            count: bool = False,
            include_bots: bool = False,
            bets: Optional[List[Bet]] = None
    ):
        """
        Initializes the LeaderboardAction object
        :param matchday: The matchday for which to generate the leaderboard.
                         If None, will use the most current matchday
        :param count: If set to true, will count the amount of bets instead
                      of evaluating their points
        :param include_bots: Whether or not to include bots.
                             Bots are identified by a robot or brain emoji
        :param bets: Allows using a specific set of bets to calculate
                     the leaderboard
        """
        self.matchday = None if matchday is None else int(matchday)
        self.count = count
        self.include_bots = include_bots
        self.bets = bets

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        if self.matchday is not None:
            self.matchday = self.resolve_and_check_matchday(self.matchday)

    def _execute(self) -> Dict[str, Any]:
        """
        Confirms a previously registered user
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        pointmap = {}
        usermap = {}
        for user in User.query.filter_by(confirmed=True).all():

            if not self.include_bots and "🤖" in user.username:
                continue  # Ignore bots

            pointmap[user.id] = 0
            usermap[user.id] = user

        if self.bets is None:
            self.bets = [
                x for x in
                Bet.query
                .options(db.joinedload(Bet.match))
                .options(db.joinedload(Bet.user))
                .all()
                if x.match.season == Config.season()
            ]

        if self.matchday is not None:
            self.bets = [
                x for x in self.bets if x.match.matchday <= self.matchday
            ]

        for bet in self.bets:

            if bet.user_id not in pointmap:
                continue

            if self.count:
                pointmap[bet.user_id] += 1
            else:
                pointmap[bet.user_id] += bet.evaluate(True)

        leaderboard = []
        for user_id, points in pointmap.items():
            leaderboard.append((usermap[user_id], points))

        leaderboard.sort(key=lambda x: x[0].id)
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        return {"leaderboard": leaderboard}

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            matchday=data.get("matchday"),
            include_bots=data.get("include_bots", "0") == "1"
        )
