# tour = 1 objet contenant 1 liste de match

# tour = Tour()
# tour.nom = nom 	# Round 1 - N
# tour.match = [match1, match2, match3, match4]
# tour.datetime_start = date/time
# tour.datetime_end = date/time


from tinydb import TinyDB, Query

# https://stackoverflow.com/questions/51752924/nested-classes-are-not-serializable-in-python-when-trying-json-dump


class Tour(object):
    def __init__(self, round_name='a', matchs='a', start_datetime='a', end_datetime='a'):
        self.round_name = round_name  # Round 1 - N
        self.matchs = matchs
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def __str__(self):
        return 'round nb: {self.round_name} match: {self.matchs}'.format(self=self)
    # Serialize a round

    def serialize_match(self):
        pair = self.matchs
        # print("matches: ", pair)
        print("pair[0]: ", pair[0])
        print("pair: ", pair)
        # print("match 1 value: ", pair[1])
        # print("match 2 value: ", pair[2])
        # print("match 3 value: ", pair[3])
        n = 0
        serialized_match = {
            #     'match 1': pair[0],
            #     'match 2': pair[1],
            #     'match 3': pair[2],
            #     'match 4': pair[3]
            # }
            "match " + str(n): pair[n] for n in range(4)}
        return serialized_match

    def serialization_round(self):
        serialized_round = {
            # "roundName": self.round_name,
            "matches": self.serialize_match(),
            "start_datetime": str(self.start_datetime),
            "end_datetime": str(self.end_datetime),
        }
        return serialized_round
