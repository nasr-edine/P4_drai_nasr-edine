import datetime
import os

from tinydb import TinyDB

import view.view as view

from model.player import Player


class ReadInformation(object):

    def read_date(self, type_date):
        switch = 1
        while switch == 1:
            if type_date == 1:
                date = input(
                    'Enter player birth date in  DD/MM/YEAR format: ')
            else:
                date = input(
                    'Enter  contest date in  DD/MM/YEAR format: ')
            date = date.strip()
            try:
                date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
                switch = 0
            except ValueError:
                view.print_msg_error_7()
        return date

    def read_sex(self):
        switch = 1
        while switch == 1:
            sex = (input('Enter your gender M or F: ')).upper()
            sex = sex.strip()
            if sex == 'M' or sex == 'F':
                switch = 0
            else:
                view.print_msg_error_8()
        return sex.lower()

    def read_time_control(self):
        switch = 1
        while switch == 1:
            try:
                view.print_menu_time_control()
                time_control = int(input())
                if time_control >= 1 and time_control <= 3:
                    switch = 0
                else:
                    view.print_msg_error_9()
                    continue
            except ValueError:
                view.print_msg_error_10()
        return time_control

    def read_ranking(self):
        switch = 1
        while switch == 1:
            try:
                ranking = int(
                    input("Please enter ranking, "
                          "a number between 1 and 100: "))
                print()
                if ranking >= 1 and ranking <= 100:
                    switch = 0
                else:
                    view.print_msg_error_11()
                    continue
            except ValueError:
                view.print_msg_error_12()
        return ranking

    def read_id2(self):
        switch = 1
        while switch == 1:
            try:
                id = int(
                    input("Enter player id: "))
                if id >= 1 and id <= 100:
                    switch = 0
                else:
                    view.print_msg_error_11()
                    continue
            except ValueError:
                view.print_msg_error_12()
        return id

    @classmethod
    def read_id(self, number_player):
        switch = 1
        while switch == 1:
            try:
                id = int(
                    input(f"Type id for player {number_player + 1}: "))
                if id >= 1 and id <= 100:
                    switch = 0
                else:
                    view.print_msg_error_11()
                    continue
            except ValueError:
                view.print_msg_error_12()
        return id

    @classmethod
    def read_score(self):
        switch = 1
        while switch == 1:
            try:
                result = float(
                    input("Type a number: "))
                if result >= 1 and result <= 3:
                    switch = 0
                else:
                    view.print_msg_error_9()
                    continue
            except ValueError:
                view.print_msg_error_12()
        return result

    def read_name(self, type_name):
        while True:
            if type_name == 1:
                name = input("Enter player firstname: ")
                print()
            elif type_name == 2:
                name = input('Enter player lastname: ')
                print()
            elif type_name == 3:
                name = input('Enter tournament name: ')
                print()
            else:
                name = input('Enter the contest location: ')
                print()
            name = name.strip()
            if not name:
                view.print_msg_error_13()
            elif not all(x.isalpha() for x in name):
                view.print_msg_error_14()
            elif len(name) > 40:
                view.print_msg_error_15()
            else:
                break
        return name.lower()

    def read_comments(self):
        switch = 1
        while switch == 1:
            comments = input('Do you want to add any comments'
                             ' (max: 1000 characters): ')
            # = input(')
            if len(comments) > 1000:
                view.print_msg_error_16()
            else:
                switch = 0
        return comments

    def check_input_player(self):
        player = Player()
        player.firstname = self.read_name(1)
        player.lastname = self.read_name(2)
        player.birthdate = self.read_date(1)
        player.sex = self.read_sex()
        player.ranking = self.read_ranking()
        if player.contains_player() is True:
            return None
        return player

    @ classmethod
    def read_contest_information(self):
        read_input = ReadInformation()
        name = read_input.read_name(3)
        location = read_input.read_name(4)
        date = read_input.read_date(0)
        time_control = read_input.read_time_control()
        comments = read_input.read_comments()
        view.clear_screen_without_msg()
        view.infos_3()
        contest_list = []
        contest_list.append(name)
        contest_list.append(location)
        contest_list.append(date)
        contest_list.append(time_control)
        contest_list.append(comments)

        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')

        if len(players_table) < 8:
            print(
                "you cannot create a contest because "
                "there are not enough registered players")
            return None,
        players_ids = []
        players_obj = []
        while len(players_ids) != 8:
            # id = int(input('Enter player Id: '))
            id = ReadInformation.read_id(len(players_ids))
            # os.system('clear')
            ret = players_table.contains(doc_id=id)
            if ret is False:
                print(
                    "this player doesn't exist in"
                    "dataBase. Please, try another Id !\n")
            elif id in players_ids:
                print("You have already saved this player for this contest\n")
            else:
                players_ids.append(id)
                player_dict = players_table.get(doc_id=id)
                print(
                    f"{player_dict['firstname']}"
                    f" {player_dict['lastname']} is added to contest.\n")
                player = Player()
                player.deserializing_player(player_dict)
                players_obj.append(player)
        print('The players are now full for this contest\n')
        print('\nType enter to continue...')
        os.system('clear')
        contest_list.append(players_obj)
        return contest_list
