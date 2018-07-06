"""
Functions to create various schedule types
"""
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

def round_robin(sch, div, play_dates, swap_loc_flag):
    """Create single round robin schedule for one division for one match per pair"""
    from funcs import zmod, mod
    nteams = div.nteams
    nrnds = nteams - 1

    for rnd in range(nrnds):
        sch.add_round(rnd, play_dates[rnd])
        game = 0
        team1 = div.teams[rnd]
        team2 = div.teams[nteams - 1]
        if zmod(rnd, 2) == 0:
            home_flag = mod(1 + swap_loc_flag, 2)
        elif zmod(rnd, 2) == 1:
            home_flag = mod(2 + swap_loc_flag, 2)
        if nrnds > 3:
            if rnd >= (nrnds - 3):
                home_flag = mod(home_flag + 1, 2)
        sch.rounds[rnd].add_match(home_flag, team1, team2)
        if zmod(nteams, 2) == 0:
            if nteams > 3:
                for _kk in range(int((nteams - 2) / 2)):
                    game = game + 1
                    k = _kk * 2 + 1
                    team1 = div.teams[zmod(rnd + k, nteams - 1)]
                    team2 = div.teams[zmod(rnd - k, nteams - 1)]
                    home_flag = 1 + swap_loc_flag
                    sch.rounds[rnd].add_match(home_flag, team1, team2)
        else:
            if nteams > 4:
                for _kk in range(int((nteams - 3) / 2)):
                    game = game + 1
                    k = _kk * 2 + 2
                    team1 = div.teams[zmod(rnd - k, nteams - 1)]
                    team2 = div.teams[zmod(rnd + k, nteams - 1)]
                    home_flag = 1 + swap_loc_flag
                    sch.rounds[rnd].add_match(home_flag, team1, team2)
    return None

def cross_div(sch, div1, div2, play_dates):
    """Create interdivisional schedule using a simple algorithm"""
    from funcs import zmod

    if div1.nteams == div2.nteams:
        nteams = div1.nteams
        nrnds = nteams
        ngames = nteams

        for rnd in range(nrnds):
            sch.add_round(rnd, play_dates[rnd])
            for game in range(ngames):
                team1 = div1.teams[game]
                team2 = div2.teams[zmod(game + rnd, nteams)]
                if zmod(rnd, 2) == 0:
                    home_flag = 1
                elif zmod(rnd, 2) == 1:
                    home_flag = 2
                sch.rounds[rnd].add_match(home_flag, team1, team2)
        return True
    print('Interdivisional schedule creator requires two equal-sized divisions')
    return False

def combine_schedules(sch, *args):
    """Combine indeterminate number of schedules"""
    if len(args) == 1:
        sch = args[0]
    else:
        _play_date_list = []
        _sch_pd_list = []
        for _subsch in args:
            _within_sch_pd_list = []
            for _rnd in range(_subsch.nrounds):
                _tmp_pd = _subsch.rounds[_rnd].play_date
                _within_sch_pd_list.append(_tmp_pd)
                _play_date_list.append(_tmp_pd)
            _sch_pd_list.append(_within_sch_pd_list)
        _play_dates = sorted(set(_play_date_list))
        _nrounds = len(_play_dates)
        for _rnd in range(_nrounds):
            sch.add_round(_rnd, _play_dates[_rnd])
            for _i in range(len(args)):
                _subsch = args[_i]
                if _play_dates[_rnd] in _sch_pd_list[_i]:
                    _subrnd = _subsch.round_lkup[_play_dates[_rnd]]
                    for _match in range(_subsch.rounds[_subrnd].nmatches):
                        _home = _subsch.rounds[_subrnd].matches[_match].home
                        _away = _subsch.rounds[_subrnd].matches[_match].away
                        sch.rounds[_rnd].add_match(1, _home, _away)