from typing import List, Iterable, Callable
import logging
import csv
import functools

from models import WordModel
from  lemmatization import Lemmanatizer
from  llm_communicator import LLMCommunicator

import config_data as cfg

# todo - make common decorator for read write to csv


def csv_helper(file_path: str, delimeter=',', skip_row0: bool = True):
    with open(file_path, mode='r', encoding=cfg.CSV_ENCODING) as file:
        csv_reader = csv.reader(file, delimiter=delimeter, )
        # next(csv_reader)  # to skip columns names
        for row in csv_reader:
            if skip_row0:
                skip_row0 = False
            else:
                yield row


def csv_write_helper(rows: List[List[str]], dest_file_path: str):
    #  writing down the output to another csv_file
    with open(dest_file_path, 'w', encoding=cfg.CSV_ENCODING, newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)


def write_iterable_to_csv(items: Iterable, dest_file_path: str,
                          col_names: List[str] = [],
                          flatten_func: Callable = None):
    rows = []
    if col_names:
        rows.append(col_names)
    if flatten_func:
        new_rows = [flatten_func(itm) for itm in items]
    else:
        new_rows = items
    rows.extend(new_rows)
    csv_write_helper(rows, dest_file_path)


def file_input_output(input_file_path: str, dest_file_path: str,
                      col_names: List[str] = cfg.CSV_HEADER,
                      flatten_func: Callable = None):
    """_summary_
    Wraps functions that takes iterable and returns another iterable 
     ,so that it reads that iterable from file and writes result to another file
    Args:
        input_file_path (str): Path to csv file for input data
        output_file_path (str): Path to resulting csv file
    """
    def decorator_file_input_output(func: Callable):
        @functools.wraps(func)
        def wrapper_input_output(*args, **kwargs):
            rows = csv_helper(input_file_path)
            # main call
            rows = list(rows)[0:10]
            ret_items = func(rows)
            write_iterable_to_csv(items=ret_items,
                                  dest_file_path=dest_file_path,
                                  col_names=col_names,
                                  flatten_func=flatten_func)
        return wrapper_input_output
    return decorator_file_input_output


lmm = Lemmanatizer()

# applying of IO decorator
lemmatize_frequency_list_io = (file_input_output(cfg.FREQ_LST_FILE_PATH,
                                                 cfg.FREQ_LST_LM_FILE_PATH,
                                                 col_names=cfg.CSV_HEADER,
                                                 flatten_func=lambda word: [word.word, word.lemma, word.pos, word.freq])
                               (lmm.lemmatize_frequency_list))


def lemmatize_frequency_list(input_file_path: str, dest_file_path: str):
    csv_h = csv_helper(input_file_path)
    rows = [row for row in csv_h]

    lst = lmm.lemmatize_frequency_list(rows[1:])  # skipping header
    # write_word_model_to_csv(lst, dest_file_path)
    logging.info(f'{len(lst)} rows have been written to {dest_file_path}')


def attach_frequencies(input_file_path: str, dest_file_path: str):
    csv_h = csv_helper(input_file_path)
    words = [row[0] for row in csv_h]
    lmm = Lemmanatizer()
    rows = lmm.attach_frequencies(words[1:])
    csv_write_helper(rows, dest_file_path)


if __name__ == "__main__":
    lemmatize_frequency_list_io()
    # attach_frequencies(cfg.INPUT_WORDS_LIST_FILE, cfg.WORDS_AND_FREQ_LIST_FILE)
