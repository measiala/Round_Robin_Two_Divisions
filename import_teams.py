"""
Process to import teams
"""

import csv
import logging
from class_defs import League


def import_teams(leag: League, ndteams: int, infile: str) -> list[list[str], list[str]]:
    """Read list of all teams from infile store in league"""

    team_list = []
    capt_list = []
    with open(infile, "r", encoding="latin1") as team_file:
        team_csv = csv.DictReader(team_file, quoting=csv.QUOTE_ALL)
        # team_csv = csv.reader(team_file)
        rec_no = 0
        for line in team_csv:
            leag.divs[int(rec_no / ndteams)].add_team(
                line["Team"], line["Captain"], line["Location"]
            )
            team_list.append(line["Team"])
            capt_list.append(line["Captain"])
            # leag.divs[int(rec_no / ndteams)].add_team(line[0], line[1], line[2])
            # team_list.append(line[0])
            # capt_list.append(line[1])
            rec_no = rec_no + 1
        logging.info("team_info file had %d records", rec_no)
    if (leag.divs[0].nteams != ndteams) or (leag.divs[1].nteams != ndteams):
        print(f"Input file did not contain {ndteams} teams as required")
        logging.error(
            "Div 1 has %d teams and Div 2 has %d teams",
            leag.divs[0].nteams,
            leag.divs[1].nteams,
        )
        exit(2)
    return [team_list, capt_list]
