import json
import time
import subprocess

DEBUG_MODE = False


def get_all(dev_path):
    cap = get_capabilities(dev_path)
    health = get_health(dev_path)
    attr = get_attributes(dev_path)

    smart = {**cap, **health, **attr}
    return smart


def get_capabilities(dev_path):
    SECONDS_PER_MIN = 60
    ATA_SMART_DATA = 'ata_smart_data'
    OFFLINE_DATA_COLLECTION = 'offline_data_collection'
    SELF_TEST = 'self_test'
    STATUS = 'status'
    PASSED = 'passed'
    POLLING_MINUTES = 'polling_minutes'
    EXTENDED = 'extended'

    # either get the real output, or use a sample file
    cap_str = ''
    if (DEBUG_MODE):
        # /smart_during_test_clean.json /smart_before_test_clean.json
        with open('input-sample/smart_after_test_clean.json', 'r') as sample_file:
            cap_str = sample_file.read()
    else:
        cap_str = subprocess.check_output(
            ['smartctl', '-jc', dev_path]).decode()

    # parse output to dictionary
    info_json = json.loads(cap_str)
    ata = info_json[ATA_SMART_DATA]

    # determine how long the extended test should take to run
    polling_minutes = ata[SELF_TEST][POLLING_MINUTES][EXTENDED]
    #polling_seconds = polling_minutes * SECONDS_PER_MIN

    # wait for the extended self test to complete
    self_test_status = ata[SELF_TEST][STATUS]
    elapsed = 0
    while (PASSED not in self_test_status):
        time.sleep(SECONDS_PER_MIN)
        elapsed += SECONDS_PER_MIN
        print(
            f'Waiting for {dev_path} test to complete. {elapsed / 60}m of {polling_minutes}m')

    # collect results
    cap = {
        'polling_minutes': polling_minutes,
        'self_test_passed': self_test_status[PASSED],
        'offline_collection_passed': ata[OFFLINE_DATA_COLLECTION][STATUS][PASSED],
    }

    return cap


def get_health(dev_path):
    SMART_STATUS = 'smart_status'
    PASSED = 'passed'

    # either get the real output, or use a sample file
    health_str = ''
    if (DEBUG_MODE):
        with open('input-sample/smart_health_dirty.json', 'r') as sample_file:  # /smart_health_dirty.json
            health_str = sample_file.read()
    else:
        health_str = subprocess.check_output(
            ['smartctl', '-jH', dev_path]).decode()

    # parse json
    health = json.loads(health_str)

    return {'smart_health_passed': health[SMART_STATUS][PASSED]}


def get_attributes(dev_path):
    ATA_SMART_ATTRIBUTES = 'ata_smart_attributes'
    TABLE = 'table'
    NAME = 'name'
    RAW = 'raw'
    VALUE = 'value'

    # either get the real output, or use a sample file
    attr_str = ''
    if (DEBUG_MODE):
        with open('input-sample/smart_attributes.json', 'r') as sample_file:
            attr_str = sample_file.read()
    else:
        attr_str = subprocess.check_output(
            ['smartctl', '-jA', dev_path]).decode()

    # parse json
    attr = json.loads(attr_str)
    attr_table = attr[ATA_SMART_ATTRIBUTES][TABLE]
    # print(attr_table)

    # https://www.ixsystems.com/community/resources/hard-drive-burn-in-testing.92/
    IMPORTANT_ATTRIBUTES = ['Reallocated_Sector_Ct',
                            'Current_Pending_Sector', 'Offline_Uncorrectable']

    attrs = {d[NAME]: d[RAW][VALUE]
             for d in attr_table if d[NAME] in IMPORTANT_ATTRIBUTES}

    attr_error_count = sum(attrs.values())

    attr_has_errors = True if  attr_error_count != 0 else False

    attr_return = {'attr_has_errors':attr_has_errors,'attr_error_count':attr_error_count, **attrs}



    return attr_return
