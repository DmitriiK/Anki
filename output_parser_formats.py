from typing import List, Optional
from langchain_core.pydantic_v1 import BaseModel, Field


class WordItem(BaseModel):
    source_word: str = Field(description="initial word from source language")

    target_words: List[str] = Field(description="""translations to target language.
                    It should be list, as if  the word has rather different  meanings,
                    it should contain all of them (but not more than 3).
                    But if the meanings of he word are similar, like "make" and "do" for turkish "etmek",
                     please take only one of them. """)

    source_examples: List[str] = Field(description="""example of usage for each of the meanings, 
                        with different grammar forms of the word from source language,
                        as a  sentence in source language,  
                        containing 4-10 words for each of the examples.
                        The root part of initial word should be separated in "<u>" tag. 
                        The words in examples should be from top 1000 of most frequent words in source language. """)

    target_examples: List[str] = Field(description="""Translations to target language for each of the above examples.
                   The translated word should be separated in <u> tag.""")
    freq: Optional[int] = Field(description='frequency index of word, not supposed to be used by llm')


class WordItems(BaseModel):
    output_list: List[WordItem] = Field(description='list of word items for each word in the input list of words')