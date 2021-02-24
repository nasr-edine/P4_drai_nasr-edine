from faker import Faker
import dumper
import random

faker = Faker()


class FakeContest:
    def __init__(self, name, location, date, player_index, time_control, comments, rounds, nb_turns=4):
        self.name = name
        self.location = location
        self.date = date
        self.nb_turns = nb_turns
        self.player_index = player_index
        self.time_control = time_control
        self.comments = comments
        self.rounds = rounds


class FakeProfile:
    def __init__(self, firstname, lastname, sex, birthdate, ranking):
        self.firstname = firstname
        self.lastname = lastname
        self.sex = sex
        self.birthdate = birthdate
        self.ranking = ranking


def print_contest(contest):
    temp = vars(contest)
    for item2 in temp:
        print(str(temp[item2]).ljust(15), end='\n')


def print_profiles(list):
    for item in list:
        temp = vars(item)
        for item2 in temp:
            print(str(temp[item2]).ljust(15), '|', sep='', end='')
        print()


def faker_contest():
    name = faker.word()
    location = faker.address()
    date = faker.date_this_month()
    nb_turns = 4
    player_index = []
    player_index += range(1, 9)
    time_control = faker.random_int(1, 3)
    comments = faker.text()
    rounds = ['Round 1', 'Round 2', 'Round 3', 'Round 4', ]
    c = FakeContest(name, location, date,
                    player_index, time_control, comments, rounds)
    return c


def faker_profiles():
    list = []
    # print("firstname".ljust(15), "|lastname".ljust(15),
    #       " |sex".ljust(15), "  |birthdate".ljust(15), "   |ranking".ljust(15), "    |", sep='', end='\n\n')
    player_ranking = []
    player_ranking += range(1, 9)
    print(player_ranking)
    player_ranking = random.sample(player_ranking, len(player_ranking))

    print(player_ranking)
    for n in range(0, 8):
        profile = faker.simple_profile()
        name = profile['name'].split()
        firstname = name[0]
        lastname = name[1]
        sex = profile['sex']
        birthdate = profile['birthdate']
        # def variable1(): return random.randint(1, 8)
        # print(player_ranking)
        ranking = player_ranking[n]
        p = FakeProfile(firstname, lastname, sex, birthdate, ranking)
        list.append(p)
    return list


result = faker_profiles()
print_profiles(result)

# result = faker_contest()
# print_contest(result)
