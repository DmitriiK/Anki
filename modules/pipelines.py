from .persistence_guy import file_input, file_output_to_csv, file_output_to_json, csv_row2WordModel, json_file2WordItems
from .persistence_guy import read_from_parquet, csv_write_helper
from .NLP.create_frequency_list import create_frequency_list
from .NLP.lemmatization import Lemmanatizer, group_by_lemma
from .LLM.llm_communicator import LLMCommunicator, WordItems
from .TTS.tts_generator import TTS_GEN
from .utils import remove_html_tags

import config_data as cfg

lmm = Lemmanatizer()

# applying of IO decorators
lemmatize_frequency_list_io = (lambda ifp, ofp: file_input(input_file_path=ifp)
    (file_output_to_csv(
        dest_file_path=ofp,
        col_names=cfg.CSV_HEADER,
        flatten_func=lambda word: [word.word, word.lemma, word.pos, word.freq]
        )
     (lmm.lemmatize_frequency_list))
                                )


group_by_lemma_io = (lambda ifp,  ofp: file_input(input_file_path=ifp, row2itm_func=csv_row2WordModel) 
                         (file_output_to_csv(dest_file_path=ofp,
                                      flatten_func=lambda x: [x[0], x[1][0], x[1][1]],
                                      col_names=['word', 'freq', 'freq_rank'])
                          (group_by_lemma)))

attach_frequencies_io = (lambda ifp, ifp2, ofp: file_input(input_file_path=ifp,
                                                           row2itm_func=lambda row: row[0],
                                                           input2_file_path=ifp2,
                                                           row2itm_func2=lambda row: (row[0], row[1], row[2]))
                         (file_output_to_csv(dest_file_path=ofp, col_names=['word', 'freq', 'freq_rank'])
                          (lmm.attach_frequencies)))

# LLM pipelines:
llmc = LLMCommunicator('Turkish', 'English')


feed_list_to_llm_io = (lambda inp, outp: file_input(input_file_path=inp,
                                                    row2itm_func=lambda row: (row[0].strip(), row[1], row[2]))
                                  (file_output_to_json(dest_file_path=outp)(llmc.feed_list_to_llm)))


def generate_audio_batch_from_file(inp_file_path: str, out_dir_path: str):
    wis: WordItems = json_file2WordItems(inp_file_path)
    items = [(x.source_word, [remove_html_tags(se) for se in x.source_examples])
             for x in wis.output_list]  # words and examples of usages
    #  items = items[100:]  # debug
    voice = TTS_GEN.find_voice('tr-TR', 'female')
    tts = TTS_GEN(voice=voice, our_dir_path=out_dir_path)
    tts.generate_audio_batch(items)


def create_frequency_list_io(inp_file: str, out_file: str, column: str):
    ss = read_from_parquet(inp_file=inp_file, column=column)
    cntr = create_frequency_list(ss)
    csv_write_helper(cntr, out_file, cfg.CSV_FL_HEADER)


if __name__ == "__main__":
    # create_frequency_list_io(cfg.INPUT_CORPUS_FILE, cfg.FREQ_LST_FILE_PATH+'.test', 'text')
    # lemmatize_frequency_list_io(cfg.FREQ_LST_FILE_PATH, cfg.FREQ_LST_LM_FILE_PATH)()
    # group_by_lemma_io(ifp=cfg.FREQ_LST_LM_FILE_PATH, ofp=cfg.FREQ_LST_GR_FILE_PATH)()
    # attach_frequencies_io(cfg.INPUT_WORDS_LIST_FILE, cfg.FREQ_LST_GR_FILE_PATH, cfg.WORDS_AND_FREQ_LIST_FILE)()
    feed_list_to_llm_io(inp=cfg.WORDS_AND_FREQ_LIST_FILE)()
    # generate_audio_batch_from_file(cfg.OUTPUT_FILE_NAME, cfg.DIR_AUDIO_FILES)