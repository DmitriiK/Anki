#!/usr/bin/env python3
# https://charly-lersteau.com/blog/2019-11-17-create-anki-deck-csv/

import re
import os
import json
import random
import html
from typing import List

import genanki
from dotenv import load_dotenv

import anki_deck_structure as ads
import TTS_generator as tts
# Filename of the data file
data_filename = r"data/input/lst.json"

deck_filename = "Turk2Eng.apkg"

# Title of the deck as shown in Anki
anki_deck_title = "Turk2Eng"

anki_model_name = "Turk2EngModel"
# Create the deck model
model_id = random.randrange(1 << 30, 1 << 31)
load_dotenv()

anki_model = genanki.Model(
    model_id,
    anki_model_name,
    fields=ads.fields,
    templates=ads.templates,
    css=ads.style,
) 

def extact_value(fld: str, row):
    if fld == 'my_media':
        return f'[sound:{row["source_word"]}.mp3]'
    val = row[fld]
    if isinstance(val, list):
        val = html.escape('; '.join(val))
    return val    

def make_audio():
    rows = get_card_date(anki_model.fields)
    for row in rows:
        txt = row[2].replace("; ", "___") # to separate sentences by pause
        tts.generate_audio(text = txt, file_name=row[0])

def get_card_date(fields: List) -> List[List[str]]:
    with open(data_filename, encoding='UTF8') as f:  
        data = json.load(f)
        rows = []
        for row in data:
            row_fields = [extact_value(x, row) for x in [fld['name'] for fld in fields]]
            rows.append(row_fields)
        return rows
    
def generate_deck():

    anki_notes = []
    rows = get_card_date(anki_model.fields)
    for row in rows:
        anki_note = genanki.Note(
            model=anki_model,
            fields=row,
        )
        anki_notes.append(anki_note)

    # Shuffle flashcards
    random.shuffle(anki_notes)

    anki_deck = genanki.Deck(model_id, anki_deck_title)
    anki_package = genanki.Package(anki_deck)
    anki_package.media_files = [f'{row[0]}.mp3' for row in rows]

    # Add flashcards to the deck
    for anki_note in anki_notes:
        anki_deck.add_note(anki_note)

    # Save the deck to a file
    anki_package.write_to_file(deck_filename)
    print("Created deck with {} flashcards".format(len(anki_deck.notes)))

if __name__ =="__main__":
    generate_deck()
    # make_audio()