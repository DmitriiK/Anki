# getting list of words and meanings  for creation of anki cards, levereging OPEN_AI (or whatever LLM)
# %% 
import os
import csv
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import CommaSeparatedListOutputParsers

import lemmatization as lmm

load_dotenv()

OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')
MODEL_NAME = 'gpt-4'  # gpt-3.5-turbo

# %%
csv_file = r"data\input\top200TurkishVerbs.csv"
words_list = lmm.attach_frequencies(csv_file, '\t')


# %%
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=MODEL_NAME, temperature=0)
pr_mess = """Given a list of {src_lang} words below,
            assign for each of them the rank by frequency of than word in the language.
            The result should be outputed as a list ot tuples (<word>, <rank>)
            --
            {words_list}"""

prompt = PromptTemplate.from_template(pr_mess)

chain = prompt | llm
prompt_params = {"words_list": words_list[0:50],
                 "src_lang": "turkish"}

r = chain.invoke(prompt_params)

print(r)




# %%
