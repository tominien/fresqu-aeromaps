#Fichier de setup des fonctions process : initialisation de la plupart des variables du modèle aeroMAPS, et fonctions de décision et de recalcul des modèles selon les choix de cartes.
#Toutes les fonctions ci-dessous retournent les datas issues du calcul par aeroMAPS


from aeromaps import create_process
from aeromaps.core.models import (
    models_traffic,
    models_efficiency_top_down,
    models_energy_without_fuel_effect,
    models_offset,
    models_climate_simple_gwpstar,
    models_sustainability,
    models_energy_cost,
    models_costs_top_down_specific,
    models_operation_cost,
)
models = {
    "models_traffic": models_traffic,
    "models_efficiency_top_down": models_efficiency_top_down,
    "models_energy_without_fuel_effect": models_energy_without_fuel_effect,
    "models_offset": models_offset,
    "models_climate_simple_gwpstar": models_climate_simple_gwpstar,
    "models_sustainability": models_sustainability,
    "models_energy_cost": models_energy_cost,
    "models_costs_top_down_specific": models_costs_top_down_specific,
    "models_operation_cost": models_operation_cost,
}

def init_process_ref():
    
    process_ref = create_process(models=models)
    # Scénario de référence

    # Air traffic evolution

    ## Growth rate by category [%]
    process_ref.parameters.cagr_passenger_short_range_reference_periods = [2020, 2030, 2040, 2050]
    process_ref.parameters.cagr_passenger_short_range_reference_periods_values = [3.0, 3.0, 3.0]
    process_ref.parameters.cagr_passenger_medium_range_reference_periods = []
    process_ref.parameters.cagr_passenger_medium_range_reference_periods_values = [3.0]
    process_ref.parameters.cagr_passenger_long_range_reference_periods = []
    process_ref.parameters.cagr_passenger_long_range_reference_periods_values = [3.0]
    process_ref.parameters.cagr_freight_reference_periods = []
    process_ref.parameters.cagr_freight_reference_periods_values = [3.0]

    # Aircraft fleet and operation evolution - Aircraft load factor

    ## Aircraft load factor in 2050 [%]
    process_ref.parameters.load_factor_end_year = 85  # 2019 value: 82.399312

    # Aircraft fleet and operation evolution - Aircraft efficiency using the top-down approach

    ## Drop-in aircraft
    ### Mean annual efficiency gains by category [%]
    process_ref.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years = []
    process_ref.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years_values = [0.5]
    process_ref.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years = []
    process_ref.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years_values = [0.5]
    process_ref.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years = []
    process_ref.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years_values = [0.5]

    ## Hydrogen aircraft
    ### Values for setting logistic functions by category
    process_ref.parameters.hydrogen_final_market_share_short_range = 0.0  # [%]
    process_ref.parameters.hydrogen_introduction_year_short_range = 2051
    process_ref.parameters.fleet_renewal_duration = 20.0
    ### Relative energy consumption for hydrogen aircraft with respect to drop-in aircraft [%]
    process_ref.parameters.relative_energy_per_ask_hydrogen_wrt_dropin_short_range_reference_years = []
    process_ref.parameters.relative_energy_per_ask_hydrogen_wrt_dropin_short_range_reference_years_values = [1.0]

    # Aircraft fleet and operation evolution - Operations

    ## Values for setting the logistic function
    process_ref.parameters.operations_final_gain = 8.0  # [%]
    process_ref.parameters.operations_start_year = 2025
    process_ref.parameters.operations_duration = 25.0

    # Aircraft energy - Introduction of alternative drop-in fuels

    ## Share of alternative fuels in the drop-in fuel mix (the rest being supplemented by kerosene) [%]
    process_ref.parameters.biofuel_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.biofuel_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]
    process_ref.parameters.electrofuel_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.electrofuel_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]

    # Carbon offset
    process_ref.parameters.carbon_offset_baseline_level_vs_2019_reference_periods = [2020, 2024, 2050]
    process_ref.parameters.carbon_offset_baseline_level_vs_2019_reference_periods_values = [500.0, 500.0]
    process_ref.parameters.residual_carbon_offset_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.residual_carbon_offset_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]

    # Environmental limits

    ## Carbon budgets and Carbon Dioxide Removal [GtCO2]
    process_ref.parameters.net_carbon_budget = 850.0
    process_ref.parameters.carbon_dioxyde_removal_2100 = 280.0

    ## Available energy resources in 2050 [EJ]
    process_ref.parameters.waste_biomass = 12.0
    process_ref.parameters.crops_biomass = 63.0
    process_ref.parameters.forest_residues_biomass = 17.0
    process_ref.parameters.agricultural_residues_biomass = 57.0
    process_ref.parameters.algae_biomass = 15.0
    process_ref.parameters.available_electricity = 250.0

    # Allocation settings

    ## Aviation share of the global (equivalent) carbon budget [%]
    process_ref.parameters.aviation_carbon_budget_allocated_share = 2.6
    process_ref.parameters.aviation_equivalentcarbonbudget_allocated_share = 5.1

    ## Aviation share of the global energy resources (biomass and electricity) [%]
    process_ref.parameters.aviation_biomass_allocated_share = 5.0
    process_ref.parameters.aviation_electricity_allocated_share = 5.0

    # Various environmental settings

    ## Share of biofuel production pathways (the rest being completed by AtJ processes) [%]
    process_ref.parameters.biofuel_hefa_fog_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.biofuel_hefa_fog_share_reference_years_values = [100, 100, 0.7, 0.7]
    process_ref.parameters.biofuel_hefa_others_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.biofuel_hefa_others_share_reference_years_values = [0.0, 0.0, 3.8, 3.8]
    process_ref.parameters.biofuel_ft_others_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.biofuel_ft_others_share_reference_years_values = [0.0, 0.0, 76.3, 76.3]
    process_ref.parameters.biofuel_ft_msw_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.biofuel_ft_msw_share_reference_years_values = [0.0, 0.0, 7.4, 7.4]

    ## Emission factors for electricity (2019 value: 429 gCO2/kWh)
    process_ref.parameters.electricity_emission_factor_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.electricity_emission_factor_reference_years_values = [429.0, 200.0, 100.0, 30.0]

    ## Share of hydrogen production pathways (the rest being completed by production via coal without CCS) [%]
            ## Distribution in 2019: Gas without CCS (71%), Coal without CCS (27%), Electrolysis (2%), Others with CCS (0%), Co-products not taken into account
    process_ref.parameters.hydrogen_electrolysis_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.hydrogen_electrolysis_share_reference_years_values = [2, 100, 100, 100]
    process_ref.parameters.hydrogen_gas_ccs_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.hydrogen_gas_ccs_share_reference_years_values = [0, 0, 0, 0]
    process_ref.parameters.hydrogen_coal_ccs_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.hydrogen_coal_ccs_share_reference_years_values = [0, 0, 0, 0]
    process_ref.parameters.hydrogen_gas_share_reference_years = [2020, 2030, 2040, 2050]
    process_ref.parameters.hydrogen_gas_share_reference_years_values = [71, 0, 0, 0]
    
    process_ref.compute()
    
    return process_ref.data

