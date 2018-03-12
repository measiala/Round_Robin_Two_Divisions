#!/usr/bin/python3

def floor(a):
    if a >= 0:
        return int(a)
    elif a < 0:
        return int(a - 1)
    else:
        print("ERROR: Incorrect argument to floor function.")

def zmod(a,m):
    return a - m * floor(a / m)

def mod(a,m):
    return zmod(a - 1, m) + 1

def create_round_date(start,omit,nround):
    from datetime import date, datetime, timedelta
    start_dt = datetime.strptime(start,"%m/%d/%y")

    round_date = []
    for round in range(nround):
        flag = 0
        if round == 0:
            flag = 1
            rnd_dt = start_dt
            round_dt = rnd_dt.strftime("%m/%d/%y")
        else:
            while flag == 0:
                rnd_dt = rnd_dt + timedelta(days=7)
                round_dt = rnd_dt.strftime("%m/%d/%y")
                if round_dt in omit:
                    flag = 0
                else:
                    flag = 1
        round_date.append(round_dt)
    return round_date

def init(ntables, ndivs, nteams):
    total_teams  = ndivs * nteams
    table_name = []
    for table_id in range(ntables):
        table_name.append("Table " + str(table_id))
    team_id = []
    team_name = []
    team_loc_id = []
    team_loc_name = []
    for div in range(ndivs):
        for team_no in range(nteams):
            team_id.append(div*nteams + team_no)
            team_name.append("Team " + str(team_no) + " in Div " + str(div))
            team_loc_id.append(team_no)
            team_loc_name.append("Table " + str(team_loc_id[team_no]))
    return [team_id, team_name, team_loc_id, team_loc_name]

def outmatch(_home,_round,_game,_team1,_team2,_around,_agame,_ateam1,_ateam2):
    _around.append(_round)
    _agame.append(_game)
    if _home == 1:
        _ateam1.append(_team1)
        _ateam2.append(_team2)
    elif _home == 2:
        _ateam1.append(_team2)
        _ateam2.append(_team1)
    else:
        print("ERROR: Incorrect argument to outmatch.")

def create_mod_canon_round_robin(dset,nteams,swap_loc):
    n = nteams / 2
    nrounds = nteams - 1

    around = []
    agame  = []
    ateam1 = []
    ateam2 = []

    for round in range(nrounds):
        game = 0
        team1 = round
        team2 = nteams - 1
        if zmod(round,2) == 0:
            home = mod(1 + swap_loc, 2)
        elif zmod(round,2) == 1:
            home = mod(2 + swap_loc, 2)
        if round >= (nrounds - 3):
            home = mod(home + 1, 2)
        outmatch(home,round,game,team1,team2,around,agame,ateam1,ateam2)
        if n >= 2:
            for kk in range(int(n / 2)):
                game = game + 1
                k = kk * 2 + 1
                team1 = zmod(round + k, nteams - 1 )
                team2 = zmod(round - k, nteams - 1 )
                home = 1 + swap_loc
                outmatch(home,round,game,team1,team2,around,agame,ateam1,ateam2)
        if n >= 3:
            for kk in range(int((n - 1) / 2)):
                game = game + 1
                k = kk * 2 + 2
                team1 = zmod(round - k, nteams - 1 )
                team2 = zmod(round + k, nteams - 1 )
                home = 1 + swap_loc
                outmatch(home,round,game,team1,team2,around,agame,ateam1,ateam2)

    return [around, agame, ateam1, ateam2]

def create_std_cross_div(nteams,dset="Cross"):
    around = []
    agame  = []
    ateam1 = []
    ateam2 = []
    for round in range(nteams):
        for game in range(nteams):
            around.append(round)
            agame.append(game)
            team1 = game
            team2 = zmod(game + round, nteams) + nteams
            if zmod(round,2) == 0:
                ateam1.append(team1)
                ateam2.append(team2)
            elif zmod(round,2) == 1:
                ateam1.append(team2)
                ateam2.append(team1)
    return [around, agame, ateam1, ateam2]

