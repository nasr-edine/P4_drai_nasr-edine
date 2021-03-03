import re
import datetime

import simpleFaker
import view.view as view

from model.player import Player
from model.contests import Contest
from tours import Tour


def showAll():
    result = Player.getAll()
    return view.showAllView(result)

    result = Player.getAll2()
    return view.showAllView(result)


def read_date(type_date):
    switch = 1
    while switch == 1:
        if type_date == 1:
            date = input(
                'Enter player birth date in  DD/MM/YEAR format: ')
        else:
            date = input(
                'Enter your tournament date in  DD/MM/YEAR format: ')
        try:
            date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
            switch = 0
        except ValueError:
            print('Unrecognized date format, please try again\n')
    return date


def read_sex():
    switch = 1
    while switch == 1:
        sex = (input('Enter your gender M or F: ')).upper()
        if sex == 'M' or sex == 'F':
            switch = 0
        else:
            print('Unrecognized gender format, please try again\n')
    return sex


def read_time_control():
    switch = 1
    while switch == 1:
        try:
            time_control = int(
                input("Please enter a time control, a number between 1 and 3: "))
            # 'choise a time control between 1: bullet, 2: blitz and 3: rapid rating:'
            if time_control >= 1 and time_control <= 3:
                switch = 0
            else:
                print("Oops!  the number is not between 1 and 3.  Try again...")
                continue
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    return time_control


def read_ranking():
    switch = 1
    while switch == 1:
        try:
            ranking = int(
                input("Please enter ranking, a number between 1 and 8: "))
            if ranking >= 1 and ranking <= 8:
                switch = 0
            else:
                print("Oops!  the number is not between 1 and 8.  Try again...")
                continue
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")
    return ranking


def read_name(type_name):
    while True:
        if type_name == 1:
            name = input("Enter player firstname: ")
        elif type_name == 2:
            name = input('Enter player lastname: ')
        elif type_name == 3:
            name = input('Enter tournament name: ')
        else:
            name = input('Enter the tournament location: ')
        if not name.isalpha():
            print("Please enter characters A-Z only")
        elif len(name) > 40:
            print("Error! Only 40 characters maximum allowed!")
        else:
            break
    return name


def start():
    view.view_function()
    serialized_players = []
    while True:
        view.print_menu()
        choice = input("Enter your choice [1-5]: ")
        if choice == '1':
            # Input user for fill all informations about a tournament
            name = read_name(3)
            location = read_name(4)
            date = input('Enter date of contest: ')
            time_control = read_time_control()
            comments = input('Do you want to add any comments: ')

            # nb_turns = input('Enter number of turns')
            players_index = []
            players_index += range(1, 9)
            # print(list)
            rounds = [i for i in range(4)]  # create a list of rounds
            # rounds = [Rounds() for i in range(4)]  # create a list of rounds

            # Create a tournament instance
            contest = Contest(name, location, date, players_index,
                              time_control, comments, rounds)

            # serialize a tournament
            contest.serialization_contest()

            # Save a tournament in DataBase
            contest.save()

        elif choice == '2':
            for n in range(0, 1):

                # Input user for fill all informations about a player
                firstname = read_name(1)
                lastname = read_name(2)
                birthdate = read_date(1)
                gender = read_sex()
                ranking = read_ranking()

                # Create an instance of a player
                player = Player(firstname, lastname,
                                birthdate, gender, ranking)

                # serialize a player
                player.serialization_player()

                # get an serialized player
                serialized_player = player.get_serialized_player()

                # Add all serialized players in a list
                serialized_players.append(serialized_player)

            # Save players list in tinyDB
            Player.saveAllPlayers(serialized_players)
        elif choice == '3':
            # create a contest (un tournoi)
            fake_contest = simpleFaker.faker_contest()
            serialized_contest = serialization_contest(fake_contest)
            Contest.setContests(serialized_contest)

            # create rounds

            # create a list of 8 players
            fake_players = simpleFaker.faker_profiles()
            for fake_player in fake_players:
                serialized_players.append(
                    Players.serialization_player(fake_player))
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
