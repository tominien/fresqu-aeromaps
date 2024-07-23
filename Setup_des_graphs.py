
import bqplot as bq
import numpy as np 
from bqplot import LinearScale, Lines, Axis, Figure, ColorScale
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

