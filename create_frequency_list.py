import re
from collections import Counter
import logging
from typing import Iterable

from nltk.tokenize import word_tokenize

from persistence_guy import csv_write_helper  # to do: move all IO to pers guy module to make it more consistent
import config_data as cfg


def clean_string(input_string: str):
    # Replace symbols within words with a space
    cleaned_string = re.sub(r'(?<=\w)[^\w\s](?=\w)', ' ', input_string)    
    # Remove all other special symbols except spaces and tabs
    cleaned_string = re.sub(r'[^\w\s\t]', '', cleaned_string)
    cleaned_string = re.sub(r'\d+|[^\w\s\t]', '', cleaned_string)    
    return cleaned_string


def create_frequency_list(ss: Iterable[str]):
    s = ' '.join(ss)
    logging.info(f'trying to clean str, len =  {len(s)}')
    s = clean_string(s)
    s = s.lower()
    logging.info(f'len of str to tokenize is {len(s)}')
    text_tokens = [token.strip() for token in word_tokenize(s)]
    cntr = Counter(text_tokens)
    return cntr.most_common()


if __name__ == "__main__":
    create_frequency_list(cfg.INPUT_CORPUS_FILE, cfg.FREQ_LST_FILE_PATH)
    