from datetime import datetime

from tinydb import TinyDB, Query, where


class Player(object):
    def __init__(self, firstname=None, lastname=None, birthdate=None, sex=None, ranking=None, point=None):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.sex = sex
        self.ranking = ranking
        self.serialized_player = {}
        self.point = point

    def __str__(self):
        return "{self.firstname}, {self.lastname}, {self.birthdate}, {self.sex}, {self.ranking}".format(self=self)

    def view_player(self):
        return ("%s %s %s %s %s" % (self.firstname.ljust(15), self.lastname.ljust(15), self.birth.ljust(15), self.gender.ljust(15), str(self.ranking).ljust(15)))

    def serialization_player(self):
        self.serialized_player = {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birthdate': self.birthdate.strftime('%d/%m/%Y'),
            'sex': self.sex,
            'ranking': self.ranking
        }

    def get_serialized_player(self):
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
    def update_point_player(self):
        db = TinyDB('db.json', indent=4)
        table = db.table('players')
        User = Query()
        print(table.get(doc_id=2))
        mySearch = table.get(doc_id=2)
        print(mySearch['firstname'])

        value = 99
        table.update({'point': value}, where(
            'firstname') == mySearch['firstname'])

    @ classmethod
    def sort_players_by_ranking(self, serialized_players):
        serialized_players = (
            sorted(serialized_players, key=lambda i: i['ranking']))
        return (serialized_players)

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
