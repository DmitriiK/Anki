from typing import List, Iterable, Callable
import logging

from persistence_guy import file_input, file_output, csv_row2WordModel, json_file2WordItems
from lemmatization import Lemmanatizer
from llm_communicator import LLMCommunicator, WordItems
from TTS_generator import TTS_GEN
from utils import remove_html_tags

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

# LLM pipelines:
llmc = LLMCommunicator('Turkish', 'English')


request_and_parse_by_chunks_io = (file_input(cfg.WORDS_AND_FREQ_LIST_FILE,
                                  row2itm_func=lambda row: tuple(row[0:2]))
                                  (llmc.request_and_parse_to_json_file))


def generate_audio_batch_from_file(inp_file_path: str, out_dir_path: str):
    wis: WordItems = json_file2WordItems(inp_file_path)
    items = [(x.source_word, [remove_html_tags(se) for se in x.source_examples])
             for x in wis.output_list]  # words and examples of usages
    #  items = items[100:]  # debug
    tts = TTS_GEN(our_dir_path=out_dir_path)
    tts.generate_audio_batch(items)


if __name__ == "__main__":
    # lemmatize_frequency_list_io()
    # attach_frequencies(cfg.INPUT_WORDS_LIST_FILE, cfg.WORDS_AND_FREQ_LIST_FILE)
    # group_by_lemma_io()
    # attach_frequencies_io()
    # request_and_parse_by_chunks_io()
    generate_audio_batch_from_file(cfg.OUTPUT_FILE_NAME, cfg.DIR_AUDIO_FILES)