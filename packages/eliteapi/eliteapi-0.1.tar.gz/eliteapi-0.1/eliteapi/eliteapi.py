import requests


URL = 'https://elitescrims.xyz/api/v1/'


class EliteCreative:
    def __init__(self, key):
        self.headers = {'authorization': key}

    def get_user_stats(self, user_id):
        response = requests.get(URL + f'stats/{user_id}', headers=self.headers)

        return response.json()

    def get_user_queue(self, user_id):
        response = requests.get(URL + f'queue/{user_id}', headers=self.headers)

        return response.json()

    def in_game(self, user_id):
        response = requests.get(URL + f'ingame/{user_id}', headers=self.headers)

        return response.json()

    def get_match_by_game_id(self, game_id):
        response = requests.get(URL + f'match-by-id/{game_id}', headers=self.headers)

        return response.json()

    def get_match_by_user_id(self, user_id):
        response = requests.get(URL + f'match-by-user/{user_id}', headers=self.headers)

        return response.json()

    def get_team_by_team_id(self, team_id):
        response = requests.get(URL + f'team-by-id/{team_id}', headers=self.headers)

        return response.json()

    def get_team_by_user_id(self, user_id):
        response = requests.get(URL + f'team-by-user/{user_id}', headers=self.headers)

        return response.json()
