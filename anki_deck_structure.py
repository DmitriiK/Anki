from enum import StrEnum, auto

style = """
.card {
 font-family: arial;
 font-size: 24px;
 text-align: center;
 color: black;
 background-color: white;
}
.source_word {
 font-size: 64px;
}
"""


class AnkiField(StrEnum):
    source_word = auto()
    target_words = auto()
    source_examples = auto()
    target_examples = auto()
    freq = auto()
    my_media = auto()


anki_fields = [{'name': str(fld)} for fld in AnkiField]


templates = [
    {
        "name": "Card 1",
        "qfmt": '<p class="source_word">{{source_word}}</p> {{my_media}}',
        "afmt": '{{FrontSide}}<hr id="answer"><p class="target_words">{{target_words}}</p><p class="source_examples">{{source_examples}}</p>',
    },
    {
        "name": "Card 2",
        "qfmt": '<p class="target_words">{{target_words}}</p>',
        "afmt": '{{FrontSide}}<hr id="answer"><p class="source_word">{{source_word}}</p><p class="source_examples">{{source_examples}}</p>',
    },
    ]
