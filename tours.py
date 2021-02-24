# tour = 1 objet contenant 1 liste de match

# tour = Tour()
# tour.nom = nom 	# Round 1 - N
# tour.match = [match1, match2, match3, match4]
# tour.datetime_start = date/time
# tour.datetime_end = date/time


from tinydb import TinyDB, Query


class Tour(object):
    def __init__(self, round_name=None, matchs=None, start_datetime=None, end_datetime=None):
        self.round_name = round_name  # Round 1 - N
        self.matchs = matchs
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
