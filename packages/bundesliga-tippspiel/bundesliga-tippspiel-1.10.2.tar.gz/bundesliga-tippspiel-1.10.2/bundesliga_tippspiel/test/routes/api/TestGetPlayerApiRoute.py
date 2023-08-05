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

from typing import Dict, Any, Type
from bundesliga_tippspiel.actions.Action import Action
from bundesliga_tippspiel.actions.GetPlayerAction import GetPlayerAction
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.api.GetterApiRouteTestFramework import \
    _GetterApiRouteTestFramework


class TestGetPlayerApiRoute(_GetterApiRouteTestFramework):
    """
    Tests the /player GET API route
    """

    @property
    def keyword(self) -> str:
        """
        :return: The route keyword.
        """
        return "player"

    @property
    def sample_filters(self) -> Dict[str, Any]:
        """
        :return: A sample dictionary of filters with appropriate values
        """
        return {
            "team_id": 1
        }

    @property
    def action_cls(self) -> Type[Action]:
        """
        :return: The action class used to fetch data
        """
        return GetPlayerAction
