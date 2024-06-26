from typing import List, Iterable, Callable
from types import GeneratorType
import logging
import csv
import pandas as pd
import json
import functools

#  from pydantic_core import from_json
from modules.data_classes.models import WordModel
from modules.data_classes.output_parser_formats import WordItems
import config_data as cfg


def json_file2WordItems(json_file_path: str) -> WordItems:
    with open(json_file_path, encoding=cfg.CSV_ENCODING) as f:
        d = json.load(f)
        ret = WordItems.validate(d)
        return ret


def csv_row2WordModel(row: List[str]) -> WordModel:
    wm = WordModel(word=row[0])
    for ind in range(1, len(row)):
        setattr(wm, cfg.CSV_HEADER[ind], row[ind])
    return wm


def read_from_parquet(inp_file: str, column: str = None):
    df = pd.read_parquet(path=inp_file, columns=[column])
    logging.info(f'read dataset {df.shape} from {inp_file}')
    return df[column]


def csv_read_helper(file_path: str, delimeter=',', skip_row0: bool = True):
    with open(file_path, mode='r', encoding=cfg.CSV_ENCODING) as file:
        csv_reader = csv.reader(file, delimiter=delimeter, )
        # next(csv_reader)  # to skip columns names
        for row in csv_reader:
            if skip_row0:
                skip_row0 = False
            else:
                yield row


def csv_write_helper(rows: List[Iterable[str]], dest_file_path: str, header: str = None):
    #  writing down the output to another csv_file
    with open(dest_file_path, 'w', encoding=cfg.CSV_ENCODING, newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if header:
            csvwriter.writerow(header)
        csvwriter.writerows(rows)


def write_iterable_to_csv(items: Iterable, dest_file_path: str,
                          col_names: List[str] = [],
                          flatten_func: Callable = None):
    rows = []
    if col_names:
        rows.append(col_names)
    if flatten_func:
        if issubclass(type(items), dict):
            new_rows = [flatten_func(itm) for itm in items.items()] 
        else:
            new_rows = [flatten_func(itm) for itm in items]
    else:
        new_rows = items
    rows.extend(new_rows)
    csv_write_helper(rows, dest_file_path)


def extract_and_transform(fp: str, fun: Callable) -> List:
    """Еxtract data from file fp and convert to list of smth..
    Args:
        fp (str): file path
        fun (Callable): Function to convert row from file to something else

    Returns:
        _type_: List of something
    """
    rows = csv_read_helper(fp)
    rows = list(rows)  # [0:10] debug
    logging.info(f'Have read {len(rows)} rows from {fp}')
    if fun:
        itms = [fun(row) for row in rows]
    else:
        itms = rows
    return itms


def file_input(input_file_path: str,
               row2itm_func: Callable = None,
               input2_file_path: str = None,
               row2itm_func2: Callable = None):
    """_summary_
    Wraps functions that takes iterable and returns another iterable 
     ,so that it reads that iterable from file 
    Args:
        input_file_path (str): Path to csv file for input data
        row2itm_func: function to convert csv row to type, than supposed to be passed as a list to main funct
    """
    def decorator_file_input(func: Callable):
        @functools.wraps(func)
        def wrapper_input(*args, **kwargs):
            fpfun = [(input_file_path, row2itm_func)]
            if input2_file_path:
                fpfun.append((input2_file_path, row2itm_func2))
            itms_itms = []
            for fp, fun in fpfun:
                itms = extract_and_transform(fp, fun)
                itms_itms.append(itms)
            # main call
            if len(itms_itms) == 1:
                return func(itms_itms[0])
            else:
                return func(itms_itms[0], itms_itms[1])
        return wrapper_input
    return decorator_file_input


def file_output_to_csv(dest_file_path: str,
                       col_names: List[str] = cfg.CSV_HEADER,
                       flatten_func: Callable = None):
    """_summary_
    Wraps functions that returns iterable,so that it  writes result to file
    Args:
        output_file_path (str): Path to resulting csv file
        col_names (str): csv header
        convert_func: function to convert itm to csv row (list of str)
    """
    def decorator_file_output(func: Callable):
        @functools.wraps(func)
        def wrapper_output(*args, **kwargs):
            # main call
            ret_items = func(*args)
            write_iterable_to_csv(items=ret_items,
                                  dest_file_path=dest_file_path,
                                  col_names=col_names,
                                  flatten_func=flatten_func)
            logging.info(f'{len(ret_items)} rows have been written to {dest_file_path}')
        return wrapper_output
    return decorator_file_output


def file_output_to_json(dest_file_path: str):
    """_summary_
    Wraps functions that returns iterable,so that it  writes result to file
    Args:
        output_file_path (str): Path to resulting json file
    """
    def decorator_file_output(func: Callable):
        @functools.wraps(func)
        def wrapper_output(*args, **kwargs):
            # main call
            ret = func(*args)
            if isinstance(ret, GeneratorType):
                xx = ret
            else:
                xx = [ret]
            for itm_to_write in xx:
                with open(dest_file_path, "w", encoding=cfg.CSV_ENCODING) as outfile:
                    json_str = itm_to_write.json(ensure_ascii=False, indent=4)
                    outfile.write(json_str)
                    logging.info(f'wrote {len(json_str)} symbols to {dest_file_path}')
        return wrapper_output
    return decorator_file_output
