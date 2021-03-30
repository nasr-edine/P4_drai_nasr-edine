from model.player import Player


def view_function():
    print('beginning')
    print('')


def print_menu():       # Your menu design here
    print(30 * "-", "MENU", 30 * "-")
    print("1. Create a new round")
    print("2. Save the current state of the contest ? ")
    print("3. Update players ranking ?")
    print("4. Display player statistics ?")
    # print("4. Use manually entered custom conf file ")
    print("5. Exit from the script ")
    print("6. Display report")

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


def print_contests_list(contests):
    print()
    print(12 * "-", "Contests list", 13 * "-")
    for contest in contests:
        print(f'| number: {contest.get_id()} '.ljust(3),
              f'| name: {contest.name}'.ljust(25), '|')
    print(40 * "-", '\n')


def print_players_sorting_by_name(players):
    Player.sort_players_by_name(players)
    print(19 * "-", "PLAYERS SORTING BY NAME", 18 * "-")
    for player in players:
        print(player.display_player())
    print(62 * "-", '\n')


def print_players_sorting_by_ranking(players):
    Player.sort_players_by_ranking(players)
    print(16 * "-", "PLAYERS SORTING BY RANKING", 18 * "-")
    for player in players:
        print(player.display_player())
    print(62 * "-", '\n')


def print_rounds(rounds):
    for round in rounds:
        print(round)


def print_msg_error_1():
    print('there are none contests recorded !')


def print_msg_error_2():
    print("this name don't exists. Try again...")


def endView():
    print('end')
