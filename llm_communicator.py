from typing import List
import logging


from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from output_parser_formats import WordItems
import config_data as cfg


class LLMCommunicator:
    def __init__(self, src_lang: str, trg_lang: str = 'English'):
        self.llm = ChatOpenAI(openai_api_key=cfg.OPENAI_API_KEY, model=cfg.MODEL_NAME, temperature=0)
        self.src_lang, self.trg_lang = src_lang, trg_lang
        self.__prepare_prompt()
        
    def enrich_date_by_open_ai(words_lst: List[str]):
        pass
        # ret_lst = request_and_parse(words_lst, llm, output_parser, prompt)
        with open(cfg.output_file, "w", encoding='UTF-8') as outfile:
            json_str = r.json(ensure_ascii=False, indent=4)
            outfile.write(json_str)

    def __prepare_prompt(self):
        example = """Example of output for turkish -> english
                    and source_words = 'olmak, etmek' : 
            [
                {
                    "source_word": "olmak",
                    "target_words": ["to be", "to become", "to happen"],
                    "source_examples": [
                        "O, çok iyi bir insan <bold>ol</bold>du.",
                        "Hava çok sıcak <bold>ol</bold>du.",
                        "Ne <bold>ol</bold>du?"
                    ],
                    "target_examples": [
                        "He <bold>was</bold> a very good person.",
                        "The weather <bold>became</bold> very hot.",
                        "What <bold>happened</bold>?"
                    ]
                },
                {
                    "source_word": "etmek",
                    "target_words": ["to do"],
                    "source_examples": ["Bugün ne <bold>et</bold>meyi planlıyorsun?" ],
                    "target_examples": [  "What do you plan to <bold>do</bold> today?"] 
                }
            ]
            """

        self.output_parser = PydanticOutputParser(pydantic_object=WordItems)
        format_instructions = self.output_parser.get_format_instructions()
        # print(format_instructions)
        pr_mess = """
        We will be referring to {src_lang} as source language and {trg_lang} as target language.
        Given as an input a comma concatenated list of words in  {src_lang},  produce a JSON list,  using format below.
                    {format_instructions}.
                    {example}.
                    Input: word: '{source_words}'.
                    """

        self.prompt = PromptTemplate(
            template=pr_mess,
            input_variables=['source_words'],
            partial_variables={"format_instructions": format_instructions,
                               "example": example,
                               "src_lang": self.src_lang,
                               'trg_lang': self.trg_lang},
        )
        self.chain = self.prompt | self.llm  # | output_parser

    def request_and_parse_by_chunks(self, words_lst: List[str]):
        CHUNK_SIZE = cfg.CHUNK_SIZE
        chunker = (words_lst[i:i + CHUNK_SIZE] for i in range(0, len(words_lst), CHUNK_SIZE))
        for cnt, chunk in enumerate(chunker):
            logging.info(f'requesting llm for chunk #{cnt}   of {len(chunk)} words') 
            yield self.request_and_parse(chunk)

    def request_and_parse(self, words_lst: List[str]) -> WordItems:
        words_str = ', '.join(words_lst)
        prompt_params = {'source_words': words_str}
        #  print(prompt.format(source_word='konuşmak, bilmek'))
        cnt_try = 0
        while cnt_try < cfg.MAX_CNT_TRY:
            cnt_try += 1
            raw_r = self.chain.invoke(prompt_params)
            logging.info(f'got request from LLM, len = {len(raw_r.content)}, trying to parse')
            parsed_r = None
            try:
                parsed_r = self.output_parser.parse(raw_r.content)
                return parsed_r
            except Exception as ex:
                logging.error(f'on parsing of result from {words_str} got exception: {ex}')
                if cnt_try >= cfg.MAX_CNT_TRY:
                    raise ex


if __name__ == "__main__":
    llmc = LLMCommunicator('Turkish', 'English')
    cfg.CHUNK_SIZE = 1
    words = ['konuşmak', 'bilmek']
    output_chunks = llmc.request_and_parse_by_chunks(words)
    for word_itm in output_chunks:
        print(word_itm)
    print('done')
