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
from bundesliga_tippspiel.actions.Action import GetAction
from bundesliga_tippspiel.db.match_data.Player import Player


class GetPlayerAction(GetAction):
    """
    Action that allows retrieving players from the database
    """

    def __init__(
            self,
            _id: Optional[int] = None,
            team_id: Optional[int] = None
    ):
        """
        Initializes the GetPlayerAction object
        :param _id: If provided, will only fetch the selected ID
        :param team_id: If provided, will only fetch players
                        in the selected team
        :raises: ActionException if any problems occur
        """
        super().__init__(_id)
        self.team_id = None if team_id is None else int(team_id)

    def validate_data(self):
        """
        Validates user-provided data
        :return: None
        :raises ActionException: if any data discrepancies are found
        """
        self.check_id_or_filters(self.id, [self.team_id])

    def _execute(self) -> Dict[str, Any]:
        """
        Registers an unconfirmed user in the database
        :return: A JSON-compatible dictionary containing the response
        :raises ActionException: if anything went wrong
        """
        if self.id is not None:
            result = [self.handle_id_fetch(self.id, Player)]

        else:

            query = Player.query

            if self.team_id is not None:
                query = query.filter_by(team_id=self.team_id)

            result = query.all()
            result.sort(key=lambda x: x.name)

        return self.prepare_get_response(result, "player")

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]):
        """
        Generates an action from a dictionary
        :param data: The dictionary containing the relevant data
        :return: The generated Action object
        """
        return cls(
            _id=data.get("id"),
            team_id=data.get("team_id")
        )
