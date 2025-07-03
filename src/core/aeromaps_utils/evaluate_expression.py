from typing import Dict, Any

import builtins

from pandas import DataFrame, Series

from core.aeromaps_utils.extract_processed_data import get_years, get_dataframe_vector_outputs, get_dataframe_climate_outputs




ALLOWED_YEAR_RANGES = ["full_years", "historic_years", "prospective_years"]


def evaluate_expression_aeromaps(
        process_data: Dict[str, Any],
        equation: str,
        year_range: str = "full_years"
    ) -> Series:
    """
    Takes a formatted equation (using AeroMAPS variables) and returns the calculated Pandas Series using the Ptython `eval` function.
    The equation is formatted the same way as Python expressions. Ony the AeroMAPS expressions are written differently (using the format `variable_type(variable_name)` where `variable_type` is either `vector_outputs` or `climate_outputs`).

    If the expression is invalid (operators back to back, inexistant AeroMaps variable, ext...), this function will raise an error.

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data, computed from an AeroMAPS process.
    - `equation (str)` : The equation to calculate.
    - `year_range (str)` : The series year range, described in the `_ALLOWED_YEAR_RANGES` list. Default to "full_years".

    #### Returns :
    - `Series` : A pandas Series containing the calculated values for the equation, indexed by the year_range.
    """
    # Check if the year_range is valid and extract the corresponding years :
    if year_range not in ALLOWED_YEAR_RANGES:
        raise ValueError(f"Invalid year range: {year_range}. Allowed values are: {ALLOWED_YEAR_RANGES}")
    selected_year_range = get_years(process_data)[year_range]

    # Extract the vector and climate outputs dataframes :
    DF_vector_outputs: DataFrame = get_dataframe_vector_outputs(process_data)
    DF_climate_outputs: DataFrame = get_dataframe_climate_outputs(process_data)

    # Create wrappers to access the vector and climate outputs DataFrames :
    def vector_outputs(variable_name: str) -> Series:
        """
        Wrapper to access the vector outputs DataFrame.
        """
        if variable_name not in DF_vector_outputs.columns:
            raise ValueError(f"Variable '{variable_name}' not found in vector outputs.")
        return DF_vector_outputs.loc[selected_year_range, variable_name]

    def climate_outputs(variable_name: str) -> Series:
        """
        Wrapper to access the climate outputs DataFrame.
        """
        if variable_name not in DF_climate_outputs.columns:
            raise ValueError(f"Variable '{variable_name}' not found in climate outputs.")
        return DF_climate_outputs.loc[selected_year_range, variable_name]

    # Create a safe restrained environment for eval :
    safe_globals = {"__builtins__": None}
    safe_locals = {
        "max": lambda a, b: a.combine(b, builtins.max) if hasattr(a, "combine") or hasattr(b, "combine") else builtins.max(a, b), # Max function, accepting two parameters and adapted to the series.
        "min": lambda a, b: a.combine(b, builtins.min) if hasattr(a, "combine") or hasattr(b, "combine") else builtins.min(a, b), # Min function, accepting two parameters and adapted to the series.
        "vector_outputs": vector_outputs,
        "climate_outputs": climate_outputs
    }

    # Evaluate the expression in a safe environment :
    try:
        result = eval(equation, safe_globals, safe_locals)
    except Exception as exception:
        raise ValueError(f"Error evaluating expression '{equation}': {exception}")

    # Check if the result is a Pandas Series (if not it's a scalar result and we need to convert it to a Series):
    if not isinstance(result, Series):
        result = Series([result] * len(selected_year_range), index = selected_year_range)

    return result
