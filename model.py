from tinydb import TinyDB, Query


class Player(object):
    def __init__(self, name=None, age=None):
        self.name = name
        self.age = age

    def view_player(self):
        return ("%s %s" % (self.name, self.age))

    @classmethod
    def setPlayer(self, name, age):
        player = Player(name, age)
        db = TinyDB('db.json')
        players_table = db.table('players')
        players_table.truncate()  # clear the table first
        serialized_player = {'name': player.name, 'age': player.age}
        players_table.insert(serialized_player)

    @classmethod
    def setPlayers(self, serialized_players):
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        players_table.truncate()  # clear the table first
        players_table.insert_multiple(serialized_players)

    @classmethod
    def getAll(self):
        db = TinyDB('db.json')
        players_table = db.table('players')
        result = []
        for item in players_table:
            player = Player(item['name'], item['age'])
            result.append(player)
        return result

    @classmethod
    def getAll2(self):
        result = []
        db = TinyDB('db.json')
        players_table = db.table('players')
        serialized_players = players_table.all()
        for item in serialized_players:
            player = Player(item['name'], item['age'])
            result.append(player)
        return result
