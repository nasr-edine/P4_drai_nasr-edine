from tinydb import TinyDB, Query
from tours import Tour


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

    @classmethod
    def setContests(self, serialized_contests):
        db = TinyDB('db.json', indent=4)
        contests_table = db.table('contests')
        contests_table.truncate()  # clear the table first
        contests_table.insert(serialized_contests)

    # @classmethod
    # def get_rounds(self):

    #     # for item in self.rounds:
    #     # print(item)
    #     # list.append(item)
    #     return self.rounds
