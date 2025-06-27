from typing import Any, Dict, List, Optional
from pandas import DataFrame, concat

from utils import generate_pastel_palette, float_to_int_string

import json
from pathlib import Path

from bqplot import Figure, Lines, Axis, LinearScale, ColorScale, Label
from .base_graph import BaseGraph

from crud.crud_aspects import get_aspects_names




# Load the aspects names from the database :
ASPECTS_NAMES: Dict[str, str] = get_aspects_names()

# Load the prospective scenario JSON file :
PROSPECTIVE_SCENARIO_JSON_PATH = Path(__file__).resolve().parents[2] / "data" / "prospective_scenario.json"
with open(PROSPECTIVE_SCENARIO_JSON_PATH, "r", encoding="utf-8") as file:
    PROSPECTIVE_SCENARIO_JSON = json.load(file)


class ProspectiveScenarioGraph(BaseGraph):
    """
    Graph class for CO2 emissions prospectives.

    Implements the `draw()` and `update()` methods.

    #### Arguments :
    - `figure_title (str)` : Title of the figure.
    - `color_palette (Optional[List[str]])` : Optional list of **`n + 3`** colors for the graph, where `n` represents the number of aspects. The color order applies the following logic :
        - Index 0 : Line "Historic", ranging from 2000 to 2019 included.
        - Index 1 : Line "Worst case scenario / No aspects considered", ranging from 2019 to 2050 incled (top line, including no aspects).
        - Index 2 : Line "Business as usual / All aspects considered", ranging from 2019 to 2050 included (bottom line, combining all aspects).
        - Index k, k ∈ [3, n + 3] : Area of the aspect k (position k in the `ASPECTS_NAMES` dictionary), ranging from 2019 to 2050 included.
    """
    def __init__(
            self,
            figure_title: str,
            color_palette: Optional[List[str]] = None
        ) -> None:
        super().__init__()

        self.figure_title = figure_title
        self.color_palette = (
            color_palette
            if (color_palette and len(color_palette) == len(ASPECTS_NAMES) + 3)
            else ["#8c564b", "#000000", "#d62728"] + generate_pastel_palette(len(ASPECTS_NAMES) + 1)
        )

        # Placeholders for marks :
        self._historic_line: Lines        = None
        self._prospective_lines: Lines    = None
        self._aspects_areas: Lines        = None
        self._aspects_labels: List[Label] = []
        self._past_shade: Lines           = None


    def draw(
            self,
            process_data: Dict[str, Any],
            override: bool = False
        ) -> Figure:
        """
        Create **initial** figure with historical, prospective, and aspects areas.

        If the figure is already drawn and you just want to update the data, it is recommended to use the `update()` method instead.
        This method will not redraw the figure but will update the lines' data only.

        However, if you want to redraw the figure completely, you can set `override = True` to force a redraw.
        This action takes more time and resources to execute.

        #### Arguments :
        - `process_data (Dict[str, Any])` : Data dictionary containing the necessary data for plotting the initial graph.
        - `override (bool)` : If `True`, forces a redraw of the figure, even if it has already been drawn. Defaults to `False`.

        #### Returns :
        - `Figure` : The initial figure with historical, prospective, and aspects areas.
        """
        # Check is the figure is already drawn and if override is set to False :
        if self.figure is not None and not override :
            return self.update(process_data)

        # Get the data from process_data :
        DF_vector_outputs: DataFrame  = process_data["vector_outputs"]
        DF_climate_outputs: DataFrame = process_data["climate_outputs"]
        years: List[int]              = process_data["years"]["full_years"]        # List of intergers ranging from 2000 to 2050 included.
        historic_years: List[int]     = process_data["years"]["historic_years"]    # List of intergers ranging from 2000 to 2019 included.
        prospective_years: List[int]  = process_data["years"]["prospective_years"] # List of intergers ranging from 2019 to 2050 included.

        # Create scales and axes :
        x_scale = LinearScale()
        y_scale = LinearScale()
        color_scale = ColorScale(colors = self.color_palette)
        x_axis = Axis(
            scale = x_scale,
            label = "Années",
            num_ticks = 6, # Display : 2000, 2010, 2020, 2030, 2040, 2050.
            label_offset = "40px"
        )
        y_axis = Axis(
            scale = y_scale,
            orientation = "vertical",
            label = "Emissions de CO2, en Mt",
            label_offset = "40px"
        )

        # Plot the historic line :
        historic_y_line = DF_climate_outputs.loc[historic_years, "co2_emissions"]
        self._historic_line = Lines(
            x = historic_years,
            y = historic_y_line,
            color = [0],
            labels = PROSPECTIVE_SCENARIO_JSON["historic_line_name"],
            display_legend = True,
            scales = {"x": x_scale, "y": y_scale, "color": color_scale}
        )
        # Plot the prospective lines :
        prospective_y_lines = [
            DF_vector_outputs.loc[prospective_years, "co2_emissions_2019technology_baseline3"],
            DF_climate_outputs.loc[prospective_years, "co2_emissions"] - DF_vector_outputs.loc[prospective_years, "carbon_offset"]
        ]
        self._prospective_lines = Lines(
            x = prospective_years,
            y = prospective_y_lines,
            color = [1, 2],
            labels = [
                PROSPECTIVE_SCENARIO_JSON["no_aspects_line_name"],
                PROSPECTIVE_SCENARIO_JSON["every_aspects_line_name"]
            ],
            display_legend = True,
            line_style = "dashed", # Make the prospective lines dashed.
            scales = {"x": x_scale, "y": y_scale, "color": color_scale}
        )
        # Plot the aspects areas :
        aspects_y_areas = [
            DF_vector_outputs.loc[years, "co2_emissions_2019technology_baseline3"],
            DF_vector_outputs.loc[years, "co2_emissions_2019technology"],
            DF_vector_outputs.loc[years, "co2_emissions_including_aircraft_efficiency"],
            DF_vector_outputs.loc[years, "co2_emissions_including_load_factor"],
            DF_vector_outputs.loc[years, "co2_emissions_including_energy"],
            DF_vector_outputs.loc[years, "co2_emissions_including_energy"] - DF_vector_outputs.loc[years, "carbon_offset"]
        ]
        indices = [index for index in range(3, len(self.color_palette))]
        self._aspects_areas = Lines(
            x = years,
            y = aspects_y_areas,
            color = indices,
            stroke_width = 0,
            fill = 'between',
            fill_colors = [self.color_palette[i] for i in indices[:-1]],
            fill_opacities = [0.3] * (len(indices) - 1),
            labels = [*ASPECTS_NAMES.values(), ""], # Empty label for the last area to avoid legend entry (corresponds to the "Buisness as usual" line).
            display_legend = True,
            scales = {"x": x_scale, "y": y_scale, "color": color_scale}
        )

        # Display the final values of the prospective lines on the right side of the graph :
        prospective_years_final_value = [serie.iloc[-1] for serie in prospective_y_lines]
        prospective_years_final_value_formatted = [float_to_int_string(value) for value in prospective_years_final_value]
        self._prospective_labels = Label(
            x = [years[-1], years[-1]], # Position the labels at the end of the prospective lines.
            y = prospective_years_final_value, # Position the labels at the same height as the end of both prospective lines.
            color = [1, 2],
            text = prospective_years_final_value_formatted,
            default_size = 12, # Size of the labels (12px).
            align = 'start',
            x_offset = 8,
            scales = {'x': x_scale, 'y': y_scale, 'color': color_scale},
            apply_clip = False
        )

        # Create the past shade area (from 2000 to 2019 / nowadays) :
        start_year = years[0]
        end_year = 2019 # Which you can replace by "date.today().year" (also add "from datetime import date" on top of the file) to meke the gray area go up to the current year.
        all_y_lines = concat([historic_y_line] + prospective_y_lines + aspects_y_areas) # To determine the y-axis limits of the past shade area.
        y_min = min(all_y_lines) if not all_y_lines.empty else 0
        y_max = max(all_y_lines) if not all_y_lines.empty else 0
        self._past_shade = Lines(
            x = [start_year, end_year, end_year, start_year, start_year],
            y = [y_min, y_min, y_max, y_max, y_min],
            scales = {"x": x_scale, "y": y_scale},
            fill = "inside",
            fill_colors = ["lightgrey"],
            fill_opacities = [0.3],
            stroke_width = 0,
            display_legend = False
        )

        # Create the figure with all marks, axes and the legend :
        self.figure = Figure(
            marks = [
                # self._past_shade,
                self._historic_line,
                self._prospective_lines,
                self._aspects_areas,
                self._prospective_labels
            ],
            axes = [x_axis, y_axis],
            title = self.figure_title,
            animation_duration = 1000,
            legend_location = 'top-left',
            legend_style = {'stroke-width': 0}
        )
        return self.figure


    def update(self, process_data: Dict[str, Any]) -> Figure:
        """
        Update lines' data only, avoiding full redraw.
        This method updates the existing figure with new data without redrawing the entire figure.

        #### Arguments :
        - `process_data (Dict[str, Any])` : New processed data to update the figure.

        #### Returns :
        - `Figure` : The updated figure object with new data.
        """
        # Check if the figure is already drawn :
        if self.figure is None:
            return self.draw(process_data, override = True)

        # Get the data from process_data :
        DF_vector_outputs: DataFrame  = process_data["vector_outputs"]
        DF_climate_outputs: DataFrame = process_data["climate_outputs"]
        years: List[int]              = process_data["years"]["full_years"]        # List of intergers ranging from 2000 to 2050 included.
        prospective_years: List[int]  = process_data["years"]["prospective_years"] # List of intergers ranging from 2019 to 2050 included.

        # Updating the historic line data is not necessary as it remains constant.
        # Update the prospective lines data (updating the x-axis is not necessary as it remains constant) :
        prospective_lines_top_line = DF_vector_outputs.loc[prospective_years, "co2_emissions_2019technology_baseline3"]
        prospective_lines_bottom_line = DF_climate_outputs.loc[prospective_years, "co2_emissions"] - DF_vector_outputs.loc[prospective_years, "carbon_offset"]
        self._prospective_lines.y = [
            prospective_lines_top_line,
            prospective_lines_bottom_line
        ]
        # Update the aspects areas data (updating the x-axis is not necessary as it remains constant) :
        self._aspects_areas.y = [
            DF_vector_outputs.loc[years, "co2_emissions_2019technology_baseline3"],
            DF_vector_outputs.loc[years, "co2_emissions_2019technology"],
            DF_vector_outputs.loc[years, "co2_emissions_including_aircraft_efficiency"],
            DF_vector_outputs.loc[years, "co2_emissions_including_load_factor"],
            DF_vector_outputs.loc[years, "co2_emissions_including_energy"],
            DF_vector_outputs.loc[years, "co2_emissions_including_energy"] - DF_vector_outputs.loc[years, "carbon_offset"]
        ]
        # Update the prospective labels data (updating the x-axis is not necessary as it remains constant) :
        self._prospective_labels.y = [
            prospective_lines_top_line.iloc[-1],
            prospective_lines_bottom_line.iloc[-1]
        ]
        self._prospective_labels.text = [
            float_to_int_string(prospective_lines_top_line.iloc[-1]),
            float_to_int_string(prospective_lines_bottom_line.iloc[-1])
        ]

        return self.figure
