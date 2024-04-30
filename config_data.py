# %% 
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')
MODEL_NAME = 'gpt-3.5-turbo'  # gpt-3.5-turbo
CHUNK_SIZE = 20  # chunk size for batch processing of words a
MAX_CNT_TRY = 3  # Max number or retry attempts in case of failed parsing
CSV_HEADER = ['word', 'lemma', 'pos', 'freq']
CSV_FL_HEADER = ['word', 'freq']


#  Azure TTL
SPEECH_REGION = 'westeurope'
SPEECH_KEY = os.getenv('SPEECH_KEY')

INPUT_CORPUS_FILE = r'D:\projects\!shared_data\wiki-tr.parquet'
INPUT_WORDS_LIST_FILE = r"data\input\YENİ İSTANBUL A1.txt"
WORDS_AND_FREQ_LIST_FILE = r"data\output\YENİ İSTANBUL A1_frq.csv"

OUTPUT_FILE_NAME = r'data\output\YENİ İSTANBUL A1_llm_output.json'

##
CSV_ENCODING = 'utf-8'
FREQ_LST_FILE_PATH = r"data\input\frequency_list.tr.csv"
FREQ_LST_LM_FILE_PATH = r"data\input\frequency_list_lemmatized.tr.csv"
FREQ_LST_GR_FILE_PATH = r"data\input\frequency_list_grouped.tr.csv"
DIR_AUDIO_FILES = r'.\data\output\audio'

LIST_OF_VOICES_FILE_PATH = r'modules\tts\TTS_voices.yml'

# obsolete
ELEVEN_LABS_API_KEY = os.getenv('ELEVEN_LABS_API_KEY')
FFMPEG_PATH = r'D:\Soft\ffmpeg-2024-04-10-git-0e4dfa4709-essentials_build\bin'
