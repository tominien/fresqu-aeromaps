from typing import Any, Dict, List

from pandas import DataFrame

from core.aeromaps_utils.extract_processed_data import get_dataframe_vector_outputs, get_dataframe_climate_outputs




def M_plot_consumptions(process_data: Dict[str, Any]) -> List[float]:
    float_inputs  = process_data["float_inputs"]
    float_outputs = process_data["float_outputs"]
    DF_vector_outputs: DataFrame  = get_dataframe_vector_outputs(process_data)
    DF_climate_outputs: DataFrame = get_dataframe_climate_outputs(process_data)

    # Budget carbone :
    gross_carbon_budget      = float(float_outputs["gross_carbon_budget_2050"])
    cumulative_co2_emissions = float(DF_vector_outputs.loc[2050, "cumulative_co2_emissions"])

    # Biomasse :
    available_biomass_total      = float_outputs["available_biomass_total"]
    biomass_consumption_end_year = float_outputs["biomass_consumption_end_year"]

    # Électricité :
    available_electricity_total      = float_inputs["available_electricity"]
    electricity_consumption_end_year = float_outputs["electricity_consumption_end_year"]

    # Forçage radiatif effectif :
    equivalent_gross_carbon_budget        = float(float_outputs["equivalent_gross_carbon_budget_2050"])
    cumulative_total_equivalent_emissions = float(DF_climate_outputs.loc[2050, "cumulative_total_equivalent_emissions"])

    return [
        max(
            cumulative_total_equivalent_emissions / equivalent_gross_carbon_budget * 100,
            0
        ),
        cumulative_co2_emissions / gross_carbon_budget * 100,
        biomass_consumption_end_year / available_biomass_total * 100,
        electricity_consumption_end_year / available_electricity_total * 100
    ]


def M_plot_budgets(process_data: Dict[str, Any]) -> List[List[float]]:
    float_inputs  = process_data["float_inputs"]
    float_outputs = process_data["float_outputs"]

    # Budget carbone :
    gross_carbon_budget    = float(float_outputs["gross_carbon_budget_2050"])
    aviation_carbon_budget = float(float_outputs["aviation_carbon_budget"])

    # Biomasse :
    available_biomass_total    = float_outputs["available_biomass_total"]
    aviation_available_biomass = float_outputs["aviation_available_biomass"]

    # Électricité :
    available_electricity_total    = float_inputs["available_electricity"]
    aviation_available_electricity = float_outputs["aviation_available_electricity"]

    # Forçage radiatif effectif :
    equivalent_gross_carbon_budget    = float(float_outputs["equivalent_gross_carbon_budget_2050"])
    aviation_equivalent_carbon_budget = float(float_outputs["aviation_equivalent_carbon_budget"])

    return [
        aviation_equivalent_carbon_budget / equivalent_gross_carbon_budget * 100,
        aviation_carbon_budget / gross_carbon_budget * 100,
        aviation_available_biomass / available_biomass_total * 100,
        aviation_available_electricity / available_electricity_total * 100
    ]
