import re
import datetime
import random
from faker import Faker

import json

import simpleFaker
import view.view as view

from model.player import Player
from model.contests import Contest
from model.tours import Tour


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
                'Enter  contest date in  DD/MM/YEAR format: ')
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
            view.print_menu_time_control()
            time_control = int(input())
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


def read_comments():
    switch = 1
    while switch == 1:
        comments = input(
            'Do you want to add any comments \(max:1000 characters\): ')
        if len(comments) > 1000:
            print('Please try again the limit characters is 1000')
        else:
            switch = 0
    return comments


def create_pair_matches(id_player1, id_player2):
    faker = Faker()
    index_player = 0
    list_matchs = []
    score = faker.random_int(0, 2)
    list1 = [id_player1, score]
    score = faker.random_int(0, 2)
    list2 = [id_player2, score]

    tuple_match = (list1, list2)
    list_matchs.append(tuple_match)
    index_player += 2
    return list_matchs


def match_generator(list_players, rounds):
    for round in rounds:
        list_matches = []
        for n in range(4):

            list_matches.append(create_pair_matches(
                list_players[n], list_players[n + 4]))
            round.matchs = list_matches
    return rounds


def create_players():
    serialized_players = []
    list1 = []
    list1 = (list(range(1, 9)))
    random.shuffle(list1)

    faker = Faker()
    # create rounds
    for n in range(0, 8):
        # create a list of 8 players
        profile = faker.simple_profile()
        name = profile['name'].split()
        firstname = name[0]
        lastname = name[1]
        birthdate = profile['birthdate']
        sex = profile['sex']
        ranking = list1[n]
        # Create an instance of a player
        player = Player(firstname, lastname,
                        birthdate, sex, ranking)
        # serialize a player
        player.serialization_player()
        # get an serialized player
        serialized_player = player.get_serialized_player()
        # Add all serialized players in a list
        serialized_players.append(serialized_player)

    # Sorting players by ranking
    serialized_players = Player.sort_players_by_ranking(serialized_players)
    print("Sorting players by ranking: ", serialized_players)

    # Save players list in tinyDB
    Player.saveAllPlayers(serialized_players)


def start():
    view.view_function()

    while True:
        view.print_menu()
        choice = input("Enter your choice [1-5]: ")
        if choice == '1':
            create_players()
            # Input user for fill all informations about a tournament
            # name = read_name(3)
            # location = read_name(4)
            # date = read_date(0)
            # time_control = read_time_control()
            # comments = read_comments()
            players_index = Player.getPlayerIndex()

            faker = Faker()
            name = faker.name()
            location = faker.address()
            date = faker.date_of_birth()
            time_control = faker.random_int(1, 3)
            comments = faker.text()

            # Create a list of rounds
            list_tours = []
            for i in range(4):
                date_start = datetime.datetime.now()
                date_end = date_start + datetime.timedelta(hours=1)
                list_tours.append(
                    Tour('Round ' + str(i), None, date_start, date_end))
            rounds = list_tours

            list_players = Player.getPlayerIndex()
            # print(list_players)
            # generate a list of matchs
            rounds = match_generator(list_players, rounds)
            print("rounds value: ", rounds)
            # Create a tournament instance
            contest = Contest(name, location, date, players_index,
                              time_control, comments, rounds)

            # serialize a tournament
            contest.serialization_contest()

            # Save a tournament in DataBase
            contest.save()
            Player.update_point_player()
            exit()

        elif choice == '2':
            serialized_players = []
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
            create_players()
        elif choice == '4':
            showAll()
        elif choice == '5':
            view.endView()
            exit()
        elif choice == '6':
            print(Player.get_index_number())
        else:
            input("Wrong menu selection. Enter any key to try again..")


if __name__ == "__main__":
    start()
