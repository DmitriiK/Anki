# %% 
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')
MODEL_NAME = 'gpt-3.5-turbo'  # gpt-3.5-turbo
CHUNK_SIZE = 10  # chunk size for batch processing of words a
MAX_CNT_TRY = 3 # Max number or retry attempts in case of failed parsing

INPUT_WORDS_LIST_FILE = r"data\input\top200TurkishVerbs.csv"
WORDS_AND_FREQ_LIST_FILE = r"data\output\top200TurkishVerbs_frq.csv"

output_file = r'data\output\word_data.json'

##
CSV_ENCODING = 'utf-8'
FREQ_LST_FILE_PATH = r"data\input\frequency_list.tr.csv"
FREQ_LST_LM_FILE_PATH = r"data\input\frequency_list_lemmatized.tr.txt"


