"""
Process command line options
"""
import argparse
import logging
from datetime import datetime, timedelta

from class_defs import ArgNameSpace


def process_options() -> ArgNameSpace:
    """Process command line options"""

    argp = argparse.ArgumentParser(description="Provide Division Size Parameters")
    argp.add_argument(
        "num_teams_div",
        metavar="NUM_DIV_TEAMS",
        type=int,
        help="Number of teams per division",
    )
    argp.add_argument(
        "num_divs",
        metavar="NUM_DIVISIONS",
        type=int,
        choices=[1, 2],
        help="Number of divisions",
        default=2,
    )
    argp.add_argument(
        "start_date", metavar="START_DATE", type=str, help="First week of season"
    )
    argp.add_argument(
        "skip_dates",
        metavar="SKIP_DATES",
        type=str,
        help="List of dates to skip, e.g., holidays",
    )
    argp.add_argument(
        "--teamfile",
        "-i",
        metavar="Team_Info_File",
        type=str,
        help="CSV Input File containing Team Information",
        default="./input/IHPL-Divisions-2022.csv",
    )
    argp.add_argument(
        "--logfile",
        metavar="LOG_FILE",
        type=str,
        help="File name for log file (out.log default)",
    )
    argp.add_argument(
        "--loglvl",
        "-l",
        metavar="Log_Level",
        choices=["ERROR", "WARNING", "INFO"],
        help="Log Output Level (ERROR/WARNING/INFO)",
        default="ERROR",
    )
    argp.add_argument(
        "--example_team",
        "-t",
        metavar="TeamName",
        type=str,
        help="Example team to print schedule",
        default="Lisa's #2",
    )

    _args: ArgNameSpace = argp.parse_args()

    if not _args.teamfile:
        _args.teamfile = "./input/team_info.csv"
    if not _args.logfile:
        _args.logfile = "./logs/out.log"
    if not _args.loglvl:
        _args.loglvl = logging.INFO
    else:
        _args.loglvl = getattr(logging, _args.loglvl.upper(), None)
    logging.basicConfig(filename=_args.logfile, filemode="w", level=int(_args.loglvl))

    return _args


def create_round_date(start: str, nround: int, omit: str = "") -> list[str]:
    """Create list of dates for every 7 days skipping omit dates"""

    start_dt = datetime.strptime(start, "%Y/%m/%d")

    round_date = []
    for rnd in range(nround):
        flag = False
        if rnd == 0:
            rnd_dt = start_dt
        else:
            rnd_dt = rnd_dt + timedelta(days=7)
        while not flag:
            round_dt = rnd_dt.strftime("%Y/%m/%d")
            if round_dt not in omit:
                flag = True
            else:
                flag = False
                rnd_dt = rnd_dt + timedelta(days=7)
        round_date.append(round_dt)
    return round_date


def create_play_dates(
    start_date: str, ndteams: str, skip_dates: str = ""
) -> list[list[str]]:
    """Create list of play dates for 1st Half, 2nd Half, Cross Division"""

    play_dates = create_round_date(start_date, 2 * (ndteams - 1) + ndteams, skip_dates)
    pdh1 = play_dates[: (ndteams - 1)]
    pdh2 = play_dates[-(ndteams - 1) :]
    pdxd = play_dates[(ndteams - 1) : -(ndteams - 1)]

    logging.info("Total play dates is %d", len(play_dates))
    logging.info("First half has %d dates", len(pdh1))
    logging.info("Second half has %d dates", len(pdh2))
    logging.info("Interdivision has %d dates", len(pdxd))

    return [pdh1, pdh2, pdxd]
