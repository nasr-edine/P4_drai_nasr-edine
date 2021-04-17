import datetime
# import json

import view.view as view
from model.player import Player
from model.contests import Contest
from model.tours import Tour
from controller.read_input import ReadInformation

from tinydb import TinyDB, Query


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
            if not contest_query.rounds[round].matches:
                print(
                    'the contest is not finished, '
                    'we cannot display the following rounds')
                view.clear_screen()
                return
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
            if not contest_query.rounds[round].matches:
                print(
                    'the contest is not finished, '
                    'we cannot display the following matches')
                view.clear_screen()
                return
            contest_query.display_scores_matches(round, 4, 0)
            view.clear_screen()
    else:
        view.print_msg_error_2()
        view.clear_screen()


def choice_add_new_contest(is_restore, current_round, contest):
    nb_matches = 4
    if is_restore == 0:
        contest_list = ReadInformation.read_contest_information()
        if not contest_list:
            return None
        db = TinyDB('db.json')
        contests_table = db.table('contests')
        User = Query()
        ret = contests_table.contains(User.name == contest_list[0])
        if ret is True:
            print("You cannot create this contest "
                  "because the name is already used !")
            view.clear_screen()
            return
        contest = Contest(contest_list[0], contest_list[1], contest_list[2],
                          contest_list[3], contest_list[4], contest_list[5])
        view.infos_contest(contest)
        view.clear_screen()
        nb_rounds = 4
        nb_matches = 4

        contest.create_rounds(nb_rounds)
        contest.create_matches(nb_rounds, nb_matches)
        contest.serialization_contest()
        contest.save()
    nb_rounds = 4 - current_round
    for n in range(nb_rounds):
        view.infos_9(current_round)
        contest.rounds[current_round].start_datetime = \
            datetime.datetime.now()
        # print("datetime: ", contest.rounds[current_round].start_datetime)

        contest.rounds[current_round].end_datetime = \
            contest.rounds[current_round].start_datetime + \
            datetime.timedelta(hours=1)
        # print("datetime: ", contest.rounds[current_round].end_datetime)

        Tour.matches_generator(contest, current_round)
        contest.display_assignement_players(current_round, nb_matches)
        view.clear_screen()
        result_matches = []
        for n in range(4):
            view.infos_6()
            view.infos_10(n)
            name_player_1 = Player.get_name_player(
                contest.rounds[current_round].matches[n][0][0])
            name_player_2 = Player.get_name_player(
                contest.rounds[current_round].matches[n][1][0])
            view.infos_11(name_player_1, name_player_2)
            result_matches.append(ReadInformation.read_score())
            view.clear_screen_without_msg()
        contest.save_scores2(current_round, nb_matches, result_matches)
        view.display_round(contest, current_round, nb_matches)
        view.clear_screen()
        contest.players = Player.sort_players_by_point(contest.players)
        current_round += 1
        contest.serialization_contest()
        contest.update_contest()

        # print("current_round:", current_round)
        if current_round < 4:
            ret = ReadInformation.read_choice_exit_contest()
            if ret == '1':
                view.clear_screen_without_msg()
                pass
            elif ret == '2':
                view.clear_screen_without_msg()
                return contest
            elif ret == '3':
                exit()
            # else:
    for player in contest.players:
        view.display_players(contest.players)
        view.infos_7(player)
        input_control = ReadInformation()
        player.ranking = input_control.read_ranking()
        player.update_ranking()
        view.clear_screen_without_msg()
        view.infos_8()
        view.infos_7(player)
        view.clear_screen()
    return contest


def restore_contest():
    name_contest = input("Type contest name: ")
    # print(name_contest)
    db = TinyDB('db.json')
    contests_table = db.table('contests')
    User = Query()
    ret = contests_table.contains(User.name == name_contest)
    contest_dict = contests_table.get(User.name == name_contest)
    # json_object = json.loads(contest_dict)
    # json_formatted_str = json.dumps(contest_dict, indent=4)
    if ret is True:
        # print(f"The contest {name_contest} exists in DB")
        contest = Contest()
        contest.deserializing_contest(contest_dict)
        # print("name:", contest.name)
        # print("location:", contest.location)
        # print(contest.rounds)
        # print(contest.rounds[3].matches)
        # print(len(contest.rounds[3].matches))
        if not contest.rounds[3].matches:
            print('You can continue this contest')
            view.clear_screen()
        else:
            print("The contest is already completed")
            view.clear_screen()
            return contest
        # input()
        for round in range(4):
            # print(f"round {round}:", contest.rounds[round].matches)
            if not contest.rounds[round].matches:
                current_round = round
                # print(f"round {round} don't begin")
                break
        # view.display_players(contest.players)
        # print(f"current_round: {current_round}")
        nb_rounds = 4 - current_round
        nb_matches = 4
        # contest.create_rounds(nb_rounds)
        contest.create_matches(nb_rounds, nb_matches)

        choice_add_new_contest(1, current_round, contest)
        view.clear_screen()
        # TODO check if statement is completed or no
    else:
        print("the contest don't exists")
    # print(json_formatted_str)


def start():
    # created_contest = 0
    while True:
        view.print_menu()
        choice = input("Enter your choice [1-10]: ")
        view.clear_screen_without_msg()
        # TODO put a switch statement
        if choice == '1':
            choice_add_new_player()
        elif choice == '2':
            contest = choice_add_new_contest(0, 0, None)
            if not contest:
                continue
            # created_contest = 1
        elif choice == '3':
            contest = restore_contest()
            # created_contest = 1
        elif choice == '4':
            choice_update_rank_player()
        # elif choice == '5':
        #     if created_contest == 0:
        #         view.print_msg_error_5()
        #         view.clear_screen()
        #     else:
        #         view.print_players_list(contest.players)
        #     view.clear_screen()
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
