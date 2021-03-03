from model.player import Player


def view_function():
    print('beginning')
    print('')


def print_menu():       # Your menu design here
    print(30 * "-", "MENU", 30 * "-")
    print("1. Add a contest ")
    print("2.  Add 8 players")
    print("3. Do you want to add a faker players ")
    print("4. Do you want visualise all players  ")
    # print("4. Use manually entered custom conf file ")
    print("5. Exit from the script ")
    print(73 * "-")


def showAllView(list):
    print("firstname".ljust(15), "|lastname".ljust(15),
          " |birthdate".ljust(15), "  |sex".ljust(15), "   |ranking".ljust(15), "    |", sep='', end='\n\n')
    for item in list:
        # print(item.view_player())
        # temp = vars(item)
        # for item2 in temp:
        print(item.firstname.ljust(15), '|', sep='', end='')
        print(item.lastname.ljust(15), '|', sep='', end='')
        print(str(item.birthdate).ljust(15), '|', sep='', end='')
        print(item.sex.ljust(15), '|', sep='', end='')
        print(str(item.ranking).ljust(15), '|', sep='', end='')
        print()


def endView():
    print('end')
