from typing import Dict

import json
from pathlib import Path




_ROOT_DIRECTORY = Path(__file__).resolve().parents[2]

_ASPECTS_JSON = _ROOT_DIRECTORY / "data" / "aspects" / "aspects.json"


def _load_aspects():
    with open(_ASPECTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def get_aspects_names() -> Dict[str, str]:
    """
    Returns the dictionary of aspects names.

    #### Returns :
    - `Dict[str, str]` : A dictionary where the keys are the aspects JSON filename and values are the aspects names.
    """
    aspects = _load_aspects()
    return aspects["aspects_names"]
