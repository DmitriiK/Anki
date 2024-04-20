#!/usr/bin/env python3
# https://charly-lersteau.com/blog/2019-11-17-create-anki-deck-csv/


import json
import random
import html
from typing import List

import genanki
from dotenv import load_dotenv

from output_parser_formats import WordItems, WordItem
import anki_deck_structure as ads
import config_data as cfg
from persistence_guy import json_file2WordItems
# Filename of the data file
data_filename = cfg.OUTPUT_FILE_NAME

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
    fields=ads.anki_fields,
    templates=ads.templates,
    css=ads.style,
)


def extact_value(fld: str, itm: WordItem):
    if fld == 'my_media':
        return f'[sound:{itm.source_word}.mp3]'
    val = str(getattr(itm, fld))
    if isinstance(val, list):
        val = html.escape('\n'.join(val))
    return val


def get_card_date(fields: List[str]) -> List[List[str]]:
    w_itms: WordItems = json_file2WordItems(cfg.OUTPUT_FILE_NAME)
    rows = [[extact_value(fld, itm) for fld in fields]
            for itm in w_itms.output_list[20:40]]
    return rows


def generate_deck():
    anki_notes = []
    fld_names = ads.AnkiField  # [fld['name'] for fld in ads.fields]
    rows = get_card_date(fld_names)
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


if __name__ == "__main__":
    generate_deck()
    # make_audio()