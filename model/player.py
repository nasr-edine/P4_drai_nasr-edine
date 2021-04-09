# import random
import datetime
from tinydb import TinyDB
# from faker import Faker
# from controller.read_input import ReadInformation


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
        row = 81 * "-"
        string += row + "\n"
        b = "| firstname".ljust(20)
        c = "| lastname".ljust(20)
        d = "| birthdate".ljust(20)
        e = "| ranking".ljust(20)
        f = "|"
        string += b + c + d + e + f
        string += "\n" + row + "\n"

        b = "| "+self.firstname.ljust(18)
        c = "| "+self.lastname.ljust(18)
        d = "| "+str(self.birthdate).ljust(18)
        e = "| "+str(self.ranking).ljust(18)
        f = "|"
        string += b + c + d + e + f
        string += "\n" + row + "\n"
        return string

        # def add_player2(self):
        #     os.system('clear')
        #     print("New player:\n")
        #     print(self.__str__())

        #     print('Good, the player is added.')
        #     view.clear_screen()
        #     serialized_player = self.serialization_player()
        #     # ret = Player.serialization_players(players)
        #     players = []
        #     players.append()
        #     Contest.save_players2(serialized_player, players)
        #     # Sorting players list by ranking
        #     # Player.sort_players_by_ranking(players)

    # def __repr__(self):
    #     return "name: {:10} {:10} id: {}   ranking: {}
    # point: {}\n".format(self.firstname, self.lastname,
    # self.id_player, self.ranking, self.point)

    # def view_player(self):
    #     # return ("name: %s %s id: %s ranking: %s point: %s" %
    #     # (self.lastname.ljust(10), self.firstname.ljust(10),
    #     # str(self.id_player).ljust(2),
    #     # str(self.ranking).ljust(2), str(self.point).ljust(2)))
    #     # print(f'+Player{10 * "-"}+{10 * "-"}+{10 * "-"}+')
    #     # print("|name".ljust(16), "|birthdate".ljust(10),
    #     # "|ranking|".ljust(10))
    #     return ("name: %s %s birthdate: %s ranking: %s" %
    # (self.lastname.ljust(10), self.firstname.ljust(10),
    # str(self.birthdate).ljust(2), str(self.ranking).ljust(2)))

    # def display_player(self):
    #     return "|firstname: {:15} |lastname: {:10} |ranking: {}
    # |".format(self.firstname, self.lastname, self.ranking)

    def get_serialized_player(self):
        return self.serialized_player

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
    # @ classmethod
    # # create a player
    # def add_player(self):
    #     # Create a list of players
    #     print("Please enter informations about player:\n")
    #     players = ReadInformation.create_players()
    #     os.system('clear')
    #     print(players[0].view_player())
    #     print('Good, the player is added.')
    #     input('Press any touch to continue.')

    #     ret = Player.serialization_players(players)
    #     Contest.save_players2(ret, players)
    #     # Sorting players list by ranking
    #     Player.sort_players_by_ranking(players)

    @ classmethod
    def get_players_data(self):
        players = []
        db = TinyDB('db.json', indent=4)
        player_table = db.table('players')
        for item in player_table:
            player = Player()
            player.deserializing_player(item)
            players.append(player)
        return players

    @ classmethod
    def get_players(self):
        players = Player.get_players_data()
        return players

    @ classmethod
    def serialization_players(self, players):
        serialized_players = []
        for player in players:
            # serialize a player
            serialized_player = player.serialization_player()
            # Add all serialized players in a list
            serialized_players.append(serialized_player)
        return serialized_players

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

    # @ classmethod
    # def create_players(self):
    #     read_input = ReadInformation()
    #     players = []
    #     random_list = []
    #     random_list = (list(range(1, 9)))
    #     random.shuffle(random_list)

    #     faker = Faker()
    #     # create rounds
    #     for n in range(0, 8):

    #         # Enter informations about a player
    #         # firstname = read_input.read_name(1)
    #         # lastname = read_input.read_name(2)
    #         # birthdate = read_input.read_date(1)
    #         # sex = read_input.read_sex()
    #         # ranking = read_input.read_ranking()

    #         # create a fake list of 8 players
    #         profile = faker.simple_profile()
    #         name = profile['name'].split()
    #         firstname = name[0]
    #         lastname = name[1]
    #         birthdate = profile['birthdate']
    #         sex = profile['sex']
    #         ranking = random_list[n]
    #         # Create an instance of a player
    #         player = Player(n, firstname, lastname,
    #                         birthdate, sex, ranking)
    #         # serialize a player
    #         serialized_player = player.serialization_player()
    #         # Add all serialized players in a list
    #         players.append(player)
    #     return(players)
