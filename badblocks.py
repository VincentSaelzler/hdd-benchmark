import os
import subprocess
import time


def run_badblocks(dev_path, log_file_path):

    before = int(time.time())
    print(before)

    print('starting badblocks. . .')
    # time.sleep(2)
    subprocess.run(['badblocks', '-wsv', '-o', log_file_path, dev_path])
    print('Finished badblocks.')

    after = int(time.time())
    print(after)

    elapsed = after - before
    print(elapsed)

    bb_runtime = {
        'begin_time': before,
        'end_time': after,
        'elapsed': elapsed,
    }

    return bb_runtime


def check_for_bad_blocks(log_file_path):
    # true/false for any bad blocks (normally false)
    bad_blocks = {'HasBadBlocks': True if os.path.getsize(
        log_file_path) > 0 else False}

    # specific number of bad blocks (normally 0)
    # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s07.html
    with open(log_file_path, 'r') as log_file:
        bad_blocks['NumBadBlocks'] = len(log_file.readlines())

    return bad_blocks