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

from unittest import mock
from typing import List, Optional, Tuple
from bundesliga_tippspiel.Config import Config
# noinspection PyProtectedMember
from bundesliga_tippspiel.test.routes.RouteTestFramework import \
    _RouteTestFramework


class TestForgotPasswordRoute(_RouteTestFramework):
    """
    Class that tests the /forgot route
    """

    @property
    def route_info(self) -> Tuple[str, List[str], Optional[str], bool]:
        """
        Info about the route to test
        :return: The route's path,
                 the route's primary methods,
                 A phrase found on the route's GET page.
                 None if no such page exists,
                 An indicator for if the page requires authentication or not
        """
        return "/forgot", ["POST"], " Passwort vergessen", False

    @mock.patch("jerrycan.routes.user_management.verify_recaptcha",
                lambda x, y, z: True)
    def test_successful_requests(self):
        """
        Tests (a) successful request(s)
        :return: None
        """
        user = self.generate_sample_user(True)[0]
        user.email = Config.SMTP_ADDRESS
        self.db.session.commit()

        old_hash = user.password_hash

        with mock.patch(
                "jerrycan.routes.user_management.send_email",
                lambda x, y, z, a, b, c, d:
                self.assertEqual(x, Config.SMTP_ADDRESS)
        ):
            post = self.client.post("/forgot", follow_redirects=True, data={
                "email": Config.SMTP_ADDRESS,
                "g-recaptcha-response": ""
            })

        self.assertNotEqual(old_hash, user.password_hash)
        self.assertTrue(b"Passwort erfolgreich zur" in post.data)

    @mock.patch("jerrycan.routes.user_management.verify_recaptcha",
                lambda x, y, z: True)
    def test_unsuccessful_requests(self):
        """
        Tests (an) unsuccessful request(s)
        :return: None
        """
        failed_post = self.client.post(
            "/forgot",
            follow_redirects=True,
            data={
                "email": Config.SMTP_ADDRESS,
                "g-recaptcha-response": ""
            }
        )
        self.assertTrue(b"Passwort erfolgreich zur" in failed_post.data)
