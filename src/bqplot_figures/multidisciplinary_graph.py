from typing import Any, Dict, List, Tuple, Optional

from bqplot import Figure, Bars, Axis, LinearScale, OrdinalScale
from bqplot_figures.base_graph import BaseGraph

from crud.crud_multidisciplinary_bars import get_bars, get_bars_names

from core.aeromaps_utils.evaluate_expression import evaluate_expression_aeromaps

from utils import generate_pastel_palette




# Load the bars from the JSON file :
BARS                                                   = get_bars()
BARS_NAMES: List[str]                                  = get_bars_names()
BARS_BUDGET_OUTPUT_FORMULAS: List[Dict[str, str]]      = [line["output_formula_BUDGET"] for line in BARS.values()]
BARS_CONSUMPTION_OUTPUT_FORMULAS: List[Dict[str, str]] = [line["output_formula_CONSUMPTION"] for line in BARS.values()]


def get_multidisciplinary_graphs_y_scales(processes_data: List[Dict[str, Any]]) -> Tuple[float, float]:
    """
    Get the minimal and maximal values of all the y-scales for the budget and consumption bars from multiple processes data.

    #### Arguments :
    - `processes_data (List[Dict[str, Any]])` : A list of processes data from AéroMAPS.

    #### Returns :
    - `Tuple[float]` : A tuple containing the minimal and maximal values of all the y-scales for the budget and consumption bars.
    """
    # Create a temporary MultidisciplinaryGraph instance to access the methods :
    temp_graph = MultidisciplinaryGraph("Temporary Graph")

    # Get the y-values for the budget and consumption bars from all processes data :
    all_y_lines = []
    for process_data in processes_data:
        # Get the y-values for the budget bars :
        y_budget_bars = temp_graph._get_y_budget_bars(process_data)
        all_y_lines.extend(y_budget_bars)

        # Get the y-values for the consumption bars :
        y_consumption_bars = temp_graph._get_y_consumption_bars(process_data)
        all_y_lines.extend(y_consumption_bars)

    return (min(all_y_lines), max(all_y_lines)) if all_y_lines else (0.0, 0.0)


