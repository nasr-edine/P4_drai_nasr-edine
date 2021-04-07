import re
import datetime
import random
import json
import simpleFaker
import os
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

    # create a player
    def add_player():
        print("Please enter informations about player:\n")
        players = ReadInformation.create_players()
        os.system('clear')
        print(players[0].view_player())
        print('Good, the player is added.')
        view.clear_screen()
        ret = Player.serialization_players(players)
        Contest.save_players2(ret, players)
        # Sorting players list by ranking
        Player.sort_players_by_ranking(players)

    # create a contest
    def create_contest():
        print("Please enter id for each player, a number between 1 and 100:\n")
        # players = []
        contest_list = ReadInformation.read_contest_information()
        if not contest_list[0]:
            return None
        contest = Contest(contest_list[0], contest_list[1], contest_list[2],
                          contest_list[3], contest_list[4], contest_list[5])
        view.infos_contest(contest)
        view.clear_screen()

        # Create rounds
        nb_rounds = 4
        contest.create_rounds(nb_rounds)

        # Create matches
        nb_matches = 4
        contest.create_matches(nb_matches, nb_matches)

        print_round_nb = ['First', 'Second', 'Third', 'Fourth']

        current_round = 0
        for n in range(4):
            if current_round == 0:
                # Generate all matches for first round
                first_round = 0
                print(f'{print_round_nb[first_round]} round:\n')
                contest.rounds[first_round].start_datetime = datetime.datetime.now()
                contest.rounds[first_round].end_datetime = contest.rounds[first_round].start_datetime + \
                    datetime.timedelta(hours=1)
                Tour.matches_generator(contest, first_round)

                contest.display_assignement_players(first_round, nb_matches)
                view.clear_screen()
                print("Record the scores\n")
                print("type 1: The first player wins the match")
                print("type 2: The second player wins the match")
                print("type 3: Draw\n")
                db = TinyDB('db.json', indent=4)
                players_table = db.table('players')
                result_matches = []
                for n in range(4):
                    print(f"match {n + 1}:")
                    player1 = players_table.get(
                        doc_id=contest.rounds[current_round].matches[n][0][0])
                    player2 = players_table.get(
                        doc_id=contest.rounds[current_round].matches[n][1][0])
                    print(
                        f"|1: {player1['firstname']} {player1['lastname']}".ljust(20), end='')
                    print(
                        f"|2: {player2['firstname']} {player2['lastname']}".ljust(20), "|")
                    result_matches.append(ReadInformation.read_score())
                    print('')
                view.clear_screen()
                # save scores for all matches in first round
                contest.save_scores2(first_round, nb_matches, result_matches)
                print(30 * "-", f"Round {first_round + 1}", 30 * "-")
                contest.display_round(first_round, nb_matches)
                print(73 * "-")
                view.clear_screen()
                contest.players = Player.sort_players_by_point(contest.players)
                current_round += 1
            elif current_round < 4:
                nb_round = current_round
                contest.rounds[nb_round].start_datetime = datetime.datetime.now()
                contest.rounds[nb_round].end_datetime = contest.rounds[nb_round].start_datetime + \
                    datetime.timedelta(hours=1)
                Tour.matches_generator(contest, nb_round)

                print(f'{print_round_nb[current_round]} round:\n')
                contest.display_assignement_players(nb_round, nb_matches)
                view.clear_screen()
                print("Record the scores\n")
                print("type 1: The first player wins the match")
                print("type 2: The second player wins the match")
                print("type 3: Draw\n")

                db = TinyDB('db.json', indent=4)
                players_table = db.table('players')
                result_matches = []
                for n in range(4):
                    print(f"match {n + 1}:")
                    player1 = players_table.get(
                        doc_id=contest.rounds[current_round].matches[n][0][0])
                    player2 = players_table.get(
                        doc_id=contest.rounds[current_round].matches[n][1][0])
                    print(
                        f"|1: {player1['firstname']} {player1['lastname']}".ljust(20), end='')
                    print(
                        f"|2: {player2['firstname']} {player2['lastname']}".ljust(20), "|")
                    result_matches.append(ReadInformation.read_score())
                    print('')
                view.clear_screen()

                contest.save_scores2(nb_round, nb_matches, result_matches)
                print(30 * "-", f"Round {nb_round + 1}", 30 * "-")
                contest.display_round(nb_round, nb_matches)
                print(73 * "-")
                view.clear_screen()
                contest.players = Player.sort_players_by_point(contest.players)
                current_round += 1
            else:
                print('you have reached the maximum possible of round for a contest')
        # print(contest.players)
        contest.serialization_contest()
        contest.save()
        players_ids = []
        players_obj = []

        def update_ranking():
            db = TinyDB('db.json', indent=4)
            players_table = db.table('players')

            for player in contest.players:
                # print(player)
                player_dict = players_table.get(doc_id=player.id_player)
                print(
                    f"player: {player_dict['firstname']} {player_dict['lastname']} current ranking: {player_dict['ranking']}")

                input_control = ReadInformation()
                player.ranking = input_control.read_ranking()
                print(
                    f"The new ranking for player: {player_dict['firstname']} {player_dict['lastname']} is updated")
                print(player.view_player())
                print('\n')
                players_table.update(
                    {'ranking': player.ranking}, doc_ids=[player.id_player])
        update_ranking()
        view.clear_screen()
        return contest
    created_contest = 0
    contest_saved = 0
    while True:

        view.print_menu()
        choice = input("Enter your choice [1-10]: ")
        os.system('clear')
        if choice == '1':
            contest = create_contest()
            if not contest:
                continue
            created_contest = 1
            contest_saved = 0
        elif choice == '2':
            add_player()
        elif choice == '3':
            def update_ranking2():
                db = TinyDB('db.json', indent=4)
                players_table = db.table('players')
                # TODO: check is player exist in db
                id = int(input('Enter player id: '))
                User = Query()
                ret = players_table.contains(doc_id=id)
                if(ret == True):
                    print("You can now update the player:", end=' ')
                    player_dict = players_table.get(doc_id=id)
                    print(
                        f"{player_dict['firstname']} {player_dict['lastname']}.")
                    player = Player()
                    player.deserializing_player(player_dict)

                    input_control = ReadInformation()
                    player.ranking = input_control.read_ranking()
                    print(
                        f"The new ranking for player {player_dict['firstname']} {player_dict['lastname']} is updated")
                    print(player.view_player())
                    players_table.update(
                        {'ranking': player.ranking}, doc_ids=[id])
                    view.clear_screen()
                else:
                    print("this player don't exist in db")
            update_ranking2()
        elif choice == '4':
            if created_contest == 0:
                print('there is no current contest')
                # input('Press any touch to continue.')
                view.clear_screen()
            else:
                print(contest.players)
        elif choice == '6':
            # display playersList
            players_list = Player.get_players()
            if not players_list:
                view.print_msg_error_3()
            else:
                view.print_players_sorting_by_name(players_list)
                view.clear_screen()
                view.print_players_sorting_by_ranking(players_list)
                view.clear_screen()
        elif choice == '7':
            # display players list for a given contest
            contest_query = Contest()
            contest_name = input('Enter the contest name: ')
            if contest_query.get_players_contest(contest_name) == 0:
                view.print_players_sorting_by_name(contest_query.players)
                view.clear_screen()
                view.print_players_sorting_by_ranking(contest_query.players)
                view.clear_screen()
            else:
                view.print_msg_error_2()
        elif choice == '5':
            # display contests list
            contests_list = Contest.get_contests()
            if not contests_list:
                view.print_msg_error_1()
            else:
                view.print_contests_list(contests_list)
                view.clear_screen()
        elif choice == '8':
            contest_query = Contest()
            contest_name = input('Enter the contest name: ')
            os.system('clear')

            if contest_query.get_players_contest(contest_name) == 0:
                # display roundsList
                # view.print_rounds(contest_query.rounds)
                for round in range(4):
                    # view.infos_round(contest_query.rounds[round])
                    contest_query.display_scores_matches(round, 4, 1)
                    view.clear_screen()
                # view.clear_screen()

            else:
                view.print_msg_error_2()
                view.clear_screen()

        elif choice == '9':
            contest_query = Contest()
            contest_name = input('Enter the contest name: ')
            os.system('clear')
            if contest_query.get_players_contest(contest_name) == 0:
                for round in range(4):
                    contest_query.display_scores_matches(round, 4, 0)
                    view.clear_screen()
            else:
                view.print_msg_error_2()
                view.clear_screen()
        elif choice == '10':
            view.endView()
            exit()
        else:
            view.wrong_menu()


if __name__ == "__main__":
    start()
