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

from typing import Dict, Any, Optional
from flask_login import current_user
from bundesliga_tippspiel.actions.Action import GetAction
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.exceptions import ActionException
from bundesliga_tippspiel.db.match_data.Match import Match
from bundesliga_tippspiel.Config import Config


class GetBetAction(GetAction):
    """
    Action that allows retrieving bets from the database
    """

    def __init__(
            self,
            _id: Optional[int] = None,
            user_id: Optional[int] = None,
            match_id: Optional[int] = None,
            matchday: Optional[int] = None,
            include_other_users_bets: bool = False
    ):
        """
        Initializes the GetBetAction object
        :param _id: If provided, returns the bet with the specified ID
        :param user_id: If provided, will only provide bets for the
                        specified user
        :param match_id: If provided, will only provide bets for the
                         specified match
        :param matchday: If provided, will only provide bets for the specified
                         matchday
        :param include_other_users_bets: If True, will include bets from other
                                         users even if the match hasn't started
                                         yet.
        :raises: ActionException if any problems occur
        """
        super().__init__(_id)
        self.user_id = None if user_id is None else int(user_id)
        self.match_id = None if match_id is None else int(match_id)
        self.matchday = None if matchday is None else int(matchday)
        self.include_other_users_bets = include_other_users_bets

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        self.check_id_or_filters(
            self.id,
            [self.user_id, self.match_id, self.matchday]
        )
        self.matchday = self.resolve_and_check_matchday(self.matchday)

    def _execute(self) -> Dict[str, Any]:
        """
        Registers an unconfirmed user in the database
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        if self.id is not None:
            result = [self.handle_id_fetch(self.id, Bet)]
            if not result[0].match.started \
                    and not current_user.id == result[0].user.id:
                raise ActionException(
                    "ID not accessible",
                    "Die angegebene ID kann nicht eingesehen werden",
                    401
                )

        else:

            query = Bet.query

            if self.user_id is not None:
                query = query.filter_by(user_id=self.user_id)
            if self.match_id is not None:
                query = query.filter_by(match_id=self.match_id)
            if self.matchday is not None:
                query = query.filter(Bet.match.has(matchday=self.matchday))

            query = query.join(Match).filter(Match.season == Config.season())

            result = query.all()
            if not self.include_other_users_bets:
                result = list(filter(
                    lambda x: x.match.started or current_user.id == x.user_id,
                    result
                ))

            result.sort(key=lambda x: x.match.kickoff)

        return self.prepare_get_response(result, "bet")

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            _id=data.get("id"),
            user_id=data.get("user_id"),
            match_id=data.get("match_id"),
            matchday=data.get("matchday"),
            include_other_users_bets=False
        )
