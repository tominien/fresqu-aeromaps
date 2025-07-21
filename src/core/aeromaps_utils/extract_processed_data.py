from typing import Any, Dict, List

from pandas import DataFrame




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


def get_dataframe_aeromaps(process_data: Dict[str, Any], dataframe_name: str) -> DataFrame:
    """
    Extract the `dataframe_name` dataframe from the process data (a computed data from an AeroMAPS process).

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data, computed from an AeroMAPS process, which should contain the `dataframe_name` dataframe.

    #### Returns :
    - `Dataframe` : The `dataframe_name` dataframe.
    """
    if dataframe_name not in process_data:
        raise ValueError(f"Process data does not contain the '{dataframe_name}' key.")

    extracted_dataframe = process_data[dataframe_name]

    if not isinstance(extracted_dataframe, DataFrame):
        raise TypeError(f"'{dataframe_name}' should be a pandas DataFrame.")

    return extracted_dataframe


def get_dataframe_vector_outputs(process_data: Dict[str, Any]) -> DataFrame:
    """
    Extract the vector outputs dataframe from the process data (a computed data from an AeroMAPS process).

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data, computed from an AeroMAPS process, which contains the vector outputs.

    #### Returns :
    - `Dataframe` : The Dataframe of the vector outputs.
    """
    return get_dataframe_aeromaps(process_data, "vector_outputs")


def get_dataframe_climate_outputs(process_data: Dict[str, Any]) -> DataFrame:
    """
    Extract the climate outputs dataframe from the process data (a computed data from an AeroMAPS process).

    #### Arguments :
    - `process_data (Dict[str, Any])` : The process data, computed from an AeroMAPS process, which contains the climate outputs.

    #### Returns :
    - `Dataframe` : The Dataframe of the climate outputs.
    """
    return get_dataframe_aeromaps(process_data, "climate_outputs")
