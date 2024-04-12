from pydantic import BaseModel, Field


class WordModel(BaseModel):
    word: str = Field(description="some word")
    pos: str = Field(description='part of speach, word, ets', default='')
    lemma: str = Field(description='initial form of word, lemma', default='')
    freq: int = Field(description='number of occurrences, based of some frequency list', default=None)