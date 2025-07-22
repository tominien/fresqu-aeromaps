from typing import Any, Dict, List, Tuple, Optional, Union

from crud.crud_cards import get_cards_name, get_card_id_by_name

from core.aeromaps_utils.process_engine import ProcessEngine

from bqplot import Figure, LinearScale
from bqplot_figures.base_graph import BaseGraph
from bqplot_figures.prospective_scenario_graph import (
    ProspectiveScenarioGraph,
    ProspectiveScenarioGroupComparisonGraph,
    get_prospective_scenario_y_scales
)
from bqplot_figures.multidisciplinary_graph import MultidisciplinaryGraph, get_multidisciplinary_graphs_y_scales

import markdown

from ipywidgets import Box, VBox, HBox, Layout, GridspecLayout, AppLayout, Checkbox, Button, HTML, Label

from utils import APPLICATION_EXPLANATIONS_PATH




CARDS_NAMES = get_cards_name()

# Define the colors used in the graphs :
COLORS_PROSPECTIVE_SCENARIO = [
    "#8c564b", "#000000", "#d62728", "#1f77b4",
    "#ff7f0e", "#2ca02c", "#e377c2", "#9467bd"
]

COLORS_PROSPECTIVE_SCENARIO_GROUP_COMPARISON = [
    "#8c564b", "#000000", "#d62728", "#1f77b4",
    "#ff7f0e", "#2ca02c", "#8c564b", "#9467bd",
    "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#b2df8a"
]

COLORS_MULTIDISCIPLINARY_GRAPH = [
    "#bf2626", "#26bfbf"
]

# Define multiple HTML styles :
def get_style_string(styles: Dict[str, str]) -> str:
    """
    Converts a dictionary of styles to a string format for HTML.
    
    #### Arguments :
    - `styles (Dict[str, str])` : A dictionary where keys are CSS properties and values are their corresponding values.
    
    #### Returns :
    - `str` : A string representation of the styles.
    """
    return "; ".join(f"{key}: {value}" for key, value in styles.items()).replace("_", "-")

TITLE_STYLE = {
    "font_size": "24px",
    "font_weight": "bold",
    "text_decoration": "underline",
    "text_align": "center"
}

BUTTON_STYLE = {
    "font_size": "32px",
    "font_weight": "bold",
    "text_align": "center"
}

MULTIDISCIPLINARY_LEGEND_STYLE = {
    "display": "inline-block",
    "width": "12px",
    "height": "12px"
}

# Define multiple layout styles :
EXPLANATIONS_VBOX_LAYOUT = {
    "width": "100%"
}

CHECKBOXES_GRID_LAYOUT = {
    "width": "100%",
    "grid_gap": "0px",
    "margin": "0px",
    "padding": "0px"
}

CHECKBOXES_GRID_LABEL_LAYOUT = {
    "display": "flex",
    "justify_content": "center",
    "align_items": "center",
    "text_align": "center"
}

CHECKBOXES_GRID_CHECKBOX_LAYOUT = {
    "display": "flex",
    "justify_content": "center",
    "align_items": "center",
    "margin": "10px 0px 0px 0px"
}

CHECKBOXES_GRID_CELL_LAYOUT = {
    "width": "auto",
    "height": "auto",
    "margin": "0px",
    "padding": "0px",
    "display": "flex",
    "justify_content": "center",
    "align_items": "center",
    "text_align": "center",
    "overflow": "hidden"
}

TITLE_BOX_LAYOUT = {
    "width" : "100%",
    "display" : "flex",
    "justify_content" : "center"
}

BUTTON_LAYOUT = {
    "width" : "100%",
    "height" : "125px"
}

BUTTON_BOX_LAYOUT = {
    "width" :  "100%",
    "height" : "175px",
    "align_items" : "center",
    "justify_content" : "center"
}

PROSPECTIVE_SCENARIO_BOX_LAYOUT = {
    "width" : "100%",
    "align_items" : "center"
}

MULTIDISCIPLINARY_BOX_LAYOUT = {
    "width" : "100%",
    "display" : "flex",
    "flex_flow" : "row nowrap",
    "justify_content" : "space-around",
    "align_items" : "flex-start"
}

