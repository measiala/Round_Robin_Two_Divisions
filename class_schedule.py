""" Classes related to the schedule
"""
from copy import deepcopy
import dataclasses
import typing
from class_league import NewLeague, NewTeam, NewLocation
from funcs import zmod

from process_options import create_round_date


@dataclasses.dataclass
class NewMatch:
    """Define a match by a home and away Team instance"""

    home: NewTeam
    away: NewTeam


@dataclasses.dataclass
class NewRound:
    """Define round as a collection of matches"""

    name: str
    matches: dict[NewLocation, NewMatch] = dataclasses.field(
        init=False, default_factory=dict
    )

    def add_match(self, home_flag: bool, team1: NewTeam, team2: NewTeam) -> None:
        """Add match using home_flag to designate home team"""
        if home_flag:
            self.matches[team1.location] = NewMatch(team1, team2)
        else:
            self.matches[team2.location] = NewMatch(team2, team1)

    def __add__(self, other: "NewRound") -> "NewRound":
        """Add two schedules"""
        if set(self.matches.keys()).isdisjoint(set(other.matches.keys())) and set(
            self.matches.values()
        ).isdisjoint(set(other.matches.values())):
            sum_rounds = deepcopy(self)
            sum_rounds.name = f"Sum of {self.name!r} and {other.name!r}"
            for key, value in other.matches.items():
                sum_rounds.return_dict[key] = value
            return sum_rounds
        raise ValueError("Matches must be non-overlapping")


@dataclasses.dataclass
class NewPlayDates:
    """Establish relationship between weeks and play dates"""

    name: typing.Optional[str] = None
    play_dates: dict[int, str] = dataclasses.field(init=False, default_factory=dict)

    def add_dates(
        self, num_weeks: int, start_date: str, skip_dates: str, skip_start: bool = False
    ):
        """Add a set of play dates"""

        if skip_start:
            skip_dates = f"{start_date},{skip_dates}"
        play_dates = create_round_date(start_date, num_weeks, skip_dates)
        start_week = 0
        if play_dates:
            start_week = max(self.play_dates.keys()) + 1

        for week in range(num_weeks):
            self.play_dates[start_week + week] = play_dates[week]

    def __add__(self, other: "NewPlayDates") -> "NewPlayDates":
        """Add two schedules"""
        if set(self.play_dates.keys()).isdisjoint(set(other.play_dates.keys())) and set(
            self.play_dates.values()
        ).isdisjoint(set(other.play_dates.values())):
            return_dates = deepcopy(self)
            for key, value in other.play_dates.items():
                return_dates.play_dates[key] = value
            return return_dates
        raise ValueError("Schedules must be non-overlapping")


@dataclasses.dataclass
class SeasonPlayDates:
    """Handle particulars of intra and interdivisional playdates"""

    start_date: dataclasses.InitVar[str]
    num_teams: dataclasses.InitVar[int]
    skip_dates: dataclasses.InitVar[str]
    season: NewPlayDates = NewPlayDates()
    first_half: NewPlayDates = NewPlayDates()
    second_half: NewPlayDates = NewPlayDates()
    inter_divisional: NewPlayDates = NewPlayDates()

    def __post_init__(self, start_date: str, num_teams: int, skip_dates: str) -> None:
        """Create three parts of schedule"""
        self.first_half.add_dates(num_teams - 1, start_date, skip_dates, False)
        start_inter = self.first_half.play_dates.values()[-1]
        self.inter_divisional.add_dates(num_teams, start_inter, skip_dates, True)
        start_second = self.inter_divisional.play_dates.values()[-1]
        self.first_half.add_dates(num_teams - 1, start_second, skip_dates, True)
        self.season = self.first_half + self.inter_divisional + self.second_half


