from model import Player
import view


def showAll():
    result = Player.getAll()
    return view.showAllView(result)

    result = Player.getAll2()
    return view.showAllView(result)


def start():
    view.view_function()
    serialized_players = []
    while True:
        view.print_menu()
        choice = input("Enter your choice [1-5]: ")
        if choice == '1':
            loop = 1
            while loop:
                firstname = input('Enter your firstname : ')
                lastname = input('Enter your lastname : ')
                birth = input('Enter date of birth: ')
                gender = input('Enter gender: ')
                ranking = 0
                player = Player(firstname, lastname,
                                birth, gender, ranking)
                serialized_player = {
                    'firstname': player.firstname,
                    'lastname': player.lastname,
                    'birth': player.birth,
                    'gender': player.gender,
                    'ranking': player.ranking
                }
                serialized_players.append(serialized_player)
                response = input('Do you want to add a new player (y/n): ')
                if response == 'y':
                    pass
                else:
                    loop = 0
            Player.setPlayers(serialized_players)
        elif choice == '2':
            showAll()
        elif choice == '3':
            showAll()
        elif choice == '5':
            view.endView()
            exit()
        else:
            # Any inputs other than values 1-4 we print an error message
            input("Wrong menu selection. Enter any key to try again..")


if __name__ == "__main__":
    start()
