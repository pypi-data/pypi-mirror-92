from .util import http_get
import requests

root_url = 'https://tryhackme.com'


class THM(object):
    """
    TryHackMe API Wrapper
    """

    def __init__(self, credentials=None):
        """
        Initializes the API Wrapper

        :type credentials: dict
        :param credentials: (Optional) Credentials for use with authenticated requests
        """

        self.session = requests.Session()

        # if (credentials is not None) and (type(credentials) == dict):
        #     if ('username' in credentials) and ('password' in credentials):
        #         self.__login(credentials)

    #
    # Statistics
    #
    def get_stats(self) -> dict:
        """
        Returns public and cloneable room count and current user count

        :return: Dict containing mentioned values
        """

        return http_get(self.session, f'{root_url}/api/getstats')

    #
    # Leaderboard
    #
    def get_leaderboard(self) -> list:
        """
        Returns the top 50 users from the all-time leaderboard

        :return: List containing top 50 users
        """

        return http_get(self.session, f'{root_url}/api/leaderboards')['topUsers']

    def get_monthly_leaderboard(self) -> list:
        """
        Returns the top 50 users from the monthly leaderboard

        :return: List containing top 50 users
        """

        return http_get(self.session, f'{root_url}/api/leaderboards')['topUsersMonthly']

    #
    # Team
    #
    def get_teams(self) -> list:
        """
        Returns all teams

        :return: List containing all teams
        """

        return http_get(self.session, f'{root_url}/api/all-teams')

    #
    # User
    #
    def user_exists(self, username) -> bool:
        """
        Checks if a username is taken

        :param username: Username to check
        :return:
        """

        return http_get(self.session, f'{root_url}/api/user-exist/{username}')['success']

    def user_created_rooms(self, username) -> list:
        """
        Gets a list of rooms created by a user

        :param username: Username to check
        :return: List of rooms created by this user
        """

        return http_get(self.session, f'{root_url}/api/created-rooms/{username}', has_success=True)['rooms']

    def user_completed_room_count(self, username) -> int:
        """
        Gets the amount of completed rooms by a user

        :param username: Username to check
        :return:
        """

        return http_get(self.session, f'{root_url}/api/roomscompleted/{username}')['completed']

    def user_all_completed_rooms(self, username) -> list:
        """
        Gets all rooms completed by a user

        :param username: Username to check
        :return: List of rooms (with all data) completed by this user
        """

        return http_get(self.session, f'{root_url}/api/all-completed-rooms/{username}')

    def user_badges(self, username) -> list:
        """
        Gets the list of badges a user has

        :param username: Username to check
        :return: List of badges
        """

        return http_get(self.session, f'{root_url}/api/get-badges/{username}')

    def user_activity(self, username) -> list:
        """
        Gets the user's activity feed

        :param username: Username to check
        :return: List of events
        """

        return http_get(self.session, f'{root_url}/api/get-activity-events/{username}', has_success=True)['data']

    def user_discord(self, token) -> dict:
        """
        Gets the user's data from his discord integration token

        :param token: Discord integration token
        :return: User data
        """

        return http_get(self.session, f'{root_url}/tokens/discord/{token}', has_success=True)

    def user_stats(self, username) -> dict:
        """
        Gets the user's basic data

        :param username: Username to check
        :return: User data (rank, points, avatar)
        """

        return http_get(self.session, f'{root_url}/api/user/{username}')

    def user_rank(self, username) -> int:
        """
        Gets the user's rank

        :param username: Username to check
        :return: User's rank
        """

        return http_get(self.session, f'{root_url}/api/usersRank/{username}')

    #
    # King of the Hill
    #
    def koth_machine_pool(self) -> list:
        """
        Gets the current koth machine pool

        :return: Machine list
        """

        return http_get(self.session, f'{root_url}/games/koth/get/machine-pool')

    def koth_game_data(self, game_id) -> dict:
        """
        Gets data about a koth game

        :type game_id: int
        :param game_id: Game id
        :return: Game data
        """

        return http_get(self.session, f'{root_url}/games/koth/data/{game_id}', has_success=True)

    def koth_recent_games(self) -> list:
        """
        Gets 5 most recently finished koth games

        :return: List of 4 most recent koth games
        """

        return http_get(self.session, f'{root_url}/games/koth/recent/games')

    #
    # Room
    #
    def room_details(self, room_code) -> dict:
        """
        Gets details of a specific room

        :param room_code: Room code
        :return: Room data
        """

        return http_get(self.session, f'{root_url}/api/room/{room_code}', has_success=True)

    def room_new_rooms(self) -> list:
        """
        Gets a list of 6 newest rooms

        :return: List of newest rooms
        """

        return http_get(self.session, f'{root_url}/api/newrooms')

    def room_graph_data(self, room_code, user_count=10) -> list:
        """
        Gets a list of top {user_count} users from a room for the graph

        :param room_code: Room code
        :type user_count: int
        :param user_count: Amount of user the call should return
        :return: List of users on the scoreboard
        """

        return http_get(self.session, f'{root_url}/api/getgraphdata/{user_count}/{room_code}')

    def room_issues(self, room_code) -> dict:
        """
        Gets issues from a specific room

        :param room_code: Room code
        :return: Room issues
        """

        return http_get(self.session, f'{root_url}/api/get-issues/{room_code}', has_success=True)['data']

    def room_votes(self, room_code) -> int:
        """
        Gets votes for a specific room

        :param room_code: Room code
        :return: Room votes
        """

        return http_get(self.session, f'{root_url}/api/get-votes/{room_code}') #/api/weekly-challenge-rooms

    def room_weekly_challenges(self) -> list:
        """
        Gets a list of weekly challenge rooms

        :return: List of weekly challenge rooms
        """

        return http_get(self.session, f'{root_url}/api/weekly-challenge-rooms')
