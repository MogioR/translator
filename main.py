from googletrans import Translator
import googletrans
from Modules.google_sheets_api import GoogleSheetsApi

import random_name_generator as rng

GOOGLE_TOKEN = 'Environment/google_token.json'
GOOGLE_DOCUMENT = '18CSD7sNaJWQ4DDOv6omd0J2jSYuT7xjlKCyAxSdz-QQ'
LIST_TO_TRANSLATE = 'translate'
PACKET_SIZE = 250

sheets = GoogleSheetsApi(GOOGLE_TOKEN)
translator = Translator()

data = sheets.get_data_from_sheets(GOOGLE_DOCUMENT, LIST_TO_TRANSLATE, 'A2', 'C' +
                                   str(sheets.get_list_size(GOOGLE_DOCUMENT, LIST_TO_TRANSLATE)[1]), 'ROWS')

translated_data = []
for row in data:
    result = translator.translate(row[0], dest=row[2])
    print(result.origin, '->', result.text)
    translated_data.append(result.text)

sheets = GoogleSheetsApi(GOOGLE_TOKEN)
sheets.put_column_to_sheets_packets(GOOGLE_DOCUMENT, LIST_TO_TRANSLATE, 'D', 2, translated_data, PACKET_SIZE)
