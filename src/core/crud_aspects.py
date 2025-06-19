ASPECTS = [
    "Allouer un budget carbone (Non implementé)",
    "Réglementation et mesures économiques (Non implementé)",
    "Sobriété",
    "Compensation des émissions",
    "Nouveaux vecteurs énergétiques",
    "Report modal",
    "Efficacité des opérations",
    "Technologie"
] # A la fin, chaque aspect devra être stocké dans une DB Sqlite3, contenant en plus du nom les différentes actions qu'il réalise sur CHAQUE paramètre d'AéroMaps.




def get_aspects() -> list[str]: # A la fin, cette fonction devra être remplacée par une requête SQL sur la table des aspects.
    """
    Returns the list of aspects.

    #### Returns :
    - `list[str]` : The list of aspects.
    """
    return ASPECTS


def get_aspect_id(aspect_name: str) -> int: # A la fin, cette fonction devra être remplacée par une requête SQL sur la table des aspects.
    """
    Returns the index of the aspect in the ASPECTS list.

    #### Arguments :
    - `aspect_name (str)` : The name of the aspect.

    #### Returns :
    - `int` : The index of the aspect in the ASPECTS list.
    """
    try:
        return ASPECTS.index(aspect_name)
    except ValueError:
        raise ValueError(f"Aspect '{aspect_name}' not found in ASPECTS list.")
