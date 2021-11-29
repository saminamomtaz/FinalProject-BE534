""" Tests for metascape.py """

# pylint:disable=consider-using-with,unspecified-encoding

import os
import re
import random
import string
from subprocess import getstatusoutput, getoutput

PRG = './metascape.py'
file1 = './inputs/foldchange.xlsx'
file2 = './inputs/enrichment.xlsx'


# --------------------------------------------------
def random_string():
    """generate a random filename"""

    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))


# --------------------------------------------------
def test_exists():
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """ Prints usage """

    for flag in ['', '-h', '--help']:
        out = getoutput(f'{PRG} {flag}')
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_bad_outfile():
    """fails on bad output"""

    bad = random_string()
    rv, out = getstatusoutput(f'{PRG} {file1} {file2} {bad}')
    assert rv != 0
    assert re.search(f"outfile \"{bad}\" must be a csv file", out)


# --------------------------------------------------
def test_bad_inputfile1():
    """fails on bad input1"""

    bad = random_string()
    out_file = random_string()
    rv, out = getstatusoutput(f'{PRG} {bad} {file2} {out_file}.csv')
    assert rv != 0
    assert re.search(f"file1 \"{bad}\" must be an excel file", out)


# --------------------------------------------------
def test_bad_inputfile2():
    """fails on bad input2"""

    bad = random_string()
    out_file = random_string()
    rv, out = getstatusoutput(f'{PRG} {file1} {bad} {out_file}.csv')
    assert rv != 0
    assert re.search(f"file2 \"{bad}\" must be an excel file", out)


# --------------------------------------------------
def run(args):
    """ Run test """

    if os.path.exists('up_reg.png'):
        os.remove('up_reg.png')
    if os.path.exists('down_reg.png'):
        os.remove('down_reg.png')
    if os.path.exists(args[2]):
        os.remove(args[2])
    rv, out = getstatusoutput(f'{PRG} {" ".join(args)}')
    assert rv == 0
    assert re.search('See', out)
    assert os.path.isfile(args[2])
    assert os.path.isfile('up_reg.png')
    assert os.path.isfile('down_reg.png')


# --------------------------------------------------
def test1():
    """ test """

    run([file1, file2, 'out.csv'])
