import json
from tinydb import TinyDB, Query

from model.tours import Tour


class Contest(object):
    def __init__(self, name, location, date, player_index, time_control, comments, rounds, nb_turns=4):
        self.name = name
        self.location = location
        self.date = date
        self.nb_turns = nb_turns
        self.player_index = player_index
        self.time_control = time_control
        self.comments = comments
        self.rounds = rounds
        self.serialized_contest = {}

    def __str__(self):
        return '{self.name}'.format(self=self)
    # Serialize a contest

    def serialization_contest(self):
        # print(self.rounds)
        self.serialized_contest = {
            'name': self.name,
            'location': self.location,
            'date': str(self.date),
            'nb_turns': self.nb_turns,
            'players_index': self.player_index,
            'time_control': self.time_control,
            'comments': self.comments,
            # 'rounds':  self.rounds

            # "rounds": {self.rounds[0].round_name: self.rounds[0].serialization_round()}


            "rounds":   {item.round_name: item.serialization_round() for item in self.rounds}
        }

        # }

    # Save a contest in database
    def save(self):
        db = TinyDB('db.json', indent=4)
        contests_table = db.table('contests')
        contests_table.truncate()  # clear the table first
        contests_table.insert(self.serialized_contest)
