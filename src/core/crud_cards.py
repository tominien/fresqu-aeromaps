CARDS = [
    "[NI] Allouer un budget carbone",
    "[NI] Réglementation et mesures économiques",
    "Sobriété",
    "Compensation des émissions",
    "Nouveaux vecteurs énergétiques",
    "Report modal",
    "Efficacité des opérations",
    "Technologie"
] # A la fin, chaque carte devra être stockée dans une DB Sqlite3, contenant en plus du nom les différentes actions qu'elle réalise sur CHAQUE paramètre d'AéroMaps.






def get_cards() -> list[str]: # A la fin, cette fonction devra être remplacée par une requête SQL sur la table des cartes.
    """
    Returns the list of cards.

    #### Returns :
    - `list[str]` : The list of cards.
    """
    return CARDS


def get_card_id(card_name: str) -> int: # A la fin, cette fonction devra être remplacée par une requête SQL sur la table des cartes.
    """
    Returns the index of the card in the CARDS list.

    #### Arguments :
    - `card_name (str)` : The name of the card.

    #### Returns :
    - `int` : The index of the card in the CARDS list.
    """
    try:
        return CARDS.index(card_name)
    except ValueError:
        raise ValueError(f"Card '{card_name}' not found in CARDS list.")
