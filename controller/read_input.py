import re
import datetime
import random
import os
from faker import Faker

import json

import simpleFaker
from tinydb import TinyDB, Query, where

# import view.view as view

from model.player import Player
# from model.contests import Contest
# from model.tours import Tour


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
            try:
                date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
                switch = 0
            except ValueError:
                print('Unrecognized date format, please try again\n')
        return date

    def read_sex(self):
        switch = 1
        while switch == 1:
            sex = (input('Enter your gender M or F: ')).upper()
            if sex == 'M' or sex == 'F':
                switch = 0
            else:
                print('Unrecognized gender format, please try again\n')
        return sex

    def read_time_control(self):
        switch = 1
        while switch == 1:
            try:
                view.print_menu_time_control()
                time_control = int(input())
                if time_control >= 1 and time_control <= 3:
                    switch = 0
                else:
                    print("Oops!  the number is not between 1 and 3.  Try again...")
                    continue
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")
        return time_control

    def read_ranking(self):
        switch = 1
        while switch == 1:
            try:
                ranking = int(
                    input("Please enter ranking, a number between 1 and 100: "))
                if ranking >= 1 and ranking <= 100:
                    switch = 0
                else:
                    print("Oops!  the number is not between 1 and 100.  Try again...")
                    continue
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")
        return ranking

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
                    print("Oops!  the number is not between 1 and 100.  Try again...\n")
                    continue
            except ValueError:
                print("Oops!  That was no valid number.  Try again...\n")
        return id

    @classmethod
    def read_score(self):
        switch = 1
        while switch == 1:
            try:
                result = float(
                    input("Type 1, 2 or 3: "))
                if result >= 1 and result <= 3:
                    switch = 0
                else:
                    print("Oops!  the number is not between 1 and 3.  Try again...\n")
                    continue
            except ValueError:
                print("Oops!  That was no valid number.  Try again...\n")
        return result

    def read_name(self, type_name):
        while True:
            if type_name == 1:
                name = input("Enter player firstname: ")
            elif type_name == 2:
                name = input('Enter player lastname: ')
            elif type_name == 3:
                name = input('Enter tournament name: ')
            else:
                name = input('Enter the tournament location: ')
            if not name.isalpha():
                print("Please enter characters A-Z only")
            elif len(name) > 40:
                print("Error! Only 40 characters maximum allowed!")
            else:
                break
        return name

    def read_comments(self):
        switch = 1
        while switch == 1:
            comments = input(
                'Do you want to add any comments \(max:1000 characters\): ')
            if len(comments) > 1000:
                print('Please try again the limit characters is 1000')
            else:
                switch = 0
        return comments

    @ classmethod
    def create_players(self):
        read_input = ReadInformation()
        players = []
        random_list = []
        random_list = (list(range(1, 9)))
        random.shuffle(random_list)

        faker = Faker()
        # create rounds
        for n in range(0, 1):

            # Enter informations about a player
            firstname = read_input.read_name(1)
            lastname = read_input.read_name(2)
            birthdate = read_input.read_date(1)
            sex = read_input.read_sex()
            ranking = read_input.read_ranking()

            # create a fake list of 8 players
            # profile = faker.simple_profile()
            # name = profile['name'].split()
            # firstname = name[0]
            # lastname = name[1]
            # birthdate = profile['birthdate']
            # sex = profile['sex']
            # ranking = random_list[n]
            # Create an instance of a player
            player = Player(n, firstname, lastname,
                            birthdate, sex, ranking)
            # serialize a player
            serialized_player = player.serialization_player()
            # Add all serialized players in a list
            players.append(player)
        return(players)

    @ classmethod
    def read_contest_information(self):
        # name = read_name(3)
        # location = read_name(4)
        # date = read_date(0)
        # time_control = read_time_control()
        # comments = read_comments()

        contest_list = []
        # Create a contest
        faker = Faker()
        name = faker.name()
        contest_list.append(name)
        location = faker.address()
        contest_list.append(location)
        date = faker.date_of_birth()
        contest_list.append(date)
        time_control = faker.random_int(1, 3)
        contest_list.append(time_control)
        comments = faker.text()
        contest_list.append(comments)

        db = TinyDB('db.json', indent=4)
        players_table = db.table('players')

        # print(type(players_table))
        # print(len(players_table))
        # print(players_table)
        if len(players_table) < 8:
            print(
                "you cannot create a contest because there are not enough registered players")
            return None,
        players_ids = []
        players_obj = []
        while len(players_ids) != 8:
            # id = int(input('Enter player Id: '))
            id = ReadInformation.read_id(len(players_ids))
            ret = players_table.contains(doc_id=id)
            if(ret == False):
                print(
                    "this player doesn't exist in dataBase. Please, try another Id !\n")
            elif id in players_ids:
                print("You have already saved this player for this contest\n")
            else:
                players_ids.append(id)
                player_dict = players_table.get(doc_id=id)
                print(
                    f"{player_dict['firstname']} {player_dict['lastname']} is added to contest.\n")
                player = Player()
                player.deserializing_player(player_dict)
                players_obj.append(player)
        print('The players are now full for this contest\n')
        print('\nType enter to continue...')
        os.system('clear')
        contest_list.append(players_obj)
        return contest_list
