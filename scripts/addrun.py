from hashlib import new
import sys
import re
from datetime import date

import pandas as pd

PATH = '/home/geodev/data/code/misc/data/runlog'
PATH_GEAR = '/home/geodev/data/code/misc/data/gear_mileage.csv'
TODAY = date.today()

def test_newrun(newrun):
    """Check the inputs of a run
    Args:
        newrun (str): a string with or without date
                      also indicating gear type
        gear type is one of {'r', 't', 'k', 'b'}
        for road, track, trek or bike
    """
    pattern_full = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{1,3}\.\d{2},[r,t,k,b]'
    pattern_today = r'\d{2}:\d{2}:\d{2},\d{1,3}\.\d{2},[r,t,k,b]'
    if re.findall(pattern_full, newrun):
        return re.findall(pattern_full, newrun)[0]
    else:
        return f'{TODAY} {re.findall(pattern_today, newrun)[0]}'

def read_runlog(PATH, newrun):
    """
    Add a run to PATH file
    Args:
        PATH: absolute or relative path to file, [str]
        newrun: run details in form `'YYYY-MM-DD HH:MM:SS,KK.MM'`
    """
    newrun = newrun[:-2]
    with open(PATH, 'a') as f:
        newrun += '\n'
        f.write(newrun)

    print(f'Run: "{newrun.strip()}" added to runlog.')
    return


def update_gear_mileage(PATH_GEAR, newrun):
    """Upate mileage for a given piece of gear.
    Args:
        PATH: absolute or relative path to file, [str]
        newrun: run details in form `'YYYY-MM-DD HH:MM:SS,KK.MM,[r,t,k,b]'`
    Notes:
        gear type is one of {'r', 't', 'k', 'b'}
        for road, track, trek or bike
    """
    colnames = {'r': 'road_shoes',
                't': 'track_shoes',
                'k': 'trek_shoes',
                'b': 'bike'
                }
    gear = newrun[-1]
    kms = float(newrun.split(',')[1])
    df = pd.read_csv(PATH_GEAR)
    df.loc[0, colnames.get(gear)] += kms
    df.to_csv(PATH_GEAR, index=False)

    print(f'{colnames.get(gear)} mileage increased by {kms}km')
    return None


if __name__ == '__main__':
    try:
        newrun = test_newrun(sys.argv[1])
        if newrun[-1] in ['r', 't']:
            read_runlog(PATH, newrun)
        update_gear_mileage(PATH_GEAR, newrun)
    except IndexError:
        print("""New run must be provided as either:
`"YYYY-MM-DD HH:MM:SS,KK.MM,[r,t,k,b]"`
or
`"HH:MM:SS,KK.MM,[r,t,k,b]"`
in which case TODAY\'s date will be inserted automatically.""")
