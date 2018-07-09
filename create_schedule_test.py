"""
Test create_schedule.py
"""

from create_schedule import round_robin, cross_div, combine_schedules
from process_options import create_round_date
from class_defs import Schedule, Division
from funcs import comb

def test_round_robin():
    """Test round robin schedule"""
    ts = Schedule("Test RR Schedule")
    td = Division("Test Division")

    """Begin with two teams"""
    td.add_team('T1', 'C1', 'L1')
    td.add_team('T2', 'C2', 'L2')
    play_dates = create_round_date('09/02/18',28)
    round_robin(ts, td, play_dates, 0)

    """Check rounds should be 1 less the number of teams"""
    assert ts.nrounds == td.nteams - 1

    """Check matches, should be 2 teams choose 2 divided by num rounds"""
    r = ts.rounds[ts.round_lkup['09/02/18']]
    assert r.nmatches == comb(td.nteams, 2) / ts.nrounds
    assert r.matches[0].home == 'T1'
    assert r.matches[0].away == 'T2'

    """Add an additional two teams"""
    td.add_team('T3', 'C3', 'L3')
    td.add_team('T4', 'C4', 'L4')
    ts.reset()
    round_robin(ts, td, play_dates, 0)

    """Check rounds should be 1 less the number of teams"""
    assert ts.nrounds == td.nteams - 1

    """Check matches, should be 4 teams choose 2 divided by num rounds"""
    r = ts.rounds[ts.round_lkup['09/02/18']]
    exp_nmatches = comb(td.nteams, 2) / ts.nrounds
    home_list = []
    away_list = []
    for rnd in range(ts.nrounds):
        assert ts.rounds[rnd].nmatches == exp_nmatches
        for match in range(ts.rounds[rnd].nmatches):
            home_list.append(ts.rounds[rnd].matches[match].home)
            away_list.append(ts.rounds[rnd].matches[match].away)
    home_sort = sorted(home_list)
    away_sort = sorted(away_list)
    assert home_sort == ['T1', 'T1', 'T2', 'T3', 'T3', 'T4']
    assert away_sort == ['T1', 'T2', 'T2', 'T3', 'T4', 'T4']
    assert home_list == ['T1', 'T2', 'T4', 'T3', 'T3', 'T1']
    assert away_list == ['T4', 'T3', 'T2', 'T1', 'T4', 'T2']

    """Add an additional two teams"""
    td.add_team('T5', 'C5', 'L5')
    td.add_team('T6', 'C6', 'L6')
    ts.reset()
    round_robin(ts, td, play_dates, 0)

    """Check rounds should be 1 less the number of teams"""
    assert ts.nrounds == td.nteams - 1

    """Check matches, should be 6 teams choose 2 divided by num rounds"""
    exp_nmatches = comb(td.nteams, 2) / ts.nrounds
    for rnd in range(ts.nrounds):
        assert ts.rounds[rnd].nmatches == exp_nmatches

def test_cross_div():
    """Test cross div schedule"""
    ts = Schedule("Test XD Schedule")
    td1 = Division("Test Division 1")
    td2 = Division("Test Division 2")

    """Begin with two teams"""
    td1.add_team('T1a', 'C1a', 'L1a')
    td2.add_team('T1b', 'C1b', 'L1b')
    play_dates = create_round_date('09/02/18',6)
    cross_div(ts, td1, td2, play_dates)

    """Test nrounds"""
    assert ts.nrounds == td1.nteams

    """Test matches"""
    exp_matches = td1.nteams
    for rnd in range(ts.nrounds):
        assert ts.rounds[rnd].nmatches == exp_matches
    assert ts.rounds[0].matches[0].home == 'T1a'
    assert ts.rounds[0].matches[0].away == 'T1b'

    """Add two more teams"""
    td1.add_team('T2a', 'C2a', 'L2a')
    td2.add_team('T2b', 'C2b', 'L2b')
    ts.reset()
    cross_div(ts, td1, td2, play_dates)

    """Test nrounds"""
    assert ts.nrounds == td1.nteams

    """Test matches"""
    exp_matches = td1.nteams
    home_list = []
    away_list = []
    for rnd in range(ts.nrounds):
        assert ts.rounds[rnd].nmatches == exp_matches
        for match in range(ts.rounds[rnd].nmatches):
            home_list.append(ts.rounds[rnd].matches[match].home)
            away_list.append(ts.rounds[rnd].matches[match].away)
    assert home_list == ['T1a', 'T2a', 'T2b', 'T1b']
    assert away_list == ['T1b', 'T2b', 'T1a', 'T2a']

    """Add two more teams"""
    td1.add_team('T3a', 'C3a', 'L3a')
    td2.add_team('T3b', 'C3b', 'L3b')
    ts.reset()
    cross_div(ts, td1, td2, play_dates)

    """Test nrounds"""
    assert ts.nrounds == td1.nteams

    """Test matches"""
    exp_matches = td1.nteams
    home_list = []
    away_list = []
    for rnd in range(ts.nrounds):
        assert ts.rounds[rnd].nmatches == exp_matches
        for match in range(ts.rounds[rnd].nmatches):
            home_list.append(ts.rounds[rnd].matches[match].home)
            away_list.append(ts.rounds[rnd].matches[match].away)
    assert home_list \
            == ['T1a', 'T2a', 'T3a', 'T2b', 'T3b', 'T1b', 'T1a', 'T2a', 'T3a']
    assert away_list \
            == ['T1b', 'T2b', 'T3b', 'T1a', 'T2a', 'T3a', 'T3b', 'T1b', 'T2b']

