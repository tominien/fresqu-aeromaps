from typing import Any, Dict, List, Tuple, Optional

from pandas import concat

from bqplot import Figure, Lines, Axis, LinearScale, Label
from bqplot_figures.base_graph import BaseGraph

from core.aeromaps_utils.extract_processed_data import get_years

from bqplot_figures.utils.prospective_scenario_graph_utils import (
    get_y_historic_line,
    get_y_prospective_lines,
    get_y_aspects_areas,
    get_y_prospective_lines_groups_comparison,
    get_y_final_values_lines,
    LINES_NAMES,
    ASPECTS_NAMES,
    NUMBER_OF_ASPECTS,
    DEFAULT_LINES_COLORS
)
from utils import generate_pastel_palette




def get_prospective_scenario_y_scales(processes_data: Dict[str, Any]) -> Tuple[float, float]:
    """
    Get the minimal and maximal values of all the y-scales for the historic line, prospective lines and aspects areas from multiple processes data.

    #### Arguments :
    - `processes_data (List[Dict[str, Any]])` : A list of processes data from AéroMAPS.

    #### Returns :
    - `Tuple[float]` : A tuple containing the minimal and maximal values of all the y-scales for the budget and consumption bars.
    """
    # Get the y-values for the historic line, prospective lines and aspects areas from all processes data :
    all_y_lines = []
    for process_data in processes_data:
        # Get the y-values for the historic line :
        y_historic_line = get_y_historic_line(process_data)
        all_y_lines.extend(y_historic_line.tolist())

        # Get the y-values for the prospective lines :
        y_prospective_lines = get_y_prospective_lines(process_data)
        for y_prospective_line in y_prospective_lines:
            all_y_lines.extend(y_prospective_line.tolist())

        # Get the y-values for the aspects areas :
        y_aspects_areas = get_y_aspects_areas(process_data)
        for y_aspect_area in y_aspects_areas:
            all_y_lines.extend(y_aspect_area.tolist())

    return (min(all_y_lines), max(all_y_lines)) if all_y_lines else (0.0, 0.0)


