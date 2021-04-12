from model.player import Player
import os


def clear_screen():
    input('\nType enter to continue...')
    os.system('clear')


def clear_screen_without_msg():
    os.system('clear')


def wrong_menu():
    input("Wrong menu selection. Type enter to try again..")
    os.system('clear')


def print_menu():       # Your menu design here
    print()
    print(30 * "-", "MENU", 30 * "-")
    print("| 1. Create a new contest".ljust(64), "|")
    print("| 2. Create a player".ljust(64), "|")
    print("| 3. Update players ranking".ljust(64), "|")
    print("| 4. Display players statistics for current contest".ljust(64), "|")
    print("| 5. Display contests".ljust(64), "|")
    print("| 6. Display all players".ljust(64), "|")
    print("| 7. Display players for a contest".ljust(64), "|")
    print("| 8. Display rounds for a contest".ljust(64), "|")
    print("| 9. Display matches for a contest".ljust(64), "|")
    print("| 10. Exit from the script ".ljust(64), "|")
    print(66 * "-", "\n")


def print_menu_time_control():       # Your menu design here
    print(17 * "-", "Please choice the time control type: ", 17 * "-")
    print("1. Rapid")
    print("2. Bullet")
    print("3. Blitz")
    print(73 * "-")


def showAllView(list):
    print("firstname".ljust(15), "|lastname".ljust(15),
          " |birthdate".ljust(15), "  |sex".ljust(15),
          "   |ranking".ljust(15), "    |", sep='', end='\n\n')
    for item in list:
        print(item.firstname.ljust(15), '|', sep='', end='')
        print(item.lastname.ljust(15), '|', sep='', end='')
        print(str(item.birthdate).ljust(15), '|', sep='', end='')
        print(item.sex.ljust(15), '|', sep='', end='')
        print(str(item.ranking).ljust(15), '|', sep='', end='')
        print()


def print_contests_list(contests):
    print()
    # print(12 * "-", "Contests list", 13 * "-")
    newline = "\n"
    row = newline + 41 * "-" + newline
    # string = row
    string = "- Contest list " + 26 * "-"
    string += newline
    # string += row
    # print(string)
    a = '| number'.ljust(15)
    b = '| name'.ljust(25)+'|'
    string += a + b + row
    # print(string)
    for contest in contests:
        c = f'| {contest.get_id()}'.ljust(15)
        d = f'| {contest.name}'.ljust(25) + '|'
        # print(f'| {contest.get_id()}'.ljust(15),
        #   f'| {contest.name}'.ljust(25) + '|')
        string += c + d + row
    print(string)
    # print(40 * "-", '\n')


def print_players_sorting_by_name(players):
    Player.sort_players_by_name(players)
    print("PLAYERS SORTING BY NAME\n")
    print_players_list(players)


def print_players_sorting_by_ranking(players):
    Player.sort_players_by_ranking(players)
    print("PLAYERS SORTING BY RANKING\n")
    print_players_list(players)


def infos_contest(contest):
    print("Information about the contest:\n")
    print(f"name:     {contest.name}\n")
    print(f"date:     {contest.date}\n")
    print(f"location: {contest.location}\n")
    print(f"comments: {contest.comments}\n")
    print("players:")
    print_players_list(contest.players)
    # for player in contest.players:
    # print(player.view_player())


def infos_round(round):
    print(f"start: {round.start_datetime}")
    print(f"end  : {round.end_datetime}")


def print_player_updated(player):
    string = "The new ranking for player "\
        f"{player.firstname} {player.lastname} is updated\n"
    string += player.__str__()
    print(string)


def print_players_list(players):

    # def list_players(players):
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
    for player in players:
        b = "| "+player.firstname.ljust(18)
        c = "| "+player.lastname.ljust(18)
        d = "| "+str(player.birthdate).ljust(18)
        e = "| "+str(player.ranking).ljust(18)
        f = "|"
        string += b + c + d + e + f
        string += "\n" + row + "\n"
    print(string)
    # print(player.__str__())


def print_msg_error_4():
    print("this player don't exist in db")


def print_msg_error_5():
    print('there is no current contest')


def print_msg_error_6():
    print('You cannot add this player because it is already registered\n')
    clear_screen()


# def print_rounds(rounds):
#     # print(11 * "-", "ROUNDS LIST", 13 * "-")
#     for round in rounds:
#         print(36 * "-",)
#         print(round.display_round())
#         print(36 * "-",)
#         clear_screen()
#     # print(36 * "-", '\n')


def print_matches(rounds):
    print(11 * "-", "MATCHES LIST", 13 * "-")
    for round in rounds:
        print(round.display_matches())
        print(36 * "-",)
    print(36 * "-", '\n')


def infos_1():
    print("Please enter informations about player:\n")


def infos_2(player):
    print("New player:\n")
    print(player.__str__())
    print('Good, the player is added.')
    clear_screen()


def print_msg_error_1():
    print('there are none contests recorded !')


def print_msg_error_2():
    print("this contest name don't exists. Try again...")


def print_msg_error_3():
    print("there are no players registered in the database.")


def endView():
    print('end')
