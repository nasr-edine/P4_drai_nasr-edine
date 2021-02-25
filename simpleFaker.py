from faker import Faker
import dumper
import random

faker = Faker()


# Create fake data of a round(tour )
class FakeTour(object):
    def __init__(self, round_name=None, matchs=None, start_datetime=None, end_datetime=None):
        self.round_name = round_name  # Round 1 - N
        self.matchs = matchs
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime


# Create a fake data of contess
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


# Create fake data of a player
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


def faker_round():
    name = 'Round N'
    match = 'match'
    TOTAL_SECONDS = 60*60*24*1  # one day

    series = faker.time_series(
        start_date='-8d', end_date='now', precision=TOTAL_SECONDS)
    list_time = []
    for val in series:
        # print(val)
        list_time.append(str(val[0]))
    # start_datetime = faker.date_time_this_month()
    # end_datetime = faker.date_time_this_month()
    rounds = []
    for n in range(4):
        object = FakeTour(name, match, list_time[n], list_time[n+1])
        rounds.append(object)


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
    player_ranking = []
    player_ranking += range(1, 9)
    # print(player_ranking)
    player_ranking = random.sample(player_ranking, len(player_ranking))
    # print(player_ranking)
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


# result = faker_profiles()
# print_profiles(result)

# result = faker_contest()
# print_contest(result)


faker_round()
