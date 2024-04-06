# getting list of words and meanings  for creation of anki cards, levereging OPEN_AI (or whatever LLM)
# %% 
import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from output_parser_formats import WordItems
# import lemmatization as lmm

load_dotenv()

OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')
MODEL_NAME = 'gpt-3.5-turbo'  # gpt-3.5-turbo

# %%
csv_file = r"data\input\top200TurkishVerbs.csv"
# words_list = lmm.attach_frequencies(csv_file, '\t')

# %%
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=MODEL_NAME, temperature=0)

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

chain = prompt | llm | output_parser
prompt_params = {'source_words': 'konuşmak, bilmek'}
# print(prompt.format(source_word='konuşmak, bilmek'))
r = chain.invoke(prompt_params)

print(r)




# %%
