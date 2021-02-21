from model import Player


def view_function():
    print('beginning')
    print('')


def print_menu():       # Your menu design here
    print(30 * "-", "MENU", 30 * "-")
    print("1. Do you want to add a player ")
    print("2. Do you want visualise all players ")
    print("3. Do you want visualise all players  ")
    # print("4. Use manually entered custom conf file ")
    print("5. Exit from the script ")
    print(73 * "-")


def showAllView(list):
    for item in list:
        print(item.view_player())


def endView():
    print('end')
