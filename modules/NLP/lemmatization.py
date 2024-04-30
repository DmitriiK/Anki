from typing import Dict, List, Iterable
from collections import defaultdict, OrderedDict
import zeyrek  # Zeyrek: Morphological Analyzer and Lemmatizer

from modules.data_classes.models import WordModel


def _attach_rank(d: Dict[str, int]):
    sdt = sorted(d.items(), key=lambda x: x[1], reverse=True)
    od = OrderedDict()
    for rank, tupl in enumerate(sdt):
        od[tupl[0]] = (tupl[1], rank+1)
    return od


def group_by_lemma(words_lst: Iterable[WordModel], attach_rank=True, part_of_speach: str = None) -> Dict:
    """
    reads frequency list and returns it grouped by lemmas
    Args:
        words_lst: list of words with frequency for grouping by lemma
        part_of_speach (str, optional): for filtering. Noun, Verb, Adj,... Defaults to None.
    Returns:
        Dictionary, lemma as key, frequency (number of occurrences in corps) as value
    """
    grouped = defaultdict(int)
    for word in words_lst:
        if part_of_speach and part_of_speach != word.pos:
            continue
        grouped[word.lemma] += int(word.freq)
    if attach_rank:
        d = _attach_rank(grouped)
    return d


class Lemmanatizer:
    def __init__(self):
        self._ma = None

    @property
    def ma(self):
        if not self._ma:
            self._ma = zeyrek.MorphAnalyzer()
        return self._ma

    def get_lemma(self, word: str) -> str:
        x = self.ma.lemmatize(word)
        return x[0][1][0]

    def lemmatize_frequency_list(self, freq_lst_rows: Iterable[List[str]]) -> List[WordModel]:
        new_rows = []
        cnt_valid = 0
        for cnt, row in enumerate(freq_lst_rows):
            if cnt_valid > 150000:
                break
            word, freq = row[0], int(row[1])
            if len(word) < 2 or freq < 10:
                continue
            aa = self.ma.analyze(word)[0]  # analyzer.lemmatize('bilmiyorum')
            lemma,  pos = ('', '') if not aa else (aa[0].lemma,  aa[0].pos)
            if lemma == 'Unk':
                continue
            new_row = WordModel(word=word, lemma=lemma, pos=pos, freq=freq)
            new_rows.append(new_row)
            cnt_valid += 1
        return new_rows

    def attach_frequencies(self, words_lst: Iterable[str],
                           freq_list: Iterable[tuple[str, int, int]]) -> List[List[str]]:
        """Mapping of frequency metrics to the list of words

        Args:
            words_lst (Iterable[str]): just list of words from some language
            freq_list (Iterable[tuple]): frequency list in that language from some corpus, format "word, freq, rank"

        Returns:
            List[List[str]]: list in format: word, frequency, frequency rank
        """
        lemmas_freq = {x[0].casefold(): (x[1], x[2]) for x in freq_list}
        ret_lst = []
        for w in set(words_lst):
            lemma = self.get_lemma(w) or w
            freq = lemmas_freq.get(lemma.casefold()) or lemmas_freq.get(w.casefold()) or (1, 0)
            ret_lst.append([w, freq[0], freq[1]])
        # ret_lst = sorted(ret_lst, key=lambda x: x[1], reverse=True)
        return ret_lst
