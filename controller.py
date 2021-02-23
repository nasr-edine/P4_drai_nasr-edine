from model import Player
import view
import simpleFaker
from contests import Contest


def showAll():
    result = Player.getAll()
    return view.showAllView(result)

    result = Player.getAll2()
    return view.showAllView(result)


def serialization_player(player):
    serialized_player = {
        'firstname': player.firstname,
        'lastname': player.lastname,
        'birth': str(player.birthdate),
        'gender': player.sex,
        'ranking': player.ranking
    }
    return serialized_player


def serialization_contest(contest):
    serialized_contest = {
        'name': contest.name,
        'location': contest.location,
        'date': contest.date,
        'nb_turns': contest.nb_turns,
        'players_index': contest.player_index,
        'time_control': contest.time_control,
        'comments': contest.comments
    }
    return serialized_contest


def start():
    view.view_function()
    serialized_players = []
    while True:
        view.print_menu()
        choice = input("Enter your choice [1-5]: ")
        if choice == '1':
            name = input('Enter name of contest: ')
            location = input('Enter location of contest: ')
            date = input('Enter date of contest: ')
            # nb_turns = input('Enter number of turns')

            players_index = []
            players_index += range(1, 9)
            time_control = input(
                'choise a time control between 1: bullet, 2: blitz and 3: rapid rating:')
            comments = input('Do you want to add any comments: ')
            # print(list)
            contest = Contest(name, location, date, players_index,
                              time_control, comments)
            serialized_contest = serialization_contest(contest)
            print(serialized_contest)
            Contest.setContests(serialized_contest)
        elif choice == '2':
            for n in range(0, 8):
                firstname = input('Enter your firstname : ')
                lastname = input('Enter your lastname : ')
                birth = input('Enter date of birth: ')
                gender = input('Enter gender: ')
                ranking = 0
                player = Player(firstname, lastname,
                                birth, gender, ranking)
                serialized_player = serialization_player(player)
                serialized_players.append(serialized_player)
            Player.setPlayers(serialized_players)
        elif choice == '3':
            result = simpleFaker.faker_profiles()
            for item in result:
                serialized_players.append(serialization_player(item))
                Player.setPlayers(serialized_players)
        elif choice == '4':
            showAll()
        elif choice == '5':
            view.endView()
            exit()
        else:
            input("Wrong menu selection. Enter any key to try again..")


if __name__ == "__main__":
    start()
