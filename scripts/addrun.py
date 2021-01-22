import sys
import re
from datetime import date

PATH = '/home/geodev/Data/code/misc/data/runlog'
TODAY = date.today()

def test_newrun(newrun):
    pattern_full = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{1,3}\.\d{2}'
    pattern_today = r'\d{2}:\d{2}:\d{2},\d{1,3}\.\d{2}'
    if re.findall(pattern_full, newrun):
        return re.findall(pattern_full, newrun)[0]
    else:
        return f'{TODAY} {re.findall(pattern_today, newrun)[0]}'
    
def read_runlog(PATH, newrun):
    """
    Add a run to PATH file
    Args:
        PATH: absolute or relative path to file, [str]
        newrun: run details in form `'YYYY-MM-DD HH:MM:SS,KK.MM'`"""

    with open(PATH, 'a') as f:
        newrun += '\n'
        f.write(newrun)

    print(f'Run: "{newrun.strip()}" added to runlog.')
    return


if __name__ == '__main__':
    try:
        newrun = test_newrun(sys.argv[1])
        read_runlog(PATH, newrun)
    except IndexError:
        print("""New run must be provided as either:
`"YYYY-MM-DD HH:MM:SS,KK.MM"`
or
`"HH:MM:SS,KK.MM"`
in which case TODAY\'s date will be inserted automatically.""")
        