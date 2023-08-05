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

from flask import Blueprint
from flask_login import login_required
from bundesliga_tippspiel.utils.routes import action_route
from bundesliga_tippspiel.actions.SetReminderSettingsAction import \
    SetReminderSettingsAction


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/set_reminder", methods=["POST"])
    @login_required
    @action_route
    def set_reminder():
        """
        Allows the user to set an email reminder
        :return: The response
        """
        action = SetReminderSettingsAction.from_site_request()
        return action.execute_with_redirects(
            "user_management.profile",
            "Erinnerungsdaten gespeichert",
            "user_management.profile"
        )

    return blueprint
