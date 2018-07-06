"""
Process to import teams
"""

def import_teams(leag, ndteams, infile):
    """Read list of all teams from infile store in league"""
    import csv
    import logging

    leag_list = []
    with open(infile, 'r') as team_file:
        team_csv = csv.reader(team_file)
        rec_no = 0
        for line in team_csv:
            leag.divs[int(rec_no / ndteams)].add_team(line[0], line[1], line[2])
            leag_list.append(line[0])
            rec_no = rec_no + 1
        logging.info("team_info file had %d records" % rec_no)
    if (leag.divs[0].nteams != ndteams) or (leag.divs[1].nteams != ndteams):
        print("Input file did not contain %d teams as required" % ndteams)
        logging.error("Div 1 has %d teams and Div 2 has %d teams" 
                      % (leag.divs[0].nteams, leag.divs[1].nteams))
        exit(2)
    return leag_list