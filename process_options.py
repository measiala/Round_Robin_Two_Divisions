"""
Process command line options
"""

def process_options():
    """Process command line options"""
    import argparse
    import logging

    ARGP = argparse.ArgumentParser(description='Provide Division Size Parameters')
    ARGP.add_argument('NDTEAMS', metavar='NUM_DIV_TEAMS', type=int,
                      help='Number of teams per division')
    ARGP.add_argument('NDIVS', metavar='NUM_DIVISIONS', type=int, choices=[1, 2],
                      help='Number of divisions')
    ARGP.add_argument('START_DATE', metavar='START_DATE', type=str,
                      help='First week of season')
    ARGP.add_argument('SKIP_DATES', metavar='SKIP_DATES', type=str,
                      help='List of dates to skip, e.g., holidays')
    ARGP.add_argument('--teamfile','-i',metavar='Team_Info_File', type=str,
                      help='CSV Input File containing Team Information')
    ARGP.add_argument('--logfile', metavar='LOG_FILE', type=str,
                      help='File name for log file (out.log default)')
    ARGP.add_argument('--loglvl','-l',metavar='Log_Level',
                      choices=['ERROR','WARNING','INFO'],
                      help='Log Output Level (ERROR/WARNING/INFO)')

    _args = ARGP.parse_args()

    if not _args.teamfile:
        _args.teamfile = './input/team_info.csv'
    if not _args.logfile:
        _args.logfile = './logs/out.log'
    if not _args.loglvl:
        _args.loglvl = logging.INFO
    else:
        _args.loglvl = getattr(logging, _args.loglvl.upper(), None)
    logging.basicConfig(filename=_args.logfile,filemode = 'w',
                        level=int(_args.loglvl))

    return _args

def create_round_date(start, nround, omit = ''):
    """Create list of dates for every 7 days skipping omit dates"""
    from datetime import datetime, timedelta
    start_dt = datetime.strptime(start,"%Y/%m/%d")

    round_date = []
    for round in range(nround):
        flag = 0
        if round == 0:
            rnd_dt = start_dt
        else:
            rnd_dt = rnd_dt + timedelta(days=7)
        while flag == 0:
            round_dt = rnd_dt.strftime("%Y/%m/%d")
            if round_dt not in omit:
                flag = 1
            else:
                flag = 0
                rnd_dt = rnd_dt + timedelta(days=7)
        round_date.append(round_dt)
    return round_date

def create_play_dates(START_DATE, ndteams, SKIP_DATES=[]):
    """Create list of play dates for 1st Half, 2nd Half, Cross Division"""
    import logging

    pd = create_round_date(START_DATE, 2*(ndteams - 1) + ndteams, 
                           SKIP_DATES)
    pdh1 = pd[:(ndteams - 1)]
    pdh2 = pd[-(ndteams - 1):]
    pdxd = pd[(ndteams - 1):-(ndteams - 1)]

    logging.info("Total play dates is %d" % len(pd))
    logging.info("First half has %d dates" % len(pdh1))
    logging.info("Second half has %d dates" % len(pdh2))
    logging.info("Interdivision has %d dates" % len(pdxd))

    return [pdh1, pdh2, pdxd]