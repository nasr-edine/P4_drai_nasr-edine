from tinydb import TinyDB, Query


class Player(object):
    def __init__(self, firstname, lastname, birthdate, sex, ranking):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.sex = sex
        self.ranking = ranking
        self.serialized_player = {}

    def view_player(self):
        return ("%s %s %s %s %s" % (self.firstname.ljust(15), self.lastname.ljust(15), self.birth.ljust(15), self.gender.ljust(15), str(self.ranking).ljust(15)))

    def serialization_player(self):
        self.serialized_player = {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birthdate': str(self.birthdate),
            'sex': self.sex,
            'ranking': self.ranking
        }

    def get_serialized_player(self):
        return self.serialized_player

    @classmethod
    def saveAllPlayers(self, serialized_players):
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
                            item['birthdate'], item['sex'], item['ranking'])
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
