"""
Create schedule for two division pool league
"""
import argparse
import csv
import logging

from create_schedule import round_robin, cross_div, combine_schedules
from class_defs import Schedule, League
from process_options import process_options, create_play_dates
from import_teams import import_teams
from print_schedule import print_schedule, print_league, print_team_schedule

# Process command line options
ARGS = process_options()
#NTEAMS = NDTEAMS * NDIV
#NLOC = NDTEAMS

# Define League Shell
IHPL = League('IHPL 2018')
for divn in range(ARGS.NDIVS):
    IHPL.add_div('Division #' + str(divn + 1))

# Read in League Info
[ihpl_teams, ihpl_capts] = import_teams(IHPL, ARGS.NDTEAMS, ARGS.teamfile)

# Define play dates
[PLAY_DATES_H1, PLAY_DATES_H2, PLAY_DATES_XD] \
        = create_play_dates(ARGS.START_DATE, ARGS.NDTEAMS, ARGS.SKIP_DATES)

"""Create intradivisional schedules"""
print("Division 1 First Half")
D1H1 = Schedule('Division 1 First Half')
round_robin(D1H1, IHPL.divs[0], PLAY_DATES_H1, 0)

print("Division 1 Second Half")
D1H2 = Schedule('Division 1 Second Half')
round_robin(D1H2, IHPL.divs[0], PLAY_DATES_H2, 1)

print("Division 2 First Half")
D2H1 = Schedule('Division 2 First Half')
round_robin(D2H1, IHPL.divs[1], PLAY_DATES_H1, 0)

print("Divsion 2 Second Half")
D2H2 = Schedule('Division 2 Second Half')
round_robin(D2H2, IHPL.divs[1], PLAY_DATES_H2, 1)

"""Create interdivisional schedule"""
print("Interdivisional")
XD12 = Schedule('Interdivisional')
cross_div(XD12, IHPL.divs[0], IHPL.divs[1], PLAY_DATES_XD)

print("Combine Schedules")
FULL_SCH = Schedule("League Schedule")
combine_schedules(FULL_SCH, D1H1, D2H1, XD12, D1H2, D2H2)

print_league(IHPL, ihpl_teams)
print_schedule(FULL_SCH, ihpl_teams)
print_team_schedule(FULL_SCH, 'Lisas #2', ihpl_teams, ihpl_capts)
