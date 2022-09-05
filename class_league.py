""" Class definitions used to define the league
"""
import dataclasses


@dataclasses.dataclass
class NewLocation:
    """Define pool location"""

    name: str
    bar_location: str
    table_id: str = None


@dataclasses.dataclass
class NewTeam:
    """Define Team related information"""

    name: str
    captain: str
    location: NewLocation


@dataclasses.dataclass
class NewDivision:
    """Define division"""

    name: str
    teams: dict[int, NewTeam] = dataclasses.field(init=False, default_factory=dict)

    @property
    def nteams(self):
        """Return the number of teams in the division"""
        return len(self.teams)


@dataclasses.dataclass
class NewLeague:
    """Define League"""

    name: str
    divisions: dict[int, NewDivision] = dataclasses.field(
        init=False, default_factory=dict
    )
    teams: dict[int, NewTeam] = dataclasses.field(init=False, default_factory=dict)

    @property
    def num_divisions(self):
        """Return the number of divisions"""
        return len(self.divisions)

    def add_team_division(self, team_idx: int, team: NewTeam, division: int):
        """Add a team and its index both to division and league index of teams"""
        self.divisions[division].teams[team_idx] = team
        self.teams[team_idx] = team
