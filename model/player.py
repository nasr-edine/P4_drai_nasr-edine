import random
from datetime import datetime
from tinydb import TinyDB, Query, where
from faker import Faker


class Player(object):
    def __init__(self, id_player, firstname=None, lastname=None, birthdate=None, sex=None, ranking=None, point=0):
        self.id_player = id_player
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.sex = sex
        self.ranking = ranking
        self.serialized_player = {}
        self.point = point

    def __str__(self):
        return "{self.firstname}, {self.lastname}, {self.birthdate}, {self.sex}, {self.ranking}".format(self=self)

    def __repr__(self):
        return "name: {:10} {:10} id: {}   ranking: {}   point: {}\n".format(self.firstname, self.lastname, self.id_player, self.ranking, self.point)

    def view_player(self):
        return ("%s %s %s %s %s" % (self.firstname.ljust(15), self.lastname.ljust(15), self.birth.ljust(15), self.gender.ljust(15), str(self.ranking).ljust(15)))

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

    def deserialize_player(self, index):
        db = TinyDB('db.json', indent=4)
        table = db.table('players')
        dict_player = table.get(doc_id=index)
        # player = Player(dict_player['firstname'], dict_player['lastname'],
        # datetime.strptime(dict_player['birthdate'], '%d/%m/%Y').date(), dict_player['sex'], dict_player['ranking'])

        self.firstname = dict_player['firstname']
        self.lastname = dict_player['lastname']
        self.birthdate = datetime.strptime(
            dict_player['birthdate'], '%d/%m/%Y').date()
        self.sex = dict_player['sex']
        self.ranking = dict_player['ranking']
        self.serialized_player = {}
        # print(self)
        # return player

    @ classmethod
    def savePlayersInDb(self, players):
        serialized_players = []
        for player in players:
            serialized_player = player.serialization_player()
            # serialized_player = player.get_serialized_player()
            serialized_players.append(serialized_player)
        Player.saveAllPlayers(serialized_players)

    @ classmethod
    def update_point_player(self, index_player, score):
        db = TinyDB('db.json', indent=4)
        table = db.table('players')
        # print(table.get(doc_id=index_player))
        mySearch = table.get(doc_id=index_player)
        # print(mySearch['firstname'])

        table.update({'point': score}, where(
            'firstname') == mySearch['firstname'])

    @ classmethod
    def getNamePlayer(self, index_player):
        db = TinyDB('db.json', indent=4)
        table = db.table('players')
        mySearch = table.get(doc_id=index_player)
        # print(mySearch['firstname'])
        return mySearch['firstname']

    @ classmethod
    def sort_players_by_point(self):
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        serialized_players = (
            sorted(players_table, key=lambda i: i['point']))
        return (serialized_players)

    @ classmethod
    def sort_players_by_point(self, players):
        # db = TinyDB('db.json', indent=4)
        # players_table = db.table('players')
        players.sort(key=lambda x: x.point, reverse=True)
        # print(players)
        return (players)
        # serialized_players = (
        #     sorted(players_table, key=lambda i: i['point']))
        # return (serialized_players)

    @ classmethod
    def sort_players_by_ranking(self, players):
        players.sort(key=lambda x: x.ranking)
        return (players)

    @ classmethod
    def getPlayerIndex(self):
        db = TinyDB('db.json', indent=4)
        table = db.table('players')
        eids = list(table._read_table().keys())
        return eids

    @ classmethod
    def saveAllPlayers(self, serialized_players):
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        players_table.truncate()  # clear the table first
        players_table.insert_multiple(serialized_players)

    @ classmethod
    def getAll(self):
        db = TinyDB('db.json')
        players_table = db.table('players')
        result = []
        for item in players_table:
            player = Player(item['firstname'], item['lastname'],
                            datetime.strptime(item['birthdate'], '%d/%m/%Y').date(), item['sex'], item['ranking'])
            result.append(player)
        return result

    @ classmethod
    def getAll2(self):
        result = []
        db = TinyDB('db.json')
        players_table = db.table('players')
        serialized_players = players_table.all()
        for item in serialized_players:
            player = Player(item['firstname'], item['lastname'],
                            item['birth'], item['gender'], item['ranking'])
            result.append(player)
        return result

    @ classmethod
    def create_players(self):
        # serialized_players = []
        players = []
        list1 = []
        list1 = (list(range(1, 9)))
        random.shuffle(list1)

        faker = Faker()
        # create rounds
        for n in range(0, 8):
            # create a list of 8 players
            profile = faker.simple_profile()
            name = profile['name'].split()
            firstname = name[0]
            lastname = name[1]
            birthdate = profile['birthdate']
            sex = profile['sex']
            ranking = list1[n]
            # Create an instance of a player
            player = Player(n, firstname, lastname,
                            birthdate, sex, ranking)
            # serialize a player
            serialized_player = player.serialization_player()
            # Add all serialized players in a list
            # Create a list of players
            players.append(player)

        # print("fake data users saved in DB")
        # print(players)
        # input()
        return(players)

    @ classmethod
    def Sorting_players_by_ranking(self, players):
        # Sorting players by ranking
        players = Player.sort_players_by_ranking(players)
        # print("after sorting by ranking")
        # print(players)
        # input()
        return players
