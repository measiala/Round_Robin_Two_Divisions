"""
Create schedule for two division pool league
"""

import csv
from openpyxl import Workbook

from create_schedule import round_robin, cross_div, combine_schedules
from class_league import NewDivision, NewLeague, NewLocation, NewTeam
from class_schedule import NewSchedule
from class_defs import Schedule, League
from process_options import process_options, create_play_dates
from import_teams import import_teams
from print_schedule import (
    create_excel_workbook,
    print_schedule,
    print_league,
    print_team_schedule,
)


def old_define_league(num_divs: int) -> League:
    """Define League Shell"""
    league = League("2022-2023 Indian Head Pool League Schedule")
    for divn in range(num_divs):
        league.add_div("Division #" + str(divn + 1))
    return league


def new_define_league(year: int, num_divs: int) -> NewLeague:
    """Define Newleague"""
    yyyy = str(year)
    yyyp = str(year + 1)
    league = NewLeague(f"{yyyy}-{yyyp} Indian Head Pool League Schedule")
    for div_num in range(num_divs):
        league.divisions[div_num] = f"Division #{div_num + 1}"
    return league


def old_define_teams_capts(league: League, num_teams_div: int, teamfile: str):
    """Read in League Info"""
    [ihpl_teams, ihpl_capts] = import_teams(league, num_teams_div, teamfile)
    return [ihpl_teams, ihpl_capts]


def new_define_teams(league: NewLeague, num_teams_div: int, teamfile: str):
    """Read in team info"""
    with open(teamfile, "r", encoding="latin1") as infile:
        csv_file = csv.DictReader(infile, quoting=csv.QUOTE_ALL)
        nrecs = 0
        for row in csv_file:
            div_num = 1
            if nrecs < num_teams_div:
                div_num = 0
            league.add_team_division(
                nrecs,
                team=NewTeam(
                    row["Team"],
                    row["Captain"],
                    NewLocation(row["Location"], row["Location"], nrecs),
                ),
                division=div_num,
            )
            nrecs += 1


def play_dates(start_date: str, num_teams_div: int, skip_dates: str):
    return create_play_dates(start_date, num_teams_div, skip_dates)


def old_create_schedule(league: League, list_teams: list[str]):
    # Create intradivisional schedules
    print("Division 1 First Half")
    D1H1 = Schedule("Division 1 First Half")
    round_robin(D1H1, league.divs[0], PLAY_DATES_H1, 0)

    print("Division 1 Second Half")
    D1H2 = Schedule("Division 1 Second Half")
    round_robin(D1H2, league.divs[0], PLAY_DATES_H2, 1)

    print("Division 2 First Half")
    D2H1 = Schedule("Division 2 First Half")
    round_robin(D2H1, league.divs[1], PLAY_DATES_H1, 0)

    print("Divsion 2 Second Half")
    D2H2 = Schedule("Division 2 Second Half")
    round_robin(D2H2, league.divs[1], PLAY_DATES_H2, 1)

    # Create interdivisional schedule
    print("Interdivisional")
    # XD12 = Schedule("Interdivisional")
    XD12 = cross_div(
        "Interdivisional", league.divs[0], league.divs[1], PLAY_DATES_XD, True
    )

    # Create full schedule
    print("Combine Schedules")
    full_schedule = Schedule("League Schedule")
    combine_schedules(full_schedule, D1H1, D2H1, XD12, D1H2, D2H2)

    print_league(league, list_teams)
    print_schedule(full_schedule, list_teams)
    # print_team_schedule(full_schedule, args.example_team, list_teams, ihpl_capts)
    # for example_team in ihpl_teams:
    #    print_team_schedule(full_schedule, example_team, ihpl_teams, ihpl_capts)

    # Create final schedule in Excel workbook
    return full_schedule


if __name__ == "__main__":
    # Process command line options
    args = process_options()

    IHPL = new_define_league(2022, 2)

    [PLAY_DATES_H1, PLAY_DATES_H2, PLAY_DATES_XD] = play_dates(
        args.start_date, args.num_teams_div, args.skip_dates
    )

    full_schedule = old_create_schedule(IHPL, IHPL.teams)
    create_excel_workbook(
        "./input/2022-2023 IHPL Schedule.xlsx",
        league=IHPL,
        schedule=full_schedule,
        list_teams=IHPL.teams,
        list_capts=IHPL.teams,
    )
