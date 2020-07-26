import sys
import re

PATH = '/media/DATA/code/misc/data/runlog'

def test_newrun(newrun):
    pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{1,3}\.\d{2}'
    fout = 'New run must follow the exact pattern: `"YYYY-MM-DD HH:MM:SS,KK.MM"`'
    assert re.findall(pattern, newrun), fout

def read_runlog(PATH, newrun):
    """
    Add a run to PATH file
    Args:
        PATH: absolute or relative path to file, [str]
        newrun: run details in form `'YYYY-MM-DD HH:MM:SS,KK.MM'`"""

    with open(PATH, 'a') as f:
        newrun += '\n'
        f.write(newrun)

    print('Run added to runlog.')
    return


if __name__ == '__main__':
    try:
        newrun = sys.argv[1]
        test_newrun(newrun)
        read_runlog(PATH, newrun)
    except IndexError:
        print('New run must follow the exact pattern: `"YYYY-MM-DD HH:MM:SS,KK.MM"`')