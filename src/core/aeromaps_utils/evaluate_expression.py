from typing import Dict, Optional, Any

import builtins

from pandas import DataFrame, Series

from core.aeromaps_utils.extract_processed_data import get_years, get_dataframe_vector_outputs, get_dataframe_climate_outputs




ALLOWED_YEAR_RANGES = [
    "full_years",        # List of intergers ranging from 2000 to 2050 included.
    "historic_years",    # List of intergers ranging from 2000 to 2019 included.
    "prospective_years", # List of intergers ranging from 2019 to 2050 included.
    2050                 # The last studied year.
]


def evaluate_expression_aeromaps(
        process_data: Dict[str, Any],
        equation: str,
        year_range: Optional[str | int] = None
    ) -> Series | float:
    """
    Takes a formatted equation (using AeroMAPS variables) and returns the calculated Pandas Series using the Ptython `eval` function.
    The equation is formatted the same way as Python expressions. Ony the AeroMAPS expressions are written differently (using the format `variable_type(variable_name)` where `variable_type` is either `vector_outputs` or `climate_outputs`).

    If the expression is invalid (operators back to back, inexistant AeroMaps variable, ext...), this function will raise an error.

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data, computed from an AeroMAPS process.
    - `equation (str)` : The equation to calculate.
    - `year_range (Optional[str | int])` : The series year range, described in the `_ALLOWED_YEAR_RANGES` list. Default to None.

    #### Returns :
    - `Series | float` : A pandas Series containing the calculated values for the equation, indexed by the year_range or a float if the equation is a scalar value.
    """
    # Check if the year_range is valid and extract the corresponding years :
    if year_range != None and year_range not in ALLOWED_YEAR_RANGES:
        raise ValueError(f"Invalid year range: {year_range}. Allowed values are: {ALLOWED_YEAR_RANGES} or None.")

    if year_range != None:
        if isinstance(year_range, int):
            selected_year_range = year_range
        else:
            selected_year_range = get_years(process_data)[year_range]
    else:
        selected_year_range = None

    # If no year_range is provided, check there is no call to the `vector_outputs` or `climate_outputs` functions in the equation :
    if selected_year_range is None and ("vector_outputs" in equation or "climate_outputs" in equation):
        raise ValueError("No year range provided, but the equation contains calls to `vector_outputs` or `climate_outputs`. Please provide a valid year range.")

    # Extract the vector and climate outputs dataframes :
    DF_vector_outputs: DataFrame  = get_dataframe_vector_outputs(process_data)
    DF_climate_outputs: DataFrame = get_dataframe_climate_outputs(process_data)

    # Create wrappers to access the AeroMAPS inputs and outputs :
    def float_inputs(variable_name: str) -> float:
        """
        Wrapper to access the float inputs from the process data.
        """
        if variable_name not in process_data["float_inputs"]:
            raise ValueError(f"Variable '{variable_name}' not found in float inputs.")
        return float(process_data["float_inputs"][variable_name])

    def float_outputs(variable_name: str) -> float:
        """
        Wrapper to access the float outputs from the process data.
        """
        if variable_name not in process_data["float_outputs"]:
            raise ValueError(f"Variable '{variable_name}' not found in float outputs.")
        return float(process_data["float_outputs"][variable_name])

    def vector_outputs(variable_name: str) -> Series:
        """
        Wrapper to access the vector outputs DataFrame.
        """
        if variable_name not in DF_vector_outputs.columns:
            raise ValueError(f"Variable '{variable_name}' not found in vector outputs.")
        return DF_vector_outputs.loc[selected_year_range, variable_name].astype(float)

    def climate_outputs(variable_name: str) -> Series:
        """
        Wrapper to access the climate outputs DataFrame.
        """
        if variable_name not in DF_climate_outputs.columns:
            raise ValueError(f"Variable '{variable_name}' not found in climate outputs.")
        return DF_climate_outputs.loc[selected_year_range, variable_name].astype(float)

    # Create a safe restrained environment for eval :
    safe_globals = {"__builtins__": None}
    safe_locals = {
        "max": lambda a, b: a.combine(b, builtins.max) if hasattr(a, "combine") or hasattr(b, "combine") else builtins.max(a, b), # Max function, accepting two parameters and adapted to the series.
        "min": lambda a, b: a.combine(b, builtins.min) if hasattr(a, "combine") or hasattr(b, "combine") else builtins.min(a, b), # Min function, accepting two parameters and adapted to the series.
        "float_inputs": float_inputs,
        "float_outputs": float_outputs,
        "vector_outputs": vector_outputs,
        "climate_outputs": climate_outputs
    }

    # Evaluate the expression in a safe environment :
    try:
        result = eval(equation, safe_globals, safe_locals)
    except Exception as exception:
        raise ValueError(f"Error evaluating expression '{equation}': {exception}")

    return result
