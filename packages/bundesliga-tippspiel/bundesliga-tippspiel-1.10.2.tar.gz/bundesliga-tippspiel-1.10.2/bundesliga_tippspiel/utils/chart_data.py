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

from typing import List, Tuple, Dict, Optional
from jerrycan.base import db
from jerrycan.db.User import User
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.actions.LeaderboardAction import LeaderboardAction
from bundesliga_tippspiel.Config import Config
from bundesliga_tippspiel.db.match_data.Match import Match


def generate_leaderboard_data(
        current_matchday: Optional[int] = None,
        bets: Optional[List[Bet]] = None,
        include_bots: bool = False
) -> Tuple[int, Dict[str, Tuple[str, List[int]]]]:
    """
    Generates leaderboard data for the rankings chart
    :param current_matchday: The current matchday
    :param bets: A list of bets to work on. If not provided, will
                 load all bets in the database
    :param include_bots: Whether or not to include bots
    :return: A tuple consisting of the matchday to display
             and the leaderboard data:
                 username: (colour, list of positions per matchday)
    """
    chart_colors = ["red", "blue", "yellow",
                    "green", "purple", "orange",
                    "brown", "black", "gray"]

    if current_matchday is None:  # pragma: no cover
        leaderboard_action = LeaderboardAction()
        current_matchday = leaderboard_action.resolve_and_check_matchday(-1)
        matchday_matches = Match.query.filter_by(matchday=current_matchday,
                                                 finished=True,
                                                 season=Config.season()).all()
        if len(matchday_matches) == 0 and current_matchday is not None:
            current_matchday -= 1

    leaderboard_history = load_leaderboard_history(
        current_matchday=current_matchday,
        bets=bets,
        include_bots=include_bots
    )
    leaderboard_data: Dict[str, Tuple[str, List[int]]] = {}

    for leaderboard in leaderboard_history:

        for index, (user, points) in enumerate(leaderboard):

            if user.username not in leaderboard_data:
                color = chart_colors[index % len(chart_colors)]
                leaderboard_data[user.username] = (color, [])

            position = index + 1
            leaderboard_data[user.username][1].append(position)

    return current_matchday, leaderboard_data  # type: ignore


def load_leaderboard_history(
        current_matchday: Optional[int] = None,
        bets: Optional[List[Bet]] = None,
        include_bots: bool = False
) -> List[List[Tuple[User, int]]]:
    """
    Generates historical leaderboard data for chart generation
    :param current_matchday: The current matchday
    :param bets: A list of bets to work on. If not provided, will
                 load all bets in the database
    :param include_bots: Whether or not to include bots
    :return: The list of leaderboard lists
    """

    history = []

    if current_matchday is None:  # pragma: no cover
        leaderboard_action = LeaderboardAction()
        current_matchday = leaderboard_action.resolve_and_check_matchday(-1)

    if bets is None:
        bets = Bet.query \
            .options(db.joinedload(Bet.match)) \
            .options(db.joinedload(Bet.user)) \
            .filter(Match.season == Config.season()) \
            .all()
    users = User.query.filter_by(confirmed=True).all()
    if not include_bots:
        users = [user for user in users if "🤖" not in user.username]

    for matchday in range(1, current_matchday + 1):  # type: ignore

        pointmap = {}
        usermap = {}
        for user in users:
            pointmap[user.id] = 0
            usermap[user.id] = user

        matchday_bets = list(filter(
            lambda x: x.match.matchday <= matchday,
            bets
        ))

        for bet in matchday_bets:
            if not include_bots and "🤖" in bet.user.username:
                continue
            pointmap[bet.user_id] += bet.evaluate(True)

        leaderboard = []
        for user_id, points in pointmap.items():
            leaderboard.append((usermap[user_id], points))
        leaderboard.sort(key=lambda x: x[1], reverse=True)

        history.append(leaderboard)

    return history
