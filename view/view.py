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
    print("| 1. Create a player".ljust(64), "|")
    print("| 2. Create a new contest".ljust(64), "|")
    print("| 3. Update players ranking".ljust(64), "|")
    print("| 4. Display players statistics for current contest".ljust(64), "|")
    print("| 5. Display contests".ljust(64), "|")
    print("| 6. Display players sorting by name".ljust(64), "|")
    print("| 7. Display players sorting by rank".ljust(64), "|")
    print("| 8. Display players for a contest".ljust(64), "|")
    print("| 9. Display rounds for a contest".ljust(64), "|")
    print("| 10. Display matches for a contest".ljust(64), "|")
    print("| 11. Exit from the script ".ljust(64), "|")
    print(66 * "-", "\n")


def print_menu_time_control():       # Your menu design here
    print()
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

    string = ""
    row = 121 * "-"
    string += row + "\n"
    a = "| id player".ljust(20)
    b = "| firstname".ljust(20)
    c = "| lastname".ljust(20)
    d = "| birthdate".ljust(20)
    e = "| ranking".ljust(20)
    f = "| point".ljust(20)
    g = "|"
    string += a + b + c + d + e + f + g
    string += "\n" + row + "\n"
    for player in players:
        a = "| "+str(player.id_player).ljust(18)
        b = "| "+player.firstname.ljust(18)
        c = "| "+player.lastname.ljust(18)
        d = "| "+str(player.birthdate).ljust(18)
        e = "| "+str(player.ranking).ljust(18)
        f = "| "+str(player.point).ljust(18)
        g = "|"
        string += a + b + c + d + e + f + g
        string += "\n" + row + "\n"
    print(string)


def print_msg_error_4():
    print("this player don't exist in db")


def print_msg_error_5():
    print('there is no current contest')


def print_msg_error_6():
    print('You cannot add this player because it is already registered\n')
    clear_screen()


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


def infos_3():
    print("Please enter id for each player, a number between 1 and 100:\n")
    clear_screen()


def infos_4():
    print('The players are now full for this contest\n')
    clear_screen()


def infos_5(player):
    print(
        f"{player.firstname}"
        f" {player.lastname} is added to contest.\n"
    )


def infos_6():
    print("Choose a number between 1 and 3 to save the scores\n")
    print("1: Player 1 wins")
    print("2: Player 2 wins")
    print("3: Draw\n")


def display_players(players):
    string = ""
    row = 121 * "-"
    string += row + "\n"
    a = "| id player".ljust(20)
    b = "| firstname".ljust(20)
    c = "| lastname".ljust(20)
    d = "| birthdate".ljust(20)
    e = "| ranking".ljust(20)
    f = "| point".ljust(20)
    g = "|"
    string += a + b + c + d + e + f + g
    string += "\n" + row + "\n"
    print(string, end='')
    for player in players:
        string = ""
        a = "| "+str(player.id_player).ljust(18)
        b = "| "+player.firstname.ljust(18)
        c = "| "+player.lastname.ljust(18)
        d = "| "+str(player.birthdate).ljust(18)
        e = "| "+str(player.ranking).ljust(18)
        f = "| "+str(player.point).ljust(18)
        g = "|"
        string += a + b + c + d + e + f + g
        string += "\n" + row + "\n"
        print(string, end='')
    print()


def infos_7(player):
    print(player.__str__())


def infos_8():
    print("The new rank for player is updated")


def infos_9(current_round):
    print_round_nb = ['First', 'Second', 'Third', 'Fourth']
    print(f'{print_round_nb[current_round]} round:\n')


def infos_10(n):
    print(f"match {n + 1}:")


def infos_11(name_player_1, name_player_2):
    string = ""
    row = 41 * "-"
    string += row + "\n"
    a = "| Player 1".ljust(20)
    b = "| Player 2".ljust(20)
    c = "|"
    string += a + b + c
    string += "\n" + row + "\n"
    c = "| " + name_player_1.ljust(18)
    d = "| " + name_player_2.ljust(18)
    e = "|"
    string += c + d + e
    string += "\n" + row + "\n"
    print(string)


# display matches
def display_round(contest, nb_round, total_nb_matches):
    print(15 * "-", f"Round {nb_round + 1}", 15 * "-", "\n")
    for match in range(total_nb_matches):
        id_player = contest.rounds[nb_round].matches[match][0][0]
        value = [x for x in contest.players if x.id_player == id_player]
        name_player_1 = value[0].firstname + " " + value[0].lastname
        score1 = contest.rounds[nb_round].matches[match][0][1]

        id_player = contest.rounds[nb_round].matches[match][1][0]
        value = [x for x in contest.players if x.id_player == id_player]
        name_player_2 = value[0].firstname + " " + value[0].lastname
        score2 = contest.rounds[nb_round].matches[match][1][1]

        string = ""
        row = 41 * "-"
        string += row + "\n"
        a = "| Player 1".ljust(20)
        b = "| Player 2".ljust(20)
        c = "|"
        string += a + b + c
        string += "\n" + row + "\n"
        a = "| " + name_player_1.ljust(18)
        b = "| " + name_player_2.ljust(18)
        c = "|\n" + row + "\n"
        d = "| " + str(score1).ljust(18)
        e = "| " + str(score2).ljust(18)
        f = "|"
        string += a + b + c + d + e + f
        string += "\n" + row + "\n"
        print(string)


def print_msg_error_1():
    print('there are none contests recorded !')
    clear_screen()


def print_msg_error_2():
    print("this contest name don't exists. Try again...")
    clear_screen()


def print_msg_error_3():
    print("there are no players registered in the database.")
    clear_screen()


def print_msg_error_7():
    print('Unrecognized date format, please try again\n')
    clear_screen()


def print_msg_error_8():
    print('Unrecognized gender format, please try again\n')
    clear_screen()


def print_msg_error_9():
    print("Oops!  the number is not between"
          " 1 and 3.  Try again...")
    clear_screen()


def print_msg_error_10():
    print("Oops!  That was no valid number.  Try again...")
    clear_screen()


def print_msg_error_11():
    print("Oops!  the number is not "
          "between 1 and 100.  Try again...")
    clear_screen()


def print_msg_error_12():
    print("Oops!  That was no valid number.  Try again...")
    clear_screen()


def print_msg_error_13():
    print("Please enter at least 1 character")
    clear_screen()


def print_msg_error_14():
    print("Please enter characters A-Z only")
    clear_screen()


def print_msg_error_15():
    print("Error! Only 40 characters maximum allowed!")
    clear_screen()


def print_msg_error_16():
    print('Please try again the limit characters is 1000')
    clear_screen()


def print_msg_error_17():
    print(
        "you cannot create a contest because "
        "there are not enough registered players")


def print_msg_error_18():
    print(
        "this player doesn't exist in"
        "dataBase. Please, try another Id !\n")


def print_msg_error_19():
    print("You have already saved this player for this contest\n")


def print_msg_error_20():
    print("you have reached the maximum "
          "possible of round for a contest")


def endView():
    exit()
