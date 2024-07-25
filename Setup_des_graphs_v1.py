
import bqplot as bq
import numpy as np 
from bqplot import LinearScale, Lines, Axis, Figure, ColorScale, OrdinalScale, Bars
sc_x = LinearScale()
sc_y = LinearScale()
sc_col = ColorScale(colors=["Black","Blue", "Yellow","Orange","Green","Magenta","Red"])

def plot_traj(process_data):
    

    df = process_data["vector_outputs"]
    df_climate = process_data["climate_outputs"]
    years = process_data["years"]["full_years"]
    historic_years = process_data["years"]["historic_years"]
    prospective_years = process_data["years"]["prospective_years"]
    
    ax_x = Axis(scale=sc_x, label="Années")
    ax_y = Axis(scale=sc_y, orientation="vertical", label="Emissions de CO2, en Mt")

    line = Lines(
        x=years, 
        y=[df.loc[years,"co2_emissions_2019technology_baseline3"],
           df["co2_emissions_2019technology"],
           df["co2_emissions_including_aircraft_efficiency"],
           df["co2_emissions_including_load_factor"],
           df["co2_emissions_including_energy"],
           df_climate.loc[years, "co2_emissions"] - df.loc[years, "carbon_offset"]],
        color=[1,2,3,4,5,6],
        stroke_width=0,
        fill='between',
        fill_colors=["Blue","Yellow","Orange","Green","Magenta"],
        fill_opacities=[0.3]*5,
        labels=["Changement de la demande","Efficacité technologique","Opérations en vol",
                "Energies alternatives","Compensation carbone","Emission restantes"],
        display_legend=True,
        scales={"x": sc_x, "y": sc_y, "color" : sc_col},
    )

    line_h = Lines(
        x=historic_years, 
        y=df_climate.loc[historic_years, "co2_emissions"],
        color=[0], 
        scales={"x": sc_x, "y": sc_y, "color" : sc_col}
    )

    line_p = Lines(
        x=prospective_years, 
        y=[df_climate.loc[prospective_years, "co2_emissions"] - df.loc[prospective_years, "carbon_offset"],
           df.loc[prospective_years,"co2_emissions_2019technology_baseline3"]],
        color=[6,0], 
        scales={"x": sc_x, "y": sc_y, "color" : sc_col},
    )
    

    return [line,line_h,line_p]
    
categories = ["Climat\n(Total)","Climat\n(CO₂)","Biomasse","Electricité"]
x_ord = OrdinalScale()
y_sc = LinearScale()

def plot_multi(process_data):
    parameters = process_data["float_inputs"]
    df = process_data["vector_outputs"]
    df_climate = process_data["climate_outputs"]
    float_outputs = process_data["float_outputs"]
    years = process_data["years"]["full_years"]
    historic_years = process_data["years"]["historic_years"]
    prospective_years = process_data["years"]["prospective_years"]

    # Carbon budget
    gross_carbon_budget = float(float_outputs["gross_carbon_budget_2050"])
    aviation_carbon_budget = float(float_outputs["aviation_carbon_budget"])
    cumulative_co2_emissions = float(df.loc[2050, "cumulative_co2_emissions"])

    # Biomass
    available_biomass_total = float_outputs["available_biomass_total"]
    aviation_available_biomass = float_outputs["aviation_available_biomass"]
    biomass_consumption_end_year = float_outputs["biomass_consumption_end_year"]

    # Electricity
    available_electricity_total = parameters["available_electricity"]
    aviation_available_electricity = float_outputs["aviation_available_electricity"]
    electricity_consumption_end_year = float_outputs["electricity_consumption_end_year"]

    # Effective radiative forcing
    equivalent_gross_carbon_budget = float(float_outputs["equivalent_gross_carbon_budget_2050"])
    aviation_equivalent_carbon_budget = float(float_outputs["aviation_equivalent_carbon_budget"])
    cumulative_total_equivalent_emissions = float(df_climate.loc[2050, "cumulative_total_equivalent_emissions"])

    budgets = [
        aviation_equivalent_carbon_budget / equivalent_gross_carbon_budget * 100,
        aviation_carbon_budget / gross_carbon_budget * 100,
        aviation_available_biomass / available_biomass_total * 100,
        aviation_available_electricity / available_electricity_total * 100,]

    consumptions = [
        np.max([cumulative_total_equivalent_emissions / equivalent_gross_carbon_budget * 100, 0]),
        cumulative_co2_emissions / gross_carbon_budget * 100,
        biomass_consumption_end_year / available_biomass_total * 100,
        electricity_consumption_end_year / available_electricity_total * 100,]

    return [consumptions,budgets]