class ProspectiveScenarioGraph(BaseGraph):
    """
    Graph class for CO₂ emissions prospectives.

    Implements the `draw()`, `update()` and `get_legend_elements()` methods.

    #### Arguments :
    - `figure_title (str)` : Title of the figure.
    - `color_palette (Optional[List[str]])` : Optional list of **`n + 3`** colors for the graph, where `n` represents the number of aspects. The color order applies the following logic :
        - Index 0 : Line "Historic", ranging from 2000 to 2019 included.
        - Index 1 : Line "Worst case scenario / No aspects considered", ranging from 2019 to 2050 incled (top line, including no aspects).
        - Index 2 : Line "Business as usual / All aspects considered", ranging from 2019 to 2050 included (bottom line, combining all aspects).
        - Index k, k ∈ [3, n + 3] : Area of the aspect k (position k in the `ASPECTS_NAMES` list), ranging from 2019 to 2050 included.
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
            if (color_palette and len(color_palette) == NUMBER_OF_ASPECTS + 3)
            else DEFAULT_LINES_COLORS + generate_pastel_palette(NUMBER_OF_ASPECTS)
        )

        # Placeholders for marks :
        self._historic_line: Lines            = None
        self._prospective_lines: Lines        = None
        self._aspects_areas: Lines            = None
        self._past_shade: Lines               = None
        self._prospective_final_values: Label = None


    def draw(
            self,
            process_data: Dict[str, Any],
            y_scale: LinearScale = None,
            override: bool = False,
            display_default_legend: bool = True
        ) -> Figure:
        """
        Create **initial** figure with the historical, prospective, and aspects areas.

        If the figure is already drawn and you just want to update the data, it is recommended to use the `update()` method instead.
        This method will not redraw the figure but will update the lines' data only.

        However, if you want to redraw the figure completely, you can set `override = True` to force a redraw.
        This action takes more time and resources to execute.

        #### Arguments :
        - `process_data (Dict[str, Any])` : Data dictionary containing the necessary data for plotting the initial graph.
        - `y_scale (LinearScale)` : Optional scale for the y-axis. If not provided, a default scale will be created.
        - `override (bool)` : If `True`, forces a redraw of the figure, even if it has already been drawn. Defaults to `False`.
        - `display_default_legend (bool)` : If `True`, the legend will be displayed. Defaults to `True`.

        #### Returns :
        - `Figure` : The initial figure with historical, prospective, and aspects areas plotted.
        """
        # Check is the figure is already drawn and if override is set to False :
        super().draw(process_data, override)

        # Extract the years from the process_data :
        years: Dict[str, List[int]]   = get_years(process_data)
        full_years: List[int]         = years["full_years"]        # List of intergers ranging from 2000 to 2050 included.
        historic_years: List[int]     = years["historic_years"]    # List of intergers ranging from 2000 to 2019 included.
        prospective_years: List[int]  = years["prospective_years"] # List of intergers ranging from 2019 to 2050 included.

        # Create scales and axes :
        x_scale = LinearScale()
        y_scale = y_scale or LinearScale()
        x_axis = Axis(
            scale = x_scale,
            label = "Années",
            num_ticks = 6, # Display : 2000, 2010, 2020, 2030, 2040, 2050.
            label_offset = "40px"
        )
        y_axis = Axis(
            scale = y_scale,
            orientation = "vertical",
            label = "Emissions de CO₂ (en Mt)",
            label_offset = "40px"
        )

        # Plot the historic line :
        y_historic_line = get_y_historic_line(process_data)
        colors_historic_line = [self.color_palette[0]]

        self._historic_line = Lines(
            x = historic_years,
            y = y_historic_line,
            colors = colors_historic_line,
            labels = LINES_NAMES[0],
            display_legend = display_default_legend,
            scales = {"x": x_scale, "y": y_scale}
        )

        # Plot the prospective lines :
        y_prospective_lines = get_y_prospective_lines(process_data)
        colors_prospective_lines = [self.color_palette[1], self.color_palette[2]]

        self._prospective_lines = Lines(
            x = prospective_years,
            y = y_prospective_lines,
            colors = colors_prospective_lines,
            labels = [
                LINES_NAMES[1],
                LINES_NAMES[2]
            ],
            display_legend = display_default_legend,
            line_style = "dashed",
            scales = {"x": x_scale, "y": y_scale}
        )

        # Plot the aspects areas :
        y_aspects_areas = get_y_aspects_areas(process_data)
        colors_aspects_areas = [self.color_palette[index] for index in range(3, NUMBER_OF_ASPECTS + 3)]

        self._aspects_areas = Lines(
            x = full_years,
            y = y_aspects_areas,
            colors = colors_aspects_areas,
            stroke_width = 0,
            fill = "between",
            fill_colors = colors_aspects_areas,
            fill_opacities = [0.3] * len(colors_aspects_areas),
            labels = [*ASPECTS_NAMES, ""], # Empty label for the last area to avoid legend entry (corresponds to the "no aspects" line).
            display_legend = display_default_legend,
            scales = {"x": x_scale, "y": y_scale}
        )

        # Plot / display the final values of the prospective lines on the right side of the graph :
        y_prospective_years_final_value, text_prospective_final_values = get_y_final_values_lines(y_prospective_lines)

        self._prospective_final_values = Label(
            x = [full_years[-1]] * 2,            # Position the final values at the end of the prospective lines.
            y = y_prospective_years_final_value, # Position the formatted final values at the same height as the end of both prospective lines.
            colors = colors_prospective_lines,
            text = text_prospective_final_values,
            default_size = 12,
            align = "start",
            x_offset = 8,
            scales = {"x": x_scale, "y": y_scale},
            apply_clip = False
        )

        # Plot the past shade area (from 2000 to 2019 / nowadays) :
        start_year = full_years[0]
        end_year = 2019 # Which you can replace by "date.today().year" (also add "from datetime import date" on top of the file) to make the gray area go up to the current year.
        all_y_lines = concat([y_historic_line] + y_prospective_lines + y_aspects_areas) # To determine the y-axis limits of the past shade area.
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
                self._prospective_final_values
            ],
            axes = [x_axis, y_axis],
            title = self.figure_title,
            animation_duration = 1000,
            legend_location = "top-left",
            legend_style = {"stroke-width": 0}
        )

        return self.figure


    def update(self, process_data: Dict[str, Any]) -> Figure:
        # Check if the figure is already drawn :
        super().update(process_data)

        # Update the figure :
        with self.figure.hold_sync():
            # Updating the historic line data is not necessary as it remains constant.
            
            y_prospective_lines = get_y_prospective_lines(process_data)
            y_prospective_final_values, text_prospective_final_values = get_y_final_values_lines(y_prospective_lines)
            # Update the y-axis of the prospective lines (updating the x-axis is not necessary as it remains constant) :
            self._prospective_lines.y = [y_prospective_line.tolist() for y_prospective_line in y_prospective_lines] # Use of the ".tolist()" method to force a BQPlot update of the data.
            # Update the y-axis of the text of the prospective final values (updating the x-axis is not necessary as it remains constant) :
            self._prospective_final_values.y = y_prospective_final_values
            # Update the text content of the text of the prospective final values :
            self._prospective_final_values.text = text_prospective_final_values
            
            # Update the y-axis of the aspects areas (updating the x-axis is not necessary as it remains constant) :
            self._aspects_areas.y = [y_aspect_area.tolist() for y_aspect_area in get_y_aspects_areas(process_data)] # Use of the ".tolist()" method to force a BQPlot update of the data.

        return self.figure


    def get_legend_elements(self) -> Tuple[List[str], List[str], List[str]]:
        # Check if the figure is already drawn :
        super().get_legend_elements()

        # Get the legend elements :
        colors    = self._historic_line.colors + self._prospective_lines.colors + self._aspects_areas.colors
        labels    = self._historic_line.labels + self._prospective_lines.labels + self._aspects_areas.labels
        opacities = self._historic_line.opacities + self._prospective_lines.opacities + self._aspects_areas.fill_opacities

        return colors, labels, opacities


class ProspectiveScenarioGroupComparisonGraph(BaseGraph):
    """
    Graph class for group comparaison of CO₂ emissions prospectives.

    Implements the `draw()`, `update()` and `get_legend_elements()` methods.

    #### Arguments :
    - `figure_title (str)` : Title of the figure.
    - `number_of_groups (int)` : Number of groups to compare in the graph (Reference scenario excluded).
    - `color_palette (Optional[List[str]])` : Optional list of **`n + 3`** colors for the graph, where `n` is the number of groups. The color order applies the following logic :
        - Index 0 : Line "Historic", ranging from 2000 to 2019 included.
        - Index 1 : Line "Worst case scenario / No aspects considered", from the reference scenario.
        - Index 2 : Line "Business as usual / All aspects considered", from the reference scenario.
        - Index k, k ∈ [3, n + 3] : Line "Business as usual / All aspects considered" from the number `k - 2` group.
    """
    def __init__(
            self,
            figure_title: str,
            number_of_groups: int,
            color_palette: Optional[List[str]] = None
        ) -> None:
        super().__init__()

        self.figure_title = figure_title
        self.color_palette = (
            color_palette
            if (color_palette and len(color_palette) == number_of_groups + 3)
            else DEFAULT_LINES_COLORS + generate_pastel_palette(number_of_groups)
        )

        # Placeholders for marks :
        self._historic_line: Lines            = None
        self._prospective_lines: Lines        = None
        self._prospective_final_values: Label = None


    def draw(
            self,
            process_data: Dict[str, Any],
            groups_process_data: List[Dict[str, Any]],
            y_scale: LinearScale = None,
            override: bool = False,
            display_default_legend: bool = True
        ) -> Figure:
        """
        Create **initial** figure with the historical, prospective, and aspects areas.

        If the figure is already drawn and you just want to update the data, it is recommended to use the `update()` method instead.
        This method will not redraw the figure but will update the lines' data only.

        However, if you want to redraw the figure completely, you can set `override = True` to force a redraw.
        This action takes more time and resources to execute.

        #### Arguments :
        - `process_data (Dict[str, Any])` : Data dictionary containing the necessary data for plotting the initial graph from the reference scenario.
        - `groups_process_data (List[Dict[str, Any]])` : List of data dictionaries containing the necessary data for plotting the initial graph from all the groups scenarios.
        - `y_scale (LinearScale)` : Optional scale for the y-axis. If not provided, a default scale will be created.
        - `override (bool)` : If `True`, forces a redraw of the figure, even if it has already been drawn. Defaults to `False`.
        - `display_default_legend (bool)` : If `True`, the legend will be displayed. Defaults to `True`.

        #### Returns :
        - `Figure` : The initial figure with historical, prospective, and "Business as usual / All aspects considered" from all the groups scenarios plotted.
        """
        # Check is the figure is already drawn and if override is set to False :
        super().draw(process_data, override)

        # Extract the years from the process_data :
        years: Dict[str, List[int]]  = get_years(process_data)
        full_years: List[int]        = years["full_years"]        # List of intergers ranging from 2000 to 2050 included.
        historic_years: List[int]    = years["historic_years"]    # List of intergers ranging from 2000 to 2019 included.
        prospective_years: List[int] = years["prospective_years"] # List of intergers ranging from 2019 to 2050 included.

        # Create scales and axes :
        x_scale = LinearScale()
        y_scale = y_scale or LinearScale()
        x_axis = Axis(
            scale = x_scale,
            label = "Années",
            num_ticks = 6, # Display : 2000, 2010, 2020, 2030, 2040, 2050.
            label_offset = "40px"
        )
        y_axis = Axis(
            scale = y_scale,
            orientation = "vertical",
            label = "Emissions de CO₂ (en Mt)",
            label_offset = "40px"
        )

        # Plot the historic line :
        y_historic_line = get_y_historic_line(process_data)
        colors_historic_line = [self.color_palette[0]]

        self._historic_line = Lines(
            x = historic_years,
            y = y_historic_line,
            colors = colors_historic_line,
            labels = LINES_NAMES[0],
            display_legend = display_default_legend,
            scales = {"x": x_scale, "y": y_scale}
        )

        # Plot the prospective lines :
        y_prospective_lines, labels_prospective_lines = get_y_prospective_lines_groups_comparison(
            process_data,
            groups_process_data
        )
        colors_prospective_lines = [
            self.color_palette[index]
            for index in range(1, len(y_prospective_lines) + 1)
        ]

        self._prospective_lines = Lines(
            x = prospective_years,
            y = y_prospective_lines,
            colors = colors_prospective_lines,
            labels = labels_prospective_lines,
            display_legend = display_default_legend,
            line_style = "dashed",
            scales = {"x": x_scale, "y": y_scale}
        )

        # Plot / display the final values of all of the displayed lines (the prospective lines based on the reference scenario AND the lines from all the groups scenarios) on the right side of the graph :
        y_prospective_final_values, text_prospective_final_values = get_y_final_values_lines(y_prospective_lines)

        self._prospective_final_values = Label(
            x = [full_years[-1]] * len(y_prospective_lines), # Position the labels at the end of the prospective lines.
            y = y_prospective_final_values,                  # Position the labels at the same height as the end of both prospective lines.
            colors = colors_prospective_lines,
            text = text_prospective_final_values,
            default_size = 12,
            align = "start",
            x_offset = 8,
            scales = {"x": x_scale, "y": y_scale},
            apply_clip = False
        )

        # Create the figure with all marks, axes and the legend :
        self.figure = Figure(
            marks = [
                self._historic_line,
                self._prospective_lines,
                self._prospective_final_values
            ],
            axes = [x_axis, y_axis],
            title = self.figure_title,
            animation_duration = 1000,
            legend_location = "top-left",
            legend_style = {"stroke-width": 0}
        )

        return self.figure


    def update(
            self,
            process_data: Dict[str, Any],
            groups_process_data: List[Dict[str, Any]]
        ) -> Figure:
        """
        Update lines' data only, avoiding full redraw.
        This method updates the existing figure with new data without redrawing the entire figure.

        #### Arguments :
        - `process_data (Dict[str, Any])` : New processed data to update the figure from the reference scenario.
        - `groups_process_data (List[Dict[str, Any]])` : List of new processed data to update the figure from all the groups scenarios.

        #### Returns :
        - `Figure` : The updated figure object with new data.
        """
        # Check if the figure is already drawn :
        super().update(process_data)

        # Update the figure :
        with self.figure.hold_sync():
            # Updating the historic line data is not necessary as it remains constant.

            # Update all the prospective lines :
            y_prospective_lines, labels_prospective_lines = get_y_prospective_lines_groups_comparison(
                process_data,
                groups_process_data
            )
            color_prospective_lines = [
                self.color_palette[index]
                for index in range(1, len(y_prospective_lines) + 1)
            ]
            # Update the y-axis of the prospective lines (updating the x-axis is not necessary as it remains constant) :
            self._prospective_lines.y = [y_prospective_line.tolist() for y_prospective_line in y_prospective_lines] # Use of the ".tolist()" method to force a BQPlot update of the data.
            # Update the colors of the prospective lines from all the groups scenarios :
            self._prospective_lines.colors = color_prospective_lines
            # Update the labels of the prospective lines from all the groups scenarios :
            self._prospective_lines.labels = labels_prospective_lines

            # Update the final values of all prospective lines :
            y_prospective_final_values, text_prospective_final_values = get_y_final_values_lines(y_prospective_lines)
            # Update the x-axis and y-axis of all the labels of the prospective lines :
            self._prospective_final_values.x = [self._prospective_final_values.x[0]] * len(y_prospective_lines) # We also need to update the number of x-axis values to match the number of prospective lines / y-values.
            self._prospective_final_values.y = y_prospective_final_values
            # Update the colors of the labels of the prospective lines :
            self._prospective_final_values.colors = color_prospective_lines
            # Update the text content of the labels of the prospective lines :
            self._prospective_final_values.text = text_prospective_final_values

        return self.figure


    def get_legend_elements(self) -> Tuple[List[str], List[str], List[str]]:
        """
        **IN THIS CLASS, THE LEGEND ELEMENTS VARIES DYNAMICALLY DEPENDING OF THE EXECUTION CONTEXT (number of groups and group's choices).**
        **IF YOU WANT TO USE THIS METHOD, YOU MUST CALL IT AFTER THE `draw()` OR `update()` METHODS.**

        Get the legend elements of the figure.
        Allows to retrieve the colors and labels of the graph's legend to create a custom legend.

        #### Returns :
        - `Tuple[List[str], List[str]]` : A tuple containing three lists:
            - The first list contains the colors of the legend elements.
            - The second list contains the labels of the legend elements.
            - The third list contains the opacities of the legend color elements.
        """
        # Check if the figure is already drawn :
        super().get_legend_elements()

        # Get the legend elements :
        colors    = self._historic_line.colors + self._prospective_lines.colors
        labels    = self._historic_line.labels + self._prospective_lines.labels
        opacities = self._historic_line.opacities + self._prospective_lines.opacities

        return colors, labels, opacities