MULTIDISCIPLINARY_LEGEND_HBOX_LAYOUT = {
    "width" : "100%",
    "justify_content" : "center",
    "margin" : "-12px 0 0 0"
}

MULTIDISCIPLINARY_GRAPH_AND_LEGEND_VBOX_LAYOUT = {
    "width" : "50%",
    "align_items" : "center"
}

APP_VBOX_LAYOUT = {
    "width": "100%"
}




def draw_explanations(markdown_file: str = APPLICATION_EXPLANATIONS_PATH) -> VBox:
    """
    Draws the explanations for the notebook interface using a markdown file.

    #### Arguments :
    - `markdown_file (str)` : The path to the markdown file containing the explanations. Defaults to `APPLICATION_EXPLANATIONS_PATH`.

    #### Returns :
    - `VBox` : A vertical box containing the explanations as HTML.
    """
    with open(markdown_file, "r", encoding = "utf-8") as file:
        markdown_content = file.read()

    return VBox(
        [HTML(markdown.markdown(markdown_content))],
        layout = Layout(**EXPLANATIONS_VBOX_LAYOUT)
    )


def create_cell_checkboxes_grid(
        widget: Union[Checkbox, Label],
        border_sides: List[str] = ["top", "bottom", "left", "right"]
    ) -> Box:
    """
    Creates a cell for the checkboxes grid with the specified widget and border sides.

    #### Arguments :
    - `widget (Union[Checkbox, Label])` : The widget to place in the cell (either a Checkbox or a Label).
    - `border_sides (List[str])` : The sides of the border to draw around the cell. Allowed values are "top", "bottom", "left", and "right".
    """
    # Check if the border sides are valid :
    if not all(side in ["top", "bottom", "left", "right"] for side in border_sides):
        raise ValueError("Invalid border side(s) specified.")

    # Create the box style for the cell :
    box_style = {
        "box_sizing": "border-box"
    }
    for side in border_sides:
        box_style[f"border_{side}"] = "1px solid lightgray"

    # Create the box with the specified widget and style :
    return Box(
        children = [widget],
        layout = Layout(
            **CHECKBOXES_GRID_CELL_LAYOUT,
            **box_style
        )
    )


def initialize_checkboxes_grid(number_of_groups: int) -> Tuple[GridspecLayout, List[List[Checkbox]]]:
    """
    Initializes the grid layout for the checkboxes and returns it along with a list of lists containing the checkbox widgets.

    #### Arguments :
    - `number_of_groups (int)` : The number of groups to create checkboxes for.

    #### Returns :
    - `GridspecLayout` : The grid layout containing the checkboxes.
    - `List[List[Checkbox]]` : A list of lists containing the checkbox widgets for each group.
    """
    # Get the number of rows and columns for the grid layout :
    number_of_rows    = len(CARDS_NAMES) + 1 # +1 for the "Groups names" row.
    number_of_columns = number_of_groups + 2 # +2 for the "Cards names" column and the "Reference scenario" column.

    # Initialize the grid layout for the checkboxes :
    grid = GridspecLayout(
        number_of_rows,
        number_of_columns,
        layout = Layout(**CHECKBOXES_GRID_LAYOUT)
    )

    # Initialise the top-left cell (as empty) :
    grid[0, 0] = create_cell_checkboxes_grid(
        Label(value = ""),
        ["right", "bottom"]
    )

    # Initialise the "Cards names" column :
    for index_row, card_name in enumerate(CARDS_NAMES):
        label = Label(
            value = card_name,
            layout = Layout(**CHECKBOXES_GRID_LABEL_LAYOUT)
        )
        grid[index_row + 1, 0] = create_cell_checkboxes_grid(label, ["right", "bottom", "left"])

    # Initialize the "Reference scenario" column :
    grid[0, 1] = create_cell_checkboxes_grid(Label(value = "Scénario de référence"), ["top", "right", "bottom"])
    for index_row, card_name in enumerate(CARDS_NAMES):
        checkbox = Checkbox(
            value = False,
            indent = False,
            disabled = True, # Disable the checkbox for the reference scenario.
            layout = Layout(**CHECKBOXES_GRID_CHECKBOX_LAYOUT)
        )
        grid[index_row + 1, 1] = create_cell_checkboxes_grid(checkbox, ["right", "bottom"])

    # initialize the "Groups" columns :
    checkboxes_lists: List[List[Checkbox]] = [] # List to store the checkboxes for each group.
    for index_column in range(2, number_of_columns):
        # Create the label for the group name :
        label = Label(
            value = f"Groupe {index_column - 1}",
            layout = Layout(**CHECKBOXES_GRID_LABEL_LAYOUT)
        )
        grid[0, index_column] = create_cell_checkboxes_grid(label, ["top", "right", "bottom"])
        # Create the checkboxes for each group :
        group_checkboxes_list: List[Checkbox] = [] # List to store the checkboxes for the current group.
        for index_row, card_name in enumerate(CARDS_NAMES):
            # Create the checkbox for the current group :
            checkbox = Checkbox(
                value = False,
                indent = False,
                layout = Layout(**CHECKBOXES_GRID_CHECKBOX_LAYOUT)
            )
            # Create the cell with the checkbox :
            cell = create_cell_checkboxes_grid(checkbox, ["right", "bottom"])
            grid[index_row + 1, index_column] = cell
            # Add the checkbox to the list of checkboxes for the current group :
            group_checkboxes_list.append(checkbox)
        # Add the list of checkboxes for the current group to the main list :
        checkboxes_lists.append(group_checkboxes_list)

    return grid, checkboxes_lists