class MultidisciplinaryGraph(BaseGraph):
    """
    Graph class for displaying multidisciplinary assessment data.

    Implements the `draw()` and `update()` methods.

    #### Arguments :
    - `figure_title (str)` : Title of the figure.
    - `color_palette (Optional[List[str]])` : Optional list of **2** colors for the graph. The color order applies the following logic :
        - Index 0 : Color for the budget bars.
        - Index 1 : Color for the consumption bars.
    """
    def __init__(
            self,
            figure_title: str,
            color_palette: Optional[List[str]] = None
            ) -> None:
        super().__init__()

        self.figure_title = figure_title
        self.color_palette = color_palette if color_palette is not None else generate_pastel_palette(2)

        # Placeholders for marks :
        self._budget_bars: Bars      = None
        self._consumption_bars: Bars = None


    def _get_y_budget_bars(self, process_data: Dict[str, Any]) -> List[float]:
        """
        Get the y-values for the budget bars from the process data.

        #### Arguments :
        - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the budget data.

        #### Returns :
        - `List[float]` : A list of floats containing the y-values for the budget bars.
        """
        return [
            evaluate_expression_aeromaps(
                process_data,
                bar_budget_output_formula["expression"],
                bar_budget_output_formula["year_range"] if "year_range" in bar_budget_output_formula.keys() else None
            )
            for bar_budget_output_formula in BARS_BUDGET_OUTPUT_FORMULAS
        ]


    def _get_y_consumption_bars(self, process_data: Dict[str, Any]) -> List[float]:
        """
        Get the y-values for the consumption bars from the process data.

        #### Arguments :
        - `process_data (Dict[str, Any])` : The process data containing the necessary information to calculate the consumption data.

        #### Returns :
        - `List[float]` : A list of floats containing the y-values for the consumption bars.
        """
        return [
            evaluate_expression_aeromaps(
                process_data,
                bar_consumption_output_formula["expression"],
                bar_consumption_output_formula["year_range"] if "year_range" in bar_consumption_output_formula.keys() else None
            )
            for bar_consumption_output_formula in BARS_CONSUMPTION_OUTPUT_FORMULAS
        ]


    def draw(
            self,
            process_data: Dict[str, Any],
            y_scale: LinearScale = None,
            override: bool = False,
            display_default_legend: bool = True
        ) -> Figure:
        """
        create **initial** figure with the budget and consumption bars.

        If the figure is already drawn and you just want to update the data, it is recommended to use the `update()` method instead.
        This method will not redraw the figure but will update the lines' data only.

        However, if you want to redraw the figure completely, you can set `override = True` to force a redraw.
        This action takes more time and resources to execute.

        #### Arguments :
        - `process_data (Dict[str, Any])` : The process data containing the necessary information to create the figure.
        - `y_scale (LinearScale)` : Optional scale for the y-axis. If not provided, a default scale will be created.
        - `override (bool)` : If set to `True`, the method will redraw the figure even if it is already drawn. Defaults to `False`.
        - `display_default_legend (bool)` : If set to `True`, the default legend will be displayed. Defaults to `True`.

        #### Returns :
        - `Figure` : The created or updated figure with the budget and consumption bars.
        """
        # Check is the figure is already drawn and if override is set to False :
        super().draw(process_data, override)

        # Create scales and axes :
        x_scale = OrdinalScale()
        y_scale = y_scale or LinearScale()
        x_axis = Axis(
            scale = x_scale,
            label = "Catégories",
            label_offset = "40px"
        )
        y_axis = Axis(
            scale = y_scale,
            tick_format = "0.2f",
            orientation = "vertical",
            label = "Part du budget mondial (en %)",
            label_offset = "40px"
        )

        # Plot the budget bars :
        y_budget_bars = self._get_y_budget_bars(process_data)

        self._budget_bars = Bars(
            x = BARS_NAMES,
            y = y_budget_bars,
            colors = [self.color_palette[0]],
            opacities = [0.5] * len(BARS_NAMES),
            labels = ["Budgets"],
            display_legend = display_default_legend,
            offset = 0.2,
            scales = {"x": x_scale, "y": y_scale}
        )

        # plot the consumption bars :
        y_consumption_bars = self._get_y_consumption_bars(process_data)

        self._consumption_bars = Bars(
            x = BARS_NAMES,
            y = y_consumption_bars,
            colors = [self.color_palette[1]],
            opacities = [0.5] * len(BARS_NAMES),
            labels = ["Consommations"],
            display_legend = display_default_legend,
            offset = 0.2,
            scales = {"x": x_scale, "y": y_scale}
        )

        # Create the figure with all marks, axes and the legend :
        self.figure = Figure(
            marks = [
                self._budget_bars,
                self._consumption_bars
            ],
            axes = [x_axis, y_axis],
            title = self.figure_title,
            animation_duration = 1000,
            legend_location = "top-right",
            legend_style = {"stroke-width": 0}
        )

        return self.figure


    def update(self, process_data: Dict[str, Any]) -> Figure:
        # Check if the figure is already drawn :
        super().update(process_data)

        # Update the figure :
        with self.figure.hold_sync():
            # Update the y-axis of the budget bars :
            self._budget_bars.y = self._get_y_budget_bars(process_data)

            # Update the y-axis of the consumption bars :
            self._consumption_bars.y = self._get_y_consumption_bars(process_data)

        return self.figure


    def get_legend_elements(self) -> Tuple[List[str], List[str]]:
        # Check if the figure is already drawn :
        super().get_legend_elements()

        # Get the legend elements :
        colors = self._budget_bars.colors + self._consumption_bars.colors
        labels = self._budget_bars.labels + self._consumption_bars.labels

        return colors, labels
