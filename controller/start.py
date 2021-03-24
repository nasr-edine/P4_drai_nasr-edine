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
    view.view_function()

    while True:
        view.print_menu()
        choice = input("Enter your choice [1-5]: ")
        if choice == '1':

            # Create a list of players
            players = Player.create_players()
            print("Create a random list of players")
            print(players)
            input()

            # Sorting players list
            Player.Sorting_players_by_ranking(players)
            print("Sorting list of players by ranking")
            print(players)
            input()

            # input players
            # name = read_name(3)
            # location = read_name(4)
            # date = read_date(0)
            # time_control = read_time_control()
            # comments = read_comments()

            # Create a tournament
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
            nb_matches = 4
            contest.create_rounds(nb_rounds)

            # Create matches
            contest.create_matches(nb_matches, nb_matches)

            # tournament serialization
            contest.serialization_contest()

            # Save  tournament in DataBase
            contest.save()

            # Generate all matches for first round
            first_round = 0
            print('generate first round')
            contest.rounds[first_round].start_datetime = datetime.datetime.now()
            contest.rounds[first_round].end_datetime = contest.rounds[first_round].start_datetime + \
                datetime.timedelta(hours=1)
            Tour.matches_generator(contest, first_round)

            # display all matches for round 0
            contest.display_round(first_round, nb_matches)

            contest.serialization_contest()
            contest.save()

            # save scores for matches in Round 0
            win = 1
            lose = 0
            draw = 0.5
            # number_list = [win, lose, draw]
            for nb_matches in range(nb_matches):
                # attribute score for player 1
                score1 = random.choice([win, lose, draw])
                contest.rounds[0].matches[nb_matches][0][1] = score1
                for x in contest.players:
                    if x.id_player == contest.rounds[0].matches[nb_matches][0][0]:
                        x.point = score1
                        break
                if score1 == win:
                    score2 = lose
                elif score1 == lose:
                    score2 = win
                else:
                    score2 = draw
                contest.rounds[0].matches[nb_matches][1][1] = score2
                for y in contest.players:
                    if y.id_player == contest.rounds[0].matches[nb_matches][1][0]:
                        y.point = score2
                        break
            print("display scores for round 0")
            contest.display_round(0, nb_matches)
            input()
            contest.serialization_contest()
            contest.save()

            print('display players after attrib scores:')
            print(contest.players)

            # sorting players by point
            print("sorting players by point")
            contest.players = Player.sort_players_by_point(contest.players)
            print(contest.players)
            contest.serialization_contest()
            contest.save()

            for nb_rounds in range(1, 4):
                # Generate second round
                print(f"Generate round: {nb_rounds}")
                contest.rounds[nb_rounds].start_datetime = datetime.datetime.now()
                contest.rounds[nb_rounds].end_datetime = contest.rounds[nb_rounds].start_datetime + \
                    datetime.timedelta(hours=1)
                Tour.matches_generator(contest, nb_rounds)
                print(contest.players)
                contest.serialization_contest()
                contest.save()
                input()

                print(f"save scores for all matches in Round {nb_rounds}")
                i = 0
                for nb_matches in range(4):
                    # attribute score for player 1
                    score1 = random.choice([win, lose, draw])

                    contest.rounds[nb_rounds].matches[nb_matches][0][1] = score1
                    for x in contest.players:
                        if x.id_player == contest.rounds[nb_rounds].matches[nb_matches][0][0]:
                            x.point += score1
                            # print(f'player 2: {y.id_player}, {y.point}')
                            break
                    # attribute score for player 2
                    if score1 == win:
                        score2 = lose
                    elif score1 == lose:
                        score2 = win
                    else:
                        score2 = draw
                    contest.rounds[nb_rounds].matches[nb_matches][1][1] = score2
                    for y in contest.players:
                        if y.id_player == contest.rounds[nb_rounds].matches[nb_matches][1][0]:
                            y.point += score2
                        # print(f'player 2: {y.id_player}, {y.point}')
                            break
                    i += 2
                contest.serialization_contest()
                contest.save()
                print(f'before sorting:\n{contest.players}')
                input('after sorting:')
                contest.players = Player.sort_players_by_point(contest.players)
                input()
                for n in range(4):
                    print(contest.rounds[nb_rounds].matches[n])
                print(contest.players)
                input()

            # sorting players by point
            contest.players = Player.sort_players_by_point(contest.players)
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
