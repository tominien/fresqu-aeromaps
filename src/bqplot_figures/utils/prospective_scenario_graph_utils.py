from typing import Any, Dict, List, Tuple

from pandas import Series

from crud.crud_prospective_scenario_aspects import get_aspects, get_aspects_names

from core.aeromaps_utils.evaluate_expression import evaluate_expression_aeromaps

from utils import PROSPECTIVE_SCENARIO_ASPECTS_LINES_JSON_PATH, get_first_positive_minimal_distance




# Load the lines (historic, no aspect and all aspect) from the JSON file :
LINES                                       = get_aspects(PROSPECTIVE_SCENARIO_ASPECTS_LINES_JSON_PATH)
LINES_NAMES: List[str]                      = get_aspects_names(PROSPECTIVE_SCENARIO_ASPECTS_LINES_JSON_PATH)
LINES_OUTPUT_FORMULAS: List[Dict[str, str]] = [line["output_formula"] for line in LINES.values()]

# Load the aspects from the JSON file :
ASPECTS                                       = get_aspects()
ASPECTS_NAMES: List[str]                      = get_aspects_names()
ASPECTS_OUTPUT_FORMULAS: List[Dict[str, str]] = [aspect["output_formula"] for aspect in ASPECTS.values()]
NUMBER_OF_ASPECTS: int                       = len(ASPECTS)

# Initialize default colors for the lines :
DEFAULT_LINES_COLORS: List[str] = ["#8c564b", "#000000", "#d62728"]


def get_y_historic_line(process_data: Dict[str, Any]) -> Series:
    """
    Get the y-values of the historic line from the process data.

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the historic line data.

    #### Returns :
    - `Series` : The y-values of the historic line.
    """
    return evaluate_expression_aeromaps(
        process_data,
        *LINES_OUTPUT_FORMULAS[0].values()
    )


def get_y_no_aspect_line(process_data: Dict[str, Any]) -> Series:
    """
    Get the y-values of the no aspect line from the process data.

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the no aspect line data.

    #### Returns :
    - `Series` : The y-values of the no aspect line.
    """
    return evaluate_expression_aeromaps(
        process_data,
        *LINES_OUTPUT_FORMULAS[1].values()
    )


def get_y_all_aspects_line(process_data: Dict[str, Any]) -> Series:
    """
    Get the y-values of the all aspects line from the process data.

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the all aspects line data.

    #### Returns :
    - `Series` : The y-values of the all aspects line.
    """
    return evaluate_expression_aeromaps(
        process_data,
        *LINES_OUTPUT_FORMULAS[2].values()
    )


def get_y_prospective_lines(process_data: Dict[str, Any]) -> List[Series]:
    """
    Get the y-values of the prospective lines from the process data.

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the prospective lines data.

    #### Returns :
    - `List[Series]` : A list of two series containing the y-values of the prospective lines (no aspects and all aspects considered).
    """
    return [
        get_y_no_aspect_line(process_data),
        get_y_all_aspects_line(process_data)
    ]


def get_y_aspects_areas(process_data: Dict[str, Any]) -> List[Series]:
    """
    Get the y-values of the aspects areas from the process data.

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the aspects areas data.

    #### Returns :
    - `List[Series]` : A list containing the y-values of the aspects areas.
    """
    return [
        evaluate_expression_aeromaps(process_data, *aspect_output_formula.values())
        for aspect_output_formula in ASPECTS_OUTPUT_FORMULAS
    ] + [
        evaluate_expression_aeromaps(process_data, LINES_OUTPUT_FORMULAS[2]["expression"], "full_years") # Add the "all aspects" line to the aspects areas, allowing to fill the bottom area of the graph (to plot `n` y-areas, you need `n + 1` lines).
    ]


