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

from controller.read_input import ReadInformation


def showAll():
    result = Player.getAll()
    return view.showAllView(result)

    result = Player.getAll2()
    return view.showAllView(result)


def start():

    # Create a list of players
    print("Please enter informations about each player:\n")
    players = Player.create_players()
    print(players)
    input()

    # Sorting players list by ranking
    Player.sort_players_by_ranking(players)
    print("Sorting players by ranking:\n")
    print(players)
    input()

    print("Please enter informations about new contest:\n")
    contest_list = ReadInformation.read_contest_information()
    contest = Contest(contest_list[0], contest_list[1], contest_list[2],
                      contest_list[3], contest_list[4], players)

    # Create rounds
    nb_rounds = 4
    contest.create_rounds(nb_rounds)

    # Create matches
    nb_matches = 4
    contest.create_matches(nb_matches, nb_matches)
    # serialize contest
    # contest.serialization_contest()
    # Save  contest in DataBase
    # contest.save()

    current_round = 0
    while True:
        view.print_menu()
        choice = input("Enter your choice [1-5]: ")
        if choice == '1':
            if current_round == 0:
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

                # contest.serialization_contest()
                # contest.save()

                print("Please enter results for each matches in round 0")
                print("type 1: Player 1 wins")
                print("type 2: Player 2 wins")
                print("type 3: draw\n")
                result_matches = [1, 2, 3, 1]
                # result_matches = []
                for n in range(4):
                    print(f"match {n}: ")
                    # result_matches.append(int(input("enter 1, 2 or 3: ")))
                    print()

                # save scores for all matches in first round
                contest.save_scores2(first_round, nb_matches, result_matches)
                # contest.save_scores(first_round, nb_matches)
                # print("display scores for first round:\n")
                # contest.display_round(first_round, nb_matches)
                # input()

                # contest.serialization_contest()
                # contest.save()

                # print('display scores by player:\n')
                # print(contest.players)
                # input()
                # print("sorting players by point:\n")
                contest.players = Player.sort_players_by_point(contest.players)
                # print(contest.players)
                # input()
                # contest.serialization_contest()
                # contest.save()
                current_round += 1
            elif current_round < 4:
                nb_round = current_round
            # for nb_round in range(1, 4):

                # Generate next round
                contest.rounds[nb_round].start_datetime = datetime.datetime.now()
                contest.rounds[nb_round].end_datetime = contest.rounds[nb_round].start_datetime + \
                    datetime.timedelta(hours=1)
                Tour.matches_generator(contest, nb_round)

                print(f"Generate round: {nb_round}\n")
                contest.display_round(nb_round, nb_matches)
                input()

                # contest.save_scores(nb_round, nb_matches)
                print(
                    f"Please enter results for each matches in round {nb_round}")
                print("type 1: Player 1 wins")
                print("type 2: Player 2 wins")
                print("type 3: draw\n")
                result_matches = []
                result_matches = [1, 2, 3, 1]
                for n in range(4):
                    print(f'match {n}: ')
                    # result_matches.append(int(input("enter 1, 2 or 3: ")))
                    print()
                # print(result_matches)
                contest.save_scores2(nb_round, nb_matches, result_matches)

                # contest.serialization_contest()
                # contest.save()

                # print(f'display scores for round: {nb_round}:\n')
                # contest.display_round(nb_round, nb_matches)
                # input()
                # print("display scores by player:\n")
                # print(contest.players)
                # input()
                contest.players = Player.sort_players_by_point(contest.players)
                # print("Sorting players by point:\n")
                # print(contest.players)
                # input()
                # contest.serialization_contest()
                # contest.save()
                current_round += 1
                print(f"{contest.players[0].history_match}")
                print(f"{contest.players[1].history_match}")
                print(f"{contest.players[2].history_match}")
                print(f"{contest.players[3].history_match}")
                print(f"{contest.players[4].history_match}")
                print(f"{contest.players[5].history_match}")
                print(f"{contest.players[6].history_match}")
                print(f"{contest.players[7].history_match}")
            else:
                print('you have reached the maximum possible of round for a contest')
            # exit()

        elif choice == '2':
            contest.serialization_contest()
            contest.save()

        elif choice == '3':
            create_players()
        elif choice == '4':
            print(contest.players)
            # showAll()
        elif choice == '5':
            view.endView()
            exit()
        elif choice == '6':
            # print(contest.players)
            for player in contest.players:
                print(player.view_player())
        else:
            input("Wrong menu selection. Enter any key to try again..")


if __name__ == "__main__":
    start()
