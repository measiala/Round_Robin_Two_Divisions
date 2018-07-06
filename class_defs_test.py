"""
Test all classes in class_defs.py
"""
from class_defs import Match, Round, Schedule, Division, League

ts = Schedule('Test Schedule')
tlg = League('Test League')

def test_schedule():
    """Test initialization"""
    assert ts.name == 'Test Schedule'
    assert len(ts.rounds) == 0
    assert ts.nrounds == 0
    assert len(ts.round_lkup.keys()) == 0
    assert ts.rounds == []
    assert ts.round_lkup == {}

    """Test add_round"""
    ts.add_round(0, '09/02/18')
    assert len(ts.rounds) == 1
    assert ts.nrounds == 1
    assert len(ts.round_lkup.keys()) == 1
    assert ('09/02/18' in ts.round_lkup.keys()) == True

    """Test second add_round"""
    ts.add_round(1, '09/09/18')
    assert len(ts.rounds) == 2
    assert ts.nrounds == 2
    assert len(ts.round_lkup.keys()) == 2
    assert ('09/09/18' in ts.round_lkup.keys()) == True

    """Verify order of keys"""
    assert ts.round_lkup['09/02/18'] == 0
    assert ts.round_lkup['09/09/18'] == 1

    """Test reset"""
    ts.reset()
    assert ts.name == 'Test Schedule'
    assert len(ts.rounds) == 0
    assert ts.nrounds == 0
    assert len(ts.round_lkup.keys()) == 0
    assert ts.rounds == []
    assert ts.round_lkup == {}
    ts.add_round(0, '09/02/18')
    ts.add_round(1, '09/09/18')   

def test_round():
    """Test initialization"""
    r = ts.rounds[ts.round_lkup['09/02/18']]
    assert r.week == 0
    assert r.play_date == '09/02/18'
    assert len(r.matches) == 0
    assert r.nmatches == 0
    assert len(r.match_lkup.keys()) == 0
    assert r.matches == []
    assert r.match_lkup == {}

    """Test add_match"""
    r.add_match(1, 'Team 1', 'Team 2')
    assert len(r.matches) == 1
    assert r.nmatches == 1
    assert len(r.match_lkup.keys()) == 1
    assert ('Team 1' in r.match_lkup.keys()) == True

    """Test second add_match"""
    r.add_match(2, 'Team 3', 'Team 4')
    assert len(r.matches) == 2
    assert r.nmatches == 2
    assert len(r.match_lkup.keys()) == 2
    assert ('Team 4' in r.match_lkup.keys()) == True

    """Verify order of keys"""
    assert r.match_lkup['Team 1'] == 0
    assert r.match_lkup['Team 4'] == 1

def test_match():
    """Test initialization of normal match"""
    r = ts.rounds[ts.round_lkup['09/02/18']]
    m1 = r.matches[r.match_lkup['Team 1']]
    assert m1.home == 'Team 1'
    assert m1.away == 'Team 2'

    """Test initialization of reversed match"""
    m2 = r.matches[r.match_lkup['Team 4']]
    assert m2.home == 'Team 4'
    assert m2.away == 'Team 3'
   
def test_league():
    """Test initialization"""
    assert tlg.name == 'Test League'
    assert len(tlg.divs) == 0
    assert tlg.ndivs == 0
    assert len(tlg.div_lkup.keys()) == 0
    assert tlg.divs == []
    assert tlg.div_lkup == {}

    """Test add_div"""
    tlg.add_div('Test Division 1') 
    assert len(tlg.divs) == 1
    assert tlg.ndivs == 1
    assert len(tlg.div_lkup.keys()) == 1
    assert ('Test Division 1' in tlg.div_lkup.keys()) == True

    """Test second add_div"""
    tlg.add_div('Test Division 2') 
    assert len(tlg.divs) == 2
    assert tlg.ndivs == 2
    assert len(tlg.div_lkup.keys()) == 2
    assert ('Test Division 2' in tlg.div_lkup.keys()) == True

    """Verify order of keys"""
    assert tlg.div_lkup['Test Division 1'] == 0
    assert tlg.div_lkup['Test Division 2'] == 1
   
def test_division():
    """Test initialization"""
    d1 = tlg.divs[tlg.div_lkup['Test Division 1']]
    assert d1.name == 'Test Division 1'
    assert d1.teams == []
    assert d1.capts == []
    assert d1.locs == []
    assert d1.nteams == 0
    assert len(d1.team_lkup.keys()) == 0
    assert d1.team_lkup == {}

    """Test add_team"""
    d1.add_team('Test Team 1', 'John Doe', 'Test Bar 1')
    assert d1.teams == ['Test Team 1']
    assert d1.capts == ['John Doe']
    assert d1.locs == ['Test Bar 1']
    assert d1.nteams == 1
    assert len(d1.team_lkup.keys()) == 1
    assert ('Test Team 1' in d1.team_lkup.keys()) == True

    """Test second add_team"""
    d1.add_team('Test Team 2', 'Jane Doe', 'Test Bar 2')
    assert d1.teams == ['Test Team 1', 'Test Team 2']
    assert d1.capts == ['John Doe', 'Jane Doe']
    assert d1.locs == ['Test Bar 1', 'Test Bar 2']
    assert d1.nteams == 2
    assert len(d1.team_lkup.keys()) == 2
    assert ('Test Team 2' in d1.team_lkup.keys()) == True

    """Verify order of keys"""
    assert d1.team_lkup['Test Team 1'] == 0
    assert d1.team_lkup['Test Team 2'] == 1
