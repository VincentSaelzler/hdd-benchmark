import os
import subprocess
import time


def run_badblocks(dev_path, log_file_path):

    # run badblocks
    before = int(time.time())
    if __debug__:
        subprocess.run(['badblocks', '-wsv', '-o', log_file_path, dev_path])
    else:
        time.sleep(2)
    after = int(time.time())
    elapsed = after - before

    # collect output
    bb_runtime = {
        'begin_time': before,
        'end_time': after,
        'elapsed': elapsed,
    }

    return bb_runtime


def check_for_bad_blocks(log_file_path):
    if __debug__:
        # true/false for any bad blocks (normally false)
        bad_blocks = {'HasBadBlocks': True if os.path.getsize(
            log_file_path) > 0 else False}

        # specific number of bad blocks (normally 0)
        # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s07.html
        with open(log_file_path, 'r') as log_file:
            bad_blocks['NumBadBlocks'] = len(log_file.readlines())

        return bad_blocks
    else:
        return {'HasBadBlocks': True, 'NumBadBlocks': 0}

