from typing import Any, Dict, List, Tuple, Optional

from pandas import DataFrame

from bqplot import Figure, Bars, Axis, OrdinalScale, LinearScale
from bqplot_figures.base_graph import BaseGraph

from core.aeromaps_utils.extract_processed_data import get_dataframe_vector_outputs, get_dataframe_climate_outputs




CATEGORIES_NAMES = [
    "ERF (CO₂ et non-CO₂)",
    "Émissions de CO₂",
    "Biomasse",
    "Électricité"
]


def M_plot_consumptions(process_data: Dict[str, Any]) -> List[float]:
    float_inputs  = process_data["float_inputs"]
    float_outputs = process_data["float_outputs"]
    DF_vector_outputs: DataFrame  = get_dataframe_vector_outputs(process_data)
    DF_climate_outputs: DataFrame = get_dataframe_climate_outputs(process_data)

    # Budget carbone :
    gross_carbon_budget      = float(float_outputs["gross_carbon_budget_2050"])
    cumulative_co2_emissions = float(DF_vector_outputs.loc[2050, "cumulative_co2_emissions"])

    # Biomasse :
    available_biomass_total      = float_outputs["available_biomass_total"]
    biomass_consumption_end_year = float_outputs["biomass_consumption_end_year"]

    # Électricité :
    available_electricity_total      = float_inputs["available_electricity"]
    electricity_consumption_end_year = float_outputs["electricity_consumption_end_year"]

    # Forçage radiatif effectif :
    equivalent_gross_carbon_budget        = float(float_outputs["equivalent_gross_carbon_budget_2050"])
    cumulative_total_equivalent_emissions = float(DF_climate_outputs.loc[2050, "cumulative_total_equivalent_emissions"])

    return [
        max(
            cumulative_total_equivalent_emissions / equivalent_gross_carbon_budget * 100,
            0
        ),
        cumulative_co2_emissions / gross_carbon_budget * 100,
        biomass_consumption_end_year / available_biomass_total * 100,
        electricity_consumption_end_year / available_electricity_total * 100
    ]


def M_plot_budgets(process_data: Dict[str, Any]) -> List[List[float]]:
    float_inputs  = process_data["float_inputs"]
    float_outputs = process_data["float_outputs"]

    # Budget carbone :
    gross_carbon_budget    = float(float_outputs["gross_carbon_budget_2050"])
    aviation_carbon_budget = float(float_outputs["aviation_carbon_budget"])

    # Biomasse :
    available_biomass_total    = float_outputs["available_biomass_total"]
    aviation_available_biomass = float_outputs["aviation_available_biomass"]

    # Électricité :
    available_electricity_total    = float_inputs["available_electricity"]
    aviation_available_electricity = float_outputs["aviation_available_electricity"]

    # Forçage radiatif effectif :
    equivalent_gross_carbon_budget    = float(float_outputs["equivalent_gross_carbon_budget_2050"])
    aviation_equivalent_carbon_budget = float(float_outputs["aviation_equivalent_carbon_budget"])

    return [
        aviation_equivalent_carbon_budget / equivalent_gross_carbon_budget * 100,
        aviation_carbon_budget / gross_carbon_budget * 100,
        aviation_available_biomass / available_biomass_total * 100,
        aviation_available_electricity / available_electricity_total * 100
    ]


class MultidisciplinaryGraphOld(BaseGraph):
    """
    Graph class for multidisciplinary data visualization.

    Implements the `draw()` and `update()` methods.

    #### Arguments :
    - `figure_title (str)` : Title of the figure.
    - `color_palette (Optional[List[str]])` : Optional list of **1** color for the graph.
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
            if (color_palette and len(color_palette) == 1)
            else ["#FFA500"]
        )

        # Placeholders for marks :
        self._categories: Bars = None


    def draw(
            self,
            process_data: Dict[str, Any],
            override: bool = False,
            display_default_legend: bool = True
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
        - `display_default_legend (bool)` : If set to `True`, the default legend will be displayed. Defaults to `True`.

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
            labels = ["Budgets"],
            display_legend = display_default_legend
        )

        # Create the figure with the categories :
        self.figure = Figure(
            marks = [self._categories],
            axes = [x_axis, y_axis],
            title = self.figure_title,
            animation_duration = 1000,
            legend_location = "top-right",
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

        # Update the categories data :
        with self._categories.hold_sync():
            self._categories.y = M_plot_budgets(process_data)

        return self.figure


    def get_legend_elements(self) -> Tuple[List[str], List[str], List[str]]:
        # Check if the figure is already drawn :
        super().get_legend_elements()

        # Get the legend elements :
        colors    = self._categories.colors
        labels    = self._categories.labels
        opacities = self._categories.opacities

        return colors, labels, opacities
