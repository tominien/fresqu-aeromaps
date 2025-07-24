from typing import Any, Dict, List, Optional

from core.aeromaps_utils.process_engine import ProcessEngine

from bqplot import Figure, LinearScale
from bqplot_figures.prospective_scenario_graph import ProspectiveScenarioGraph, ProspectiveScenarioGroupComparisonGraph
from bqplot_figures.multidisciplinary_graph import MultidisciplinaryGraph

from ipywidgets import VBox, HBox, Layout, Checkbox, HTML, Label

from crud.crud_cards import get_card_id_by_name

from ui.utils.fresque_aeromaps_UI_constants import (
    CARDS_NAMES,
    get_style_string,
    COLORS_PROSPECTIVE_SCENARIO,
    COLORS_PROSPECTIVE_SCENARIO_GROUP_COMPARISON,
    COLORS_MULTIDISCIPLINARY_GRAPH,
    PROSPECTIVE_SCENARIO_GRAPH_LAYOUT,
    MULTIDISCIPLINARY_LEGEND_STYLE,
    MULTIDISCIPLINARY_LEGEND_HBOX_LAYOUT,
    MULTIDISCIPLINARY_GRAPH_AND_LEGEND_VBOX_LAYOUT
)




###################
# PROCESS ENGINES #
###################
def initialize_process_engine() -> ProcessEngine:
    """
    Initializes a AeroMAPS process engine.

    #### Returns :
    - `ProcessEngine` : A new instance of the AeroMAPS process engine.
    """
    return ProcessEngine()


def compute_process_engine(
    process_engine: ProcessEngine,
    checkboxes: Optional[List[Checkbox]] = []
) -> Dict[str, Any]:
    """
    Computes the data for a single process engine based on the selected checkbox widgets.

    #### Parameters :
    - `process_engine (ProcessEngine)` : The process engine to compute.
    - `checkboxes (List[Checkbox])` : A list of checkbox widgets representing the selected cards. If empty, no cards are selected. Defaults to [].

    #### Returns :
    - `Dict[str, Any]` : The computed data for the process engine.
    """
    # Get the selected card IDs for the current group :
    selected_ids = []
    for index_checkbox, checkbox in enumerate(checkboxes):
        if checkbox.value:
            # If the checkbox is checked, get the card ID by its name :
            selected_ids.append(get_card_id_by_name(CARDS_NAMES[index_checkbox]))

    # Compute the process engine with the selected card IDs :
    return process_engine.compute(
        tuple(selected_ids) if selected_ids else None
    )


#########################
# GRAPHS INITIALIZATION #
#########################
def initialize_prospective_scenario_graph(title: Optional[str] = None) -> ProspectiveScenarioGraph:
    """
    Initializes a prospective scenario graph.

    #### Arguments :
    - `title` : An optional title for the prospective scenario graph. Defaults to "Scénario de référence".

    #### Returns :
    - `ProspectiveScenarioGraph` : The prospective scenario graph.
    """
    return ProspectiveScenarioGraph(title or "Scénario de référence", COLORS_PROSPECTIVE_SCENARIO)


def initialize_prospective_scenario_group_comparison_graph(number_of_groups: int, title: Optional[str] = None) -> ProspectiveScenarioGroupComparisonGraph:
    """
    Initializes the prospective scenario group comparison graph.

    #### Arguments :
    - `number_of_groups` : The number of groups to create the prospective scenario group comparison graph for (Reference scenario excluded).
    - `title` : An optional title for the prospective scenario group comparison graph. Defaults to "Comparaison entre le scénario de référence et celui obtenu par chaque groupe".

    #### Returns :
    - `ProspectiveScenarioGroupComparisonGraph` : The prospective scenario group comparison graph.
    """
    return ProspectiveScenarioGroupComparisonGraph(
        title or "Comparaison entre le scénario de référence et celui obtenu par chaque groupe",
        number_of_groups,
        COLORS_PROSPECTIVE_SCENARIO_GROUP_COMPARISON[:number_of_groups + 3]
    )


def initialize_multidisciplinary_graph(title: Optional[str] = None) -> MultidisciplinaryGraph:
    """
    Initializes a multidisciplinary graph.

    #### Arguments :
    - `title` : An optional title for the multidisciplinary graph. Defaults to "Scénario de référence".

    #### Returns :
    - `MultidisciplinaryGraph` : The multidisciplinary graph.
    """
    return MultidisciplinaryGraph(title or "Scénario de référence", COLORS_MULTIDISCIPLINARY_GRAPH)


