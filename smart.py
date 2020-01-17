import json
ATA_SMART_DATA = 'ata_smart_data'
OFFLINE_DATA_COLLECTION = 'offline_data_collection'
SELF_TEST = 'self_test'
STATUS = 'status'
PASSED = 'passed'
POLLING_MINUTES = 'polling_minutes'
EXTENDED = 'extended'

# run lsblk and collect output
info_str = ''
#info_str = subprocess.check_output(['lsblk', '-OJb', path]).decode()

# .  .  .or use sample output for testing
with open('input-sample/smart_before_test_clean.json', 'r') as sample_file:
	info_str = sample_file.read()

results = {}

# parse output to dictionary
info_json = json.loads(info_str)

ata = info_json[ATA_SMART_DATA]

results[f'{POLLING_MINUTES}_{EXTENDED}'] = ata[SELF_TEST][POLLING_MINUTES][EXTENDED]
results[f'{OFFLINE_DATA_COLLECTION}_{PASSED}'] = ata[OFFLINE_DATA_COLLECTION][STATUS][PASSED]
results[f'{SELF_TEST}_{PASSED}'] = ata[SELF_TEST][STATUS][PASSED]

#next up: handle key error when test is in-progress


# print(info_json)
#print(ata)
print(results)