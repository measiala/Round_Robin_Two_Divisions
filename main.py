"""
Create schedule for two division pool league
"""

from openpyxl import Workbook

from create_schedule import round_robin, cross_div, combine_schedules
from class_defs import Schedule, League
from process_options import process_options, create_play_dates
from import_teams import import_teams
from print_schedule import (
    create_excel_workbook,
    print_schedule,
    print_league,
    print_team_schedule,
)

# Process command line options
args = process_options()
# NTEAMS = NDTEAMS * NDIV
# NLOC = NDTEAMS

# Define League Shell
IHPL = League("2022-2023 Indian Head Pool League Schedule")
for divn in range(args.num_divs):
    IHPL.add_div("Division #" + str(divn + 1))

# Read in League Info
[ihpl_teams, ihpl_capts] = import_teams(IHPL, args.num_teams_div, args.teamfile)

# Define play dates
[PLAY_DATES_H1, PLAY_DATES_H2, PLAY_DATES_XD] = create_play_dates(
    args.start_date, args.num_teams_div, args.skip_dates
)

# Create intradivisional schedules
print("Division 1 First Half")
D1H1 = Schedule("Division 1 First Half")
round_robin(D1H1, IHPL.divs[0], PLAY_DATES_H1, 0)

print("Division 1 Second Half")
D1H2 = Schedule("Division 1 Second Half")
round_robin(D1H2, IHPL.divs[0], PLAY_DATES_H2, 1)

print("Division 2 First Half")
D2H1 = Schedule("Division 2 First Half")
round_robin(D2H1, IHPL.divs[1], PLAY_DATES_H1, 0)

print("Divsion 2 Second Half")
D2H2 = Schedule("Division 2 Second Half")
round_robin(D2H2, IHPL.divs[1], PLAY_DATES_H2, 1)

# Create interdivisional schedule
print("Interdivisional")
# XD12 = Schedule("Interdivisional")
XD12 = cross_div("Interdivisional", IHPL.divs[0], IHPL.divs[1], PLAY_DATES_XD, True)

# Create full schedule
print("Combine Schedules")
FULL_SCH = Schedule("League Schedule")
combine_schedules(FULL_SCH, D1H1, D2H1, XD12, D1H2, D2H2)

print_league(IHPL, ihpl_teams)
print_schedule(FULL_SCH, ihpl_teams)
# print_team_schedule(FULL_SCH, args.example_team, ihpl_teams, ihpl_capts)
# for example_team in ihpl_teams:
#    print_team_schedule(FULL_SCH, example_team, ihpl_teams, ihpl_capts)

# Create final schedule in Excel workbook
create_excel_workbook(
    "./input/2022-2023 IHPL Schedule.xlsx",
    league=IHPL,
    schedule=FULL_SCH,
    list_teams=ihpl_teams,
    list_capts=ihpl_capts,
)
