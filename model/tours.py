from tinydb import TinyDB, Query
from faker import Faker


class Tour(object):
    def __init__(self, round_name='Round X', start_datetime='0000-00-00', end_datetime='0000-00-00'):
        self.round_name = round_name  # Round 1 - N
        self.matches = []
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def add_matches(self, match):
        self.matches.append(match)

    def __str__(self):
        return 'round nb: {self.round_name} match: {self.matches}'.format(self=self)
    # Serialize a round

    def print_matches(self):
        return "{:10} {:10} {}\n".format(self.firstname, self.lastname, self.ranking)

    def serialize_match(self):
        pair = self.matches
        n = 0
        serialized_match = {
            "match " + str(n): pair[n] for n in range(4)
        }
        return serialized_match

    def serialization_round(self):
        serialized_round = {
            "matches": self.serialize_match(),
            "start_datetime": str(self.start_datetime),
            "end_datetime": str(self.end_datetime),
        }
        return serialized_round

    @ classmethod
    def create_pair_matches(self, id_player1, id_player2, nb_match, contest, round_nb):
        # faker = Faker()
        list_matchs = []
        first_round = 0
        init_score = 0

        match_player1 = [id_player1, init_score]
        match_player2 = [id_player2, init_score]

        # Init scores for all players to 0 for first time
        if round_nb == first_round:
            contest.players[id_player1].point = init_score
            contest.players[id_player2].point = init_score

        # Insert tuple match in  my contest object
        contest.rounds[round_nb].matches[nb_match] = (
            match_player1, match_player2)

    @ classmethod
    def matches_generator(self, contest, round_nb):
        list_players = []
        first_round = 0
        for player in contest.players:
            list_players.append(player.id_player)
        i = 0
        for nb_player in range(4):
            if round_nb == first_round:
                Tour.create_pair_matches(
                    list_players[nb_player], list_players[nb_player + 4], nb_player, contest, round_nb)
            else:
                Tour.create_pair_matches(
                    list_players[i], list_players[i + 1], nb_player, contest, round_nb)
                i += 2
