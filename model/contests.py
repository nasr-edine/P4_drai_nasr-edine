import json
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
