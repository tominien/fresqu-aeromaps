from typing import Any, Dict, List




def plot_multi(process_data: Dict[str, Any]) -> List[List[float]]:
    """
    Function that plots the multi-disciplinary graph, based on the data from `process_data`.

    Arguments :
    - `process_data (Dict[str, Any])` : A dictionary containing the processed data by AeroMAPS.

    Returns :
    - `List[List[float]]` : A list containing two lists, the first for consumptions and the second for budgets.
    """
    parameters = process_data["float_inputs"]
    df = process_data["vector_outputs"]
    df_climate = process_data["climate_outputs"]
    float_outputs = process_data["float_outputs"]

    # Budget carbone :
    gross_carbon_budget = float(float_outputs["gross_carbon_budget_2050"])
    aviation_carbon_budget = float(float_outputs["aviation_carbon_budget"])
    cumulative_co2_emissions = float(df.loc[2050, "cumulative_co2_emissions"])

    # Biomasse :
    available_biomass_total = float_outputs["available_biomass_total"]
    aviation_available_biomass = float_outputs["aviation_available_biomass"]
    biomass_consumption_end_year = float_outputs["biomass_consumption_end_year"]

    # Electricité :
    available_electricity_total = parameters["available_electricity"]
    aviation_available_electricity = float_outputs["aviation_available_electricity"]
    electricity_consumption_end_year = float_outputs["electricity_consumption_end_year"]

    # Forçage radiatif effectif :
    equivalent_gross_carbon_budget = float(float_outputs["equivalent_gross_carbon_budget_2050"])
    aviation_equivalent_carbon_budget = float(float_outputs["aviation_equivalent_carbon_budget"])
    cumulative_total_equivalent_emissions = float(df_climate.loc[2050, "cumulative_total_equivalent_emissions"])

    budgets = [
        aviation_equivalent_carbon_budget / equivalent_gross_carbon_budget * 100,
        aviation_carbon_budget / gross_carbon_budget * 100,
        aviation_available_biomass / available_biomass_total * 100,
        aviation_available_electricity / available_electricity_total * 100
    ]

    consumptions = [
        max(cumulative_total_equivalent_emissions / equivalent_gross_carbon_budget * 100, 0),
        cumulative_co2_emissions / gross_carbon_budget * 100,
        biomass_consumption_end_year / available_biomass_total * 100,
        electricity_consumption_end_year / available_electricity_total * 100
    ]

    return [consumptions, budgets]
