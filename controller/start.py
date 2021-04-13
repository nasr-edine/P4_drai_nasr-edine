import datetime

from tinydb import TinyDB

import view.view as view
from model.player import Player
from model.contests import Contest
from model.tours import Tour
from controller.read_input import ReadInformation


def choice_add_new_player():
    player_infos = ReadInformation()
    view.infos_1()
    player = player_infos.check_input_player()
    view.clear_screen_without_msg()
    if not player:
        view.print_msg_error_6()
        return
    view.infos_2(player)
    player.save_player()


def choice_update_rank_player():
    input_control = ReadInformation()
    id_player = input_control.read_id2()
    ranking = input_control.read_ranking()
    player = Player()
    ret = player.update_ranking2(id_player, ranking)
    if ret == 1:
        view.print_player_updated(player)
    else:
        view.print_msg_error_4()
    view.clear_screen()


def choice_display_contests():
    # display contests list
    contests_list = Contest.get_contests()
    if not contests_list:
        view.print_msg_error_1()
    else:
        view.print_contests_list(contests_list)
        view.clear_screen()


def choice_display_players():
    players_list = Player.get_players()
    if not players_list:
        view.print_msg_error_3()
    else:
        view.print_players_sorting_by_name(players_list)
        view.clear_screen()
        view.print_players_sorting_by_ranking(players_list)
        view.clear_screen()


def choice_display_players_for_a_contest():
    contest_query = Contest()
    contest_name = input('Enter the contest name: ')
    view.clear_screen_without_msg()
    if contest_query.get_players_contest(contest_name) == 0:
        view.print_players_sorting_by_name(contest_query.players)
        view.clear_screen()
        view.print_players_sorting_by_ranking(
            contest_query.players)
        view.clear_screen()
    else:
        view.print_msg_error_2()


def choice_display_rounds():
    contest_query = Contest()
    contest_name = input('Enter the contest name: ')
    view.clear_screen_without_msg()
    if contest_query.get_players_contest(contest_name) == 0:
        for round in range(4):
            contest_query.display_scores_matches(round, 4, 1)
            view.clear_screen()
    else:
        view.print_msg_error_2()
        view.clear_screen()


def choice_display_matches():
    contest_query = Contest()
    contest_name = input('Enter the contest name: ')
    view.clear_screen_without_msg()
    if contest_query.get_players_contest(contest_name) == 0:
        for round in range(4):
            contest_query.display_scores_matches(round, 4, 0)
            view.clear_screen()
    else:
        view.print_msg_error_2()
        view.clear_screen()


def start():
    # create a contest
    def choice_add_new_contest():
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
                contest.rounds[first_round].start_datetime = \
                    datetime.datetime.now()
                contest.rounds[first_round].end_datetime = \
                    contest.rounds[first_round].start_datetime + \
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
                        f"|1: {player1['firstname']} "
                        f"{player1['lastname']}".ljust(20), end='')
                    print(
                        f"|2: {player2['firstname']} "
                        f"{player2['lastname']}".ljust(20), "|")
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
                contest.rounds[nb_round].start_datetime = \
                    datetime.datetime.now()
                contest.rounds[nb_round].end_datetime = \
                    contest.rounds[nb_round].start_datetime + \
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
                        f"|1: {player1['firstname']} \
                            {player1['lastname']}".ljust(20), end='')
                    print(
                        f"|2: {player2['firstname']} \
                            {player2['lastname']}".ljust(20), "|")
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
                print("you have reached the maximum "
                      "possible of round for a contest")
        contest.serialization_contest()
        contest.save()

        def update_ranking():
            db = TinyDB('db.json', indent=4)
            players_table = db.table('players')

            for player in contest.players:
                # print(player)
                player_dict = players_table.get(doc_id=player.id_player)
                print(
                    f"player: {player_dict['firstname']} "
                    f"{player_dict['lastname']} current ranking: "
                    f"{player_dict['ranking']}")

                input_control = ReadInformation()
                player.ranking = input_control.read_ranking()
                print(
                    f"The new ranking for player: {player_dict['firstname']} "
                    f"{player_dict['lastname']} is updated")
                print(player.__str__())
                print('\n')
                players_table.update(
                    {'ranking': player.ranking}, doc_ids=[player.id_player])
        update_ranking()
        view.clear_screen()
        return contest
    created_contest = 0
    while True:
        view.print_menu()
        choice = input("Enter your choice [1-10]: ")
        view.clear_screen_without_msg()
        if choice == '1':
            contest = choice_add_new_contest()
            if not contest:
                continue
            created_contest = 1
        elif choice == '2':
            choice_add_new_player()
        elif choice == '3':
            choice_update_rank_player()
        elif choice == '4':
            if created_contest == 0:
                view.print_msg_error_5()
                view.clear_screen()
            else:
                view.print_players_list(contest.players)
            view.clear_screen()
        elif choice == '5':
            choice_display_contests()
        elif choice == '6':
            choice_display_players()
        elif choice == '7':
            choice_display_players_for_a_contest()
        elif choice == '8':
            choice_display_rounds()
        elif choice == '9':
            choice_display_matches()
        elif choice == '10':
            view.endView()

        else:
            view.wrong_menu()


if __name__ == "__main__":
    start()
