def print_schedule(sch, leag_list, outfile='print'):
    """Print compact schedule"""
    if outfile == 'print':
        def pline(txt):
            print(txt)
    else:
        def pline(txt):
            outfile.write(txt)

    for rnd in range(sch.nrounds):
        _rnd = sch.rounds[rnd]
        line = '{}'.format(_rnd.play_date)
        for match in range(_rnd.nmatches):
            _match = _rnd.matches[match]
            _away = _match.away
            _home = _match.home
            #line = line + " " + '{} @ {}'.format(_away,_home)
            line = line + " " + '{:2} @ {:2}'.format(leag_list.index(_away) + 1,
                                                     leag_list.index(_home) + 1)
        pline(line)

def print_league(leag, leag_list, outfile='print'):
    import logging
    """Print list of teams"""
    if outfile == 'print':
        def pline(txt):
            print(txt)
    else:
        def pline(txt):
            outfile.write(txt + '\n')
    line = ''
    max_teams = 0
    logging.info('Total number of divisions: %d' % leag.ndivs)
    for _div_i in range(leag.ndivs):
        logging.info('Division %d in loop out of %s' % (_div_i, leag.ndivs))
        line = line + '{:<32}'.format(str(leag.divs[_div_i].name))
        max_teams = max(max_teams, leag.divs[_div_i].nteams)
    pline(line)
    line = ''
    for _team_i in range(max_teams):
        for _div_i in range(leag.ndivs):
            _div = leag.divs[_div_i]
            if _team_i < _div.nteams:
                _num = str(leag_list.index(_div.teams[_team_i]) + 1)
                line = line \
                       + '{:>2}{:<30}'.format(_num, '.  ' + _div.teams[_team_i] 
                                         + ' - ' 
                                         + _div.capts[_team_i])
            else:
                line = line + '{:<32}'.format('')
        pline(line)
        line = ''
"""
def print_team_schedule( team, rounds, dates, games, home_team, away_team):
    num_rnds = rounds[-1] + 1
    num_games = games[-1] + 1

    print("\nTeam: " + team + "\n")
    team_idx = team_names.index(team)
    for round in range(num_rnds):
        rdate = dates[round]
        line = '{}'.format(rdate)
        hteam = home_team[round*num_games:(round+1)*num_games]
        ateam = away_team[round*num_games:(round+1)*num_games]
        try:
            hidx = hteam.index(team_idx)
            #print(hidx)
        except ValueError:
            try:
                aidx = ateam.index(team_idx)
                #print(aidx)
            except ValueError:
                print("ERROR")
            else:
                #print("away path",home_team[aidx])
                line = line+ "  " + "At {} versus {} ({})"\
                .format(team_loc[hteam[aidx]],team_names[hteam[aidx]],\
                            capt_names[hteam[aidx]])
        else:
            #print("home path")
            line = line + "  " + "Home versus {} ({})"\
                .format(team_names[ateam[hidx]],capt_names[ateam[hidx]])

        print(line)
"""
