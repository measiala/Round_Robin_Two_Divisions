"""
Test print output
"""

from print_schedule import print_schedule, print_league
from create_schedule import round_robin, cross_div, combine_schedules
from process_options import create_play_dates
from class_defs import League, Schedule

def test_print_schedule():
    tl = League('Test League')
    tl.add_div('Test Div 1')
    tl.divs[0].add_team('T1a','C1a','L1a')
    tl.divs[0].add_team('T2a','C2a','L2a')
    tl_list = ['T1a', 'T2a']
    assert tl.ndivs == 1
    assert tl.divs[0].nteams == 2
    tl.add_div('Test Div 2')
    tl.divs[1].add_team('T1b','C1b','L1b')
    tl.divs[1].add_team('T2b','C2b','L2b')
    tl_list = tl_list + ['T1b', 'T2b']
    assert tl.ndivs == 2
    assert tl.divs[0].nteams == 2
    assert tl.divs[1].nteams == 2

    [pdh1, pdh2, pdxd] = create_play_dates('2018/09/02', 2, SKIP_DATES=[])
    assert pdh1 == ['2018/09/02']
    assert pdh2 == ['2018/09/23']
    assert pdxd == ['2018/09/09','2018/09/16']
    ts = Schedule('Overall Schedule')

    ts1h1 = Schedule('Test Div 1 Half 1')
    ts2h1 = Schedule('Test Div 2 Half 1')
    ts1h2 = Schedule('Test Div 1 Half 2')
    ts2h2 = Schedule('Test Div 2 Half 2')
    tsxd = Schedule('Test Inter')

    round_robin(ts1h1, tl.divs[0], pdh1, 0)
    round_robin(ts2h1, tl.divs[1], pdh1, 0)
    round_robin(ts1h2, tl.divs[0], pdh2, 1)
    round_robin(ts2h2, tl.divs[1], pdh2, 1)
    cross_div(tsxd, tl.divs[0], tl.divs[1], pdxd)
    combine_schedules(ts, ts1h1, ts1h2, ts2h1, ts2h2, tsxd)

    print_schedule(ts1h1, tl_list)
    print('')
    print_schedule(ts2h1, tl_list)
    print('')
    print_schedule(ts1h2, tl_list)
    print('')
    print_schedule(ts2h2, tl_list)
    print('')
    print_schedule(tsxd, tl_list)
    print('')
    print_schedule(ts, tl_list)
    print('')

def test_print_league():
    tl = League('Test League')
    tl.add_div('Test Div 1')
    tl.divs[0].add_team('T1a','C1a','L1a')
    tl.divs[0].add_team('T2a','C2a','L2a')
    tl_list = ['T1a', 'T2a']
    assert tl.ndivs == 1
    assert tl.divs[0].nteams == 2
    print_league(tl, tl_list)
    print('')

    tl.add_div('Test Div 2')
    tl.divs[1].add_team('T1b','C1b','L1b')
    tl.divs[1].add_team('T2b','C2b','L2b')
    tl_list = tl_list + ['T1b', 'T2b']
    assert tl.ndivs == 2
    assert tl.divs[0].nteams == 2
    assert tl.divs[1].nteams == 2
    print_league(tl, tl_list)
    with open('./output/test_league.out','w') as outleague:
        print_league(tl, tl_list, outleague)

if __name__ == '__main__':
    test_print_schedule()
    test_print_league()