def test_combine_schedules():
    play_dates = create_round_date('09/02/18',4)

    ts1h1 = Schedule('Test Div 1 RR Half 1')
    ts2h1 = Schedule('Test Div 2 RR Half 1')
    tsxd = Schedule('Test XD')
    ts1h2 = Schedule('Test Div 1 RR Half 2')
    ts2h2 = Schedule('Test Div 2 RR Half 2')

    td1 = Division("Test Division 1")
    td1.add_team('T1a', 'C1a', 'L1a')
    td1.add_team('T2a', 'C2a', 'L2a')

    td2 = Division("Test Division 2")
    td2.add_team('T1b', 'C1b', 'L1b')
    td2.add_team('T2b', 'C2b', 'L2b')

    round_robin(ts1h1, td1, [play_dates[0]], 0)
    round_robin(ts1h2, td1, [play_dates[-1]], 1)
    cross_div(tsxd, td1, td2, play_dates[1:-1])
    round_robin(ts2h1, td2, [play_dates[0]], 0)
    round_robin(ts2h2, td2, [play_dates[-1]], 1)

    tsh1 = Schedule('Test RR Half 1')
    assert ts1h1.nrounds == 1
    assert ts2h1.nrounds == 1
    assert ('09/02/18' in ts1h1.round_lkup.keys()) == True
    assert ts1h1.round_lkup.keys() == ts2h1.round_lkup.keys()
    assert ts1h1.rounds[0].nmatches == 1
    assert ts2h1.rounds[0].nmatches == 1
    combine_schedules(tsh1, ts1h1, ts2h1)
    assert tsh1.nrounds == 1
    assert ('09/02/18' in tsh1.round_lkup.keys()) == True
    assert tsh1.round_lkup.keys() == ts1h1.round_lkup.keys()
    assert tsh1.rounds[0].nmatches == 2
    assert tsh1.rounds[0].matches[0].home == ts1h1.rounds[0].matches[0].home
    assert tsh1.rounds[0].matches[0].away == ts1h1.rounds[0].matches[0].away
    assert tsh1.rounds[0].matches[1].home == ts2h1.rounds[0].matches[0].home
    assert tsh1.rounds[0].matches[1].away == ts2h1.rounds[0].matches[0].away

    tsh2 = Schedule('Test RR Half 2')
    assert ts1h2.nrounds == 1
    assert ts2h2.nrounds == 1
    assert ('09/23/18' in ts1h2.round_lkup.keys()) == True
    assert ts1h2.round_lkup.keys() == ts2h2.round_lkup.keys()
    assert ts1h2.rounds[0].nmatches == 1
    assert ts2h2.rounds[0].nmatches == 1
    combine_schedules(tsh2, ts1h2, ts2h2)
    assert tsh2.nrounds == 1
    assert ('09/23/18' in tsh2.round_lkup.keys()) == True
    assert tsh2.round_lkup.keys() == ts1h2.round_lkup.keys()
    assert tsh2.rounds[0].nmatches == 2
    assert tsh2.rounds[0].matches[0].home == ts1h2.rounds[0].matches[0].home
    assert tsh2.rounds[0].matches[0].away == ts1h2.rounds[0].matches[0].away
    assert tsh2.rounds[0].matches[1].home == ts2h2.rounds[0].matches[0].home
    assert tsh2.rounds[0].matches[1].away == ts2h2.rounds[0].matches[0].away

    tsa = Schedule('Test Schedule Complete A')
    tsb = Schedule('Test Schedule Complete B')
    tsc = Schedule('Test Schedule Complete C')
    assert tsxd.nrounds == 2
    combine_schedules(tsa, tsh1, tsxd, tsh2)
    combine_schedules(tsb, tsxd, tsh1, tsh2)
    combine_schedules(tsc, tsh2, tsxd, tsh1)
    assert tsa.nrounds == 4
    assert tsb.nrounds == 4
    assert tsc.nrounds == 4
