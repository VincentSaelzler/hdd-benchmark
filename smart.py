import json
import time
import subprocess

DEBUG_MODE = True

def main():
    cap = get_capabilities()
    health = get_health()
	attr = get_attributes()

    smart = {**cap, **health}
    print(smart)

def get_capabilities():
    SECONDS_PER_MIN = 60
    ATA_SMART_DATA = 'ata_smart_data'
    OFFLINE_DATA_COLLECTION = 'offline_data_collection'
    SELF_TEST = 'self_test'
    STATUS = 'status'
    PASSED = 'passed'
    POLLING_MINUTES = 'polling_minutes'
    EXTENDED = 'extended'

    # run lsblk and collect output
    cap_str = ''
    # cap_str = subprocess.check_output(['lsblk', '-OJb', path]).decode()

    # .  .  .or use sample output for testing
    with open('input-sample/smart_after_test_clean.json', 'r') as sample_file:
        cap_str = sample_file.read()

    # parse output to dictionary
    info_json = json.loads(cap_str)
    ata = info_json[ATA_SMART_DATA]

    # determine how long the extended test should take to run
    polling_minutes = ata[SELF_TEST][POLLING_MINUTES][EXTENDED]
    polling_seconds = polling_minutes * SECONDS_PER_MIN

    # wait for the extended self test to complete
    self_test_status = ata[SELF_TEST][STATUS]
    while (PASSED not in self_test_status):
        time.sleep(1)  # TODO put polling seconds
        print('sleeping. . .')

    # collect results
    cap = {
        'polling_minutes': polling_minutes,
        'self_test_passed': self_test_status[PASSED],
        'offline_collection_passed': ata[OFFLINE_DATA_COLLECTION][STATUS][PASSED],
    }

    return cap


def get_health():
    SMART_STATUS = 'smart_status'
    PASSED = 'passed'

    # either get the real output, or use a sameple file
    health_str = ''
    if (DEBUG_MODE):
        with open('input-sample/smart_health_dirty.json', 'r') as sample_file:  # /smart_health_dirty.json
            health_str = sample_file.read()
    else:
        health_str = subprocess.check_output(
            ['smartctl', '-jH', 'DEVPATH']).decode()

    # parse json
    health = json.loads(health_str)

    return {'smart_health_passed': health[SMART_STATUS][PASSED]}


def get_attributes():
	


if __name__ == '__main__':
    main()
