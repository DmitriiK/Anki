from typing import Dict
import csv
from collections import defaultdict
import zeyrek

CSV_ENCODING = 'utf-8'
freq_lst_file_path = r"data\input\frequency_list.tr.csv"
freq_lst_lm_file_path = r"data\input\frequency_list_lemmatized.tr.txt"

_ma = zeyrek.MorphAnalyzer()


def _csv_helper(file_path: str, delimeter=','):
    with open(file_path, mode='r', encoding=CSV_ENCODING) as file:
        csv_reader = csv.reader(file, delimiter=delimeter, )
        # next(csv_reader)  # to skip columns names
        for row in csv_reader:
            yield row


def get_lemma(word: str) -> str:
    x = _ma.lemmatize(word)
    return x[0][1][0]


def lemmatize_frequency_list():
    csv_h = _csv_helper(freq_lst_file_path)
    new_rows = []
    for row in csv_h:
        if not new_rows:
            new_row = [row[0], row[1], 'pos', 'freq']  # columns
        else:
            word, freq = row[0], int(row[1])
            aa = _ma.analyze(word)[0]  # analyzer.lemmatize('bilmiyorum')
            lemma,  pos = ('', '') if not aa else (aa[0].lemma,  aa[0].pos)
            new_row = [word, lemma, pos, freq]
        new_rows.append(new_row)
    #  writing down the output to another csv_file
    with open(freq_lst_lm_file_path, 'w', encoding=CSV_ENCODING, newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(new_rows)


def group_by_lemma(part_of_speach: str = None) -> Dict:
    """
    reads frequency list and returns it grouped by lemmas
    Args:
        part_of_speach (str, optional): for filtering. Noun, Verb, Adj,... Defaults to None.
    Returns:
        Dictionary, lemma as key, frequency (number of occurrences in corps) as value
    """
    csv_h = _csv_helper(freq_lst_lm_file_path)
    grouped = defaultdict(int)
    is_header = True
    for row in csv_h:
        if is_header:
            is_header = False
            continue
        if row:
            lemma, pos, freq = row[1], row[2], int(row[3])
            if part_of_speach and part_of_speach != pos:
                continue
            grouped[lemma] += freq
    return dict(grouped)


def attach_frequencies(words_list_file: str, delimeter=','):
    words_list = []
    lemmas_freq = group_by_lemma()
    csvh = _csv_helper(words_list_file, delimeter)
    for row in csvh:
        word = row[0]
        x = _ma.lemmatize(word)
        lemma = x[0][1][0]     
        lemma = get_lemma(word) or word
        freq = lemmas_freq.get(lemma, 1)
        words_list.append((word, freq))
    words_list = sorted(words_list, key=lambda x: x[1], reverse=True)
    return words_list

if __name__ == "__main__":
    ret =  group_by_lemma('Verb')
    print('done')

