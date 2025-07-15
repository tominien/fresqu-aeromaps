from typing import Any, Dict, List

from utils import MULTIDISCIPLINARY_BARS_JSON_PATH

import json




def _load_bars(path: str = MULTIDISCIPLINARY_BARS_JSON_PATH) -> Dict[str, Dict[str, Any]]:
    with open(path, "r", encoding = "utf-8") as file:
        return json.load(file)


def get_bars(path: str = MULTIDISCIPLINARY_BARS_JSON_PATH) -> Dict[str, Dict[str, Any]]:
    """
    Returns the dictionary of bars.

    #### Returns :
    - `Dict[str, Dict[str, Any]]` : A dictionary where each key / element is an bar and the associated value is another dictionnary containing the bars name and outputs formulas for the budget and consumption.
    """
    bars: Dict = _load_bars(path)
    return bars


def get_bars_names(path: str = MULTIDISCIPLINARY_BARS_JSON_PATH) -> List[str]:
    """
    Returns the list of bars names.

    #### Returns :
    - `List[str]` : A list of all the bars names.
    """
    bars: Dict = _load_bars(path)
    return [bar["name"] for bar in bars.values()]
