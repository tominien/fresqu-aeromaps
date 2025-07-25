from typing import Any, Dict, List

from src.crud.crud_multidisciplinary_bars import get_bars, get_bars_names

from src.core.aeromaps_utils.evaluate_expression import evaluate_expression_aeromaps




# Load the bars from the JSON file :
BARS                                                   = get_bars()
BARS_NAMES: List[str]                                  = get_bars_names()
BARS_BUDGET_OUTPUT_FORMULAS: List[Dict[str, str]]      = [line["output_formula_BUDGET"] for line in BARS.values()]
BARS_CONSUMPTION_OUTPUT_FORMULAS: List[Dict[str, str]] = [line["output_formula_CONSUMPTION"] for line in BARS.values()]


def get_y_consumption_bars(process_data: Dict[str, Any]) -> List[float]:
    """
    Get the y-values for the consumption bars from the process data.

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the consumption data.

    #### Returns :
    - `List[float]` : A list of floats containing the y-values for the consumption bars.
    """
    return [
        evaluate_expression_aeromaps(
            process_data,
            bar_consumption_output_formula["expression"],
            bar_consumption_output_formula["year_range"] if "year_range" in bar_consumption_output_formula.keys() else None
        )
        for bar_consumption_output_formula in BARS_CONSUMPTION_OUTPUT_FORMULAS
    ]


def get_y_budget_bars(process_data: Dict[str, Any]) -> List[float]:
    """
    Get the y-values for the budget bars from the process data.

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the budget data.

    #### Returns :
    - `List[float]` : A list of floats containing the y-values for the budget bars.
    """
    return [
        evaluate_expression_aeromaps(
            process_data,
            bar_budget_output_formula["expression"],
            bar_budget_output_formula["year_range"] if "year_range" in bar_budget_output_formula.keys() else None
        )
        for bar_budget_output_formula in BARS_BUDGET_OUTPUT_FORMULAS
    ]
