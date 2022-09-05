"""
Class definitions for Round Robin project
"""
import dataclasses
import typing


@dataclasses.dataclass
class Location:
    """Define pool location"""

    name: str
    bar: str
    table_id: str = None


@dataclasses.dataclass
class Team:
    """Define Team related information"""

    name: str
    captain: str
    location: Location


@dataclasses.dataclass
class Match:
    """Define a match by a home and away Team"""

    home: str
    away: str


@dataclasses.dataclass
class Round:
    """A round is defined by week of play, a play_date, and a list of matches"""

    week: int
    play_date: str
    matches: list[Match] = dataclasses.field(init=False, default_factory=list)
    nmatches: int = 0
    match_lkup: dict[str, int] = dataclasses.field(init=False, default_factory=dict)

    def add_match(
        self, home_flag: typing.Literal[0, 1], team1: str, team2: str
    ) -> None:
        """Add a match to the round"""
        if home_flag == 1:
            home = team1
            away = team2
        else:
            home = team2
            away = team1
        new_match = Match(home, away)
        self.matches.append(new_match)
        self.nmatches = len(self.matches)
        self.match_lkup[home] = self.nmatches - 1


@dataclasses.dataclass
class Schedule:
    """Holds schedule for league"""

    name: str
    rounds: list[Round] = dataclasses.field(init=False, default_factory=list)
    round_lkup: dict[str, int] = dataclasses.field(init=False, default_factory=dict)
    nrounds: int = 0

    def add_round(self, week: int, play_date: str) -> None:
        """Add a round to the schedule"""
        new_round = Round(week, play_date)
        self.rounds.append(new_round)
        self.nrounds = len(self.rounds)
        self.round_lkup[play_date] = self.nrounds - 1

    def swap_rounds(self, week1: int, week2: int):
        """Swap the matches between two weeks"""
        tmp_matches = self.rounds[week1].matches
        self.rounds[week1].matches = self.rounds[week2].matches
        self.rounds[week2].matches = tmp_matches

    def reset(self) -> None:
        """Reset the schedule retaining only the name"""
        self.rounds = []
        self.round_lkup = {}
        self.nrounds = 0


@dataclasses.dataclass
class Division:
    """This class holds all the information for a single division"""

    name: str
    teams: list[str] = dataclasses.field(init=False, default_factory=list)
    capts: list[str] = dataclasses.field(init=False, default_factory=list)
    locs: list[str] = dataclasses.field(init=False, default_factory=list)
    nteams: int = 0
    team_lkup: dict[str, int] = dataclasses.field(init=False, default_factory=dict)

    def add_team(self, team: str, capt: str, loc: str) -> None:
        """This method will add a team to the division class"""
        self.teams.append(team)
        self.capts.append(capt)
        self.locs.append(loc)
        self.nteams = len(self.teams)
        self.team_lkup[team] = self.nteams - 1


@dataclasses.dataclass
class League:
    """This class is a holder for all divisions"""

    name: str
    divs: list[Division] = dataclasses.field(init=False, default_factory=list)
    ndivs: int = 0
    div_lkup: dict[str, int] = dataclasses.field(init=False, default_factory=dict)

    def add_div(self, name: str) -> None:
        """Add a new division defined by its name"""
        new_div = Division(name)
        self.divs.append(new_div)
        self.ndivs = len(self.divs)
        self.div_lkup[name] = self.ndivs - 1


@dataclasses.dataclass
class ArgNameSpace:
    """Dummy argspace to help with typing"""

    num_teams_div: int
    num_divs: typing.Literal[1, 2]
    start_date: str
    skip_dates: str
    teamfile: str
    logfile: str
    loglvl: typing.Literal["ERROR", "WARNING", "INFO"]
    example_team: str
