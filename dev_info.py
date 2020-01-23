import subprocess
import json


def get_info(path):
    # hard-coding based on the output format of lsblk
    PARENT_KEY = 'blockdevices'
    DEV_INDEX = 0

    info_str = ''
    if __debug__:
        info_str = subprocess.check_output(['lsblk', '-OJb', path]).decode()
    else:
        with open('input-sample/lsblk.json', 'r') as sample_file:
            info_str = sample_file.read()

    # parse output to dictionary
    info_json = json.loads(info_str)
    info = info_json[PARENT_KEY][DEV_INDEX]

    # creating a new "clean dictionary" from dict comprehensin also seems possible
    # and the comprehension thing seems all the rave with python, but fundamentally this is
    # an update, so not doing that here.
    for key, val in info.items():
        info[key] = val.strip() if isinstance(val, str) else val

    return info


def get_serial(path):
    SERIAL_KEY = 'serial'
    info = get_info(path)
    return info[SERIAL_KEY]
