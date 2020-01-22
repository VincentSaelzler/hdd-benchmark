from dev import Dev
import concurrent.futures
import logging
import threading
import time
import csv
import os
import datetime


def get_time_stamp():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone().replace(microsecond=0).isoformat()


def process_dev(dev, lock, devs_file_path, badblocks_file_path, smart_file_path):
    #NUM_TRIALS = 2

    dev_row = {'create_time': dev.create_time,
               'time_stamp': get_time_stamp(), **dev.info}
    write_row(lock, devs_file_path, dev_row)

    # trials = range(NUM_TRIALS)

    # for trial in trials:
    #     log_file_path = f'./log/{dev.create_time}-{dev.dev_name}-{trial}.log'
    #     badblocks_row = {'create_time': dev.create_time,
    #                      'time_stamp': get_time_stamp(),
    #                      'serial': dev.serial,
    #                      'trial_num': trial,
    #                      **dev.run_badblocks(log_file_path),
    #                      **dev.check_for_bad_blocks(log_file_path)}
    #     write_row(lock, badblocks_file_path, badblocks_row)

    smart_row = {'create_time': dev.create_time,
                'time_stamp': get_time_stamp(), **dev.get_smart()}
    write_row(lock, smart_file_path, smart_row)


def write_row(lock, file_path, row):
    with lock:
        # take the naive approach each time.
        # check for file existance; write header if necessary
        if not os.path.isfile(file_path):
            logging.info(f'{file_path}: Creating file with headers.')
            with open(file_path, 'w', newline='') as file:
                csv_writer = csv.DictWriter(
                    file, fieldnames=row.keys(), dialect='excel')
                csv_writer.writeheader()

        with open(file_path, 'a', newline='') as file:
            csv_writer = csv.DictWriter(
                file, fieldnames=row.keys(), dialect='excel')
            csv_writer.writerow(row)


if __name__ == '__main__':
    # make more specific if running multiple tests, on multiple machines, etc.
    TEST_DESC = 'Testing disks.'
    FORM_FACTOR = 'Unknown'

    # log and lock
    format = '%(asctime)s: %(message)s'
    logging.basicConfig(format=format, level=logging.INFO, datefmt='%H:%M:%S')
    # logging.getLogger().setLevel(logging.DEBUG)
    lock = threading.Lock()
    now_unix = int(time.time())
    devs_file_path = f'./output/devs.csv'
    badblocks_file_path = f'./output/badblocks.csv'
    test_file_path = f'./output/test.csv'
    smart_file_path = f'./output/smart.csv'

    assert not os.path.exists(
        devs_file_path), f'An output file already exists. Delete before proceeding: {devs_file_path}'
    assert not os.path.exists(
        badblocks_file_path), f'An output file already exists. Delete before proceeding: {badblocks_file_path}'
    assert not os.path.exists(
        test_file_path), f'An output file already exists. Delete before proceeding: {test_file_path}'
    assert not os.path.exists(
        smart_file_path), f'An output file already exists. Delete before proceeding: {smart_file_path}'

    # write test description row
    write_row(lock, test_file_path, {'create_time': now_unix,
                                     'time_stamp': get_time_stamp(),
                                     'test_desc': TEST_DESC,
                                     'form_factor': FORM_FACTOR})

    # devices
    dev_letters = ['b', 'c', 'd']
    devs = [Dev('sd' + dl, now_unix) for dl in dev_letters]

    # run serially to help with debugging
    # for dev in devs:
    #     process_dev(dev, lock, devs_file_path, badblocks_file_path, smart_file_path)

    # run in parallel for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(devs)) as executor:
        for dev in devs:
            logging.info(f'Before {dev.dev_name}')
            executor.submit(process_dev, dev, lock,
                            devs_file_path, badblocks_file_path, smart_file_path)
            logging.info(f'After  {dev.dev_name}')
