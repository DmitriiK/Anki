from modules.pipelines import (create_frequency_list_io,
                               lemmatize_frequency_list_io, 
                               group_by_lemma_io,
                               request_and_parse_by_chunks_io,
                               generate_audio_batch_from_file)
import config_data as cfg

if __name__ == "__main__":
    # create_frequency_list_io(cfg.INPUT_CORPUS_FILE, cfg.FREQ_LST_FILE_PATH+'.test', 'text')
    # lemmatize_frequency_list_io(cfg.FREQ_LST_FILE_PATH, cfg.FREQ_LST_LM_FILE_PATH)()
    # group_by_lemma_io(ifp=cfg.FREQ_LST_LM_FILE_PATH, ofp=cfg.FREQ_LST_GR_FILE_PATH)()
    # attach_frequencies_io(cfg.INPUT_WORDS_LIST_FILE, cfg.FREQ_LST_GR_FILE_PATH, cfg.WORDS_AND_FREQ_LIST_FILE)()
     # request_and_parse_by_chunks_io(inp=cfg.WORDS_AND_FREQ_LIST_FILE)()
    generate_audio_batch_from_file(cfg.OUTPUT_FILE_NAME, cfg.DIR_AUDIO_FILES)