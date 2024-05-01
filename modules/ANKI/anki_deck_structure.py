from enum import StrEnum, auto
style = """
.card {
    font-family: arial;
    font-size: 24px;
    text-align: left;
    color: black;
    background-color: white;
}
.source_word {
    font-size: 40;
    font-weight: bold;
}
.hd {
    color:blue;
    font-size: 30;
}
.inf {
    font-size: 15;
}
"""


class AnkiField(StrEnum):
    source_word = auto()
    target_words = auto()
    source_examples = auto()
    target_examples = auto()
    freq = auto()
    freq_rank = auto()
    my_media = auto()


anki_fields = [{'name': str(fld)} for fld in AnkiField]


templates = [
    {
        "name": "Card 1",
        "qfmt": """<div class="source_word">{{source_word}}</div>
            <hr width="100%" size="2">
            <div class="hd">Usage examples:</div>
            <div>{{source_examples}}</div>
            {{my_media}}""",

        "afmt": """{{FrontSide}}<hr id="answer">
            <div>{{target_words}}</div>
            <div class="hd">Usage examples:</div>
            <div>{{target_examples}}</div>
             <div class = "inf"> Frequency: {{freq}}.  Frequency rank: {{freq_rank}}</div>
            """,
    },
    
    {
        "name": "Card 2",
        "qfmt": '<div class="target_words">{{target_words}}</div>',
        "afmt": """{{FrontSide}}
            <hr id="answer">
            <div class="source_word">{{source_word}}</div>
            <div class="hd">Usage examples:</div>
            <div class="source_examples">{{source_examples}}</div>
             <div class = "inf"> Frequency: {{freq}}.  Frequency rank: {{freq_rank}}</div>
             {{my_media}}
            """,
    },
    ]
