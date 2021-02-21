from tinydb import TinyDB, Query


class Player(object):
    def __init__(self, firstname, lastname, birth, gender, ranking):
        self.firstname = firstname
        self.lastname = lastname
        self.birth = birth
        self.gender = gender
        self.ranking = ranking

    def view_player(self):
        return ("%s %s %s %s %s" % (self.firstname, self.lastname, self.birth, self.gender, self.ranking))

    @classmethod
    def setPlayer(self, firstname, lastname, birth, gender, ranking):
        player = Player(firstname, lastname, birth, gender, ranking)
        db = TinyDB('db.json')
        players_table = db.table('players')
        players_table.truncate()  # clear the table first
        serialized_player = {'firstname': player.firstname, 'lastname': player.lastname,
                             'birth': player.birth, 'gender': player.gender, 'ranking': player.ranking}
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
            player = Player(item['firstname'], item['lastname'],
                            item['birth'], item['gender'], item['ranking'])
            result.append(player)
        return result

    @classmethod
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
