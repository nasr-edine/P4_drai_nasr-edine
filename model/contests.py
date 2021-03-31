import json
import random

from tinydb import TinyDB, Query, where

from model.tours import Tour
from model.player import Player


class Contest(object):
    def __init__(self, name=None, location=None, date=None, time_control=None, comments=None, players=None, nb_turns=4):
        # def __init__(self, name, location, date, time_control, comments, players, nb_turns=4):
        self.name = name
        self.location = location
        self.date = date
        self.nb_turns = nb_turns
        self.time_control = time_control
        self.comments = comments
        self.rounds = []
        self.players = players

    def __str__(self):
        return "name: {self.name}, \nlocation: {self.location}, \ndate: {self.date}, \nnb turns: {self.nb_turns}, \ntime control: {self.time_control}, \ncomments: {self.comments}, \nplayers: \n {self.players}".format(self=self)

    def __repr__(self):
        return "name: {self.name},\nlocation: {self.location},\ndate: {self.date},\nnb turns: {self.nb_turns},\ntime control: {self.time_control},\ncomments: {self.comments},\nplayers:\n{self.players}\n\n".format(self=self)

    def add_rounds(self, round):
        self.rounds.append(round)

    # Create a list of rounds
    def create_rounds(self, nb_rounds):
        for i in range(nb_rounds):
            self.add_rounds(Tour('Round ' + str(i)))

    def create_matches(self, nb_rounds, nb_matches):
        for i in range(nb_matches):
            for j in range(nb_matches):
                self.rounds[i].add_matches([])

    # get a list of serialized players
    def serialization_players(self):
        serialized_players = []
        for player in self.players:
            # serialize a player
            serialized_player = player.serialization_player()
            # Add all serialized players in a list
            serialized_players.append(serialized_player)
        return serialized_players

    # Serialize a contest
    def serialization_contest(self):
        self.serialized_contest = {
            'name': self.name,
            'location': self.location,
            'date': str(self.date),
            'nb_turns': self.nb_turns,
            'time_control': self.time_control,
            'comments': self.comments,
            # "rounds":   self.rounds.serialization_round(),
            "rounds":   {round.round_name: round.serialization_round() for round in self.rounds},
            'players': self.serialization_players()
        }

    def get_id(self):
        db = TinyDB('db.json', indent=4)
        contests_table = db.table('contests')
        doc = contests_table.search(where('name') == self.name)
        return doc[0].doc_id

    # Save a contest in database
    def save(self):
        db = TinyDB('db.json', indent=4)
        contests_table = db.table('contests')
        # contests_table.truncate()  # clear the table first
        contests_table.insert(self.serialized_contest)

    def deserializing_players_list(self, players_dict):
        self.players = []
        for player_item in players_dict:
            player = Player()
            player.deserializing_player(player_item)
            self.players.append(player)

    def deserializing_rounds(self, rounds):
        self.rounds = []
        # print(type(rounds), ':\n')
        # print(rounds, '\n')
        # print(rounds['Round 0']['matches'])
        # print(rounds['Round 0']['matches']['match 1'])
        # print(rounds['Round 0']['matches']['match 2'])
        # print(rounds['Round 0']['matches']['match 3'])
        for key, value in rounds.items():

            # print(f'name:    {key}')
            # print(f"matches: {value['matches']}")
            # print(f"start:   {value['start_datetime']}")
            # print(f"end:     {value['end_datetime']}")
            # print()
            round = Tour(key, value['start_datetime'], value['end_datetime'])
            for key2, value2 in value['matches'].items():
                list1 = []
                list2 = []
                # print(key2)
                # print('type value: ', type(value2))
                # print('value: ', value2)
                if not value2:
                    # print('there are no match in this contest')
                    pass
                else:
                    # print('type: ', type(value2[0]))

                    # print('player 1: ', value2[0][0])
                    # print('score 1: ', value2[0][1])
                    # print('player 2: ', value2[1][0])
                    # print('score 2: ', value2[1][1])
                    list1 = [value2[0][0], value2[0][1]]
                    list2 = [value2[1][0], value2[1][1]]
                    match_tuple = (list1, list2)
                    round.matches.append(match_tuple)

                # print()
                # self.rounds[0].matches[]

            self.rounds.append(round)
        #     for key2, value2 in value.items():
        #         print(f'[{key2}]: {value2}')
        #         print()
        #         for key3, value3 in value.items():
        #             print(f'[{key3}]: {value3}')
        #         print()
        #     print()
        # for round_item in rounds:
        # print(type(round_item))
        # print((round_item))
        # round = Tour()
        # print(type(round_item['start_datetime']))
        # round.start_datetime = round_item['start_datetime']
        # round.end_datetime = round_item['end_datetime']

    def deserializing_contest(self, contest):
        self.name = contest['name']
        self.location = contest['location']
        self.date = contest['date']
        self.nb_turns = contest['nb_turns']
        self.time_control = contest['time_control']
        self.comments = contest['comments']
        self.deserializing_rounds(contest['rounds'])
        self.deserializing_players_list(contest['players'])

    def get_contest(self, id):
        db = TinyDB('db.json', indent=4)
        contests_table = db.table('contests')
        deserialize_contest = contests_table.get(doc_id=id)

    @ classmethod
    def get_contests_data(self):
        contests = []
        db = TinyDB('db.json', indent=4)
        contest_table = db.table('contests')
        for item in contest_table:
            contest = Contest()
            contest.deserializing_contest(item)
            contests.append(contest)
        return contests

    def get_players_contest(self, contest_name):
        db = TinyDB('db.json', indent=4)
        contests_table = db.table('contests')
        contest_doc = contests_table.search(
            where('name') == contest_name)
        if not contest_doc:
            return -1
        else:
            self.deserializing_contest(contest_doc[0])
            return 0
            # return doc[0].doc_id

    @ classmethod
    def get_contests(self):
        contests = Contest.get_contests_data()
        return contests

    # display matches
    def display_round(self, nb_round, total_nb_matches):
        for match in range(total_nb_matches):
            print(self.rounds[nb_round].matches[match])

    # save scores for matches in Round 0

    def save_scores(self, nb_round, nb_matches):
        win = 1
        lose = 0
        draw = 0.5
        for nb_match in range(nb_matches):
            # attribute score for player 1
            score1 = random.choice([win, lose, draw])
            self.rounds[nb_round].matches[nb_match][0][1] = score1
            for x in self.players:
                if x.id_player == self.rounds[nb_round].matches[nb_match][0][0]:
                    if nb_round == 0:
                        x.point = score1
                    else:
                        x.point += score1
                    break
            if score1 == win:
                score2 = lose
            elif score1 == lose:
                score2 = win
            else:
                score2 = draw
            # attribute score for player 2
            self.rounds[nb_round].matches[nb_match][1][1] = score2
            for y in self.players:
                if y.id_player == self.rounds[nb_round].matches[nb_match][1][0]:
                    if nb_round == 0:
                        y.point = score2
                    else:
                        y.point += score2
                    break
    # save scores for matches in Round 0

    def save_scores2(self, nb_round, nb_matches, result_matches):
        win = 1
        lose = 0
        draw = 0.5
        for nb_match in range(nb_matches):
            # attribute score for player 1
            # score1 = random.choice([win, lose, draw])
            if result_matches[nb_match] == 1:
                score1 = win
                score2 = lose
            elif result_matches[nb_match] == 2:
                score1 = lose
                score2 = win
            else:
                score1 = draw
                score2 = draw
            id_player1 = 0
            id_player2 = 0
            self.rounds[nb_round].matches[nb_match][0][1] = score1
            for x in self.players:
                if x.id_player == self.rounds[nb_round].matches[nb_match][0][0]:
                    # player1 = x
                    # id_player1 = x.id_player
                    if nb_round == 0:
                        x.point = score1
                    else:
                        x.point += score1
                    break
            # attribute score for player 2
            self.rounds[nb_round].matches[nb_match][1][1] = score2
            for y in self.players:
                if y.id_player == self.rounds[nb_round].matches[nb_match][1][0]:
                    # player2 = y
                    # id_player2 = y.id_player
                    if nb_round == 0:
                        y.point = score2
                    else:
                        y.point += score2
                    break
            # player1.history_match.append(id_player2)
            # player2.history_match.append(id_player1)
