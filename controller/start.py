import re
import datetime
import random
import json
import simpleFaker
import controller.start
from faker import Faker
import view.view as view
from model.player import Player
from model.contests import Contest
from model.tours import Tour


def showAll():
    result = Player.getAll()
    return view.showAllView(result)

    result = Player.getAll2()
    return view.showAllView(result)


def start():

    # Create a list of players
    players = Player.create_players()
    print("Create players list:\n")
    print(players)
    input()

    view.view_function()

    while True:
        view.print_menu()
        choice = input("Enter your choice [1-5]: ")
        if choice == '1':

            # Sorting players list by ranking
            Player.Sorting_players_by_ranking(players)
            print("Sorting players by ranking:\n")
            print(players)
            input()

            # input players
            # name = read_name(3)
            # location = read_name(4)
            # date = read_date(0)
            # time_control = read_time_control()
            # comments = read_comments()

            # Create a contest
            faker = Faker()
            name = faker.name()
            location = faker.address()
            date = faker.date_of_birth()
            time_control = faker.random_int(1, 3)
            comments = faker.text()

            # Instance of contest
            contest = Contest(name, location, date,
                              time_control, comments, players)

            # Create rounds
            nb_rounds = 4
            contest.create_rounds(nb_rounds)

            # Create matches
            nb_matches = 4
            contest.create_matches(nb_matches, nb_matches)

            # serialize contest
            contest.serialization_contest()

            # Save  contest in DataBase
            contest.save()

            # Generate all matches for first round
            first_round = 0
            print('generate first round:\n')
            contest.rounds[first_round].start_datetime = datetime.datetime.now()
            contest.rounds[first_round].end_datetime = contest.rounds[first_round].start_datetime + \
                datetime.timedelta(hours=1)
            Tour.matches_generator(contest, first_round)
            # display matches for first round
            contest.display_round(first_round, nb_matches)
            input()

            contest.serialization_contest()
            contest.save()

            # save scores for all matches in first round
            contest.save_scores(first_round, nb_matches)
            print("display scores for first round:\n")
            contest.display_round(first_round, nb_matches)
            input()

            contest.serialization_contest()
            contest.save()

            print('display scores by player:\n')
            print(contest.players)
            input()
            print("sorting players by point:\n")
            contest.players = Player.sort_players_by_point(contest.players)
            print(contest.players)
            input()
            contest.serialization_contest()
            contest.save()

            for nb_round in range(1, 4):

                # Generate next round
                contest.rounds[nb_round].start_datetime = datetime.datetime.now()
                contest.rounds[nb_round].end_datetime = contest.rounds[nb_round].start_datetime + \
                    datetime.timedelta(hours=1)
                Tour.matches_generator(contest, nb_round)

                print(f"Generate round: {nb_round}\n")
                contest.display_round(nb_round, nb_matches)
                input()

                contest.save_scores(nb_round, nb_matches)

                contest.serialization_contest()
                contest.save()

                print(f'display scores for round: {nb_round}:\n')
                contest.display_round(nb_round, nb_matches)
                input()
                print("display scores by player:\n")
                print(contest.players)
                input()
                contest.players = Player.sort_players_by_point(contest.players)
                print("Sorting players by point:\n")
                print(contest.players)
                input()
            contest.serialization_contest()
            contest.save()
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
        # elif choice == '6':
            # print(Player.get_index_number())
        else:
            input("Wrong menu selection. Enter any key to try again..")


if __name__ == "__main__":
    start()
