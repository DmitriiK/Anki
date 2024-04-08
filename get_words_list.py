# getting list of words and meanings  for creation of anki cards, levereging OPEN_AI (or whatever LLM)
# %% 
import os
from typing import List
from dotenv import load_dotenv
import logging


from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from output_parser_formats import WordItems
import lemmatization as lmm

load_dotenv()
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')
MODEL_NAME = 'gpt-3.5-turbo'  # gpt-3.5-turbo

# %%
input_words_list_file = r"data\input\top200TurkishVerbs.csv"
output_file = r'data\output\word_data.json'
# words_list = lmm.attach_frequencies(input_words_list, '\t')



# %%
def enrich_date_by_open_ai(words_lst: List[str]):
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=MODEL_NAME, temperature=0)

    output_parser, prompt = prepare_prompt()

    ret_lst = RequestAndParse(words_lst, llm, output_parser, prompt)
    
    # %% 
    with open(output_file, "w", encoding='UTF-8') as outfile:
        json_str = r.json(ensure_ascii=False, indent=4)
        outfile.write(json_str)

def prepare_prompt():
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

    output_parser = PydanticOutputParser(pydantic_object=WordItems)
    format_instructions = output_parser.get_format_instructions()
    # print(format_instructions)
    pr_mess = """
    We will be referring to {src_lang} as source language and {trg_lang} as target language.
    Given as an input a comma concatenated list of words in  {src_lang},  produce a JSON list,  using format below.
                {format_instructions}.
                {example}.
                Input: word: '{source_words}'.
                """

    prompt = PromptTemplate(
        template=pr_mess,
        input_variables=['source_words'],
        partial_variables={"format_instructions": format_instructions,
                           "example": example,
                           "src_lang": 'Turkish',
                           'trg_lang': 'English'},
    )
    
    return output_parser, prompt


def RequestAndParse(words_lst, llm, output_parser, prompt) -> List[WordItems]:
    chain = prompt | llm  # | output_parser
    CHUNK_SIZE, max_cnt_try = 10, 3
    chunker = (words_lst[i:i + CHUNK_SIZE] for i in range(0, len(words_lst), CHUNK_SIZE)) 
    
    ret_lst: List[WordItems] = []
    for cnt, chunk in enumerate(chunker):
        cnt += 1
        words_str = ', '.join(chunk)
        prompt_params = {'source_words': words_str}
        # print(prompt.format(source_word='konuşmak, bilmek'))
        things_done, cnt_try = False, 0
        while not things_done and cnt_try < max_cnt_try:
            cnt_try += 1
            logging.info(f'requesting llm for chunk #{cnt}   of {len(chunk)} words') 
            raw_r = chain.invoke(prompt_params) 
            parsed_r = None
            try:
                logging.info(f'trying to parse result') 
                parsed_r = output_parser.parse(raw_r.content)
                things_done = True
            except Exception as ex:
                if cnt_try < max_cnt_try:
                    raise ex                
                logging.error(f'on parsing of result from {words_str} got exception: {ex}')
        if not things_done:
            logging.error('was not able to parse result after')
        if parsed_r:
            ret_lst.extend(parsed_r.output_list)
    return ret_lst


def gather_all():
    words_lst = [row[0] for row in
                 lmm.csv_helper(input_words_list_file, '\t')]
    # words_lst = words_lst[10:20]
    enrich_date_by_open_ai(words_lst=words_lst)

   
gather_all()

# %%
