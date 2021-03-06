import json
import time
import subprocess
import re
import util


def get_all(dev_path):
    cap = get_capabilities(dev_path)
    health = get_health(dev_path)
    attr = get_attributes(dev_path)
    smart = {**cap, **health, **attr}
    return smart


def get_capabilities(dev_path):
    POLL_FREQ = 60 if  util.is_prod() else 2
    ATA_SMART_DATA = 'ata_smart_data'
    OFFLINE_DATA_COLLECTION = 'offline_data_collection'
    SELF_TEST = 'self_test'
    STATUS = 'status'
    POLLING_MINUTES = 'polling_minutes'
    EXTENDED = 'extended'
    STRING = 'string'

    #break this out because it needs to be refreshed each POLL_FREQ
    def get_ata_cap(dev_path):
        # either get the real output, or use a sample file
        cap_str = ''
        if util.is_prod():
            cap_str = subprocess.check_output(
                ['smartctl', '-jc', dev_path]).decode()
        else:
            with open('input-sample/smart_during_test_clean.json', 'r') as sample_file:
                cap_str = sample_file.read()

        # parse output to dictionary
        info_json = json.loads(cap_str)
        ata = info_json[ATA_SMART_DATA]

        return ata

    # determine how long the extended test should take to run
    polling_minutes = get_ata_cap(dev_path)[SELF_TEST][POLLING_MINUTES][EXTENDED]

    # wait for the extended self test to complete
    elapsed = 0
    self_test_status = ''
    while True:
        time.sleep(POLL_FREQ)
        elapsed += POLL_FREQ
        self_test_status = get_ata_cap(dev_path)[SELF_TEST][STATUS][STRING]
        print(f'before match: {dev_path} - "{self_test_status}"')
        if re.match('in progress', self_test_status):
            print(f'in match: {dev_path}')
            print(
                f'Waiting for {dev_path} extended test to complete. {elapsed / 60}m of estimated {polling_minutes}m')
        else:
            print(f'about to break: {dev_path}')
            break
        print(f'post break: {dev_path}')

    # wait for the offline collection to complete (unlikely but I'm not sure how this test works.)
    elapsed = 0
    offline_collection_status = ''
    while True:
        time.sleep(POLL_FREQ)
        elapsed += POLL_FREQ
        offline_collection_status = get_ata_cap(dev_path)[OFFLINE_DATA_COLLECTION][STATUS][STRING]
        if re.match('in progress', offline_collection_status):
            print(
                f'Waiting for {dev_path} offline collection to complete. {elapsed / 60}m of unknown minutes.')
        else:
            break

    # collect results
    cap = {
        'polling_minutes': polling_minutes,
        'self_test_status': self_test_status,
        'offline_collection_status': offline_collection_status,
    }

    return cap


def get_health(dev_path):
    SMART_STATUS = 'smart_status'
    PASSED = 'passed'

    # either get the real output, or use a sample file
    health_str = ''
    if util.is_prod():
        health_str = subprocess.check_output(
            ['smartctl', '-jH', dev_path]).decode()
    else:
        with open('input-sample/smart_health_dirty.json', 'r') as sample_file:  # /smart_health_dirty.json
            health_str = sample_file.read()

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
    if util.is_prod():
        attr_str = subprocess.check_output(
            ['smartctl', '-jA', dev_path]).decode()
    else:
        with open('input-sample/smart_attributes.json', 'r') as sample_file:
            attr_str = sample_file.read()

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

    attr_has_errors = True if attr_error_count != 0 else False

    # originally was trying to return the actual attrs.
    # turned out not to work very well because some SSDs don't have any of these attributes.
    # ended up stumbling into the ideal strat! if there is an attr, count it. If not, doesn't matter.
    attr_return = {'attr_has_errors': attr_has_errors,
                   'attr_error_count': attr_error_count}

    return attr_return


def run_test(dev_path):
    if util.is_prod():
        subprocess.run(['smartctl', '-t', 'long', dev_path])
    else:
        pass