def get_y_prospective_lines_groups_comparison(
        reference_process_data: Dict[str, Any],
        groups_process_data: List[Dict[str, Any]]
    ) -> Tuple[List[Series], List[str]]:
    """
    Get the y-values of the prospective lines for group comparison from the process data.

    #### Arguments :
    - `reference_process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the prospective lines data from a reference scenario.
    - `groups_process_data (List[Series])` : A list of all of the process data for each group scenario.

    #### Returns :
    - `List[Series]` : A list containing the y-values of the prospective lines for :
        - The reference scenario (no aspect and all aspects lines).
        - The group scenarios (no aspect line for each group).
    - `List[str]` : A list of labels corresponding to each prospective line.
    """
    # Get the y-values of the prospective lines for the reference scenario :
    reference_lines = get_y_prospective_lines(reference_process_data)

    # Get the y-values of the prospective lines for each group scenario :
    all_groups_lines = [
        get_y_all_aspects_line(group_process_data)
        for group_process_data in groups_process_data
    ]

    """
    Lines :
    """
    # Merge the groups lines following the exact same values :
    groups_lines: List[Series]  = []
    groups_ids: List[List[int]] = []
    for index_line, group_line in enumerate(all_groups_lines):
        # Check if the line already exists in the list :
        for index_unique_line, group_unique_line in enumerate(groups_lines):
            if group_line.equals(group_unique_line):
                groups_ids[index_unique_line].append(index_line + 1)
                break
        else:
            groups_lines.append(group_line)
            groups_ids.append([index_line + 1])

    """
    Labels :
    """
    # Create the labels for the reference scenario lines :
    reference_labels = [
        f"{LINES_NAMES[1]} (Scénario de référence)",
        f"Émissions restantes en n'appliquant aucune carte (Scénario de référence)"
    ]

    # Create the labels for the groups lines :
    groups_labels: List[str] = []
    for group_line, group_ids in zip(groups_lines, groups_ids):
        # Application of the label depending on the number of groups :
        if len(group_ids) == 1:
            groups_labels.append(f"Scénario du groupe {group_ids[0]}")
        else:
            remaining_groups = ", ".join(str(index) for index in group_ids[:-1])
            groups_labels.append(f"Scénario des groupes {remaining_groups} et {group_ids[-1]}")

        # Add a suffix to the label if it is the same line as the reference scenario :
        if group_line.equals(reference_lines[1]):
            groups_labels[-1] += " (Identique au scénario de référence)"

    """
    Return the values :
    """
    return (
        reference_lines + groups_lines,
        reference_labels + groups_labels
    )


def get_y_prospective_labels_groups_comparison(
        prospective_lines: List[Series],
        minimal_distance: float = 100
    ) -> Tuple[List[float], List[str]]:
    """
    Get the y-values and end values of the prospective labels for group comparison from the prospective lines.

    #### Arguments :
    - `prospective_lines (List[Series])` : A list of Series objects representing the y-values of the prospective lines.
    - `minimal_distance (float)` : The minimal distance between the end values of the prospective labels to display them. If the distance is less than or equal to this value, the end values will not be displayed.

    #### Returns :
    - `List[float]` : A list containing the y-values of the prospective labels.
    - `List[str]` : A list of end values corresponding to each prospective label.
    """
    # Get the y-values of the prospective labels :
    prospective_labels_y_values: List[float] = [
        prospective_line.iloc[-1] for prospective_line in prospective_lines
    ]

    # Get the prospective labels (if the end values are too close to each other, return "" instead of the formatted end values) :
    first_positive_minimal_distance = get_first_positive_minimal_distance(prospective_labels_y_values)
    if 0 < first_positive_minimal_distance <= minimal_distance:
        prospective_labels_end_values = [""] * len(prospective_labels_y_values)
    else:
        prospective_labels_end_values = [
            format_final_value(value)
            for value in prospective_labels_y_values
        ]

    return prospective_labels_y_values, prospective_labels_end_values


def format_final_value(value: float) -> str:
    """
    Format the final value of a prospective line.

    Converts the value to a string with 'Mt CO₂' suffix and formats it as an integer.

    #### Arguments :
    - `value (float)` : The value to format.

    #### Returns :
    - `str` : The formatted string.
    """
    return f"{str(int(value))} Mt CO₂"
