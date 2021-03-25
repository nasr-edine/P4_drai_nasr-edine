import json
import random

from tinydb import TinyDB, Query

from model.tours import Tour


class Contest(object):
    def __init__(self, name, location, date, time_control, comments, players, nb_turns=4):
        self.name = name
        self.location = location
        self.date = date
        self.nb_turns = nb_turns
        self.time_control = time_control
        self.comments = comments
        self.rounds = []
        self.players = players

    def __str__(self):
        return '{self.name}'.format(self=self)

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

    # Save a contest in database
    def save(self):
        db = TinyDB('db.json', indent=4)
        contests_table = db.table('contests')
        contests_table.truncate()  # clear the table first
        contests_table.insert(self.serialized_contest)

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
    # @ classmethod
    # def input_contest()
