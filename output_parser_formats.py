from typing import List, Optional
from langchain_core.pydantic_v1 import BaseModel, Field


class WordItem(BaseModel):
    source_word: str = Field(description="initial word from source language")
    source_word_pos: str = Field(description="""parts of speech for initial word from source language, like verb, noun, etc..
                                 If there maybe different parts of speech,
                                 put all of them as concatenated list though '; '.""")
    target_words: List[str] = Field(description="""translation to target language.
                    For cases, when the target word has very distinct meanings in source language, 
                    like turkish word 'çalmak' has meanings 'play' (musical instrument) and 'steal',
                    it should contain all meanings, but not more than 3.
                    But for most cases the meanings of he word are similar, like "close" and "shut" for turkish "kapatmak",
                     please take only one of them. """)

    source_examples: List[str] = Field(description="""example of usage for each of the meanings from target_words list, 
                        with different grammar forms of the word from source language,
                        as a  sentence in source language,  containing 5-10 words for each of the examples.
                        For verbs provide at least 2 examples, where at list one of them should be in positive form of
                        present tense (Şimdiki zaman for Turkish)
                        The root part of initial word should be separated in "<u>" tag. 
                        The words in examples should be from top 1000 of most frequent words in source language.
                        It would be also great if phrases from examples are from pieces of poetry (but not necessary)
                        """)

    target_examples: List[str] = Field(description="""Translations to target language for each of the above examples.
                   The translated word should be separated in <u> tag.""")
    freq: Optional[int] = Field(description='frequency index of word, not supposed to be used by llm')
    freq_rank: Optional[int] = Field(description='frequency rank of word in the input list, not supposed to be used by llm')


class WordItems(BaseModel):
    output_list: List[WordItem] = Field(description='list of word items for each word in the input list of words')