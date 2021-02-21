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
                name = input('Enter name : ')
                age = input('Enter age: ')
                # Player.setPlayer(name, age)
                player = Player(name, age)
                serialized_player = {
                    'name': player.name,
                    'age': player.age
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
        Player.setPlayers(serialized_players)


if __name__ == "__main__":
    start()
