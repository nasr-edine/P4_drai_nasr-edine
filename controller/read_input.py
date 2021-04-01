import re
import datetime
import random
from faker import Faker

import json

import simpleFaker
# import view.view as view

# from model.player import Player
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
                    input("Please enter ranking, a number between 1 and 8: "))
                if ranking >= 1 and ranking <= 8:
                    switch = 0
                else:
                    print("Oops!  the number is not between 1 and 8.  Try again...")
                    continue
            except ValueError:
                print("Oops!  That was no valid number.  Try again...")
        return ranking

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
        return contest_list