def compute_process1(Liste_des_widgets1):
    process1 = create_process(models=models)
    # Scénario du groupe 1

    # Air traffic evolution

    ## Growth rate by category [%]
    process1.parameters.cagr_passenger_short_range_reference_periods = [2020, 2030, 2040, 2050]
    process1.parameters.cagr_passenger_short_range_reference_periods_values = [3.0, 3.0, 3.0]
    process1.parameters.cagr_passenger_medium_range_reference_periods = []
    process1.parameters.cagr_passenger_medium_range_reference_periods_values = [3.0]
    process1.parameters.cagr_passenger_long_range_reference_periods = []
    process1.parameters.cagr_passenger_long_range_reference_periods_values = [3.0]
    process1.parameters.cagr_freight_reference_periods = []
    process1.parameters.cagr_freight_reference_periods_values = [3.0]

    # Aircraft fleet and operation evolution - Aircraft load factor

    ## Aircraft load factor in 2050 [%]
    process1.parameters.load_factor_end_year = 85  # 2019 value: 82.399312

    # Aircraft fleet and operation evolution - Aircraft efficiency using the top-down approach

    ## Drop-in aircraft
    ### Mean annual efficiency gains by category [%]
    process1.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years = []
    process1.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years_values = [0.5]
    process1.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years = []
    process1.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years_values = [0.5]
    process1.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years = []
    process1.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years_values = [0.5]

    ## Hydrogen aircraft
    ### Values for setting logistic functions by category
    process1.parameters.hydrogen_final_market_share_short_range = 0.0  # [%]
    process1.parameters.hydrogen_introduction_year_short_range = 2051
    process1.parameters.fleet_renewal_duration = 20.0
    ### Relative energy consumption for hydrogen aircraft with respect to drop-in aircraft [%]
    process1.parameters.relative_energy_per_ask_hydrogen_wrt_dropin_short_range_reference_years = []
    process1.parameters.relative_energy_per_ask_hydrogen_wrt_dropin_short_range_reference_years_values = [1.0]

    # Aircraft fleet and operation evolution - Operations

    ## Values for setting the logistic function
    process1.parameters.operations_final_gain = 8.0  # [%]
    process1.parameters.operations_start_year = 2025
    process1.parameters.operations_duration = 25.0

    # Aircraft energy - Introduction of alternative drop-in fuels

    ## Share of alternative fuels in the drop-in fuel mix (the rest being supplemented by kerosene) [%]
    process1.parameters.biofuel_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.biofuel_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]
    process1.parameters.electrofuel_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.electrofuel_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]

    # Carbon offset
    process1.parameters.carbon_offset_baseline_level_vs_2019_reference_periods = [2020, 2024, 2050]
    process1.parameters.carbon_offset_baseline_level_vs_2019_reference_periods_values = [500.0, 500.0]
    process1.parameters.residual_carbon_offset_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.residual_carbon_offset_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]

    # Environmental limits

    ## Carbon budgets and Carbon Dioxide Removal [GtCO2]
    process1.parameters.net_carbon_budget = 850.0
    process1.parameters.carbon_dioxyde_removal_2100 = 280.0

    ## Available energy resources in 2050 [EJ]
    process1.parameters.waste_biomass = 12.0
    process1.parameters.crops_biomass = 63.0
    process1.parameters.forest_residues_biomass = 17.0
    process1.parameters.agricultural_residues_biomass = 57.0
    process1.parameters.algae_biomass = 15.0
    process1.parameters.available_electricity = 250.0

    # Allocation settings

    ## Aviation share of the global (equivalent) carbon budget [%]
    process1.parameters.aviation_carbon_budget_allocated_share = 2.6
    process1.parameters.aviation_equivalentcarbonbudget_allocated_share = 5.1

    ## Aviation share of the global energy resources (biomass and electricity) [%]
    process1.parameters.aviation_biomass_allocated_share = 5.0
    process1.parameters.aviation_electricity_allocated_share = 5.0

    # Various environmental settings

    ## Share of biofuel production pathways (the rest being completed by AtJ processes) [%]
    process1.parameters.biofuel_hefa_fog_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.biofuel_hefa_fog_share_reference_years_values = [100, 100, 0.7, 0.7]
    process1.parameters.biofuel_hefa_others_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.biofuel_hefa_others_share_reference_years_values = [0.0, 0.0, 3.8, 3.8]
    process1.parameters.biofuel_ft_others_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.biofuel_ft_others_share_reference_years_values = [0.0, 0.0, 76.3, 76.3]
    process1.parameters.biofuel_ft_msw_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.biofuel_ft_msw_share_reference_years_values = [0.0, 0.0, 7.4, 7.4]

    ## Emission factors for electricity (2019 value: 429 gCO2/kWh)
    process1.parameters.electricity_emission_factor_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.electricity_emission_factor_reference_years_values = [429.0, 200.0, 100.0, 30.0]

    ## Share of hydrogen production pathways (the rest being completed by production via coal without CCS) [%]
    ## Distribution in 2019: Gas without CCS (71%), Coal without CCS (27%), Electrolysis (2%), Others with CCS (0%), Co-products not taken into account
    process1.parameters.hydrogen_electrolysis_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.hydrogen_electrolysis_share_reference_years_values = [2, 100, 100, 100]
    process1.parameters.hydrogen_gas_ccs_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.hydrogen_gas_ccs_share_reference_years_values = [0, 0, 0, 0]
    process1.parameters.hydrogen_coal_ccs_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.hydrogen_coal_ccs_share_reference_years_values = [0, 0, 0, 0]
    process1.parameters.hydrogen_gas_share_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.hydrogen_gas_share_reference_years_values = [71, 0, 0, 0]

    ### Economic aspects

    process1.parameters.co2_cost_reference_years = []
    process1.parameters.co2_cost_reference_years_values = [0.225]
    process1.parameters.carbon_tax_reference_years = []
    process1.parameters.carbon_tax_reference_years_values = [5.0]
    process1.parameters.exogenous_carbon_price_reference_years = [2020, 2030, 2040, 2050]
    process1.parameters.exogenous_carbon_price_reference_years_values = [54, 250, 500, 775]
    process1.parameters.carbon_offset_price_reference_years = []
    process1.parameters.carbon_offset_price_reference_years_values = [5.0]
    
    if Liste_des_widgets1 != []:
        #if Liste_des_widgets1[0].value:
        #if Liste_des_widgets1[1].value:
        
        if Liste_des_widgets1[5].value:
            process1.parameters.cagr_passenger_short_range_reference_periods_values = [1.0, 1.0, 1.0]
        if Liste_des_widgets1[2].value:
            process1.parameters.cagr_passenger_medium_range_reference_periods_values = [2.0]
            process1.parameters.cagr_passenger_long_range_reference_periods_values = [2.0]
            process1.parameters.cagr_freight_reference_periods_values = [2.0]
            if Liste_des_widgets1[5].value:
                process1.parameters.cagr_passenger_short_range_reference_periods_values = [0.0, 0.0, 0.0]
        if Liste_des_widgets1[3].value:
            process1.parameters.residual_carbon_offset_share_reference_years_values = [0.0, 0.0, 20.0, 20.0]
        if Liste_des_widgets1[4].value:
            process1.parameters.biofuel_share_reference_years_values = [0.0, 4.8, 24.0, 35.0]
            process1.parameters.electrofuel_share_reference_years_values = [0.0, 1.2, 10.0, 35.0]
        
        if Liste_des_widgets1[6].value:
            process1.parameters.load_factor_end_year = 90
            process1.parameters.operations_final_gain = 10.0  # [%]
            process1.parameters.operations_start_year = 2025
            process1.parameters.operations_duration = 25.0
        if Liste_des_widgets1[7].value:
            process1.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years_values = [1.0]
            process1.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years_values = [1.0]
            process1.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years_values = [1.0]
            process1.parameters.hydrogen_final_market_share_short_range = 50.0  # [%]
            process1.parameters.hydrogen_introduction_year_short_range = 2035
            process1.parameters.fleet_renewal_duration = 15.0
    
    process1.compute()
    
    return process1.data


