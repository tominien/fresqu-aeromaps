from typing import Any, Dict, List, Optional

import copy

from functools import lru_cache

from aeromaps import create_process
from aeromaps.core.process import AeroMAPSProcess
from aeromaps.models.parameters import Parameters

from src.crud.crud_cards import get_cards_ids




@lru_cache(maxsize = None)
def compute_process(
        process: AeroMAPSProcess,
        cards_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
    """
    Initialize the AeroMAPS process with default parameters and compute the results.

    This function sets the parameters for the AeroMAPS process, including :
    - Air traffic evolution,
    - Aircraft fleet and operation evolution,
    - Aircraft energy,
    - Carbon offset,
    - Environmental limits,
    - Allocation settings,
    - And various environmental settings.

    #### Arguments :
    - `cards_ids (list[str], optional)` : List of cards ids to apply to the process. Defaults to None (no cards are applied <=> reference scenario).

    #### Returns :
    - `dict [str, Any]` : The computed data from the AeroMAPS process.
    """
    # Check if all the cards_ids are valid :
    if cards_ids and not all(card_id in get_cards_ids() for card_id in cards_ids):
        raise ValueError("Invalid card IDs provided. Please check the available cards.")

    # Initialize the AeroMAPS process :
    parameters: Parameters = process.parameters

    # Air traffic evolution :
        # Growth rate by category :
    parameters.cagr_passenger_short_range_reference_periods        = [2020, 2030, 2040, 2050]
    parameters.cagr_passenger_short_range_reference_periods_values = [3.0, 3.0, 3.0]

    # Aircraft fleet and operation evolution - Aircraft efficiency using the top-down approach :
    parameters.fleet_renewal_duration = 20.0
        # Drop-in aircraft :
    parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years_values  = [0.5]
    parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years_values = [0.5]
    parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years_values   = [0.5]

    # Aircraft fleet and operation evolution - Operations :
        # Values for setting the logistic function :
    parameters.operations_final_gain = 5.0
    parameters.operations_start_year = 2025
    parameters.operations_duration   = 25.0

    # Aircraft energy - Introduction of alternative drop-in fuels :
        # Share of alternative fuels in the drop-in fuel mix (the rest being supplemented by kerosene) :
    parameters.biofuel_share_reference_years            = [2020, 2030, 2040, 2050]
    parameters.biofuel_share_reference_years_values     = [0.0, 0.0, 0.0, 0.0]
    parameters.electrofuel_share_reference_years        = [2020, 2030, 2040, 2050]
    parameters.electrofuel_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]

    # Carbon offset :
    parameters.carbon_offset_baseline_level_vs_2019_reference_periods        = [2020, 2024, 2050]
    parameters.carbon_offset_baseline_level_vs_2019_reference_periods_values = [500.0, 500.0]
    parameters.residual_carbon_offset_share_reference_years                  = [2020, 2030, 2040, 2050]
    parameters.residual_carbon_offset_share_reference_years_values           = [0.0, 0.0, 0.0, 0.0]

    # Environmental limits :
        # Carbon budgets and Carbon Dioxide Removal :
    parameters.net_carbon_budget           = 850.0
    parameters.carbon_dioxyde_removal_2100 = 280.0
        # Available energy resources in 2050 :
    parameters.available_electricity = 250.0

    # Allocation settings :
        # Aviation share of the global energy resources (biomass and electricity) :
    parameters.aviation_biomass_allocated_share     = 5.0
    parameters.aviation_electricity_allocated_share = 5.0

    # Various environmental settings :
        # Share of biofuel production pathways (the rest being completed by AtJ processes) :
    parameters.biofuel_hefa_fog_share_reference_years           = [2020, 2030, 2040, 2050]
    parameters.biofuel_hefa_fog_share_reference_years_values    = [100, 100, 0.7, 0.7]
    parameters.biofuel_hefa_others_share_reference_years        = [2020, 2030, 2040, 2050]
    parameters.biofuel_hefa_others_share_reference_years_values = [0.0, 0.0, 3.8, 3.8]
    parameters.biofuel_ft_others_share_reference_years          = [2020, 2030, 2040, 2050]
    parameters.biofuel_ft_others_share_reference_years_values   = [0.0, 0.0, 76.3, 76.3]
    parameters.biofuel_ft_msw_share_reference_years             = [2020, 2030, 2040, 2050]
    parameters.biofuel_ft_msw_share_reference_years_values      = [0.0, 0.0, 7.4, 7.4]
        # Emission factors for electricity (2019 value: 429 gCO₂/kWh) :
    parameters.electricity_emission_factor_reference_years        = [2020, 2030, 2040, 2050]
    parameters.electricity_emission_factor_reference_years_values = [429.0, 200.0, 100.0, 30.0]
        # Share of hydrogen production pathways (the rest being completed by production via coal without CCS, distribution in 2019: Gas without CCS (71%), Coal without CCS (27%), Electrolysis (2%), Others with CCS (0%), Co-products not taken into account) :
    parameters.hydrogen_electrolysis_share_reference_years        = [2020, 2030, 2040, 2050]
    parameters.hydrogen_electrolysis_share_reference_years_values = [2, 100, 100, 100]
    parameters.hydrogen_gas_ccs_share_reference_years             = [2020, 2030, 2040, 2050]
    parameters.hydrogen_gas_ccs_share_reference_years_values      = [0, 0, 0, 0]
    parameters.hydrogen_coal_ccs_share_reference_years            = [2020, 2030, 2040, 2050]
    parameters.hydrogen_coal_ccs_share_reference_years_values     = [0, 0, 0, 0]
    parameters.hydrogen_gas_share_reference_years                 = [2020, 2030, 2040, 2050]
    parameters.hydrogen_gas_share_reference_years_values          = [71, 0, 0, 0]

    # Apply cards if provided :
    if cards_ids:
        # Sobriété :
        if "sobriety" in cards_ids:
            parameters.cagr_passenger_medium_range_reference_periods_values = [1.5]
            parameters.cagr_passenger_long_range_reference_periods_values   = [1.5]
            parameters.cagr_freight_reference_periods_values                = [1.5]

        # Compensation des émissions :
        if "emmissions_compensation" in cards_ids:
            parameters.residual_carbon_offset_share_reference_years_values = [0.0, 0.0, 10.0, 10.0]

        # Nouveaux vecteurs énergétiques :
        if "new_energies" in cards_ids:
            parameters.biofuel_share_reference_years_values     = [0.0, 4.8, 24.0, 35.0]
            parameters.electrofuel_share_reference_years_values = [0.0, 1.2, 10.0, 35.0]

        # Report modal :
        if "modal_shift" in cards_ids:
            if "sobriety" in cards_ids:
                parameters.cagr_passenger_short_range_reference_periods_values = [0.0, 0.0, 0.0]
            else:
                parameters.cagr_passenger_short_range_reference_periods_values = [1.0, 1.0, 1.0]

        # Efficacité des opérations :
        if "operations_efficiency" in cards_ids:
            parameters.load_factor_end_year  = 90.0
            parameters.operations_final_gain = 10.0
            parameters.operations_start_year = 2025
            parameters.operations_duration   = 25.0

        # Technologie :
        if "technology" in cards_ids:
            parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years_values  = [1.0]
            parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years_values = [1.0]
            parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years_values   = [1.0]
            parameters.fleet_renewal_duration                                              = 15.0

        # Budget carbone :
        if "carbon_budget" in cards_ids:
            ... # TODO: After implementing this card, remove the "[NI] " tag from the card name in the database and the markdown "explanation file".

        # Réglementations et mesures économiques :
        if "reglementations_and_economical_measures" in cards_ids:
            ... # TODO: After implementing this card, remove the "[NI] " tag from the card name in the database and the markdown "explanation file".

        # Sensibiliser & Éduquer :
        if "awareness_and_education" in cards_ids:
            ... # TODO: After implementing this card, remove the "[NI] " tag from the card name in the database and the markdown "explanation file".

    process.compute()
    return process.data


class ProcessEngine:
    """
    Engine for running an AeroMAPS simulation process from a reference scenario and chosen cards.
    """
    def __init__(self) -> None:
        """
        Initialize the process engine with the given configuration.
        """
        self.process: AeroMAPSProcess = create_process()


    @lru_cache(maxsize = None)
    def get_process(self) -> AeroMAPSProcess:
        """
        Get the AeroMAPS process instance.

        #### Returns :
        - `AeroMAPSProcess` : The AeroMAPS process instance.
        """
        return self.process


    @lru_cache(maxsize = None)
    def compute(
            self,
            cards_ids: Optional[List[int]] = None
        ) -> Dict[str, Any]:
        """
        Compute the AeroMAPS process with the given cards (each card affect one or more aspects of the process).

        #### Arguments :
        - `cards_ids (list[int], optional)` : List of cards IDs to apply to the process. Defaults to None (no cards are applied <=> reference scenario).

        #### Returns :
        - `dict [str, Any]` : The computed data from the AeroMAPS process.
        """
        process_data = compute_process(self.process, tuple(cards_ids) if cards_ids else None) # Converted to tuple for LRU cache compatibility.

        return copy.deepcopy(process_data)
