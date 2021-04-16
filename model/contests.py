# import json
import random
import datetime

from tinydb import TinyDB, where

from model.tours import Tour
from model.player import Player


class Contest(object):
    def __init__(self, name=None, location=None, date=None,
                 time_control=None, comments=None, players=None, nb_turns=4):
        self.name = name
        self.location = location
        self.date = date
        self.nb_turns = nb_turns
        self.time_control = time_control
        self.comments = comments
        self.rounds = []
        self.players = players

    def add_rounds(self, round):
        self.rounds.append(round)

    # Create a list of rounds
    def create_rounds(self, nb_rounds):
        for i in range(nb_rounds):
            self.add_rounds(Tour('Round ' + str(i + 1)))

    def create_matches(self, nb_rounds, nb_matches):
        for i in range(nb_matches):
            for j in range(nb_matches):
                self.rounds[i].add_matches([])

    # get a list of serialized players
    def serialization_players(self):
        serialized_players = []
        for player in self.players:
            # serialize a player
            serialized_player = player.serialization_player2()
            # TODO change serialization_player
            # Add all serialized players in a list
            serialized_players.append(serialized_player)
        return serialized_players

    # Serialize a contest
    def serialization_contest(self):
        self.serialized_contest = {
            'name': self.name,
            'location': self.location,
            'date': str(self.date),
            'nb_turns': self.nb_turns,
            'time_control': self.time_control,
            'comments': self.comments,
            "rounds":   {round.round_name:
                         round.serialization_round() for round in self.rounds},
            'players': self.serialization_players()
        }

    def get_id(self):
        db = TinyDB('db.json', indent=4)
        contests_table = db.table('contests')
        doc = contests_table.search(where('name') == self.name)
        return doc[0].doc_id

    # Save players table in database
    @ classmethod
    def save_players2(self, serialized_players, players):
        n = 0
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        for item in serialized_players:
            # print(item)
            id = players_table.insert(item)
            players_table.update({'id_player': id}, doc_ids=[id])
            item['id_player'] = id
            for player in players:
                if player.lastname == item['lastname'] and \
                        player.firstname == item['firstname']:
                    player.id_player = id
            n += 1

    def save(self):
        db = TinyDB('db.json', indent=4)
        contests_table = db.table('contests')
        players_table = db.table('players')
        contests_table.insert(self.serialized_contest)
        # TODO insert id_player in contests table

        # TODO update rank and point in players table
        for player in self.players:
            ret = players_table.update_multiple([
                # ({'firstname': firstname}, where('id_player') == id_player),
                # ({'lastname': lastname}, where('id_player') == id_player),
                # ({'birthdate': birthdate}, where('id_player') == id_player),
                # ({'sex': sex}, where('id_player') == id_player),
                ({'ranking': player.ranking}, where(
                    'id_player') == player.id_player),
                ({'point': player.point}, where('id_player') == player.id_player),
            ])

    def deserializing_players_list(self, players_dict):
        db = TinyDB('db.json', indent=4)
        player_table = db.table('players')
        self.players = []
        for player_item in players_dict:
            # print(player_item)
            # print(player_item['id_player'])
            player_dict = player_table.get(doc_id=player_item['id_player'])
            # print(f"test:[{player_dict}]")
            # input()
            player = Player()
            player.deserializing_player(player_dict)
            self.players.append(player)

    def deserializing_rounds(self, rounds):
        self.rounds = []
        for key, value in rounds.items():
            round = Tour(key, value['start_datetime'], value['end_datetime'])
            for key2, value2 in value['matches'].items():
                list1 = []
                list2 = []

                if not value2:
                    pass
                else:
                    list1 = [value2[0][0], value2[0][1]]
                    list2 = [value2[1][0], value2[1][1]]
                    match_tuple = (list1, list2)
                    round.matches.append(match_tuple)
            self.rounds.append(round)

    def deserializing_contest(self, contest):
        self.name = contest['name']
        self.location = contest['location']
        self.date = contest['date']
        self.nb_turns = contest['nb_turns']
        self.time_control = contest['time_control']
        self.comments = contest['comments']
        self.deserializing_rounds(contest['rounds'])
        self.deserializing_players_list(contest['players'])

    @ classmethod
    def get_contests_data(self):
        contests = []
        db = TinyDB('db.json', indent=4)
        contest_table = db.table('contests')
        for item in contest_table:
            contest = Contest()
            contest.deserializing_contest(item)
            contests.append(contest)
        return contests

    def get_players_contest(self, contest_name):
        db = TinyDB('db.json', indent=4)
        contests_table = db.table('contests')
        # update
        # players_table = db.table('players')
        contest_doc = contests_table.search(
            where('name') == contest_name)
        if not contest_doc:
            return -1
        else:
            self.deserializing_contest(contest_doc[0])
            return 0

    @ classmethod
    def get_contests(self):
        contests = Contest.get_contests_data()
        return contests

    def display_scores_matches(self, nb_round, total_nb_matches, cond):
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        # User = Query()
        print(f'Round {nb_round + 1}:\n')
        if cond == 1:
            string = self.rounds[nb_round].start_datetime
            date = datetime.datetime.strptime(string, "%Y-%m-%d  %H:%M:%S.%f")
            print(
                f"start: {date.year}/{date.month}/{date.day} "
                f"{date.hour}:{date.minute}:{date.second}\n")
            string = self.rounds[nb_round].end_datetime
            date = datetime.datetime.strptime(string, "%Y-%m-%d  %H:%M:%S.%f")
            print(
                f"end  : {date.year}/{date.month}/{date.day} "
                f"{date.hour}:{date.minute}:{date.second}\n")
        print()
        print(65 * "-")
        print(
            f"| match{3 * ' '}| Player 1{11 * ' '}| "
            f"Player 2{10 * ' '}| scores{5 * ' '}|")
        print(65 * "-")
        for match in range(total_nb_matches):
            id_player = self.rounds[nb_round].matches[match][0][0]
            score1 = self.rounds[nb_round].matches[match][0][1]
            player_dict = players_table.get(doc_id=id_player)
            print(
                f"| {match + 1} {6 * ' '}| {player_dict['firstname']} "
                f"{player_dict['lastname']} ".ljust(31), end='|')

            id_player = self.rounds[nb_round].matches[match][1][0]
            score2 = self.rounds[nb_round].matches[match][1][1]
            player_dict = players_table.get(doc_id=id_player)
            print(
                f" {player_dict['firstname']} "
                f"{player_dict['lastname']}".ljust(19), end='|')
            print(f" {score1}".ljust(4),   f"- {score2}".ljust(6), "|")
            print(65 * "-")

    def display_assignement_players(self, nb_round, total_nb_matches):
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        # User = Query()
        print(50 * "-")
        for match in range(total_nb_matches):
            id_player = self.rounds[nb_round].matches[match][0][0]
            player_dict = players_table.get(doc_id=id_player)
            print(
                f"|match: {match + 1} | {player_dict['firstname']} "
                f"{player_dict['lastname']} ".ljust(33), end='|')

            id_player = self.rounds[nb_round].matches[match][1][0]
            player_dict = players_table.get(doc_id=id_player)
            print(
                f" {player_dict['firstname']} "
                f"{player_dict['lastname']}".ljust(15), end='|\n')
            print(50 * "-")

    # display matches
    def display_round(self, nb_round, total_nb_matches):
        # db = TinyDB('db.json', indent=4)
        # players_table = db.table('players')
        for match in range(total_nb_matches):
            id_player = self.rounds[nb_round].matches[match][0][0]
            # contest.players

            value = [x for x in self.players if x.id_player == id_player]
            print(
                f"player 1: {value[0].firstname} {value[0].lastname}: {self.rounds[nb_round].matches[match][0][1]}")
            # print(f"value: {value}")
            # player_dict = players_table.get(doc_id=id_player)
            # print(
            #     f"{player_dict['firstname']} "
            #     f"{player_dict['lastname']}: ".ljust(20), end=' ')
            # print(f'{self.rounds[nb_round].matches[match][0][1]}')

            id_player = self.rounds[nb_round].matches[match][1][0]
            value = [x for x in self.players if x.id_player == id_player]
            print(
                f"player 2: {value[0].firstname} {value[0].lastname}: {self.rounds[nb_round].matches[match][1][1]}")

            # player_dict = players_table.get(doc_id=id_player)
            # print(
            #     f"{player_dict['firstname']} "
            #     f"{player_dict['lastname']}: ".ljust(20), end=' ')
            # print(f'{self.rounds[nb_round].matches[match][1][1]}\n')

    # save scores for matches in Round 0
    def save_scores(self, nb_round, nb_matches):
        win = 1
        lose = 0
        draw = 0.5
        for nb_match in range(nb_matches):
            # attribute score for player 1
            score1 = random.choice([win, lose, draw])
            self.rounds[nb_round].matches[nb_match][0][1] = score1
            for x in self.players:
                if x.id_player == \
                        self.rounds[nb_round].matches[nb_match][0][0]:
                    if nb_round == 0:
                        x.point = score1
                    else:
                        x.point += score1
                    break
            if score1 == win:
                score2 = lose
            elif score1 == lose:
                score2 = win
            else:
                score2 = draw
            # attribute score for player 2
            self.rounds[nb_round].matches[nb_match][1][1] = score2
            for y in self.players:
                if y.id_player == \
                        self.rounds[nb_round].matches[nb_match][1][0]:
                    if nb_round == 0:
                        y.point = score2
                    else:
                        y.point += score2
                    break
    # save scores for matches in Round 0

    def save_scores2(self, nb_round, nb_matches, result_matches):
        win = 1
        lose = 0
        draw = 0.5
        for nb_match in range(nb_matches):
            # attribute score for player 1
            # score1 = random.choice([win, lose, draw])
            if result_matches[nb_match] == 1:
                score1 = win
                score2 = lose
            elif result_matches[nb_match] == 2:
                score1 = lose
                score2 = win
            else:
                score1 = draw
                score2 = draw
            # id_player1 = 0
            # id_player2 = 0
            self.rounds[nb_round].matches[nb_match][0][1] = score1
            for x in self.players:
                if x.id_player == \
                        self.rounds[nb_round].matches[nb_match][0][0]:
                    # player1 = x
                    # id_player1 = x.id_player
                    if nb_round == 0:
                        x.point = score1
                    else:
                        x.point += score1
                    break
            # attribute score for player 2
            self.rounds[nb_round].matches[nb_match][1][1] = score2
            for y in self.players:
                if y.id_player == \
                        self.rounds[nb_round].matches[nb_match][1][0]:
                    # player2 = y
                    # id_player2 = y.id_player
                    if nb_round == 0:
                        y.point = score2
                    else:
                        y.point += score2
                    break
            # player1.history_match.append(id_player2)
            # player2.history_match.append(id_player1)

    @ classmethod
    def get_size_players_table(self):
        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')
        if len(players_table) < 8:
            return None
        else:
            return players_table