def compute_process2(Liste_des_widgets2):
    process2 = create_process(models=models)
    # Air traffic evolution

    ## Growth rate by category [%]
    process2.parameters.cagr_passenger_short_range_reference_periods = [2020, 2030, 2040, 2050]
    process2.parameters.cagr_passenger_short_range_reference_periods_values = [3.0, 3.0, 3.0]
    process2.parameters.cagr_passenger_medium_range_reference_periods = []
    process2.parameters.cagr_passenger_medium_range_reference_periods_values = [3.0]
    process2.parameters.cagr_passenger_long_range_reference_periods = []
    process2.parameters.cagr_passenger_long_range_reference_periods_values = [3.0]
    process2.parameters.cagr_freight_reference_periods = []
    process2.parameters.cagr_freight_reference_periods_values = [3.0]

    # Aircraft fleet and operation evolution - Aircraft load factor

    ## Aircraft load factor in 2050 [%]
    process2.parameters.load_factor_end_year = 85  # 2019 value: 82.399312

    # Aircraft fleet and operation evolution - Aircraft efficiency using the top-down approach

    ## Drop-in aircraft
    ### Mean annual efficiency gains by category [%]
    process2.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years = []
    process2.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years_values = [0.5]
    process2.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years = []
    process2.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years_values = [0.5]
    process2.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years = []
    process2.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years_values = [0.5]

    ## Hydrogen aircraft
    ### Values for setting logistic functions by category
    process2.parameters.hydrogen_final_market_share_short_range = 0.0  # [%]
    process2.parameters.hydrogen_introduction_year_short_range = 2051
    process2.parameters.fleet_renewal_duration = 20.0
    ### Relative energy consumption for hydrogen aircraft with respect to drop-in aircraft [%]
    process2.parameters.relative_energy_per_ask_hydrogen_wrt_dropin_short_range_reference_years = []
    process2.parameters.relative_energy_per_ask_hydrogen_wrt_dropin_short_range_reference_years_values = [1.0]

    # Aircraft fleet and operation evolution - Operations

    ## Values for setting the logistic function
    process2.parameters.operations_final_gain = 8.0  # [%]
    process2.parameters.operations_start_year = 2025
    process2.parameters.operations_duration = 25.0

    # Aircraft energy - Introduction of alternative drop-in fuels

    ## Share of alternative fuels in the drop-in fuel mix (the rest being supplemented by kerosene) [%]
    process2.parameters.biofuel_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.biofuel_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]
    process2.parameters.electrofuel_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.electrofuel_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]

    # Carbon offset
    process2.parameters.carbon_offset_baseline_level_vs_2019_reference_periods = [2020, 2024, 2050]
    process2.parameters.carbon_offset_baseline_level_vs_2019_reference_periods_values = [500.0, 500.0]
    process2.parameters.residual_carbon_offset_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.residual_carbon_offset_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]

    # Environmental limits

    ## Carbon budgets and Carbon Dioxide Removal [GtCO2]
    process2.parameters.net_carbon_budget = 850.0
    process2.parameters.carbon_dioxyde_removal_2100 = 280.0

    ## Available energy resources in 2050 [EJ]
    process2.parameters.waste_biomass = 12.0
    process2.parameters.crops_biomass = 63.0
    process2.parameters.forest_residues_biomass = 17.0
    process2.parameters.agricultural_residues_biomass = 57.0
    process2.parameters.algae_biomass = 15.0
    process2.parameters.available_electricity = 250.0

    # Allocation settings

    ## Aviation share of the global (equivalent) carbon budget [%]
    process2.parameters.aviation_carbon_budget_allocated_share = 2.6
    process2.parameters.aviation_equivalentcarbonbudget_allocated_share = 5.1

    ## Aviation share of the global energy resources (biomass and electricity) [%]
    process2.parameters.aviation_biomass_allocated_share = 5.0
    process2.parameters.aviation_electricity_allocated_share = 5.0

    # Various environmental settings

    ## Share of biofuel production pathways (the rest being completed by AtJ processes) [%]
    process2.parameters.biofuel_hefa_fog_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.biofuel_hefa_fog_share_reference_years_values = [100, 100, 0.7, 0.7]
    process2.parameters.biofuel_hefa_others_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.biofuel_hefa_others_share_reference_years_values = [0.0, 0.0, 3.8, 3.8]
    process2.parameters.biofuel_ft_others_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.biofuel_ft_others_share_reference_years_values = [0.0, 0.0, 76.3, 76.3]
    process2.parameters.biofuel_ft_msw_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.biofuel_ft_msw_share_reference_years_values = [0.0, 0.0, 7.4, 7.4]

    ## Emission factors for electricity (2019 value: 429 gCO2/kWh)
    process2.parameters.electricity_emission_factor_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.electricity_emission_factor_reference_years_values = [429.0, 200.0, 100.0, 30.0]

    ## Share of hydrogen production pathways (the rest being completed by production via coal without CCS) [%]
    ## Distribution in 2019: Gas without CCS (71%), Coal without CCS (27%), Electrolysis (2%), Others with CCS (0%), Co-products not taken into account
    process2.parameters.hydrogen_electrolysis_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.hydrogen_electrolysis_share_reference_years_values = [2, 100, 100, 100]
    process2.parameters.hydrogen_gas_ccs_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.hydrogen_gas_ccs_share_reference_years_values = [0, 0, 0, 0]
    process2.parameters.hydrogen_coal_ccs_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.hydrogen_coal_ccs_share_reference_years_values = [0, 0, 0, 0]
    process2.parameters.hydrogen_gas_share_reference_years = [2020, 2030, 2040, 2050]
    process2.parameters.hydrogen_gas_share_reference_years_values = [71, 0, 0, 0]

    if Liste_des_widgets2 != []:
        #if Liste_des_widgets2[0].value:
        #if Liste_des_widgets2[1].value:

        if Liste_des_widgets2[5].value:
            process2.parameters.cagr_passenger_short_range_reference_periods_values = [1.0, 1.0, 1.0]
        if Liste_des_widgets2[2].value:
            process2.parameters.cagr_passenger_medium_range_reference_periods_values = [2.0]
            process2.parameters.cagr_passenger_long_range_reference_periods_values = [2.0]
            process2.parameters.cagr_freight_reference_periods_values = [2.0]
            if Liste_des_widgets2[5].value:
                process2.parameters.cagr_passenger_short_range_reference_periods_values = [0.0, 0.0, 0.0]        
        if Liste_des_widgets2[3].value:
            process2.parameters.residual_carbon_offset_share_reference_years_values = [0.0, 0.0, 20.0, 20.0]
        if Liste_des_widgets2[4].value:
            process2.parameters.biofuel_share_reference_years_values = [0.0, 4.8, 24.0, 35.0]
            process2.parameters.electrofuel_share_reference_years_values = [0.0, 1.2, 10.0, 35.0]
        if Liste_des_widgets2[6].value:
            process2.parameters.load_factor_end_year = 90
            process2.parameters.operations_final_gain = 10.0  # [%]
            process2.parameters.operations_start_year = 2025
            process2.parameters.operations_duration = 25.0
        if Liste_des_widgets2[7].value:
            process2.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years_values = [1.0]
            process2.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years_values = [1.0]
            process2.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years_values = [1.0]
            process2.parameters.hydrogen_final_market_share_short_range = 50.0  # [%]
            process2.parameters.hydrogen_introduction_year_short_range = 2035
            process2.parameters.fleet_renewal_duration = 15.0
        
    process2.compute()
    return process2.data

