from typing import Dict, List, Any, Union

from pandas import DataFrame, Series


FormulaToken = Union[List[str], str]

_ALLOWED_OUTPUT_TYPES = ["vector_outputs", "climate_outputs"]

_ALLOWED_YEAR_SECTIONS = ["full_years", "historic_years", "prospective_years"]

_ALLOWED_OPERATORS = ["+", "-", "*", "/"]




def get_years(process_data: Dict[str, Any]) -> Dict[str, List[int]]:
    """
    Extract the lists of "full_years", "historic_years" and "prospective_years" from the process data (a computed data from an AeroMAPS process).

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data, computed from an AeroMAPS process, which contains the three lists of years mentioned above.

    #### Returns :
    - `Dict[str, List[int]]` : A dictionary containing the three lists of years, with respective keys of "full_years", "historic_years" and "prospective_years".
    """
    list_keys = ["full_years", "historic_years", "prospective_years"]
    years_data = {}

    for key in list_keys:
        if key not in process_data["years"]:
            raise ValueError(f"Process data does not contain the '{key}' key.")
        
        years = process_data["years"][key]
        
        if not isinstance(years, list) or not all(isinstance(year, int) for year in years):
            raise TypeError(f"'{key}' should be a list of integers. {type(years)}, {type(years[0])} found.")
        
        years_data[key] = years

    return years_data


def get_dataframe_vector_outputs(process_data: Dict[str, Any]) -> DataFrame:
    """
    Extract the vector outputs dataframe from the process data (a computed data from an AeroMAPS process).

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data, computed from an AeroMAPS process, which contains the vector outputs.

    #### Returns :
    - `Dataframe` : The Dataframe of the vector outputs.
    """
    if "vector_outputs" not in process_data:
        raise ValueError("Process data does not contain the 'vector_outputs' key.")
    
    vector_outputs = process_data["vector_outputs"]
    
    if not isinstance(vector_outputs, DataFrame):
        raise TypeError("'vector_outputs' should be a pandas DataFrame.")
    
    return vector_outputs


def get_dataframe_climate_outputs(process_data: Dict[str, Any]) -> DataFrame:
    """
    Extract the climate outputs dataframe from the process data (a computed data from an AeroMAPS process).

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data, computed from an AeroMAPS process, which contains the climate outputs.

    #### Returns :
    - `Dataframe` : The Dataframe of the climate outputs.
    """
    if "climate_outputs" not in process_data:
        raise ValueError("Process data does not contain the 'climate_outputs' key.")
    
    climate_outputs = process_data["climate_outputs"]
    
    if not isinstance(climate_outputs, DataFrame):
        raise TypeError("'climate_outputs' should be a pandas DataFrame.")
    
    return climate_outputs


def calculate_aspect_output_value(
    process_data: Dict[str, Any],
    output_formula: List[FormulaToken],
) -> Series:
    """
    Calculate the value of an aspect output based on its formula.

    `output_formula (List[FormulaToken])` is a list of tokens.
    A token can be :
    - An operator / constant if it is a string.
    - A list of strings if it is an AeroMAPS output variable, following the format `["variable_name", "variable_type", "year_section"]`.

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data, computed from an AeroMAPS process.
    - `output_formula (List[FormulaToken])` : The formula of the aspect output.

    #### Returns :
    - `Series` : A pandas Series containing the calculated values for the aspect output, indexed by the years.
    """
    # Get the dataframes from the process data :
    DF_vector_outputs: DataFrame  = get_dataframe_vector_outputs(process_data)
    DF_climate_outputs: DataFrame = get_dataframe_climate_outputs(process_data)

    # Extract the years from the process_data :
    years: Dict[str, List[int]]   = get_years(process_data)
    year_section = None

    # Check that if output_format if well formatted (a list of tokens and every AeroMAPS output variable use the same year section) :
    if not isinstance(output_formula, list):
        raise TypeError("The output formula must be a list of tokens.")

    for token in output_formula:
        if isinstance(token, list):
            if len(token) != 3 or not all(isinstance(item, str) for item in token):
                raise ValueError("Each AeroMAPS output variable in the formula must be a list of three strings: [variable_name, variable_type, year_section].")
            _, token_type, token_year = token
            if token_type not in _ALLOWED_OUTPUT_TYPES:
                raise ValueError(f"Invalid output type '{token_type}' in the formula. Expected one of {_ALLOWED_OUTPUT_TYPES}.")
            if token_year not in years:
                raise ValueError(f"Invalid year section '{token_year}' in the formula. Expected one of {list(years.keys())}.")
            if year_section is None:
                if token_year not in _ALLOWED_YEAR_SECTIONS:
                    raise ValueError(f"Invalid year section '{token_year}' in the formula. Expected one of {_ALLOWED_YEAR_SECTIONS}.")
                year_section = token_year
            elif year_section != token_year:
                raise ValueError("All AeroMAPS output variables in the formula must use the same year section.")
        elif isinstance(token, str):
            if token not in _ALLOWED_OPERATORS:
                try:
                    float(token)
                except ValueError:
                    raise ValueError(f"Invalid token '{token}' in the formula. Expected a string (operator or constant) or a list of strings (AeroMAPS output variable).")
        else:
            raise TypeError(f"Each token in the output formula must be a string or a list of strings.")

    year_section_data = years[year_section] if year_section else years["full_years"]

    # Build two lists to store the operands and operators :
    operands: List[Series] = []
    operators: List[str]   = []
    for token in output_formula:
        # Tho token is an AeroMAPS output variable :
        if isinstance(token, list):
            variable_name, variable_type, _ = token
            if variable_type == "vector_outputs":
                operands.append(DF_vector_outputs.loc[year_section_data, variable_name])
            elif variable_type == "climate_outputs":
                operands.append(DF_climate_outputs.loc[year_section_data, variable_name])
            else:
                raise ValueError(f"Invalid output type '{variable_type}' for variable '{variable_name}' in the formula. Expected one of {_ALLOWED_OUTPUT_TYPES}.")

        # The token is an operator :
        elif token in _ALLOWED_OPERATORS:
            operators.append(token)

        # The token is a constant :
        else:
            operands.append(Series([float(token)] * len(year_section_data), index = year_section_data))

    # Check that the number of operands and operators is correct :
    if len(operands) - 1 != len(operators):
        raise ValueError("The number of operands must be one more than the number of operators in the output formula.")

    # Calculate the output value (evaluation the formula from left to right) :
    result = operands[0].copy()
    for operator, operand in zip(operators, operands[1:]):
        if operator == "+":
            result += operand
        elif operator == "-":
            result -= operand
        elif operator == "*":
            result *= operand
        elif operator == "/":
            if (operand == 0).any():
                raise ZeroDivisionError("Division by zero in the output formula.")
            result /= operand
        else:
            raise ValueError(f"Invalid operator '{operator}' in the output formula.")

    # Return the result as a Series indexed by the years :
    return result
