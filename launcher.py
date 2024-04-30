
import argparse

from modules.pipelines import (create_frequency_list_io,
                               lemmatize_frequency_list_io,
                               attach_frequencies_io,
                               group_by_lemma_io,
                               request_and_parse_by_chunks_io,
                               generate_audio_batch_from_file)
import config_data as cfg

parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-cfl", "--create_frequency_list_io", help="run create_frequency_list_io", action='store_true')
parser.add_argument("-lfl", "--lemmatize_frequency_list_io", help="run lemmatize_frequency_list_io", action='store_true')
parser.add_argument("-afl", "--attach_frequencies_io", help="run attach_frequencies_io", action='store_true')
parser.add_argument("-llm", "--llm_request", help="run request llm and_parse_by_chunks_io", action='store_true')
parser.add_argument("-gab", "--generate_audio_batch_from_file", help="run generate_audio_batch_from_file",
                    action='store_true')

args = parser.parse_args()

# python launcher.py --create_frequency_list_io
if args.create_frequency_list_io:
    create_frequency_list_io(cfg.INPUT_CORPUS_FILE, cfg.FREQ_LST_FILE_PATH+'.test', 'text')

if args.lemmatize_frequency_list_io:
    lemmatize_frequency_list_io(cfg.FREQ_LST_FILE_PATH, cfg.FREQ_LST_LM_FILE_PATH)()

if args.lemmatize_frequency_list_io:
    group_by_lemma_io(ifp=cfg.FREQ_LST_LM_FILE_PATH, ofp=cfg.FREQ_LST_GR_FILE_PATH)()

if args.attach_frequencies_io:
    attach_frequencies_io(cfg.INPUT_WORDS_LIST_FILE, cfg.FREQ_LST_GR_FILE_PATH, cfg.WORDS_AND_FREQ_LIST_FILE)()

if args.llm_request:
    request_and_parse_by_chunks_io(inp=cfg.WORDS_AND_FREQ_LIST_FILE)()

if args.generate_audio_batch_from_file:
    generate_audio_batch_from_file(cfg.OUTPUT_FILE_NAME, cfg.DIR_AUDIO_FILES)
else:
    print('default execution..add something you need')
