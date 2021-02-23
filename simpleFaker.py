from faker import Faker
import dumper
faker = Faker()


class Profile:
    def __init__(self, firstname, lastname, sex, birthdate, ranking):
        self.firstname = firstname
        self.lastname = lastname
        self.sex = sex
        self.birthdate = birthdate
        self.ranking = ranking


def print_profiles(list):
    for item in list:
        temp = vars(item)
        for item2 in temp:
            print(str(temp[item2]).ljust(15), '|', sep='', end='')
        print()


def faker_profiles():
    list = []
    # print("firstname".ljust(15), "|lastname".ljust(15),
    #       " |sex".ljust(15), "  |birthdate".ljust(15), "   |ranking".ljust(15), "    |", sep='', end='\n\n')
    for n in range(0, 8):
        profile = faker.simple_profile()
        name = profile['name'].split()
        firstname = name[0]
        lastname = name[1]
        sex = profile['sex']
        birthdate = profile['birthdate']
        ranking = 0
        p = Profile(firstname, lastname, sex, birthdate, ranking)
        list.append(p)
    return list


# result = faker_profiles()
# print_profiles(result)
