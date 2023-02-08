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
        gear type is one of {'kw', 'kb, 'p'}
        for linvara_white, kinvara_blue or peregrine
    """
    pattern_full = r'\d{4}-\d{2}-\d{2},\d{2}:\d{2}:\d{2},\d{1,3}\.\d{1,2},(kw|kb|p)?'
    pattern_today =                  r'\d{2}:\d{2}:\d{2},\d{1,3}\.\d{1,2},(kw|kb|p)?'
    if re.fullmatch(pattern_full, newrun):
        return re.fullmatch(pattern_full, newrun).group()
    else:
        return f'{TODAY},{re.fullmatch(pattern_today, newrun).group()}'

def read_runlog(PATH, newrun):
    """
    Add a run to PATH file
    Args:
        PATH: absolute or relative path to file, [str]
        newrun: run details in form `'YYYY-MM-DD,HH:MM:SS,KK.MM'`
    """
    timedate = ' '.join(newrun.split(',')[:2])
    distance = newrun.split(',')[2]
    newrun = ','.join([timedate, distance])
    with open(PATH, 'a') as f:
        newrun += '\n'
        f.write(newrun)

    print(f'Run: "{newrun}" added to runlog.')
    return


def update_gear_mileage(PATH_GEAR, newrun):
    """Upate mileage for a given piece of gear.
    Args:
        PATH: absolute or relative path to file, [str]
        newrun: run details in form `'YYYY-MM-DD,HH:MM:SS,KK.MM,[kw,kb,p,t,b]'`
    Notes:
        gear type is one of {'kw', 'kb', 'p', 't', 'b'}
        kw and kb are the main road running shoes when either there is an overlap
        between an old and new pair, or if there are two pairs to prepare for a
        long race.
        for road, trail, trek or bike
    """
    colnames = {'kb': 'kinvara_blue',
                'kw': 'kinvara_white',
                'p': 'peregrine',
                't': 'trek_shoes',
                'b': 'bike'
                }
    gear = newrun.split(',')[-1]
    kms = float(newrun.split(',')[-2])
    df = pd.read_csv(PATH_GEAR)
    df.loc[0, colnames.get(gear)] += kms
    df.to_csv(PATH_GEAR, index=False)

    print(f'{colnames.get(gear)} mileage increased by {kms}km')
    return None


if __name__ == '__main__':
    try:
        newrun = test_newrun(sys.argv[1])
        if newrun.split(',')[-1] in ['kw', 'kb', 'p']:
            read_runlog(PATH, newrun)
        update_gear_mileage(PATH_GEAR, newrun)
    except IndexError:
        print("""New run must be provided as either:
`"YYYY-MM-DD HH:MM:SS,KK.MM,[kw,kb,p,t,b]"`
or
`"HH:MM:SS,KK.MM,[kw,kb,p,t,b]"`
in which case TODAY\'s date will be inserted automatically.""")
