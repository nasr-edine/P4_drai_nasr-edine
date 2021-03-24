from model.player import Player


def view_function():
    print('beginning')
    print('')


def print_menu():       # Your menu design here
    print(30 * "-", "MENU", 30 * "-")
    print("1. Do you want to create a new round")
    print("2. Do you want to save the current state of the contest ? ")
    print("3. Do you want to update players ranking ?")
    print("4. Do you want to see players statistics ?")
    # print("4. Use manually entered custom conf file ")
    print("5. Exit from the script ")
    print(73 * "-")


def print_menu_time_control():       # Your menu design here
    print(17 * "-", "Please choice the time control type: ", 17 * "-")
    print("1. Rapid")
    print("2. Bullet")
    print("3. Blitz")
    print(73 * "-")


def showAllView(list):
    print("firstname".ljust(15), "|lastname".ljust(15),
          " |birthdate".ljust(15), "  |sex".ljust(15), "   |ranking".ljust(15), "    |", sep='', end='\n\n')
    for item in list:
        print(item.firstname.ljust(15), '|', sep='', end='')
        print(item.lastname.ljust(15), '|', sep='', end='')
        print(str(item.birthdate).ljust(15), '|', sep='', end='')
        print(item.sex.ljust(15), '|', sep='', end='')
        print(str(item.ranking).ljust(15), '|', sep='', end='')
        print()


def endView():
    print('end')
