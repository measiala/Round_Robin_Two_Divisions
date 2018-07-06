"""
Class definitions for Round Robin project
"""
class Match:
    def __init__(self, home, away):
        self.home = home
        self.away = away

class Round:
    def __init__(self, week, play_date):
        self.week = week
        self.play_date = play_date
        self.matches = []
        self.nmatches = 0
        self.match_lkup = {}

    def add_match(self, home_flag, team1, team2):
        if home_flag == 1:
            home = team1
            away = team2
        else:
            home = team2
            away = team1
        new_match = Match(home,away)
        self.matches.append(new_match)
        self.nmatches = len(self.matches)
        self.match_lkup[home] = self.nmatches - 1

class Schedule:
    def __init__(self, name):
        self.name = name
        self.rounds = []
        self.round_lkup = {}
        self.nrounds = 0

    def add_round(self, week, play_date):
        new_round = Round(week, play_date)
        self.rounds.append(new_round)
        self.nrounds = len(self.rounds)
        self.round_lkup[play_date] = self.nrounds - 1

    def reset(self):
        self.rounds = []
        self.round_lkup = {}
        self.nrounds = 0

class Division:
    """This class holds all the information for a single division"""
    def __init__(self, name: str):
        self.name = name
        self.teams = []
        self.capts = []
        self.locs = []
        self.nteams = 0
        self.team_lkup = {}

    def add_team(self, team: str, capt: str, loc: str):
        """This method will add a team to the division class"""
        self.teams.append(team)
        self.capts.append(capt)
        self.locs.append(loc)
        self.nteams = len(self.teams)
        self.team_lkup[team] = self.nteams - 1

class League:
    """This class is a holder for all divisions"""
    def __init__(self, name: str):
        self.name = name
        self.divs = []
        self.ndivs = 0
        self.div_lkup = {}

    def add_div(self, name: str):
        new_div = Division(name)
        self.divs.append(new_div)
        self.ndivs = len(self.divs)
        self.div_lkup[name] = self.ndivs - 1