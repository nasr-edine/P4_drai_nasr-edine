import datetime

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
    player.save_player()
    view.infos_2(player)


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


def choice_display_players(type_sorting):
    players_list = Player.get_players()
    # print(type(players_list))
    # print((players_list))
    if not players_list:
        view.print_msg_error_3()
    elif type_sorting == 1:
        view.print_players_sorting_by_name(players_list)
        view.clear_screen()
    else:
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


def choice_add_new_contest():
    contest_list = ReadInformation.read_contest_information()
    if not contest_list:
        return None
    contest = Contest(contest_list[0], contest_list[1], contest_list[2],
                      contest_list[3], contest_list[4], contest_list[5])
    view.infos_contest(contest)
    view.clear_screen()
    nb_rounds = 4
    nb_matches = 4
    current_round = 0

    contest.create_rounds(nb_rounds)
    contest.create_matches(nb_rounds, nb_matches)
    for n in range(4):
        view.infos_9(current_round)
        contest.rounds[current_round].start_datetime = \
            datetime.datetime.now()
        contest.rounds[current_round].end_datetime = \
            contest.rounds[current_round].start_datetime + \
            datetime.timedelta(hours=1)
        Tour.matches_generator(contest, current_round)
        contest.display_assignement_players(current_round, nb_matches)
        view.clear_screen()
        view.infos_6()
        result_matches = []
        for n in range(4):
            view.infos_10(n)
            name_player_1 = Player.get_name_player(
                contest.rounds[current_round].matches[n][0][0])
            name_player_2 = Player.get_name_player(
                contest.rounds[current_round].matches[n][1][0])
            view.infos_11(name_player_1, name_player_2)
            result_matches.append(ReadInformation.read_score())
            view.clear_screen()
        view.clear_screen()
        contest.save_scores2(current_round, nb_matches, result_matches)
        view.display_round(contest, current_round, nb_matches)
        view.clear_screen()
        contest.players = Player.sort_players_by_point(contest.players)
        current_round += 1
    contest.serialization_contest()
    contest.save()
    for player in contest.players:
        view.infos_7(player)
        input_control = ReadInformation()
        player.ranking = input_control.read_ranking()
        player.update_ranking()
        view.infos_8()
        view.infos_7(player)
        view.clear_screen()
    return contest


def start():
    created_contest = 0
    while True:
        view.print_menu()
        choice = input("Enter your choice [1-10]: ")
        view.clear_screen_without_msg()
        # TODO put a switch statement
        # switch()
        if choice == '1':
            choice_add_new_player()
        elif choice == '2':
            contest = choice_add_new_contest()
            if not contest:
                continue
            created_contest = 1
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
            choice_display_players(1)
        elif choice == '7':
            choice_display_players(2)
        elif choice == '8':
            choice_display_players_for_a_contest()
        elif choice == '9':
            choice_display_rounds()
        elif choice == '10':
            choice_display_matches()
        elif choice == '11':
            view.endView()
        else:
            view.wrong_menu()


if __name__ == "__main__":
    start()
