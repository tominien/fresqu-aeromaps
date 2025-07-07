from typing import Dict, List, Any

from utils import PROSPECTIVE_SCENARIO_ASPECTS_AREAS_JSON_PATH

import json




def _load_aspects(path: str = PROSPECTIVE_SCENARIO_ASPECTS_AREAS_JSON_PATH) -> Dict[str, Dict[str, Any]]:
    with open(path, "r", encoding = "utf-8") as file:
        return json.load(file)


def get_aspects(path: str = PROSPECTIVE_SCENARIO_ASPECTS_AREAS_JSON_PATH) -> Dict[str, Dict[str, Any]]:
    """
    Returns the dictionary of aspects.

    #### Returns :
    - `Dict[str, Dict[str, Any]]` : A dictionary where each key / element is an aspect and the associated value is another dictionnary containing the aspect name and output formula.
    """
    aspects: Dict = _load_aspects(path)
    return aspects


def get_aspects_names(path: str = PROSPECTIVE_SCENARIO_ASPECTS_AREAS_JSON_PATH) -> List[str]:
    """
    Returns the list of aspect names.

    #### Returns :
    - `List[str]` : A list of all the aspect names.
    """
    aspects: Dict = _load_aspects(path)
    return [aspect["name"] for aspect in aspects.values()]
