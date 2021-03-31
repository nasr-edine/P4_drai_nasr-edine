from tinydb import TinyDB, Query
from faker import Faker

import numpy as np


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

    def display_matches(self):
        string = ""
        match_nb = 0
        for match in self.matches:
            # print(match)
            # string += f"|{9 * ' '}{match[0]} : {match[1]}{11 * ' '}|\n"
            string += f"|match {match_nb}:{27 * ' '}|\n"
            match_nb += 1
            string += "|{}player id: {} score: {}{}|\n".format(
                9 * ' ', match[0][0], match[0][1], 5 * ' ')
            string += "|{}player id: {} score: {}{}|\n".format(
                9 * ' ', match[1][0], match[1][1], 5 * ' ')
        return string

    def display_round(self):
        return "|name   : {:25} |\n|{:35}|\n|start  : {:20}|\n|end    : {:24}|\n|matches:{:27}|\n{}|".format(
            self.round_name, "", self.start_datetime, self.end_datetime, '', self.display_matches())

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
    def create_pair_matches(self, id_player1, id_player2, nb_match, contest, round_nb, list_players, list_players_already_assigned):
        # faker = Faker()
        list_matchs = []
        first_round = 0
        init_score = 0
        list_number = list(range(0, 8))
        # print(list_number)
        for x in contest.players:
            if x.id_player == id_player1:
                if id_player2 in x.history_match:
                    new_list = list_number.copy()
                    new_list.remove(id_player1)
                    main_list = np.setdiff1d(new_list, x.history_match)
                    main_list2 = np.setdiff1d(
                        main_list, list_players_already_assigned)
                    id_player2 = int(main_list2[0])
                # index = list_players.index(id_player2)
                # if index + 1 == 8:
                # index = -1
                # id_player2 = list_players[index + 1]
                x.history_match.append(id_player2)
        for y in contest.players:
            if y.id_player == id_player2:
                y.history_match.append(id_player1)
        match_player1 = [id_player1, init_score]
        match_player2 = [id_player2, init_score]
        list_players_already_assigned.append(id_player1)
        list_players_already_assigned.append(id_player2)
        # Init scores for all players to 0 for first time
        if round_nb == first_round:
            contest.players[id_player1].point = init_score
            contest.players[id_player2].point = init_score

        # Insert tuple match in  my contest object
        contest.rounds[round_nb].matches[nb_match] = (
            match_player1, match_player2)
        return list_players_already_assigned

    @ classmethod
    def matches_generator(self, contest, round_nb):
        list_players = []
        # list_players2 = []
        first_round = 0
        for player in contest.players:
            list_players.append(player.id_player)
            # list_players2.append(str(player.id_player))
        i = 0
        list_players_already_assigned = []
        for nb_player in range(4):
            if round_nb == first_round:

                ret_list = Tour.create_pair_matches(
                    list_players[nb_player], list_players[nb_player + 4], nb_player, contest, round_nb, list_players, list_players_already_assigned)
                list_players_already_assigned += ret_list
            else:
                ret_list = Tour.create_pair_matches(
                    list_players[i], list_players[i + 1], nb_player, contest, round_nb, list_players, list_players_already_assigned)
                list_players_already_assigned += ret_list
                i += 2