@dataclasses.dataclass
class NewSchedule:
    """Define schedule as mapping of playdates to Rounds"""

    start_date: dataclasses.InitVar[str]
    num_teams: dataclasses.InitVar[int]
    skip_dates: dataclasses.InitVar[str]
    league: typing.ClassVar[NewLeague] = None
    rounds: dict[int, NewRound] = dataclasses.field(init=False, default_factory=dict)
    play_dates: SeasonPlayDates = dataclasses.field(init=False, default=None)

    def __post_init__(self, start_date: str, num_teams: int, skip_dates: str) -> None:
        """Create play_dates"""
        self.play_dates(start_date, num_teams, skip_dates)

    def add_round(self, week: int, play_date: str, new_round: NewRound) -> None:
        """Add a round to the schedule"""
        self.play_dates[week] = play_date
        self.rounds[play_date] = new_round

    @staticmethod
    def swap_rounds(
        rounds: dict[int, NewRound], week1: int, week2: int
    ) -> dict[int, NewRound]:
        """Swap the matches between two weeks"""
        round1 = rounds[week1]
        rounds[week1] = rounds[week2]
        rounds[week2] = round1
        return rounds

    @staticmethod
    def horizontal_concat_rounds(
        rounds1: dict[int, NewRound], rounds2: dict[int, NewRound]
    ) -> dict[int, NewRound]:
        """Concatenate Rounds within weeks"""
        return_dict = {}
        for key in set(rounds1).union(set(rounds2)):
            if key in rounds1:
                if key in rounds2:
                    return_dict[key] = rounds1[key] + rounds2[key]
                else:
                    return_dict[key] = rounds1[key]
            else:
                return_dict[key] = rounds2[key]
        return return_dict

    @staticmethod
    def vertical_concat_rounds(
        rounds1: dict[int, NewRound], rounds2: dict[int, NewRound]
    ) -> dict[int, NewRound]:
        """Concatenate Rounds within weeks"""
        return_dict = deepcopy(rounds1)
        for key, value in rounds2.items():
            return_dict[key] = value
        return return_dict

    def create_schedule(self) -> None:
        """New round robin"""
        # First half of round-robin intradivisional
        div1_half1 = self.general_round_robin(1, 0, False)
        div2_half1 = self.general_round_robin(1, 1, False)
        half1 = self.horizontal_concat_rounds(div1_half1, div2_half1)
        # Interdivisional
        xdiv = self.create_interdivisional(10, True)
        # Second half of round-robin intradivisional
        div1_half2 = self.general_round_robin(20, 0, True)
        div2_half2 = self.general_round_robin(20, 1, True)
        half2 = self.horizontal_concat_rounds(div1_half2, div2_half2)
        # Make final schedule
        self.rounds = self.vertical_concat_rounds(
            self.vertical_concat_rounds(half1, xdiv), half2
        )

    def general_round_robin(
        self, start_week: int, div_num: int, swap_loc_flag: False
    ) -> dict[int, NewRound]:
        """Create single round robin schedule for one division for one match per pair"""

        division = self.league.divisions[div_num]
        num_teams = division.nteams
        num_rounds = num_teams - 1

        rounds: dict[int, NewRound] = {}
        for rnd in range(num_rounds):
            rounds[rnd + start_week] = NewRound(f"Week {rnd + start_week}")
            weekly_round = rounds[rnd + start_week]
            game = 0
            team1 = division.teams[rnd]
            team2 = division.teams[num_teams - 1]
            if zmod(rnd, 2) == 0:
                # home_flag = mod(1 + swap_loc_flag, 2)
                home_flag = not swap_loc_flag
            elif zmod(rnd, 2) == 1:
                # home_flag = mod(2 + swap_loc_flag, 2)
                home_flag = swap_loc_flag
            if num_rounds > 3:
                if rnd >= (num_rounds - 3):
                    home_flag = not home_flag
            weekly_round.add_match(home_flag, team1, team2)
            if zmod(num_teams, 2) == 0:
                if num_teams > 3:
                    for _kk in range(int((num_teams - 2) / 2)):
                        game = game + 1
                        k = _kk * 2 + 1
                        team1 = division.teams[zmod(rnd + k, num_teams - 1)]
                        team2 = division.teams[zmod(rnd - k, num_teams - 1)]
                        home_flag = not swap_loc_flag
                        weekly_round.add_match(home_flag, team1, team2)
            else:
                if num_teams > 4:
                    for _kk in range(int((num_teams - 3) / 2)):
                        game = game + 1
                        k = _kk * 2 + 2
                        team1 = division.teams[zmod(rnd - k, num_teams - 1)]
                        team2 = division.teams[zmod(rnd + k, num_teams - 1)]
                        home_flag = not swap_loc_flag
                        weekly_round.add_match(home_flag, team1, team2)
        return rounds

    def create_interdivisional(
        self, start_week: int, bye_teams: bool = False
    ) -> dict[int, NewRound]:
        """Create interdivisional schedule using a simple algorithm"""

        div1 = self.league.divisions[0]
        div2 = self.league.divisions[1]

        rounds: dict[int, NewRound] = {}

        if div1.nteams != div2.nteams:
            raise ValueError(
                "Interdivisional schedule creator requires two equal-sized divisions"
            )

        nteams = div1.nteams
        nrnds = nteams
        ngames = nteams

        for rnd in range(nrnds):
            rounds[rnd + start_week] = NewRound(f"Week {rnd + start_week}")
            weekly_round = rounds[rnd + start_week]
            for game in range(ngames):
                team1 = div1.teams[game]
                team2 = div2.teams[zmod(game + rnd, nteams)]
                if zmod(rnd, 2) == 0:
                    home_flag = True
                elif zmod(rnd, 2) == 1:
                    home_flag = False
                weekly_round.add_match(home_flag, team1, team2)
        if bye_teams:
            rounds = self.swap_rounds(rounds, nrnds - 1, nrnds - 3)
            rounds = self.swap_rounds(rounds, nrnds - 2, nrnds - 4)
        return rounds
