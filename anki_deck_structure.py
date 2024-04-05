
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

fields=[{"name": "source_word"}, 
        {"name": "target_words"}, 
        {"name": "source_examples"}, 
        {"name": "target_examples"},  
        {'name': 'my_media'},  ]

templates=[
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

