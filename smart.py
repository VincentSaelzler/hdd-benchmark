import json
import time




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
    #cap_str = subprocess.check_output(['lsblk', '-OJb', path]).decode()

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


	# def get_health():
	# SMART_STATUS = 'smart_status'
	# pass

	# def get_attributes():
	# # these are the specific things like unallocated sector
	# pass


	# # # run lsblk and collect output
	# # info_str = ''
	# # #info_str = subprocess.check_output(['lsblk', '-OJb', path]).decode()


	# # # run lsblk and collect output
	# # health_str = ''
	# # #info_str = subprocess.check_output(['lsblk', '-OJb', path]).decode()

	# # # .  .  .or use sample output for testing
	# # with open('input-sample/smart_health_clean.json', 'r') as sample_file:
	# # 	health_str = sample_file.read()


	# # # result dictionary
	# # # results[f'{POLLING_MINUTES}_{EXTENDED}'] =
	# # # results[f'{OFFLINE_DATA_COLLECTION}_{PASSED}'] = ata[OFFLINE_DATA_COLLECTION][STATUS][PASSED]
	# # # results[f'{SELF_TEST}_{PASSED}'] = [PASSED]


	# # # print(info_json)
	# # # print(ata)
	# # print(results)

if __name__ == '__main__':
    cap = get_capabilities()
    smart = {**cap}

    print(smart)