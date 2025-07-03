from typing import Any, Dict, List, Optional

from pandas import Series, concat

from bqplot import Figure, Lines, Axis, LinearScale, Label
from bqplot_figures.base_graph import BaseGraph

from crud.crud_aspects import get_aspects, get_aspects_names

from core.aeromaps_utils.extract_processed_data import get_years
from core.aeromaps_utils.evaluate_expression import evaluate_expression_aeromaps

from utils import LINES_JSON_PATH, generate_pastel_palette, float_to_int_string




# Load the lines (historic, no aspect and all aspect) from the JSON file :
LINES                                       = get_aspects(LINES_JSON_PATH)
LINES_NAMES: List[str]                      = get_aspects_names(LINES_JSON_PATH)
LINES_OUTPUT_FORMULAS: List[Dict[str, str]] = [line["output_formula"] for line in LINES.values()]

# Load the aspects from the JSON file :
ASPECTS                                       = get_aspects()
ASPECTS_NAMES: List[str]                      = get_aspects_names()
ASPECTS_OUTPUT_FORMULAS: List[Dict[str, str]] = [aspect["output_formula"] for aspect in ASPECTS.values()]


def format_final_value(value: float) -> str:
    """
    Format the final value of a prospective line.

    Converts the value to a string with 'Mt CO₂' suffix and formats it as an integer.

    #### Arguments :
    - `value (float)` : The value to format.

    #### Returns :
    - `str` : The formatted string.
    """
    return f"{float_to_int_string(value)} Mt CO₂"


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
            if (color_palette and len(color_palette) == len(ASPECTS) + 3)
            else ["#8c564b", "#000000", "#d62728"] + generate_pastel_palette(len(ASPECTS))
        )

        # Placeholders for marks :
        self._historic_line: Lines      = None
        self._prospective_lines: Lines  = None
        self._aspects_areas: Lines      = None
        self._past_shade: Lines         = None
        self._prospective_labels: Label = None


    def _get_y_historic_line(self, process_data: Dict[str, Any]) -> Series:
        """
        Get the y-values of the historic line.

        This method is used to calculate the y-values of the historic line from the process data.

        #### Arguments :
        - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the historic line data.

        #### Returns :
        - `Series` : The y-values of the historic line.
        """
        return evaluate_expression_aeromaps(
            process_data,
            *LINES_OUTPUT_FORMULAS[0].values()
        )


    def _get_y_prospective_lines(self, process_data: Dict[str, Any]) -> List[Series]:
        """
        Get the y-values of the prospective lines.

        This method is used to calculate the y-values of the prospective lines from the process data.

        #### Arguments :
        - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the prospective lines data.

        #### Returns :
        - `List[Series]` : A list containing the y-values of the prospective lines.
        """
        return [
            evaluate_expression_aeromaps(process_data, *line_output_formula.values())
            for line_output_formula in [LINES_OUTPUT_FORMULAS[1], LINES_OUTPUT_FORMULAS[2]]
        ]


    def _get_y_aspects_areas(self, process_data: Dict[str, Any]) -> List[Series]:
        """
        Get the y-values of the aspects areas.

        This method is used to calculate the y-values of the aspects areas from the process data.

        #### Arguments :
        - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the aspects areas data.

        #### Returns :
        - `List[Series]` : A list containing the y-values of the aspects areas.
        """
        return [
            evaluate_expression_aeromaps(process_data, *aspect_output_formula.values())
            for aspect_output_formula in ASPECTS_OUTPUT_FORMULAS
        ] + [
            evaluate_expression_aeromaps(process_data, LINES_OUTPUT_FORMULAS[2]["expression"], "full_years") # Add the "all aspects" line to the aspects areas, allowing to fill the bottom area of the graph (to plot `n` y-areas, you need `n + 1` lines).
        ]


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
        - `Figure` : The initial figure with historical, prospective, and aspects areas plotted.
        """
        # Check is the figure is already drawn and if override is set to False :
        if self.figure is not None and not override :
            return self.update(process_data)

        # Extract the years from the process_data :
        years: Dict[str, List[int]]   = get_years(process_data)
        full_years: List[int]         = years["full_years"]        # List of intergers ranging from 2000 to 2050 included.
        historic_years: List[int]     = years["historic_years"]    # List of intergers ranging from 2000 to 2019 included.
        prospective_years: List[int]  = years["prospective_years"] # List of intergers ranging from 2019 to 2050 included.

        # Create scales and axes :
        x_scale = LinearScale()
        y_scale = LinearScale()
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
        y_historic_line = self._get_y_historic_line(process_data)
        colors_historic_line = [self.color_palette[0]]

        self._historic_line = Lines(
            x = historic_years,
            y = y_historic_line,
            colors = colors_historic_line,
            labels = LINES_NAMES[0],
            display_legend = True,
            scales = {"x": x_scale, "y": y_scale}
        )

        # Plot the prospective lines :
        y_prospective_lines = self._get_y_prospective_lines(process_data)
        colors_prospective_lines = [self.color_palette[1], self.color_palette[2]]

        self._prospective_lines = Lines(
            x = prospective_years,
            y = y_prospective_lines,
            colors = colors_prospective_lines,
            labels = [
                LINES_NAMES[1],
                LINES_NAMES[2]
            ],
            display_legend = True,
            line_style = "dashed",
            scales = {"x": x_scale, "y": y_scale}
        )

        # Plot the aspects areas :
        y_aspects_areas = self._get_y_aspects_areas(process_data)
        colors_aspects_areas = [self.color_palette[index] for index in range(3, 3 + len(ASPECTS))]

        self._aspects_areas = Lines(
            x = full_years,
            y = y_aspects_areas,
            colors = colors_aspects_areas,
            stroke_width = 0,
            fill = "between",
            fill_colors = colors_aspects_areas,
            fill_opacities = [0.3] * len(colors_aspects_areas),
            labels = [*ASPECTS_NAMES, ""], # Empty label for the last area to avoid legend entry (corresponds to the "no aspects" line).
            display_legend = True,
            scales = {"x": x_scale, "y": y_scale}
        )

        # Plot / display the final values of the prospective lines on the right side of the graph :
        prospective_years_final_value = [serie.iloc[-1] for serie in y_prospective_lines]
        prospective_years_final_value_formatted = [format_final_value(value) for value in prospective_years_final_value]

        self._prospective_labels = Label(
            x = [full_years[-1], full_years[-1]], # Position the labels at the end of the prospective lines.
            y = prospective_years_final_value,    # Position the labels at the same height as the end of both prospective lines.
            colors = colors_prospective_lines,
            text = prospective_years_final_value_formatted,
            default_size = 12, # Size of the labels (12px).
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
                self._prospective_labels
            ],
            axes = [x_axis, y_axis],
            title = self.figure_title,
            animation_duration = 1000,
            legend_location = "top-left",
            legend_style = {"stroke-width": 0}
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

        # Update the figure :
        with self.figure.hold_sync():
            # Updating the historic line data is not necessary as it remains constant.
            
            y_prospective_lines = self._get_y_prospective_lines(process_data)
            # Update the y-axis of the prospective lines (updating the x-axis is not necessary as it remains constant) :
            self._prospective_lines.y = y_prospective_lines
            # Update the y-axis of the text of the prospective labels (updating the x-axis is not necessary as it remains constant) :
            self._prospective_labels.y = [serie.iloc[-1] for serie in y_prospective_lines]
            # Update the text content of the text of the prospective labels :
            self._prospective_labels.text = [format_final_value(value) for value in self._prospective_labels.y]
            
            # Update the y-axis of the aspects areas (updating the x-axis is not necessary as it remains constant) :
            self._aspects_areas.y = self._get_y_aspects_areas(process_data)

        return self.figure
