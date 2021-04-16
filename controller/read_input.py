import datetime

import view.view as view

from model.player import Player
from model.contests import Contest


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
                time_control = int(input("tape a number: "))
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
                          "a number between 0 and 100: "))
                print()
                if ranking >= 0 and ranking <= 100:
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
                    input(f"Tape id number for player {number_player + 1}: "))
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
                name = input('Enter the contest name: ')
                print()
            else:
                name = input('Enter the contest location: ')
                print()
            name = name.strip()
            if not name:
                view.print_msg_error_13()
            elif type_name == 3 or type_name == 4:
                break
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
        players_table = Contest.get_size_players_table()
        if not players_table:
            view.print_msg_error_17()
            view.clear_screen()
            return None
        read_input = ReadInformation()
        contest_list = []
        contest_list.append(read_input.read_name(3))
        contest_list.append(read_input.read_name(4))
        contest_list.append(read_input.read_date(0))
        contest_list.append(read_input.read_time_control())
        contest_list.append(read_input.read_comments())
        view.clear_screen_without_msg()

        view.infos_3()
        players_ids = []
        players_obj = []
        while len(players_ids) != 8:
            id = ReadInformation.read_id(len(players_ids))

            ret = Player.player_exists(players_table, id)
            if ret is False:
                view.print_msg_error_18()
            elif id in players_ids:
                view.print_msg_error_19()
            else:
                players_ids.append(id)
                player = Player()
                player_dict = player.get_player_from_id(id)
                player.deserializing_player(player_dict)
                view.infos_5(player)
                players_obj.append(player)
        view.infos_4()
        contest_list.append(players_obj)
        return contest_list