def compute_process3(Liste_des_widgets3):
    process3 = create_process(models=models)
    # Air traffic evolution

    ## Growth rate by category [%]
    process3.parameters.cagr_passenger_short_range_reference_periods = [2020, 2030, 2040, 2050]
    process3.parameters.cagr_passenger_short_range_reference_periods_values = [3.0, 3.0, 3.0]
    process3.parameters.cagr_passenger_medium_range_reference_periods = []
    process3.parameters.cagr_passenger_medium_range_reference_periods_values = [3.0]
    process3.parameters.cagr_passenger_long_range_reference_periods = []
    process3.parameters.cagr_passenger_long_range_reference_periods_values = [3.0]
    process3.parameters.cagr_freight_reference_periods = []
    process3.parameters.cagr_freight_reference_periods_values = [3.0]

    # Aircraft fleet and operation evolution - Aircraft load factor

    ## Aircraft load factor in 2050 [%]
    process3.parameters.load_factor_end_year = 85  # 2019 value: 82.399312

    # Aircraft fleet and operation evolution - Aircraft efficiency using the top-down approach

    ## Drop-in aircraft
    ### Mean annual efficiency gains by category [%]
    process3.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years = []
    process3.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years_values = [0.5]
    process3.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years = []
    process3.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years_values = [0.5]
    process3.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years = []
    process3.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years_values = [0.5]

    ## Hydrogen aircraft
    ### Values for setting logistic functions by category
    process3.parameters.hydrogen_final_market_share_short_range = 0.0  # [%]
    process3.parameters.hydrogen_introduction_year_short_range = 2051
    process3.parameters.fleet_renewal_duration = 20.0
    ### Relative energy consumption for hydrogen aircraft with respect to drop-in aircraft [%]
    process3.parameters.relative_energy_per_ask_hydrogen_wrt_dropin_short_range_reference_years = []
    process3.parameters.relative_energy_per_ask_hydrogen_wrt_dropin_short_range_reference_years_values = [1.0]

    # Aircraft fleet and operation evolution - Operations

    ## Values for setting the logistic function
    process3.parameters.operations_final_gain = 8.0  # [%]
    process3.parameters.operations_start_year = 2025
    process3.parameters.operations_duration = 25.0

    # Aircraft energy - Introduction of alternative drop-in fuels

    ## Share of alternative fuels in the drop-in fuel mix (the rest being supplemented by kerosene) [%]
    process3.parameters.biofuel_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.biofuel_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]
    process3.parameters.electrofuel_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.electrofuel_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]

    # Carbon offset
    process3.parameters.carbon_offset_baseline_level_vs_2019_reference_periods = [2020, 2024, 2050]
    process3.parameters.carbon_offset_baseline_level_vs_2019_reference_periods_values = [500.0, 500.0]
    process3.parameters.residual_carbon_offset_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.residual_carbon_offset_share_reference_years_values = [0.0, 0.0, 0.0, 0.0]

    # Environmental limits

    ## Carbon budgets and Carbon Dioxide Removal [GtCO2]
    process3.parameters.net_carbon_budget = 850.0
    process3.parameters.carbon_dioxyde_removal_2100 = 280.0

    ## Available energy resources in 2050 [EJ]
    process3.parameters.waste_biomass = 12.0
    process3.parameters.crops_biomass = 63.0
    process3.parameters.forest_residues_biomass = 17.0
    process3.parameters.agricultural_residues_biomass = 57.0
    process3.parameters.algae_biomass = 15.0
    process3.parameters.available_electricity = 250.0

    # Allocation settings

    ## Aviation share of the global (equivalent) carbon budget [%]
    process3.parameters.aviation_carbon_budget_allocated_share = 2.6
    process3.parameters.aviation_equivalentcarbonbudget_allocated_share = 5.1

    ## Aviation share of the global energy resources (biomass and electricity) [%]
    process3.parameters.aviation_biomass_allocated_share = 5.0
    process3.parameters.aviation_electricity_allocated_share = 5.0

    # Various environmental settings

    ## Share of biofuel production pathways (the rest being completed by AtJ processes) [%]
    process3.parameters.biofuel_hefa_fog_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.biofuel_hefa_fog_share_reference_years_values = [100, 100, 0.7, 0.7]
    process3.parameters.biofuel_hefa_others_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.biofuel_hefa_others_share_reference_years_values = [0.0, 0.0, 3.8, 3.8]
    process3.parameters.biofuel_ft_others_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.biofuel_ft_others_share_reference_years_values = [0.0, 0.0, 76.3, 76.3]
    process3.parameters.biofuel_ft_msw_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.biofuel_ft_msw_share_reference_years_values = [0.0, 0.0, 7.4, 7.4]

    ## Emission factors for electricity (2019 value: 429 gCO2/kWh)
    process3.parameters.electricity_emission_factor_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.electricity_emission_factor_reference_years_values = [429.0, 200.0, 100.0, 30.0]

    ## Share of hydrogen production pathways (the rest being completed by production via coal without CCS) [%]
    ## Distribution in 2019: Gas without CCS (71%), Coal without CCS (27%), Electrolysis (2%), Others with CCS (0%), Co-products not taken into account
    process3.parameters.hydrogen_electrolysis_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.hydrogen_electrolysis_share_reference_years_values = [2, 100, 100, 100]
    process3.parameters.hydrogen_gas_ccs_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.hydrogen_gas_ccs_share_reference_years_values = [0, 0, 0, 0]
    process3.parameters.hydrogen_coal_ccs_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.hydrogen_coal_ccs_share_reference_years_values = [0, 0, 0, 0]
    process3.parameters.hydrogen_gas_share_reference_years = [2020, 2030, 2040, 2050]
    process3.parameters.hydrogen_gas_share_reference_years_values = [71, 0, 0, 0]

    if Liste_des_widgets3 != []:
        #if Liste_des_widgets3[0].value:
        #if Liste_des_widgets3[1].value:
        if Liste_des_widgets3[5].value:
            process3.parameters.cagr_passenger_short_range_reference_periods_values = [1.0, 1.0, 1.0]
        if Liste_des_widgets3[2].value:
            process3.parameters.cagr_passenger_medium_range_reference_periods_values = [2.0]
            process3.parameters.cagr_passenger_long_range_reference_periods_values = [2.0]
            process3.parameters.cagr_freight_reference_periods_values = [2.0]
            if Liste_des_widgets3[5].value:
                process3.parameters.cagr_passenger_short_range_reference_periods_values = [0.0, 0.0, 0.0]
        if Liste_des_widgets3[3].value:
            process3.parameters.residual_carbon_offset_share_reference_years_values = [0.0, 0.0, 20.0, 20.0]
        if Liste_des_widgets3[4].value:
            process3.parameters.biofuel_share_reference_years_values = [0.0, 4.8, 24.0, 35.0]
            process3.parameters.electrofuel_share_reference_years_values = [0.0, 1.2, 10.0, 35.0]
        if Liste_des_widgets3[6].value:
            process3.parameters.load_factor_end_year = 90
            process3.parameters.operations_final_gain = 10.0  # [%]
            process3.parameters.operations_start_year = 2025
            process3.parameters.operations_duration = 25.0
        if Liste_des_widgets3[7].value:
            process3.parameters.energy_per_ask_short_range_dropin_fuel_gain_reference_years_values = [1.0]
            process3.parameters.energy_per_ask_medium_range_dropin_fuel_gain_reference_years_values = [1.0]
            process3.parameters.energy_per_ask_long_range_dropin_fuel_gain_reference_years_values = [1.0]
            process3.parameters.hydrogen_final_market_share_short_range = 50.0  # [%]
            process3.parameters.hydrogen_introduction_year_short_range = 2035
            process3.parameters.fleet_renewal_duration = 15.0

    process3.compute()
    return process3.data






	
