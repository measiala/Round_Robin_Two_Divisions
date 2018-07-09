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

def print_team_schedule(sch, team, team_list, capt_list, outfile='print'):
    import logging
    """Print individual team schedule"""
    if outfile == 'print':
        def pline(txt):
            print(txt)
    else:
        def pline(txt):
            outfile.write(txt + '\n')
    line = ''

    pline("\nTeam: " + team + "\n")
    for rnd in range(sch.nrounds):
        _rnd = sch.rounds[rnd]
        line = '{}'.format(_rnd.play_date)
        game_not_found = True
        match = 0
        while game_not_found and match < _rnd.nmatches:
            _match = _rnd.matches[match]
            if _match.home == team:
                _teamidx = team_list.index(_match.away)
                _capt = capt_list[_teamidx]
                line = line + " <-- Home versus {} ({})".format(_match.away,_capt)
                game_not_found = False
            elif _match.away == team:
                _teamidx = team_list.index(_match.home)
                _capt = capt_list[_teamidx]
                line = line + " --> Away at {} ({})".format(_match.home,_capt)
                game_not_found = False
            else:
                match = match + 1
        if game_not_found == True:
            logging.warning("Bye week is not expected.")
            line = line + "Bye Week"
        pline(line)
               

