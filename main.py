import time
from tqdm import tqdm
from googletrans import Translator
import googletrans
from Modules.google_sheets_api import GoogleSheetsApi

import random_name_generator as rng

GOOGLE_TOKEN = 'Environment/google_token.json'
GOOGLE_DOCUMENT = '18CSD7sNaJWQ4DDOv6omd0J2jSYuT7xjlKCyAxSdz-QQ'
LIST_TO_TRANSLATE = 'translate'
PACKET_SIZE = 250
SLEEP = 500
TRANSLATE_LIMIT = 300

sheets = GoogleSheetsApi(GOOGLE_TOKEN)
translator = Translator()

data = sheets.get_data_from_sheets(GOOGLE_DOCUMENT, LIST_TO_TRANSLATE, 'A2', 'C' +
                                   str(sheets.get_list_size(GOOGLE_DOCUMENT, LIST_TO_TRANSLATE)[1]), 'ROWS')

time.sleep(SLEEP)
translated_data = []
for i, row in tqdm(enumerate(data), total=len(data)):
    if i % TRANSLATE_LIMIT == 0:
        print('Sleep')
        time.sleep(SLEEP)
    try:
        result = translator.translate(row[0], dest=row[2])
        translated_data.append(result.text)
    except:
        print('Stop in:', i)
        break

sheets = GoogleSheetsApi(GOOGLE_TOKEN)
sheets.put_column_to_sheets_packets(GOOGLE_DOCUMENT, LIST_TO_TRANSLATE, 'D', 2, translated_data, PACKET_SIZE)
