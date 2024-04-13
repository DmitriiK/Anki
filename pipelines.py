from typing import List, Iterable, Callable


from persistence_guy import file_input, file_output, csv_row2WordModel
from lemmatization import Lemmanatizer
from llm_communicator import LLMCommunicator

import config_data as cfg

lmm = Lemmanatizer()

# applying of IO decorators
lemmatize_frequency_list_io = (
    file_input(cfg.FREQ_LST_FILE_PATH)
    (file_output(
        cfg.FREQ_LST_LM_FILE_PATH,
        col_names=cfg.CSV_HEADER,
        flatten_func=lambda word: [word.word, word.lemma, word.pos, word.freq]
        )
     (lmm.lemmatize_frequency_list))
                                )


group_by_lemma_io = (file_input(cfg.FREQ_LST_LM_FILE_PATH,
                                row2itm_func=csv_row2WordModel)
                     (Lemmanatizer.group_by_lemma))

attach_frequencies_io = (file_input(input_file_path=cfg.INPUT_WORDS_LIST_FILE,
                                    row2itm_func=lambda row: row[0],
                                    input2_file_path=cfg.FREQ_LST_LM_FILE_PATH,
                                    row2itm_func2=csv_row2WordModel
                                    )
                         (file_output(cfg.WORDS_AND_FREQ_LIST_FILE, col_names=['word', 'freq'])
                            (lmm.attach_frequencies)))


if __name__ == "__main__":
    # lemmatize_frequency_list_io()
    # attach_frequencies(cfg.INPUT_WORDS_LIST_FILE, cfg.WORDS_AND_FREQ_LIST_FILE)
    # group_by_lemma_io()
    attach_frequencies_io()
