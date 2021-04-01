import re
import datetime
import random
import json
import simpleFaker

from tinydb import TinyDB, Query, where
from faker import Faker

import controller.start
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

    # create a contest
    def create_contest():
        # Create a list of players
        print("Please enter informations about each player:\n")
        players = Player.create_players()
        print('list of players')
        print(players)
        input()
        ret = Player.serialization_players(players)
        Contest.save_players2(ret, players)
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
        for n in range(4):
            if current_round == 0:
                # Generate all matches for first round
                first_round = 0
                print('creating first round:\n')
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
                # save scores for all matches in first round
                contest.save_scores2(first_round, nb_matches, result_matches)
                print(f'results for round {first_round}')
                contest.display_round(first_round, nb_matches)
                input()
                contest.players = Player.sort_players_by_point(contest.players)
                current_round += 1
            elif current_round < 4:
                nb_round = current_round
                contest.rounds[nb_round].start_datetime = datetime.datetime.now()
                contest.rounds[nb_round].end_datetime = contest.rounds[nb_round].start_datetime + \
                    datetime.timedelta(hours=1)
                Tour.matches_generator(contest, nb_round)

                print(f"Generate round: {nb_round}\n")
                contest.display_round(nb_round, nb_matches)
                input()
                print(
                    f"Please enter results for each matches in round {nb_round}")
                print("type 1: Player 1 wins")
                print("type 2: Player 2 wins")
                print("type 3: draw\n")
                result_matches = []
                result_matches = [1, 2, 3, 1]
                contest.save_scores2(nb_round, nb_matches, result_matches)
                contest.display_round(nb_round, nb_matches)
                input()
                contest.players = Player.sort_players_by_point(contest.players)
                current_round += 1
            else:
                print('you have reached the maximum possible of round for a contest')
        return contest
    created_contest = 0
    contest_saved = 0
    while True:

        view.print_menu()
        choice = input("Enter your choice [1-5]: ")
        if choice == '1':
            contest = create_contest()
            created_contest = 1
            contest_saved = 0
        elif choice == '2':
            if created_contest == 0:
                print('there is no contest created')
            else:
                if contest_saved == 0:
                    contest.serialization_contest()
                # contest.save_players()
                # ret = Player.serialization_players(contest.players)
                # Contest.save_players2(ret, contest.players)
                    contest.save()
                    contest_saved = 1
                else:
                    print('the contest has already been saved')

        elif choice == '3':
            # create_players()
            pass

        elif choice == '4':
            if created_contest == 0:
                print('there is no contest created')
            else:
                print(contest.players)
        elif choice == '5':
            view.endView()
            exit()
        elif choice == '6':
            # display playersList
            players_list = Player.get_players()
            if not players_list:
                view.print_msg_error_3()
            else:
                # display playersList sorting by name
                view.print_players_sorting_by_name(players_list)
                # display playersList sorting by ranking
                view.print_players_sorting_by_ranking(players_list)
        elif choice == '7':
            # display players list for a given contest
            contest_query = Contest()
            contest_name = input('Enter the contest name: ')
            if contest_query.get_players_contest(contest_name) == 0:
                # playersList sorting by name
                view.print_players_sorting_by_name(contest_query.players)
                # playersList sorting by ranking
                view.print_players_sorting_by_ranking(contest_query.players)

                # display roundsList
                # view.print_rounds(contest_query.rounds)
                # todo matchesList
                # view.print_matches(contest_query.rounds)
            else:
                view.print_msg_error_2()
        elif choice == '8':
            # display contests list
            contests_list = Contest.get_contests()
            if not contests_list:
                view.print_msg_error_1()
            else:
                view.print_contests_list(contests_list)
        elif choice == '9':
            contest_query = Contest()
            contest_name = input('Enter the contest name: ')
            if contest_query.get_players_contest(contest_name) == 0:
                # display roundsList
                view.print_rounds(contest_query.rounds)
                # todo matchesList
                # view.print_matches(contest_query.rounds)
            else:
                view.print_msg_error_2()
        elif choice == '10':
            contest_query = Contest()
            contest_name = input('Enter the contest name: ')
            if contest_query.get_players_contest(contest_name) == 0:
                # playersList sorting by name
                # view.print_players_sorting_by_name(contest_query.players)
                # playersList sorting by ranking
                # view.print_players_sorting_by_ranking(contest_query.players)

                # display roundsList
                # view.print_rounds(contest_query.rounds)
                # todo matchesList
                view.print_matches(contest_query.rounds)
            else:
                view.print_msg_error_2()
        else:
            input("Wrong menu selection. Enter any key to try again..")


if __name__ == "__main__":
    start()