def initialize_process_engines(number_of_groups: int) -> List[ProcessEngine]:
    """
    Initializes the process engines for each group.

    #### Arguments :
    - `number_of_groups` : The number of groups to create process engines for.

    #### Returns :
    - `List[ProcessEngine]` : A list of process engines for each group.
    """
    return [ProcessEngine() for _ in range(number_of_groups)]


def compute_process_engines(
    process_engines: List[ProcessEngine],
    checkboxes_lists: List[List[Checkbox]]
) -> List[List[dict]]:
    """
    Computes the data for each process engine based on the selected checkbox widgets.

    #### Parameters :
    - `process_engines` : A list of process engines to compute.
    - `checkboxes_lists` : A list of lists containing the checkbox widgets for each group.

    #### Returns :
    - `List[List[dict]]` : A list of computed data for each process engine.
    """
    return [
        engine.compute(
            tuple(
                get_card_id_by_name(checkbox.description) for checkbox in widgets if checkbox.value
            ) or None
        )
        for engine, widgets in zip(process_engines, checkboxes_lists)
    ]


def initialize_prospective_scenarios_graphs(number_of_groups: int, titles: Optional[List[str]] = None) -> List[ProspectiveScenarioGraph]:
    """
    Initializes the prospective scenario graphs for each group.

    #### Arguments :
    - `number_of_groups` : The number of groups to create prospective scenario graphs for.
    - `titles` : An optional list of titles for each prospective scenario graph.

    #### Returns :
    - `List[ProspectiveScenarioGraph]` : A list of prospective scenario graphs for each group.
    """
    if titles is not None and len(titles) != number_of_groups:
        raise ValueError("La liste des titres doit avoir la même longueur que le nombre de groupes.")

    return (
        [
            ProspectiveScenarioGraph(
                f"Scénario du groupe {index + 1}",
                COLORS_PROSPECTIVE_SCENARIO
            ) for index in range(number_of_groups)
        ]
        if titles is None
        else [ProspectiveScenarioGraph(title, COLORS_PROSPECTIVE_SCENARIO) for title in titles]
    )


def initialize_reference_prospective_scenario_graph(title: Optional[List[str]] = None) -> ProspectiveScenarioGraph:
    """
    Initializes the reference prospective scenario graph.

    #### Arguments :
    - `title` : An optional title for the reference prospective scenario graph. Defaults to "Scénario de référence".

    #### Returns :
    - `ProspectiveScenarioGraph` : The reference prospective scenario graph.
    """
    return initialize_prospective_scenarios_graphs(1, [title or "Scénario de référence"])[0]


