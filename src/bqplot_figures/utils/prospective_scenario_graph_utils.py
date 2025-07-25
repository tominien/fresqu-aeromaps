from typing import Any, Dict, List, Tuple, Optional

from pandas import Series

from src.crud.crud_prospective_scenario_aspects import get_aspects, get_aspects_names

from src.core.aeromaps_utils.evaluate_expression import evaluate_expression_aeromaps

from src.utils import PROSPECTIVE_SCENARIO_ASPECTS_LINES_JSON_PATH, get_first_positive_minimal_distance




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
    ) -> Tuple[List[Series], List[str], List[List[int]]]:
    """
    Get the y-values of the prospective lines for group comparison from the process data.

    #### Arguments :
    - `reference_process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the prospective lines data from a reference scenario.
    - `groups_process_data (List[Series])` : A list of all of the process data for each group scenario.
    - `merge_group_equal_to_reference (bool)` : Whether to merge the group of lines that are equal to the reference scenario's "all aspects" line.
        If `True`, the groups lines that are equal to the reference scenario's "all aspects" line will be merged into the "all aspects" line and label.

    #### Returns :
    - `List[Series]` : A list containing the y-values of the prospective lines for :
        - The reference scenario (no aspect and all aspects lines).
        - The group scenarios (no aspect line for each group).
    - `List[str]` : A list of labels corresponding to each prospective line.
    - `List[List[int]]` : A list of lists containing the group indices where each "group of lines" corresponds to the same line.
        Does not include a list of all the groups that are equal to the reference scenario's "all aspects" line.
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
    groups_lines: List[Series]               = []
    groups_ids_equal_to_reference: List[int] = [] # List of group indices that are equal to the reference scenario's "all aspects" line.
    groups_ids: List[List[int]]              = [] # List of lists containing the group indices where each "group of lines" corresponds to the same line.
    for index_line, group_line in enumerate(all_groups_lines):
        # Check if the line is equal to the reference scenario's "all aspects" line :
        if group_line.equals(reference_lines[1]):
            groups_ids_equal_to_reference.append(index_line + 1)
            continue
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
    labels: List[str] = []

    # Create the label for the "no_aspect" reference scenario line :
    labels.append(LINES_NAMES[1])

    # Create the label for the "all_aspects" reference scenario line :
    all_aspects_label = "Émissions restantes en n'appliquant aucune carte (Scénario de référence"
    if len(groups_ids_equal_to_reference) == 0:
        all_aspects_label += ")"
    elif len(groups_ids_equal_to_reference) == 1:
        all_aspects_label += f" et du groupe {groups_ids_equal_to_reference[0]})"
    else:
        all_aspects_label += f" et des groupes {', '.join(map(str, groups_ids_equal_to_reference[:-1]))} et {groups_ids_equal_to_reference[-1]})"

    labels.append(all_aspects_label)

    # Create the labels for the groups lines :
    for group_line, group_ids in zip(groups_lines, groups_ids):
        # Application of the label depending on the number of groups :
        if len(group_ids) == 1:
            labels.append(f"Scénario du groupe {group_ids[0]}")
        else:
            remaining_groups = ", ".join(str(index) for index in group_ids[:-1])
            labels.append(f"Scénario des groupes {remaining_groups} et {group_ids[-1]}")

        # Add a suffix to the label if it is the same line as the reference scenario :
        if group_line.equals(reference_lines[1]):
            labels[-1] += " (Identique au scénario de référence)"

    """
    Return the values :
    """
    return (
        reference_lines + groups_lines,
        labels,
        groups_ids # Does NOT includes the list of groups that are equal to the reference scenario's "all aspects" line.
    )


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


def get_y_final_values_lines(
        lines: List[Series],
        minimal_distance: float = 100
    ) -> Tuple[List[float], List[str]]:
    """
    Get the final y-values and formatted final values of each line.

    #### Arguments :
    - `lines (List[Series])` : A list of Series objects representing the y-values of the lines.
    - `minimal_distance (float)` : The minimal required distance between all final y-values of the lines to display them.
        If any two final y-values are closer than the minimal distance, no final values will not be displayed.

    #### Returns :
    - `List[float]` : A list containing the final y-values of the lines.
    - `List[str]` : A list of **string-formatted** final values for each line.
    """
    # Get the final y-values of the lines :
    final_y_values: List[float] = [
        line.iloc[-1] for line in lines
    ]

    # Get the formatted final values (if any two final values are closer than the minimal distance, don't display any final values) :
    first_positive_minimal_distance = get_first_positive_minimal_distance(final_y_values)
    if 0 < first_positive_minimal_distance <= minimal_distance:
        final_y_values_text = [""] * len(final_y_values)
    else:
        final_y_values_text = [
            format_final_value(value)
            for value in final_y_values
        ]

    return final_y_values, final_y_values_text


def format_final_values_group_comparison(
        values: List[float],
        include_group_names: bool = True,
        groups_ids: Optional[List[List[int]]] = None
    ) -> List[str]:
    """
    Format the final value of a list of values.
    This function should only be used for the ProspectiveScenarioGroupComparison graphs.

    #### Arguments :
    - `values (List[float])` : The values to format.
    - `include_group_names (bool)` : Whether to include the group names in the formatted values. If `True`, the group names will be included in the formatted values, following this logic :
        - Index 0 : Value of the "no aspect" line from the reference scenario.
        - Index 1 : Value of the "all aspects" line from the reference scenario.
        - Index k : k ∈ [2, len(values) - 1] : Value of the "no aspect" line from the group scenario k - 1, with the group name included in the formatted value.
    - `groups_ids (List[List[int]])` : A list of group indices where each "group of lines" corresponds to the same line (except for the list of groups that are equal to the reference scenario's "all aspects" line).

    #### Returns :
    - `str` : The formatted final values as a list of strings.
    """
    # Check if the groups_ids is the correct length :
    if groups_ids is not None and len(groups_ids) != len(values) - 2 : # -2 because we have the "no aspect" and "all aspects" lines from the reference scenario.
        raise ValueError("Invalid groups_ids length.")

    # Format the final values to include the 'Mt CO₂' suffix :
    final_values_CO2_suffix = [
        format_final_value(value)
        for value in values
    ]

    # Add the "Reference" / "Groups names" to the formatted final values :
    if include_group_names:
        # Label of the lines from the reference scenario :
        final_values_text = [
            final_values_CO2_suffix[0],
            f"{final_values_CO2_suffix[0]} (Référence)"
        ]

        # Label of each group of lines :
        for final_value, group_ids in zip(final_values_CO2_suffix[2:], groups_ids):
            if len(group_ids) == 1:
                final_values_text.append(
                    f"{final_value} (Groupe {group_ids[0]})"
                )
            elif len(group_ids) < 4:
                remaining_groups = ", ".join(str(index) for index in group_ids[:-1])
                final_values_text.append(
                    f"{final_value} (Groupes {remaining_groups} & {group_ids[-1]})"
                )
            else: # If there is more than 3 groups, juste display the first 2 followed by "..." :
                remaining_groups = ", ".join(str(index) for index in group_ids[:2])
                final_values_text.append(
                    f"{final_value} (Groupes {remaining_groups}, ...)"
                )
    else:
        final_values_text = final_values_CO2_suffix

    return final_values_text


def get_y_final_values_lines_group_comparison(
        lines: List[Series],
        minimal_distance: float = 100,
        include_group_names: bool = True,
        groups_ids: Optional[List[List[int]]] = None
    ) -> Tuple[List[float], List[str]]:
    """
    Get the final y-values and formatted final values of each line.
    This function should only be used for the ProspectiveScenarioGroupComparison graphs.

    #### Arguments :
    - `lines (List[Series])` : A list of Series objects representing the y-values of the lines.
    - `minimal_distance (float)` : The minimal required distance between all final y-values of the lines to display them.
        If any two final y-values are closer than the minimal distance, no final values will not be displayed.
    - `include_group_names (bool)` : Whether to include the group names in the formatted final values.
        If `True`, the group names will be included in the formatted values, following this logic :
        - Index 0 : Value of the "no aspect" line from the reference scenario.
        - Index 1 : Value of the "all aspects" line from the reference scenario.
        - Index k : k ∈ [2, len(lines) - 1] : Value of the "no aspect" line from the group scenario k - 1, with the group name included in the formatted value.
    - `groups_ids (Optional[List[List[int]]])` : A list of group indices where each "group of lines" corresponds to the same line (except for the list of groups that are equal to the reference scenario's "all aspects" line).

    #### Returns :
    - `List[float]` : A list containing the final y-values of the lines.
    - `List[str]` : A list of **string-formatted** final values for each line.
    """
    # Get the final y-values of the lines :
    final_y_values: List[float] = [
        line.iloc[-1] for line in lines
    ]

    # Get the formatted final values (if any two final values are closer than the minimal distance, don't display any final values) :
    first_positive_minimal_distance = get_first_positive_minimal_distance(final_y_values)
    if 0 < first_positive_minimal_distance <= minimal_distance:
        final_y_values_text = [""] * len(final_y_values)
    else:
        final_y_values_text = format_final_values_group_comparison(final_y_values, include_group_names, groups_ids)

    return final_y_values, final_y_values_text
