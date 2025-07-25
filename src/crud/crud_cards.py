from typing import Dict, List

from src.utils import CARDS_JSON_PATH

import json




def _load_cards(path: str = CARDS_JSON_PATH) -> Dict[str, Dict[str, str]]:
    with open(path, "r", encoding = "utf-8") as file:
        return json.load(file)


def get_cards_name(path: str = CARDS_JSON_PATH) -> List[str]:
    """
    Returns the list of cards names.

    #### Returns :
    - `list[str]` : A list of all the cards names.
    """
    cards: Dict[str, str] = _load_cards(path)
    return [card["name"] for card in cards.values()]


def get_cards_ids(path: str = CARDS_JSON_PATH) -> List[str]:
    """
    Returns the list of cards identifiers.

    #### Returns :
    - `list[str]` : A list of all the cards identifiers.
    """
    cards: Dict[str, str] = _load_cards(path)
    return [card["id"] for card in cards.values()]


def get_card_id_by_name(card_name: str, path: str = CARDS_JSON_PATH) -> str:
    """
    Returns the identifier of a card given its name.

    #### Arguments :
    - `card_name (str)` : The name of the card.

    #### Returns :
    - `str` : The identifier of the card.
    """
    cards: Dict[str, str] = _load_cards(path)

    for card in cards.values():
        if card["name"] == card_name:
            return card["id"]

    raise ValueError(f"Card with name '{card_name}' not found.")
