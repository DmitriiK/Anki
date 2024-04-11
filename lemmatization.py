from typing import Dict, List, Iterable
from collections import defaultdict
import zeyrek  # Zeyrek: Morphological Analyzer and Lemmatizer

from models import WordModel


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
        for row in freq_lst_rows:
            word, freq = row[0], int(row[1])
            aa = self.ma.analyze(word)[0]  # analyzer.lemmatize('bilmiyorum')
            lemma,  pos = ('', '') if not aa else (aa[0].lemma,  aa[0].pos)
            new_row = WordModel(word=word, lemma=lemma, pos=pos, freq=freq)
            new_rows.append(new_row)
        return new_rows

    @staticmethod
    def group_by_lemma(words_lst: Iterable[WordModel], part_of_speach: str = None) -> Dict:
        """
        reads frequency list and returns it grouped by lemmas
        Args:
            words_lst: list of words with frequency for grouping by lemma
            part_of_speach (str, optional): for filtering. Noun, Verb, Adj,... Defaults to None.
        Returns:
            Dictionary, lemma as key, frequency (number of occurrences in corps) as value
        """
        grouped = defaultdict(int)
        for row in words_lst:
            if row:
                lemma, pos, freq = row[1], row[2], int(row[3])
                if part_of_speach and part_of_speach != pos:
                    continue
                grouped[lemma] += freq
        return dict(grouped)

    def attach_frequencies(self, words_lst: Iterable[str]) -> List[List[str]]:
        lemmas_freq = Lemmanatizer.group_by_lemma()
        ret_lst = []
        for w in words_lst:
            lemma = self.get_lemma(w) or w
            freq = lemmas_freq.get(lemma, 1)
            ret_lst.append([w, freq])
        ret_lst = sorted(ret_lst, key=lambda x: x.freq, reverse=True)
        return ret_lst