def initialize_prospective_scenario_group_comparison_graph(number_of_groups: int, title: Optional[str] = None) -> ProspectiveScenarioGroupComparisonGraph:
    """
    Initializes the prospective scenario group comparison graph.

    #### Arguments :
    - `number_of_groups` : The number of groups to create the prospective scenario group comparison graph for (Reference scenario excluded).
    - `title` : An optional title for the prospective scenario group comparison graph. Defaults to "Comparaison des scénarios des groupes".

    #### Returns :
    - `ProspectiveScenarioGroupComparisonGraph` : The prospective scenario group comparison graph.
    """
    return ProspectiveScenarioGroupComparisonGraph(
        title or "Comparaison entre le scénario de référence et celui obtenu par chaque groupe",
        number_of_groups,
        COLORS_PROSPECTIVE_SCENARIO_GROUP_COMPARISON[:number_of_groups + 3]
    )


def initialize_multidisciplinary_graphs(number_of_groups: int, titles: Optional[List[str]] = None) -> List[MultidisciplinaryGraph]:
    """
    Initializes the multidisciplinary graphs for each group.

    #### Arguments :
    - `number_of_groups` : The number of groups to create multidisciplinary graphs for.
    - `titles` : A optionalelist of titles for each multidisciplinary graph.

    #### Returns :
    - `List[MultidisciplinaryGraph]` : A list of multidisciplinary graphs for each group.
    """
    if titles is not None and len(titles) != number_of_groups:
        raise ValueError("La liste des titres doit avoir la même longueur que le nombre de groupes.")


    return (
        [
            MultidisciplinaryGraph(
                f"Scénario du groupe {index + 1}",
                COLORS_MULTIDISCIPLINARY_GRAPH
            ) for index in range(number_of_groups)
        ]
        if titles is None
        else [MultidisciplinaryGraph(title, COLORS_MULTIDISCIPLINARY_GRAPH) for title in titles]
    )


def initialize_reference_multidisciplinary_graph(title: Optional[str] = None) -> MultidisciplinaryGraph:
    """
    Initializes the reference multidisciplinary graph.

    #### Arguments :
    - `title` : An optional title for the reference multidisciplinary graph. Defaults to "Scénario de référence".

    #### Returns :
    - `MultidisciplinaryGraph` : The reference multidisciplinary graph.
    """
    return initialize_multidisciplinary_graphs(1, [title or "Scénario de référence"])[0]


def draw_prospective_scenario_graphs(
    prospective_scenarios_graphs: List[ProspectiveScenarioGraph],
    process_engines_data: List[Dict[str, Any]],
    shared_y_scale: Optional[LinearScale] = None
) -> List[Figure]:
    """
    Draws the prospective scenario graphs for each group.

    #### Parameters :
    - `prospective_scenarios_graphs` : A list of prospective scenario graphs to draw.
    - `process_engines_data` : A list of computed data for each process engine.
    - `shared_y_scale` : An optional shared y-axis scale for all prospective scenario graphs. If not provided, each graph will have its own scale.

    #### Returns :
    - `List[Figure]` : A list of drawn figures for each prospective scenario graph.
    """
    figures = []

    # Draw each prospective scenario graph with the corresponding data :
    for graph, data in zip(prospective_scenarios_graphs, process_engines_data):
        figure = graph.draw(data, y_scale = shared_y_scale)
        figure.fig_margin = {"top": 60, "bottom": 60, "left": 60, "right": 90}

        figures.append(figure)

    return figures


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

    return figure


def draw_multidisciplinary_graphs(
    multidisciplinary_graphs: List[MultidisciplinaryGraph],
    process_engines_data: List[Dict[str, Any]],
    shared_y_scale: Optional[LinearScale] = None
) -> List[VBox]:
    """
    Draws the multidisciplinary graphs for each group.

    #### Parameters :
    - `multidisciplinary_graphs` : A list of multidisciplinary graphs to draw.
    - `process_engines_data` : A list of computed data for each process engine.
    - `shared_y_scale` : An optional shared y-axis scale for all multidisciplinary graphs. If not provided, each graph will have its own scale.

    #### Returns :
    - `List[VBox]` : A list of drawn widgets for each multidisciplinary graph.
    """
    # Create a wrapper function to draw the graphs' legends :
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

    widgets = []

    # Draw each multidisciplinary graph with the corresponding data :
    for graph, data in zip(multidisciplinary_graphs, process_engines_data):
        figure = graph.draw(data, y_scale = shared_y_scale, display_default_legend = False)
        figure.layout = Layout(width = "100%")
        figure_legend = draw_multidisciplinary_graph_legend(*graph.get_legend_elements())

        # Create a VBox to contain the figure and its legend :
        widgets.append(
            VBox(
                [figure, figure_legend],
                layout = Layout(**MULTIDISCIPLINARY_GRAPH_AND_LEGEND_VBOX_LAYOUT)
            )
        )

    return widgets


