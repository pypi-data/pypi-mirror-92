import requests


URL = 'https://elitescrims.xyz/api/v1/'


class EliteCreative:
    def __init__(self, key):
        self.session = requests.Session()
        self.session.headers.update({'authorization': key})

    def get_user_stats(self, user_id):
        return self.session.get(URL + 'stats/%s' % user_id).json()

    def get_user_queue(self, user_id):
        return self.session.get(URL + 'queue/%s' % user_id).json()

    def in_game(self, user_id):
        return self.session.get(URL + 'ingame/%s' % user_id).json()

    def get_match_by_game_id(self, game_id):
        return self.session.get(URL + 'match-by-id/%s' % game_id).json()

    def get_match_by_user_id(self, user_id):
        return self.session.get(URL + 'match-by-user/%s' % user_id).json()

    def get_team_by_team_id(self, team_id):
        return self.session.get(URL + 'team-by-id/%s' % team_id).json()

    def get_team_by_user_id(self, user_id):
        return self.session.get(URL + 'team-by-user/%s' % user_id).json()
