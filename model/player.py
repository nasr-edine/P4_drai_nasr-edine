import random
from datetime import datetime
from tinydb import TinyDB, Query, where
from faker import Faker

from controller.read_input import ReadInformation


class Player(object):
    def __init__(self, id_player=None, firstname=None, lastname=None, birthdate=None, sex=None, ranking=None, point=0):
        self.id_player = id_player
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.sex = sex
        self.ranking = ranking
        self.serialized_player = {}
        self.point = point
        self.history_match = []

    def __str__(self):
        # return "{self.firstname}, {self.lastname}, {self.birthdate}, {self.sex}, {self.ranking}".format(self=self)
        return "|firstname: {:15} |laatname: {:10} |id: {}   |ranking: {}   |point: {}|".format(self.firstname, self.lastname, self.id_player, self.ranking, self.point)

    def __repr__(self):
        return "name: {:10} {:10} id: {}   ranking: {}   point: {}\n".format(self.firstname, self.lastname, self.id_player, self.ranking, self.point)

    def view_player(self):
        return ("name: %s %s id: %s ranking: %s point: %s" % (self.lastname.ljust(10), self.firstname.ljust(10), str(self.id_player).ljust(2), str(self.ranking).ljust(2), str(self.point).ljust(2)))

    def display_player(self):
        return "|firstname: {:15} |lastname: {:10} |ranking: {}|".format(self.firstname, self.lastname, self.ranking)

    def get_serialized_player(self):
        return self.serialized_player

    def serialization_player(self):
        self.serialized_player = {
            'id_player': self.id_player,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birthdate': self.birthdate.strftime('%d/%m/%Y'),
            'sex': self.sex,
            'ranking': self.ranking,
            'point': self.point
        }
        return self.serialized_player

    def deserializing_player(self, player):
        self.id_player = player['id_player']
        self.firstname = player['firstname']
        self.lastname = player['lastname']
        self.birthdate = player['birthdate']
        self.sex = player['sex']
        self.ranking = player['ranking']
        self.point = player['point']

    @ classmethod
    def sort_players_by_point(self, players):
        players.sort(key=lambda x: x.point, reverse=True)
        return (players)

    @ classmethod
    def sort_players_by_ranking(self, players):
        players.sort(key=lambda x: x.ranking)
        return (players)

    @ classmethod
    def sort_players_by_name(self, players):
        players.sort(key=lambda x: x.lastname)
        return (players)

    @ classmethod
    def create_players(self):
        read_input = ReadInformation()
        players = []
        random_list = []
        random_list = (list(range(1, 9)))
        random.shuffle(random_list)

        faker = Faker()
        # create rounds
        for n in range(0, 8):

            # Enter informations about a player
            # firstname = read_input.read_name(1)
            # lastname = read_input.read_name(2)
            # birthdate = read_input.read_date(1)
            # sex = read_input.read_sex()
            # ranking = read_input.read_ranking()

            # create a fake list of 8 players
            profile = faker.simple_profile()
            name = profile['name'].split()
            firstname = name[0]
            lastname = name[1]
            birthdate = profile['birthdate']
            sex = profile['sex']
            ranking = random_list[n]
            # Create an instance of a player
            player = Player(n, firstname, lastname,
                            birthdate, sex, ranking)
            # serialize a player
            serialized_player = player.serialization_player()
            # Add all serialized players in a list
            players.append(player)
        return(players)
