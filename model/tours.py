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
        # print("matches: ", pair)
        # print("pair[0]: ", pair[0])
        # print("pair: ", pair)
        # print("match 1 value: ", pair[1])
        # print("match 2 value: ", pair[2])
        # print("match 3 value: ", pair[3])
        n = 0
        serialized_match = {
            #     'match 1': pair[0],
            #     'match 2': pair[1],
            #     'match 3': pair[2],
            #     'match 4': pair[3]
            # }
            "match " + str(n): pair[n] for n in range(4)
        }
        return serialized_match

    def serialization_round(self):
        serialized_round = {
            # "roundName": self.round_name,
            "matches": self.serialize_match(),
            "start_datetime": str(self.start_datetime),
            "end_datetime": str(self.end_datetime),
        }
        return serialized_round

    @ classmethod
    def create_pair_matches(self, id_player1, id_player2, nb_match, players, contest, round_nb):
        faker = Faker()
        list_matchs = []

        score1 = 0
        score2 = 0
        list1 = [id_player1, score1]
        if round_nb == 0:
            players[id_player1].point = score1

        list2 = [id_player2, score2]
        if round_nb == 0:
            players[id_player2].point = score2

        tuple_match = (list1, list2)
        contest.rounds[round_nb].matches[nb_match] = tuple_match

    @ classmethod
    def match_generator_round1(self, list_players, round, contest, round_nb):
        list_players = []
        for player in contest.players:
            list_players.append(player.id_player)
        # #print(list_players)
        i = 0
        for n in range(4):
            if round_nb == 0:
                Tour.create_pair_matches(
                    list_players[n], list_players[n + 4], n, contest.players, contest, round_nb)
            else:
                Tour.create_pair_matches(
                    list_players[i], list_players[i + 1], n, contest.players, contest, round_nb)
                i += 2