def combine_intra_div(r1,g1,h1,a1,r2,g2,h2,a2):
    if len(r1) != len(r2):
        print("ERROR: The two intradivisional schedules have different size")
    else:
        nround = r1[-1] + 1
        ngame  = g1[-1] + 1
        ndteam = ngame * 2
        for ii in range(len(g2)):
            g2[ii] = g2[ii] + ngame
            h2[ii] = h2[ii] + ndteam
            a2[ii] = a2[ii] + ndteam
        r = []
        g = []
        h = []
        a = []
        for round in range(nround):
            for game in range(ngame):
                r.append(round)
                g.append(game)
                ii = round*ngame + game
                h.append(h1[ii])
                a.append(a1[ii])
            for game in range(ngame):
                r.append(round)
                g.append(game + ngame)
                ii = round*ngame + game
                h.append(h2[ii])
                a.append(a2[ii])
        return [r,g,h,a]

def combine_all_schedules(r1,g1,h1,a1,r2,g2,h2,a2,r3,g3,h3,a3):
    g = g1 + g2 + g3
    h = h1 + h2 + h3
    a = a1 + a2 + a3
    for ii in range(len(r2)):
        r2[ii] = r2[ii] + r1[-1] + 1
    for ii in range(len(r3)):
        r3[ii] = r3[ii] + r2[-1] + 1
    r = r1 + r2 + r3
    return [r,g,h,a]

def print_schedule( rounds, dates, games, home_team, away_team ):
    num_rnds  = rounds[-1] + 1
    num_games = games[-1] + 1

    for round in range(num_rnds):
        rdate = dates[round]
        line = '{}'.format(rdate)
        for game in range(num_games):
            ii = round * num_games + game
            line = line + "  " '{:2} @ {:2}'.format(away_team[ii]+1,home_team[ii]+1)
        print(line)

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

def check_home(h,a):
    return 1
    
            
ndteams = 10
ndiv = 2
nteams = ndteams * ndiv
nloc = ndteams

team_names = ['Huntts #1','Lamonts #1','Scotts #4','Lamonts #3','Woodys #3',\
                  'Lisas #1','Moose #1','Scotts #3','Lamonts #2','Woodys #1',\
                  'Huntts #2','Lamonts #4','Scotts #2','Lamonts #6','Lisas #3',\
                  'Lisas #2','Moose #2','Scotts #1','Lamonts #5','Woodys #2']
capt_names = ['House','Savoy','Necole','Baltimore','Fuchs',\
                  'Wright','Armstrong','Burch','Hall','McClure',\
                  'Bowie','Adams','Ellis','Gray','Montoya',\
                  'Boswell','Cross','Grieninger','Holmes','Raines']

team_loc = []
for ii in range(len(team_names)):
    team_loc.append(team_names[ii].split()[0])
print(team_loc)

# team_id, team_name, team_loc_id, team_loc_name
[a,b,c,d] = init(ndteams, ndiv, nloc)

# Game dates
round_date = create_round_date('09/12/17',['12/26/17'],28)

# around, agame, ateam1, ateam2
print("Division 1 First Half")
[r11,g11,h11,a11] = create_mod_canon_round_robin("div11",ndteams,0)
#print_schedule(r11,round_date,g11,h11,a11)
print("Division 1 Second Half")
[r12,g12,h12,a12] = create_mod_canon_round_robin("div12",ndteams,1)
#print_schedule(r12,round_date,g12,h12,a12)
print("Division 2 First Half")
[r21,g21,h21,a21] = create_mod_canon_round_robin("div21",ndteams,1)
#print_schedule(r21,round_date,g21,h21,a21)
print("Divsion 2 Second Half")
[r22,g22,h22,a22] = create_mod_canon_round_robin("div22",ndteams,0)
#print_schedule(r22,round_date,g22,h22,a22)
print("Interdivisional")
[rx,gx,hx,ax] = create_std_cross_div(ndteams,"xdiv")
#print_schedule(rx,round_date,gx,hx,ax)
print("Combine First Half")
[r1,g1,h1,a1] = combine_intra_div(r11,g11,h11,a11,r21,g21,h21,a21)
#print_schedule(r1,round_date,g1,h1,a1)
print("Combine Second Half")
[r2,g2,h2,a2] = combine_intra_div(r12,g12,h12,a12,r22,g22,h22,a22)
#print_schedule(r2,round_date,g2,h2,a2)
print("Combine all schedules")
[r,g,h,a] = combine_all_schedules(r1,g1,h1,a1,rx,gx,hx,ax,r2,g2,h2,a2)
print_schedule(r,round_date,g,h,a)

print_team_schedule("Lisas #2",r,round_date,g,h,a)



