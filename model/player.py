import datetime
from tinydb import TinyDB, Query, where


class Player(object):
    def __init__(self, id_player=None, firstname=None,
                 lastname=None, birthdate=None,
                 sex=None, ranking=None, point=0):
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
        string = ""
        row = 101 * "-"
        string += row + "\n"
        a = "| id player".ljust(20)
        b = "| firstname".ljust(20)
        c = "| lastname".ljust(20)
        d = "| birthdate".ljust(20)
        e = "| ranking".ljust(20)
        f = "|"
        string += a + b + c + d + e + f
        string += "\n" + row + "\n"

        a = "| "+str(self.id_player).ljust(18)
        b = "| "+self.firstname.ljust(18)
        c = "| "+self.lastname.ljust(18)
        d = "| "+str(self.birthdate).ljust(18)
        e = "| "+str(self.ranking).ljust(18)
        f = "|"
        string += a + b + c + d + e + f
        string += "\n" + row + "\n"
        return string

    def contains_player(self):
        db = TinyDB('db.json')
        players = db.table('players')
        User = Query()
        birthdate = self.birthdate.strftime('%d/%m/%Y')
        ret = players.contains((User.lastname == self.lastname.lower()))
        player_dict = players.search(
            where('lastname') == self.lastname.lower())
        if ret is True:
            for player_item in player_dict:
                if player_item['firstname'] == self.firstname.lower() \
                    and player_item['sex'] == self.sex.lower() and \
                        player_item['birthdate'] == birthdate:
                    return True
        else:
            return False

    def get_serialized_player(self):
        return self.serialized_player

    def update_ranking(self):
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        players_table.update(
            {'ranking': self.ranking}, doc_ids=[self.id_player])

    def update_ranking2(self, id, ranking):
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        print()
        ret = players_table.contains(doc_id=id)
        if ret is True:
            player_dict = players_table.get(doc_id=id)
            self.deserializing_player(player_dict)
            self.ranking = ranking
            players_table.update(
                {'ranking': self.ranking}, doc_ids=[id])
            return 1
        else:
            return 0

    @ classmethod
    def get_players_data(self):
        players = []
        db = TinyDB('db.json', indent=4)
        player_table = db.table('players')
        for item in player_table:
            player = Player()
            player.deserializing_player(item)
            players.append(player)
        # print("len: ", len(players))
        return players

    @ classmethod
    def get_players(self):
        players = Player.get_players_data()
        return players

    # @ classmethod
    def save_player(self):
        serialized_player = self.serialization_player()
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        id = players_table.insert(serialized_player)
        players_table.update({'id_player': id}, doc_ids=[id])
        serialized_player['id_player'] = id
        self.id_player = id

    @ classmethod
    def serialization_players(self, players):
        serialized_players = []
        for player in players:
            # serialize a player
            serialized_player = player.serialization_player()
            # serialized_player = player.serialization_player2()
            # Add all serialized players in a list
            serialized_players.append(serialized_player)
        return serialized_players

    def serialization_player2(self):
        self.serialized_player = {
            'id_player': self.id_player,
            # 'firstname': self.firstname.lower(),
            # 'lastname': self.lastname.lower(),
            # 'birthdate': self.birthdate.strftime('%d/%m/%Y'),
            # 'sex': self.sex.lower(),
            # 'ranking': self.ranking,
            # 'point': self.point
        }
        return self.serialized_player

    def serialization_player(self):
        self.serialized_player = {
            'id_player': self.id_player,
            'firstname': self.firstname.lower(),
            'lastname': self.lastname.lower(),
            'birthdate': self.birthdate.strftime('%d/%m/%Y'),
            'sex': self.sex.lower(),
            'ranking': self.ranking,
            'point': self.point
        }
        return self.serialized_player

    def deserializing_player(self, player):
        self.id_player = player['id_player']
        self.firstname = player['firstname']
        self.lastname = player['lastname']
        self.birthdate = datetime.datetime.strptime(
            player['birthdate'], '%d/%m/%Y').date()
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
        players.sort(key=lambda x: x.lastname.lower())
        return (players)

    @ classmethod
    def player_exists(self, players_table, id):
        return players_table.contains(doc_id=id)

    def get_player_from_id(self, id):
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        player_dict = players_table.get(doc_id=id)
        return player_dict

    @ classmethod
    def get_name_player(self, id):
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        player = players_table.get(doc_id=id)
        return player['firstname'] + " " + player['lastname']
