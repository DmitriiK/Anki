# getting list of words and meanings  for creation of anki cards, levereging OPEN_AI (or whatever LLM)
# %% 
import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# import lemmatization as lmm

load_dotenv()

OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')
MODEL_NAME = 'gpt-3.5-turbo'  # gpt-3.5-turbo

# %%
csv_file = r"data\input\top200TurkishVerbs.csv"
# words_list = lmm.attach_frequencies(csv_file, '\t')

# %%
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=MODEL_NAME, temperature=0)


response_schemas = [
    ResponseSchema(name="input_word", 
                   description="initial word from source language"),
    ResponseSchema(name="target_words", 
                   description="""It's translations to {trg_lang} language. 
                    It should be list, as if  the word has rather different  meanings, 
                    it should contain all of them (but not more than 3). 
                    But if the meanings of he word are similar, like "make" and "do" for turkish "etmek", please take only one of them. """),
    ResponseSchema(name="source_examples",
                   description="""Example of usage for each of the meanings, 
                        with different grammar forms of the word from source language,
                        as a  sentence in source language,  
                        containing 4-10 words for each of the examples. 
                        The root part of initial word should be separated in "<bold>" tag. 
                        The words in examples should be from top 1000 of most frequent words in source language. """),
    ResponseSchema(name="target_examples",
                   description="""Translations to target language for each of the above examples. 
                   The translated word should be included in bold tag."""),
    ]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# The format instructions that LangChain makes. Let's look at them
format_instructions = output_parser.get_format_instructions()
# print(format_instructions)
example = """Example of output for turkish -> english: 
            {
                "input_word": "olmak",
                "target_words": ["to be",  "to happen"],
                "source_examples": [
                    "O, çok iyi bir insan oldu.",
                    "Ne oldu?"
                ],
                "target_examples": [
                    "He was a very good person.",
                    "What happened?"
                ]
            }"""

pr_mess = """Given a word in  {src_lang} language  produce result using format below.
            {format_instructions}. 
            {example}.        
            Input: word: '{source_word}'.
            """

prompt = PromptTemplate(
    template=pr_mess,
    input_variables=['source_word'],
    partial_variables={"format_instructions": format_instructions,
                       "example": example,
                       "src_lang": 'Turkish',
                       'trg_lang': 'English'},
)

chain = prompt | llm | output_parser
prompt_params = {'source_word': 'konuşmak'}
# print(prompt.format(source_word='konuşmak'))
r = chain.invoke(prompt_params)

print(r)




# %%
