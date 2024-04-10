from typing import List
import logging
import csv

from models import WordModel
from  lemmatization import Lemmanatizer
from  llm_communicator import LLMCommunicator

import config_data as cfg


def csv_helper(file_path: str, delimeter=','):
    with open(file_path, mode='r', encoding=cfg.CSV_ENCODING) as file:
        csv_reader = csv.reader(file, delimiter=delimeter, )
        # next(csv_reader)  # to skip columns names
        for row in csv_reader:
            yield row
 
          
def csv_write_helper(rows: List[List[str]], dest_file_path: str):
    #  writing down the output to another csv_file
    with open(dest_file_path, 'w', encoding=cfg.CSV_ENCODING, newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)


def write_word_model_to_csv(words: List[WordModel], dest_file_path: str):
    rows = [['word', 'lemma', 'pos', 'freq']]  # column names
    new_rows = [[word.word, word.lemma, word.pos, word.freq] for word in words]
    rows.extend(new_rows)
    csv_write_helper(rows, dest_file_path)


def lemmatize_frequency_list(input_file_path: str, dest_file_path: str):
    csv_h = csv_helper(input_file_path)
    rows = [row for row in csv_h]
    lmm = Lemmanatizer()
    lst = lmm.lemmatize_frequency_list(rows[1:])  # skipping header
    write_word_model_to_csv(lst, dest_file_path)
    logging.info(f'{len(lst)} rows have been written to {dest_file_path}')


def attach_frequencies(input_file_path: str, dest_file_path: str):
    csv_h = csv_helper(input_file_path)
    words = [row[0] for row in csv_h]
    lmm = Lemmanatizer()
    rows = lmm.attach_frequencies(words[1:])
    csv_write_helper(rows, dest_file_path)


if __name__ == "__main__":
    # lemmatize_frequency_list(cfg.FREQ_LST_FILE_PATH, cfg.FREQ_LST_LM_FILE_PATH)
    attach_frequencies(cfg.INPUT_WORDS_LIST_FILE, cfg.WORDS_AND_FREQ_LIST_FILE)
