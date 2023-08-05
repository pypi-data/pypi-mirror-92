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
from bundesliga_tippspiel.db.user_generated.SeasonPositionBet import \
    SeasonPositionBet
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.models.ModelTestFramework import \
    _ModelTestFramework


class TestSeasonPositionBet(_ModelTestFramework):
    """
    Tests the SeasonPositionBet SQL model
    """

    def setUp(self):
        """
        Sets up the data needed by the tests
        :return: None
        """
        super().setUp()
        self.model_cls = SeasonPositionBet
        self.position_bet = SeasonPositionBet(
            user=self.user_one, season=2010,
            team=self.team_one, position=7
        )
        db.session.add(self.position_bet)
        db.session.commit()

    def test_missing_column_data(self):
        """
        Tests that missing column data is handled correctly
        :return: None
        """
        self._test_missing_column_data([
            SeasonPositionBet(
                season=2000,
                team=self.team_one, position=7
            ),
            SeasonPositionBet(
                user=self.user_one,
                team=self.team_one, position=7
            ),
            SeasonPositionBet(
                user=self.user_one, season=2000,
                position=7
            ),
            SeasonPositionBet(
                user=self.user_one, season=2000,
                team=self.team_one
            )
        ])

    def test_uniqueness(self):
        """
        Tests that unique attributes are correctly checked
        :return: None
        """
        self._test_uniqueness([
            SeasonPositionBet(
                user=self.user_one, season=2010,
                team=self.team_one, position=7
            ),
            SeasonPositionBet(
                user=self.user_one, season=2010,
                team=self.team_one, position=10
            )
        ])

    def test_cascades(self):
        """
        Tests if cascade deletes work correctly
        :return: None
        """
        self.assertEqual(len(SeasonPositionBet.query.all()), 1)
        db.session.delete(self.user_one)
        self.assertEqual(len(SeasonPositionBet.query.all()), 0)

    def test_json_representation(self):
        """
        Tests the JSON representation of the model
        :return: None
        """
        without_children = self.position_bet.__json__(False)
        without_children.update({
            "user":
                self.position_bet.user.__json__(
                    True, ["season_position_bets"]
                ),
            "team": self.position_bet.team.__json__(
                True, ["season_position_bets"]
                )
        })
        self.assertEqual(
            self.position_bet.__json__(True),
            without_children
        )

    def test_string_representation(self):
        """
        Tests the str and repr methods of the model
        :return: None
        """
        self._test_string_representation(self.position_bet)
