# %% 
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')
MODEL_NAME = 'gpt-3.5-turbo'  # gpt-3.5-turbo
CHUNK_SIZE = 10  # chunk size for batch processing of words a
MAX_CNT_TRY = 3 # Max number or retry attempts in case of some failed parsing
input_words_list_file = r"data\input\top200TurkishVerbs.csv"
output_file = r'data\output\word_data.json'


