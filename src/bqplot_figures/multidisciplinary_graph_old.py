from typing import Any, Dict, List, Optional

from bqplot import Figure, Bars, Axis, OrdinalScale, LinearScale
from bqplot_figures.base_graph import BaseGraph

from core.aeromaps_utils.TEMPORARY_FILE_multidisciplinary_graph_utils import M_plot_budgets




CATEGORIES_NAMES = [
    "ERF (CO₂ et non-CO₂)",
    "Émissions de CO₂",
    "Biomasse",
    "Électricité"
]


class MultidisciplinaryGraphOld(BaseGraph):
    """
    Graph class for multidisciplinary data visualization.

    Implements the `draw()` and `update()` methods.

    #### Arguments :
    - `figure_title (str)` : Title of the figure.
    - `color_palette (Optional[List[str]])` : Optional list of **4** colors for the graph.
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
            if (color_palette and len(color_palette) == 4)
            else ["#FFA500"] * 4
        )

        # Placeholders for marks :
        self._categories: Bars = None


    def draw(
            self,
            process_data: Dict[str, Any],
            override: bool = False
        ) -> Figure:
        """
        Create **initial** figure with the multidisciplinary data.

        If the figure is already drawn and you just want to update the data, it is recommended to use the `update()` method instead.
        This method will not redraw the figure but will update the lines' data only.

        However, if you want to redraw the figure completely, you can set `override = True` to force a redraw.
        This action takes more time and resources to execute.

        #### Arguments :
        - `process_data (Dict[str, Any])` : Data dictionary containing the necessary data for plotting the initial graph.
        - `override (bool)` : If `True`, forces a redraw of the figure, even if it has already been drawn. Defaults to `False`.

        #### Returns :
        - `Figure` : The initial figure with the multidisciplinary data plotted.
        """
        # Check is the figure is already drawn and if override is set to False :
        if self.figure is not None and not override :
            return self.update(process_data)

        # Create scales and axes :
        x_scale = OrdinalScale()
        y_scale = LinearScale()
        x_axis = Axis(
            scale = x_scale,
            tick_style = {"font-weight": "bold"}
        )
        y_axis = Axis(
            scale = y_scale,
            tick_format = "0.2f",
            orientation = "vertical",
            label = "Part du budget mondial (en %)",
            label_offset = "40px"
        )

        # Plot the categories :
        categories_y_bars = M_plot_budgets(process_data)
        self._categories = Bars(
            x = CATEGORIES_NAMES,
            y = categories_y_bars,
            scales = {"x": x_scale, "y": y_scale},
            colors = self.color_palette,
            display_legend = False
        )

        # Create the figure with the categories :
        self.figure = Figure(
            marks = [self._categories],
            axes = [x_axis, y_axis],
            title = self.figure_title,
            animation_duration = 1000
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

        # Update the categories data :
        with self._categories.hold_sync():
            self._categories.y = M_plot_budgets(process_data)

        return self.figure