##################
# GRAPHS DRAWING #
##################
def draw_prospective_scenario_graph(
    prospective_scenario_graph: ProspectiveScenarioGraph,
    process_engine_data: Dict[str, Any],
    shared_y_scale: Optional[LinearScale] = None
    ) -> Figure:
    """
    Draws a single prospective scenario graph.

    #### Parameters :
    - `prospective_scenario_graph` : The prospective scenario graph to draw.
    - `process_engine_data` : The computed data for the process engine.
    - `shared_y_scale` : An optional shared y-axis scale for the prospective scenario graph. If not provided, the graph will have its own scale.

    #### Returns :
    - `Figure` : The drawn figure for the prospective scenario graph.
    """
    figure = prospective_scenario_graph.draw(process_engine_data, y_scale = shared_y_scale)
    figure.fig_margin = {"top": 60, "bottom": 60, "left": 60, "right": 90}
    figure.layout = Layout(**PROSPECTIVE_SCENARIO_GRAPH_LAYOUT)

    return figure


def draw_prospective_scenario_group_comparison_graph(
    group_comparison_prospective_scenario_graph: ProspectiveScenarioGroupComparisonGraph,
    reference_process_engine_data: Dict[str, Any],
    process_engines_data: List[Dict[str, Any]],
    shared_y_scale: Optional[LinearScale] = None
) -> Figure:
    """
    Draws the prospective scenario group comparison graph.

    #### Parameters :
    - `group_comparison_prospective_scenario_graph` : The prospective scenario group comparison graph to draw.
    - `reference_process_engine_data` : The data of the reference process engine to use for the comparison.
    - `process_engines_data` : A list of computed data for each process engine.
    - `shared_y_scale` : An optional shared y-axis scale for the group comparison graph. If not provided, the graph will have its own scale.

    #### Returns :
    - `Figure` : The drawn figure for the prospective scenario group comparison graph.
    """
    figure = group_comparison_prospective_scenario_graph.draw(
        reference_process_engine_data,
        process_engines_data,
        y_scale = shared_y_scale
    )
    figure.fig_margin = {"top": 60, "bottom": 60, "left": 60, "right": 180}
    figure.layout = Layout(**PROSPECTIVE_SCENARIO_GRAPH_LAYOUT)

    return figure


def draw_multidisciplinary_graph_legend(colors: List[str], labels: List[str], opacities: List[str]) -> HBox:
    """
    Draws the legend for the multidisciplinary graphs.

    #### Arguments :
    - `colors` : A list of colors for the legend items.
    - `labels` : A list of labels for the legend items.
    - `opacities` : A list of opacities for the legend items colors.

    #### Returns :
    - `HBox` : A horizontal box containing the legend items.
    """
    # Check if the colors and labels lists are of the same length :
    if len(colors) != len(labels) or len(colors) != len(opacities):
        raise ValueError("Les listes de couleurs, de labels et d'opacités doivent avoir la même longueur.")

    # Create the legend items :
    legend_items = []
    for color, label, alpha in zip(colors, labels, opacities):
        # Add a colored square and a label to the legend items :
        legend_items.append(
            HTML(
                value = f"<span style = '{get_style_string(MULTIDISCIPLINARY_LEGEND_STYLE)}; background-color: {color}; opacity:{alpha}'></span>"
            )
        )
        legend_items.append(
            Label(
                value = label,
                layout = Layout(
                    margin = "0 12px 0 4px"
                )
            )
        )

        # Space the legend items :
        if label != labels[-1]:
            legend_items.append(
                HTML(
                    value = "<span style = 'width: 48px; display: inline-block'></span>"
                )
            )

    # Create the horizontal box :
    return HBox(
        children = legend_items,
        layout = Layout(**MULTIDISCIPLINARY_LEGEND_HBOX_LAYOUT)
    )


def draw_multidisciplinary_graph(
    multidisciplinary_graph: MultidisciplinaryGraph,
    process_engine_data: Dict[str, Any],
    shared_y_scale: Optional[LinearScale] = None
) -> VBox:
    """
    Draws a single multidisciplinary graph.

    #### Parameters :
    - `multidisciplinary_graph` : The multidisciplinary graph to draw.
    - `process_engine_data` : The computed data for the process engine.
    - `shared_y_scale` : An optional shared y-axis scale for the multidisciplinary graph. If not provided, the graph will have its own scale.

    #### Returns :
    - `VBox` : A vertical box containing the drawn figure and its legend.
    """
    figure = multidisciplinary_graph.draw(process_engine_data, y_scale = shared_y_scale, display_default_legend = False)
    figure.layout = Layout(width = "100%")
    figure_legend = draw_multidisciplinary_graph_legend(*multidisciplinary_graph.get_legend_elements())

    return VBox(
        [figure, figure_legend],
        layout = Layout(**MULTIDISCIPLINARY_GRAPH_AND_LEGEND_VBOX_LAYOUT)
    )