def update_figures(
    _button: Button,
    number_of_groups: int,
    reference_process_engine_data: Dict[str, Any],
    process_engines: List[ProcessEngine],
    checkboxes_lists: List[List[Checkbox]],
    graphs: Dict[str, List[BaseGraph]],
    shared_y_scales: Dict[str, LinearScale]
) -> None:
    """
    Updates the figures based on the selected checkboxes and the process engines.

    #### Arguments :
    - `_button` : The button that triggered the update (not used in this function).
    - `number_of_groups` : The number of groups to update the figures for.
    - `reference_process_engine_data` : The data of the reference process engine to use for the comparison of Prospective Scenario Group Comparison Graph.
    - `process_engines` : A list of process engines to compute the new data.
    - `checkboxes_lists` : A list of lists containing the checkbox widgets for each group.
    - `graphs` : A dictionary containing the prospective scenario graphs and multidisciplinary graphs.

    #### Returns :
    - `None` : This function does not return anything, it updates the graphs in place
    """
    # Get each type of graph from the dictionary :
    prospective_scenario_graphs                 = graphs["prospective_scenarios_graphs"]
    group_comparison_prospective_scenario_graph = graphs["prospective_scenario_group_comparison_graph"][0]
    multidisciplinary_graphs                    = graphs["multidisciplinary_graphs"]

    # Compute each process based on the selected widgets :
    new_data = [None] * number_of_groups # Initialize a list to store the new data for each group
    for index in range(number_of_groups):
        # Get the selected card IDs for the current group :
        selected_ids = []
        for index_checkbox, checkbox in enumerate(checkboxes_lists[index]):
            if checkbox.value:
                # If the checkbox is checked, get the card ID by its name :
                selected_ids.append(get_card_id_by_name(CARDS_NAMES[index_checkbox]))

        # Compute the new data for the current process engine :
        new_data[index] = process_engines[index].compute(
            tuple(selected_ids) if selected_ids else None
        )

    # Update the graphs shared y-axis :
    prospective_scenario_graphs_shared_y_scale = shared_y_scales.get("prospective_scenario_y_scale", None)
    multidisciplinary_graphs_shared_y_scale    = shared_y_scales.get("multidisciplinary_y_scale", None)

    if prospective_scenario_graphs_shared_y_scale is not None:
        # Update the shared y-axis scale for the prospective scenario graphs :
        min_y, max_y = get_prospective_scenario_y_scales(new_data)
        prospective_scenario_graphs_shared_y_scale.min = min_y
        prospective_scenario_graphs_shared_y_scale.max = max_y

    if multidisciplinary_graphs_shared_y_scale is not None:
        # Update the shared y-axis scale for the prospective scenario graphs :
        min_y, max_y = get_multidisciplinary_graphs_y_scales(new_data)
        multidisciplinary_graphs_shared_y_scale.min = min_y
        multidisciplinary_graphs_shared_y_scale.max = max_y

    # Update each graph based on the selected widgets :
    for index in range(number_of_groups):
        prospective_scenario_graphs[index].update(new_data[index])
        multidisciplinary_graphs[index].update(new_data[index])

    group_comparison_prospective_scenario_graph.update(
        reference_process_engine_data,
        new_data
    )


