from typing import List

from pathlib import Path

import colorsys




ROOT_DIRECTORY_PATH = Path(__file__).resolve().parents[1]

CARDS_JSON_PATH = ROOT_DIRECTORY_PATH / "data" / "cards" / "cards.json"

PROSPECTIVE_SCENARIO_ASPECTS_AREAS_JSON_PATH = ROOT_DIRECTORY_PATH / "data" / "prospective_scenario_graph" / "prospective_scenario_aspects_areas.json"

PROSPECTIVE_SCENARIO_ASPECTS_LINES_JSON_PATH = ROOT_DIRECTORY_PATH / "data" / "prospective_scenario_graph" / "prospective_scenario_aspects_lines.json"

MULTIDISCIPLINARY_BARS_JSON_PATH = ROOT_DIRECTORY_PATH / "data" / "multidisciplinary_graph" / "multidisciplinary_bars.json"


def generate_pastel_palette(number_of_colors: int) -> list[str]:
    """
    Generate a pastel color palette with `number_of_colors` colors.

    #### Arguments :
    - `number_of_colors (int)` : The number of colors to generate.

    #### Returns :
    - `list[str]` : A list of pastel colors in hexadecimal format.
    """
    if number_of_colors < 1:
        return []

    # Initialize the color palette :
    palette    = []
    saturation = 0.8
    hsv_value  = 0.75

    for index in range(number_of_colors):
        hue = index / number_of_colors
        red, green, blue = colorsys.hsv_to_rgb(hue, saturation, hsv_value)
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(red * 255),
            int(green * 255),
            int(blue * 255)
        )
        palette.append(hex_color)

    return palette


def get_all_distances(values: List[float]) -> List[float]:
    """
    Returns the list of all distances between all of the values.

    #### Arguments :
    - `values (List[float])` : A list of float values.

    #### Returns :
    - `List(float)` : A list of `n * (n - 1) / 2` distances between all of the values, where `n` is the number of values. 
    """
    # If there are less than 2 values, return an empty list :
    if len(values) < 2:
        return []

    # Calculate the distances between all of the values :
    distances = []
    for index_first_value, first_value in enumerate(values):
        for second_value in values[index_first_value + 1:]:
            distances.append(abs(first_value - second_value))

    # Sort the distances :
    distances.sort()

    return distances


def get_first_positive_minimal_distance(values: List[float]) -> float:
    """
    Returns the first minimal distance greater than 0 between all of the values.

    #### Arguments :
    - `values (List[float])` : A list of float values.

    #### Returns :
    - `float` : The first minimal distance greater than 0 between all of the values or 0.0 if there are no positive distances.
    """
    # Get all of the distances (sorted) :
    all_distances = get_all_distances(values)

    # Get all of the positive distances :
    positive_distances = [distance for distance in all_distances if distance > 0]

    return min(positive_distances) if positive_distances else 0.0
