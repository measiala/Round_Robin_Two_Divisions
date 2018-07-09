"""
Test process_options entities
"""

from process_options import process_options, create_round_date, create_play_dates

def test_create_round_date():
    """Test creating dates"""
    assert create_round_date('2018/09/02', 1) == ['2018/09/02']
    assert create_round_date('2018/09/02', 2) == ['2018/09/02', '2018/09/09']
    assert create_round_date('2018/09/02', 1, '2018/09/02') == ['2018/09/09']
    assert create_round_date('2018/09/02', 2, '2018/09/09') \
            == ['2018/09/02', '2018/09/16']

def test_create_play_date():
    """Test create play dates for intra and interdivisional schedules"""
    n = 2
    [h1, h2, xd] = create_play_dates('2018/09/04', n)
    assert h1 == ['2018/09/04']
    assert xd == ['2018/09/11','2018/09/18']
    assert h2 == ['2018/09/25']
    n = 2
    [h1, h2, xd] = create_play_dates('2018/09/04', n, ['2018/09/18'])
    assert h1 == ['2018/09/04']
    assert xd == ['2018/09/11','2018/09/25']
    assert h2 == ['2018/10/02']
    n = 4
    [h1, h2, xd] = create_play_dates('2018/09/04', n)
    assert h1 == ['2018/09/04', '2018/09/11', '2018/09/18']
    assert xd == ['2018/09/25', '2018/10/02', '2018/10/09', '2018/10/16']
    assert h2 == ['2018/10/23', '2018/10/30', '2018/11/06']
