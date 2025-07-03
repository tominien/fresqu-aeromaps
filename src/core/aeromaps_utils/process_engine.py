from typing import Dict, List, Any, Optional

from crud.crud_cards import get_cards_ids

from functools import lru_cache

from aeromaps import create_process
from aeromaps.core.process import AeroMAPSProcess
from aeromaps.models.parameters import Parameters




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
        # Growth rate by category [%] :
    parameters.cagr_passenger_short_range_reference_periods         = [2020, 2030, 2040, 2050]
    parameters.cagr_passenger_short_range_reference_periods_values  = [3.0, 3.0, 3.0]
    parameters.cagr_passenger_medium_range_reference_periods        = []
    parameters.cagr_passenger_medium_range_reference_periods_values = [3.0]
    parameters.cagr_passenger_long_range_reference_periods          = []
    parameters.cagr_passenger_long_range_reference_periods_values   = [3.0]
    parameters.cagr_freight_reference_periods                       = []
    parameters.cagr_freight_reference_periods_values                = [3.0]

    # Aircraft fleet and operation evolution - Aircraft load factor :
        # Aircraft load factor in 2050 [%] :
    parameters.load_factor_end_year = 85.0 # 2019 value = 82.399312

    # Aircraft fleet and operation evolution - Aircraft efficiency using the top-down approach :
        # Drop-in aircraft :
            # Mean annual efficiency gains by category [%] :
    parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years         = []
    parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years_values  = [0.5]
    parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years        = []
    parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years_values = [0.5]
    parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years          = []
    parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years_values   = [0.5]
        # Hydrogen aircraft :
            # Values for setting logistic functions by category :
    parameters.hydrogen_final_market_share_short_range = 0.0
    parameters.hydrogen_introduction_year_short_range  = 2051
    parameters.fleet_renewal_duration                  = 20.0
            # Relative energy consumption for hydrogen aircraft with respect to drop-in aircraft [%] :
    parameters.relative_energy_per_ask_hydrogen_wrt_dropin_short_range_reference_years        = []
    parameters.relative_energy_per_ask_hydrogen_wrt_dropin_short_range_reference_years_values = [1.0]

    # Aircraft fleet and operation evolution - Operations :
        # Values for setting the logistic function :
    parameters.operations_final_gain = 5.0
    parameters.operations_start_year = 2025
    parameters.operations_duration   = 25.0

    # Aircraft energy - Introduction of alternative drop-in fuels :
        # Share of alternative fuels in the drop-in fuel mix (the rest being supplemented by kerosene) [%] :
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
        # Carbon budgets and Carbon Dioxide Removal [GtCO2] :
    parameters.net_carbon_budget           = 850.0
    parameters.carbon_dioxyde_removal_2100 = 280.0
        # Available energy resources in 2050 [EJ] :
    parameters.waste_biomass                 = 12.0
    parameters.crops_biomass                 = 63.0
    parameters.forest_residues_biomass       = 17.0
    parameters.agricultural_residues_biomass = 57.0
    parameters.algae_biomass                 = 15.0
    parameters.available_electricity         = 250.0

    # Allocation settings :
        # Aviation share of the global (equivalent) carbon budget [%] :
    parameters.aviation_carbon_budget_allocated_share          = 2.6
    parameters.aviation_equivalentcarbonbudget_allocated_share = 5.1
        # Aviation share of the global energy resources (biomass and electricity) [%] :
    parameters.aviation_biomass_allocated_share     = 5.0
    parameters.aviation_electricity_allocated_share = 5.0

    # Various environmental settings :
        # Share of biofuel production pathways (the rest being completed by AtJ processes) [%] :
    parameters.biofuel_hefa_fog_share_reference_years           = [2020, 2030, 2040, 2050]
    parameters.biofuel_hefa_fog_share_reference_years_values    = [100, 100, 0.7, 0.7]
    parameters.biofuel_hefa_others_share_reference_years        = [2020, 2030, 2040, 2050]
    parameters.biofuel_hefa_others_share_reference_years_values = [0.0, 0.0, 3.8, 3.8]
    parameters.biofuel_ft_others_share_reference_years          = [2020, 2030, 2040, 2050]
    parameters.biofuel_ft_others_share_reference_years_values   = [0.0, 0.0, 76.3, 76.3]
    parameters.biofuel_ft_msw_share_reference_years             = [2020, 2030, 2040, 2050]
    parameters.biofuel_ft_msw_share_reference_years_values      = [0.0, 0.0, 7.4, 7.4]
        # Emission factors for electricity (2019 value: 429 gCO2/kWh) :
    parameters.electricity_emission_factor_reference_years        = [2020, 2030, 2040, 2050]
    parameters.electricity_emission_factor_reference_years_values = [429.0, 200.0, 100.0, 30.0]
        # Share of hydrogen production pathways (the rest being completed by production via coal without CCS, distribution in 2019: Gas without CCS (71%), Coal without CCS (27%), Electrolysis (2%), Others with CCS (0%), Co-products not taken into account) [%] :
    parameters.hydrogen_electrolysis_share_reference_years        = [2020, 2030, 2040, 2050]
    parameters.hydrogen_electrolysis_share_reference_years_values = [2, 100, 100, 100]
    parameters.hydrogen_gas_ccs_share_reference_years             = [2020, 2030, 2040, 2050]
    parameters.hydrogen_gas_ccs_share_reference_years_values      = [0, 0, 0, 0]
    parameters.hydrogen_coal_ccs_share_reference_years            = [2020, 2030, 2040, 2050]
    parameters.hydrogen_coal_ccs_share_reference_years_values     = [0, 0, 0, 0]
    parameters.hydrogen_gas_share_reference_years                 = [2020, 2030, 2040, 2050]
    parameters.hydrogen_gas_share_reference_years_values          = [71, 0, 0, 0]
            # Economic aspects :
    parameters.co2_cost_reference_years                      = []
    parameters.co2_cost_reference_years_values               = [0.225]
    parameters.carbon_tax_reference_years                    = []
    parameters.carbon_tax_reference_years_values             = [5.0]
    parameters.exogenous_carbon_price_reference_years        = [2020, 2030, 2040, 2050] # Non trouvé.
    parameters.exogenous_carbon_price_reference_years_values = [54, 250, 500, 775]      # Non trouvé.
    parameters.carbon_offset_price_reference_years           = []
    parameters.carbon_offset_price_reference_years_values    = [5.0]

    # Apply cards if provided :
    if cards_ids:
        # Budget carbone :
        if "carbon_budget" in cards_ids:
            ...
    
        # Réglementations et mesures économiques :
        if "reglementations_and_economical_measures" in cards_ids:
            ...

        # Sensibiliser & Éduquer :
        if "awareness_and_education" in cards_ids:
            ...

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
            parameters.biofuel_share_reference_years_values     = [0.0, 4.8, 24.0, 35.0] # Vérifier ces données !
            parameters.electrofuel_share_reference_years_values = [0.0, 1.2, 10.0, 35.0] # Vérifier ces données !

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
            parameters.hydrogen_final_market_share_short_range                             = 0.0
            parameters.fleet_renewal_duration                                              = 15.0

    process.compute()
    return process.data


class ProcessEngine:
    """
    Engine for running an AeroMAPS simulation process from a reference scenario and chosen cards.
    """
    def __init__(self) -> None:
        """
        Initialize the process engine with the given configuration.

        #### Arguments :
        - `configuration_file (str, optional)` : Path to the configuration file. Defaults to None.
        - `models (list[str], optional)` : List of models to use. Defaults to None.
        - `use_fleet_model (bool)` : Whether to use the fleet model. Defaults to False.
        - `add_examples_aircraft_and_subcategory (bool)` : Whether to add example aircraft and subcategories. Defaults to True.
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
        return compute_process(self.process, tuple(cards_ids) if cards_ids else None) # Converted to tuple for LRU cache compatibility
