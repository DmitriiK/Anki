# Python modules for creation of custom dictionaries for learning of foreign languages and Anki decks

## Objectives:
 - Given a list of of  words or some text in specific language (let's call it 'Source language'), prepare materials for memorization of meanings of input words in 'Target' language, including examples of usages and media-files for these examples of usages. Final output is Anki decks.
 
## What technologies are being used?
-  Python morphological Analyzer and Lemmatizer for Turkish language for lemmatization and frequency analysis : [zeyrek](https://github.com/obulat/zeyrek)
- Open AI for translation and for preparation of usage examples: [OpenAI](https://openai.com/blog/openai-api)
- Langchain for formatting of input prompts and output for LLM-s: [https://www.langchain.com/](https://www.langchain.com/)
- Microsoft Azure Text-To-Speech API [MS Azure Text-to-Speech](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/index-text-to-speech)
- genanki: A Library for Generating Anki Decks: [genakli](https://github.com/kerrickstaley/genanki)
- Anki applications (mobile, desktop and Web) [Anki](https://apps.ankiweb.net/)


## Data sources:
- [Wiktionary:Frequency lists/40K Turkish Subtitles](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/40K_Turkish_Subtitles)
    Ready frequency list, not full enough, for some reason I was not able to find words 'nar' and 'cami'
- [Kaggle Turkish Wikipedia Dataset](https://www.kaggle.com/datasets/osmankagankurnaz/turkish-wikipedia-dataset?resource=download)
    Huge parquet file with Wikipedia articles, that I have been used as corpus to create own frequency list. Frequency and frequency rank in Anki cards are based on this text, thus it can be significantly different from usual speaking language.
- [Yeni İstanbul Uluslararası Öğrenciler İçin Türkçe A1](https://akdemyayinlari.com/urun/yeni-istanbul-uluslararasi-ogrenciler-icin-turkce-a1/)
    Turkish language, A1, - to create input list of words to study.


## Currently the secuqunce of executions for pipeline looks like this:
 - *create_frequency_list(cfg.INPUT_CORPUS_FILE, cfg.FREQ_LST_FILE_PATH)*:
      reading of corpus texts and creation of frequency list
- *lemmatize_frequency_list_io(cfg.FREQ_LST_FILE_PATH, cfg.FREQ_LST_LM_FILE_PATH)()*: 
       lemmatization of the word from frequency list
- *group_by_lemma_io(ifp=cfg.FREQ_LST_LM_FILE_PATH, ofp=cfg.FREQ_LST_GR_FILE_PATH)()* :
    grouping by lemma (main grammar form)
- *attach_frequencies_io(cfg.INPUT_WORDS_LIST_FILE, cfg.FREQ_LST_GR_FILE_PATH, cfg.WORDS_AND_FREQ_LIST_FILE)()* :
    join of frequency list to input list of words
- *request_and_parse_by_chunks_io(inp=cfg.WORDS_AND_FREQ_LIST_FILE, outp = )()* :
    calling to Open AI in order to translate the list of words and to prepare examples of usage
- *generate_audio_batch_from_file(cfg.OUTPUT_FILE_NAME, cfg.DIR_AUDIO_FILES)* :
    calling to Text-To-Speech API on order to produce .mp3 files for the examples of usage from the previous steps
- *create-anki-deck.generate_deck()*:
    creation of anki deck to study translations of words and examples of usage. 
    Note: in order to leverage this for creation of Anki decks with multimedia they should be in the same directory, where main python file been launched..

Root executor for the sequence above is [launcher](./launcher.py) module.  
Module [persistence_guy](./modules/persistence_guy.py) contains decorators with functions to input output data from/to files.
Module [pipelines](./modules/pipelines.py) chains decorators from module above and main functions together.

## [Resulting Anki decks](https://github.com/DmitriiK/Anki/tree/main/data/output/anki)
- [Resulting Anki deck file for A1 book (to English)](https://raw.githubusercontent.com/DmitriiK/Anki/main/data/output/anki/TurkishTop200Verbs-to-Eng.apkg)
- [top200 Turkish words (to English)](https://raw.githubusercontent.com/DmitriiK/Anki/main/data/output/anki/TurkishTop200Verbs-to-Eng.apkg)
  
Anki decks contain: 
- words in some, let's say, source language, (for my case it is Turkish),
- it's translations to target language( English)
- the examples of usage of these words in both languages (underlined root part of word for source language and the whole word for target)
- sound multimedia for the examples in source language
- frequencies metrics for these words by some corpus of texts.  
You can easily configure the code to make similar decks for whatever pair of languages.
You can use Anki decks in desktop, mobile, or web application. 
![image](https://github.com/DmitriiK/Anki/assets/20965831/f1aad0f3-e126-45a0-afde-99017df17a2f)

 