def draw_interface(number_of_groups: int) -> VBox:
    """
    Draws the main interface of the notebook with all the explanations, graphs and widgets.

    #### Arguments :
    - `number_of_groups` : The number of groups to create the interface for. Must be an interger between 1 and 10.

    #### Returns :
    - `VBox` : A vertical box containing the layout of the interface with all the graphs and widgets.
    """
    # Check if the number of groups is valid :
    if not isinstance(number_of_groups, int) or not (1 <= number_of_groups <= 10):
        raise ValueError("Le nombre de groupes doit être un entier entre 1 et 10.")

    """
    Explanations initialization :
    """
    explanations = draw_explanations()

    """
    Process engines (and checkboxes) initialization :
    """
    # Initialize the reference process engine :
    reference_process_engine      = ProcessEngine()
    reference_process_engine_data = reference_process_engine.compute()

    # Initialize the process engines (and checkboxes) for each group :
    checkboxes_grid, checkboxes_lists = initialize_checkboxes_grid(number_of_groups)
    process_engines                   = initialize_process_engines(number_of_groups)
    process_engines_data              = compute_process_engines(process_engines, checkboxes_lists)

    """
    Prospective Scenario Graphs initialization :
    """
    # Initialize a shared y-axis for all prospective scenario graphs (make them all share the same scale) :
    min_y, max_y = get_prospective_scenario_y_scales(process_engines_data)
    prospective_scenario_graphs_shared_y_scale = LinearScale(min = min_y, max = max_y)

    # Initialize the reference prospective scenario graph :
    reference_prospective_scenario_graph  = initialize_reference_prospective_scenario_graph()
    reference_prospective_scenario_figure = draw_prospective_scenario_graphs(
        [reference_prospective_scenario_graph],
        [reference_process_engine_data],
        prospective_scenario_graphs_shared_y_scale
    )[0]

    # Initialize the prospective scenario graph for each group :
    prospective_scenarios_graphs  = initialize_prospective_scenarios_graphs(number_of_groups)
    prospective_scenarios_figures = draw_prospective_scenario_graphs(
        prospective_scenarios_graphs,
        process_engines_data,
        prospective_scenario_graphs_shared_y_scale
    )

    # Initialize the group comparison prospective scenario graph :
    group_comparison_prospective_scenario_graph = initialize_prospective_scenario_group_comparison_graph(number_of_groups)
    group_comparison_prospective_scenario_figure = draw_prospective_scenario_group_comparison_graph(
        group_comparison_prospective_scenario_graph,
        reference_process_engine_data,
        process_engines_data,
        prospective_scenario_graphs_shared_y_scale
    )

    """
    Multidisciplinary graphs initialization :
    """
    # Initialize a shared y-axis for all multidisciplinary graphs (make them all share the same scale) :
    min_y, max_y = get_multidisciplinary_graphs_y_scales(process_engines_data)
    multidisciplinary_graphs_shared_y_scale = LinearScale(min = min_y, max = max_y)

    # Initialize the reference multidisciplinary graph :
    reference_multidisciplinary_graph  = initialize_reference_multidisciplinary_graph()
    reference_multidisciplinary_figure = draw_multidisciplinary_graphs(
        [reference_multidisciplinary_graph],
        [reference_process_engine_data],
        multidisciplinary_graphs_shared_y_scale
    )[0]

    # Initialize the multidisciplinary graph for each group :
    multidisciplinary_graphs  = initialize_multidisciplinary_graphs(number_of_groups)
    multidisciplinary_figures = draw_multidisciplinary_graphs(
        multidisciplinary_graphs,
        process_engines_data,
        multidisciplinary_graphs_shared_y_scale
    )

    """
    Plot the figures in a grid layout :
    """
    # Create a widget for the title of the checkboxes selection grid :
    checkboxes_grid_title = HTML(f"<div style='margin:50px 0 25px 0; {get_style_string(TITLE_STYLE)}'>Sélection des cartes</div>")
    checkboxes_grid_title_box = Box(
        [checkboxes_grid_title],
        layout = Layout(**TITLE_BOX_LAYOUT)
    )

    # Create a widget for the title of the reference prospective scenario section :
    prospective_scenario_graphs_title = HTML(f"<h1 style='margin:50px 0 0 0; {get_style_string(TITLE_STYLE)}'>Simulations de la trajectoire des émissions de CO₂ du transport aérien entre 2019 et 2050</h1>")
    prospective_scenario_graphs_title_box = Box(
        [prospective_scenario_graphs_title],
        layout = Layout(**TITLE_BOX_LAYOUT)
    )

    # Create a widget for the title of the multidisciplinary graphs section :
    multidisciplinary_graphs_title = HTML(f"<h1 style='margin:50px 0 0 0; {get_style_string(TITLE_STYLE)}'>Pourcentage du budget mondial des ressources consommées par le transport aérien entre 2019 et 2050</h1>")
    multidisciplinary_graphs_title_box = Box(
        [multidisciplinary_graphs_title],
        layout = Layout(**TITLE_BOX_LAYOUT)
    )

    # Create the update button to update all the figures :
    update_button = Button(
        description = "Calculer",
        button_style = "success",
        style = BUTTON_STYLE,
        layout = Layout(**BUTTON_LAYOUT)
    )
    update_button.on_click(
        lambda button: update_figures(
            button,
            number_of_groups,
            reference_process_engine_data,
            process_engines,
            checkboxes_lists,
            {
                "prospective_scenarios_graphs": prospective_scenarios_graphs,
                "prospective_scenario_group_comparison_graph": [group_comparison_prospective_scenario_graph],
                "multidisciplinary_graphs": multidisciplinary_graphs
            },
            {
                "prospective_scenario_y_scale": prospective_scenario_graphs_shared_y_scale,
                "multidisciplinary_y_scale": multidisciplinary_graphs_shared_y_scale
            }
        )
    )

    button_box = Box(
        [update_button],
        layout = Layout(**BUTTON_BOX_LAYOUT)
    )

    # Create the boxes for the prospective scenario figures :
    reference_prospective_scenario_box = AppLayout(
        center = reference_prospective_scenario_figure,
        layout = Layout(**PROSPECTIVE_SCENARIO_BOX_LAYOUT)
    )

    prospective_scenario_boxes = [
        AppLayout(
            center = figure,
            layout = Layout(**PROSPECTIVE_SCENARIO_BOX_LAYOUT)
        )
        for figure in prospective_scenarios_figures
    ]

    # Create the box for the group comparison prospective scenario figure :
    group_comparison_prospective_scenario_box = AppLayout(
        center = group_comparison_prospective_scenario_figure,
        layout = Layout(**PROSPECTIVE_SCENARIO_BOX_LAYOUT)
    )

    # Create the boxes for the multidisciplinary figures (each box contains two figures) :
    multidisciplinary_boxes = []
    if number_of_groups % 2 == 0:
        # If the number of groups is even, we can pair them up (and center the reference scenario) :
        multidisciplinary_boxes.append(
            Box(
                [reference_multidisciplinary_figure],
                layout = Layout(**MULTIDISCIPLINARY_BOX_LAYOUT)
            )
        )
        for index in range(0, len(multidisciplinary_figures), 2):
            multidisciplinary_boxes.append(
                Box(
                    multidisciplinary_figures[index : index + 2],
                    layout = Layout(**MULTIDISCIPLINARY_BOX_LAYOUT)
                )
            )
    else:
        # If the number of groups is odd, we add the reference scenario to the first box :
        all_multidisciplinary_figures = [reference_multidisciplinary_figure] + multidisciplinary_figures

        for index in range(0, len(all_multidisciplinary_figures), 2):
            multidisciplinary_boxes.append(
                Box(
                    all_multidisciplinary_figures[index : index + 2],
                    layout = Layout(**MULTIDISCIPLINARY_BOX_LAYOUT)
                )
            )

    """
    Organize the layout of the interface using a container grid :
    """
    # Create the list of rows for the grid layout :
    rows = [
        explanations,
        checkboxes_grid_title_box,
        checkboxes_grid,
        button_box,
        prospective_scenario_graphs_title_box,
        reference_prospective_scenario_box,
        *prospective_scenario_boxes,
        group_comparison_prospective_scenario_box,
        multidisciplinary_graphs_title_box,
        *multidisciplinary_boxes
    ]

    # Create the container grid layout with the specified number of rows and one column :
    container = VBox(rows, layout = Layout(**APP_VBOX_LAYOUT))

    return container
