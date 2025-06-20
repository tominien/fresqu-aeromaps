from typing import Any, Dict, List, Optional
from pandas import DataFrame
from bqplot import Figure, Lines, Axis, LinearScale, ColorScale
from .base_graph import BaseGraph




class ProspectiveScenarioGraph(BaseGraph):
    """
    Graph class for CO2 emissions prospectives.

    Implements the `draw()` and `update()` methods.

    #### Arguments :
    - `figure_title (str)` : Title of the figure.
    - `color_palette (Optional[List[str]])` : Optional list of **7** colors for the graph.
    """
    def __init__(
            self,
            figure_title: str,
            color_palette: Optional[List[str]] = None
        ) -> None:
        super().__init__()
        self.figure_title = figure_title
        self.color_palette = color_palette if (color_palette and len(color_palette) == 7) else ["#000000", "#1f77b4", "#ff7f0e", "#2ca02c", "#8c564b", "#9467bd", "#d62728"]

        # Placeholders for marks :
        self._historic_line: Lines = None
        self._prospective_lines: Lines = None
        self._aspects_areas: Lines = None


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
        self._historic_line = Lines(
            x = historic_years,
            y = DF_climate_outputs.loc[historic_years, "co2_emissions"],
            color = [0],
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
            color = [0, 6],
            labels = [
                "Historique (2000-2019) / Croissance de 3% par an (2019-2050)",
                "Business as usual (2019-2050)"
            ],
            display_legend = True,
            scales = {"x": x_scale, "y": y_scale, "color": color_scale}
        )
        # Plot the aspects areas :
        aspects_y_areas = [
            DF_vector_outputs.loc[years, "co2_emissions_2019technology_baseline3"],
            DF_vector_outputs.loc[years, "co2_emissions_2019technology"],
            DF_vector_outputs.loc[years, "co2_emissions_including_aircraft_efficiency"],
            DF_vector_outputs.loc[years, "co2_emissions_including_load_factor"],
            DF_vector_outputs.loc[years, "co2_emissions_including_energy"],
        ]
        indices = [1, 2, 3, 4, 5]
        self._aspects_areas = Lines(
            x = years,
            y = aspects_y_areas,
            color = indices,
            stroke_width = 0,
            fill = 'between',
            fill_colors = [self.color_palette[i] for i in indices],
            fill_opacities = [0.3] * len(indices),
            labels = [
                "Changement de la demande",
                "Efficacité technologique",
                "Opérations en vol",
                "Energies alternatives",
                "Compensation carbone"
            ],
            display_legend = True,
            scales = {"x": x_scale, "y": y_scale, "color": color_scale}
        )

        # Create the figure with all marks, axes and a legend :
        self.figure = Figure(
            marks = [self._historic_line, self._prospective_lines, self._aspects_areas],
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
        self._prospective_lines.y = [
            DF_vector_outputs.loc[prospective_years, "co2_emissions_2019technology_baseline3"],
            DF_climate_outputs.loc[prospective_years, "co2_emissions"] - DF_vector_outputs.loc[prospective_years, "carbon_offset"]
        ]
        # Update the aspects areas data (updating the x-axis is not necessary as it remains constant) :
        self._aspects_areas.y = [
            DF_vector_outputs.loc[years, "co2_emissions_2019technology_baseline3"],
            DF_vector_outputs.loc[years, "co2_emissions_2019technology"],
            DF_vector_outputs.loc[years, "co2_emissions_including_aircraft_efficiency"],
            DF_vector_outputs.loc[years, "co2_emissions_including_load_factor"],
            DF_vector_outputs.loc[years, "co2_emissions_including_energy"]
        ]

        return self.figure
