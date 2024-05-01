# https://charly-lersteau.com/blog/2019-11-17-create-anki-deck-csv/
"""_summary_
Generates Anki deck with card to study foreign words.
Important. - Looks like multimedia file, been referenced in anki card, supposed to be in the current directory, 
where python file is executed

"""

import random
from typing import List, Tuple

import genanki

from modules.data_classes.output_parser_formats import WordItems, WordItem
from . import anki_deck_structure as ads
from ..persistence_guy import json_file2WordItems


def _extract_value(fld: str, itm: WordItem):
    if fld == ads.AnkiField.my_media:
        return f'[sound:{itm.source_word}.mp3]'
    val = getattr(itm, fld)
    if fld in [ads.AnkiField.freq, ads.AnkiField.freq_rank]:
        return str(val)
    if isinstance(val, list):
        val = '<br>'.join([f'- {itm}' for itm in val])  # html.escape(
    return val


def _get_card_date(data_file_path: str) -> List[Tuple[List[str], str]]:
    """_summary_
    returns anki deck card data
    Args:
        data_file_path (str): _description_

    Returns:
       list of tuples, first element is list of string of anki deck creation, 
       second - part of speach for tag
    """
    w_itms: WordItems = json_file2WordItems(data_file_path)
    rows = [([_extract_value(fld, itm) for fld in ads.AnkiField], itm.source_word_pos)
            for itm in w_itms.output_list]
    return rows


def generate_deck(input_file: str,
                  deck_title: str,
                  anki_model_name: str,
                  output_file: str,
                  randomize=False,
                  deck_tags: List[str] = None):
    """_summary_
    Generates anki deck
    Args:
        input_file (str): Json File with date for card creation, should fit to WordItems class format
        deck_title (str): Title of the deck as shown in Anki
        anki_model_name (str): Model, structure of a deck, can have several decks with the same model
        output_file (str): path to ouput .apkg file
    """
    model_id = random.randrange(1 << 30, 1 << 31)
    anki_model = genanki.Model(
        model_id,
        anki_model_name,
        fields=ads.anki_fields,
        templates=ads.templates,
        css=ads.style,
    )

    anki_notes, rows_and_poss = _generate_notes(input_file, anki_model, deck_tags)
    if randomize:
        random.shuffle(anki_notes)

    anki_deck = genanki.Deck(model_id, deck_title)
    anki_package = genanki.Package(anki_deck)
    anki_package.media_files = [f'{row[0][0]}.mp3' for row in rows_and_poss]

    # Add flashcards to the deck
    for anki_note in anki_notes:
        anki_deck.add_note(anki_note)

    # Save the deck to a file
    anki_package.write_to_file(output_file)
    print("Created deck with {} flashcards".format(len(anki_deck.notes)))


def _generate_notes(data_file_path, anki_model, deck_tags: List[str]):
    anki_notes = []
    rows_and_poss = _get_card_date(data_file_path)

    for row, pos in rows_and_poss:
        card_tags = deck_tags or []
        if pos:
            poss = [x.strip() for x in pos.split(',')]  # parts of speech might be comma conc. list
            card_tags.extend(poss)
        anki_note = genanki.Note(
            model=anki_model,
            fields=row,
            tags=card_tags
        )
        anki_notes.append(anki_note)
    return anki_notes, rows_and_poss


if __name__ == "__main__":
    inp_file = r'data\output\YENİ İSTANBUL A1_llm_output.json'
    generate_deck(inp_file, "Turk2Eng", "Turk2EngModel", "Turk2Eng.apkg", False, ['Turkish'])
