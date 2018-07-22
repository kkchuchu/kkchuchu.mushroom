import json
import sys
import pandas as pd
from pdb import set_trace


def run(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
        d = {}
        i = 0
        for content in map(get_content, lines):
            records = to_dict(content)
            for r in records:
                d[i] = r
                i += 1

        df = pd.DataFrame.from_dict(d, orient='index')
        df.to_csv(file_name + '.csv')
            

def get_content(line):
    if 'SHOW_ACTION' in line:
        _, _, content = line.split('>>>')
        return json.loads(content)
    else:
        return None

def to_dict(content):
    if content is None:
        return []
    data = content['data']
    players = data['players']
    action = data['action']
    table = data['table']
    # small_blind = data['smallBlind']
    # big_blind = data['bigBlind']
    for player in players:
        player['roundName'] = table['roundName']
        player['board'] = table['board']
    return players



if __name__ == '__main__':
    file_name = sys.argv[1]
    run(file_name)
    r = pd.DataFrame.read_csv(file_name + '.csv')
    print(r.head())
