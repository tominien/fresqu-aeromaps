from typing import Any, Dict, List, Optional

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

from ipywidgets import VBox, HBox, Layout, AppLayout, Checkbox, Button, HTML, Label

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
        layout = Layout(
            width = "100%",
            overflow = "auto",
            align_items = "center"
        )
    )


def initialize_checkboxes(number_of_groups: int) -> List[List[Checkbox]]:
    """
    Initializes the checkbox widgets for each group.

    #### Arguments :
    - `number_of_groups` : The number of groups to create checkboxes for.

    #### Returns :
    - `List[List[Checkbox]]` : A list of lists containing the checkbox widgets for each group.
    """
    # Get the list of cards names :
    cards_list = CARDS_NAMES

    # Create a list of widgets for each group :
    checkboxes_lists = []
    for _ in range(number_of_groups):
        widgets = [
            Checkbox(
                value = False,
                description = card,
                indent = False
            )
            for card in cards_list
        ]
        checkboxes_lists.append(widgets)

    return checkboxes_lists


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
    def draw_disciplinary_graph_legend(colors: List[str], labels: List[str], opacities: List[str]) -> HBox:
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
                    value = f"<span style = 'display: inline-block; width: 12px; height: 12px; background-color: {color}; opacity:{alpha}'></span>"
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
            layout = Layout(
                width = "100%",
                justify_content = "center",
                margin = "-12px 0 0 0"
            )
        )

    widgets = []

    # Draw each multidisciplinary graph with the corresponding data :
    for graph, data in zip(multidisciplinary_graphs, process_engines_data):
        figure = graph.draw(data, y_scale = shared_y_scale, display_default_legend = False)
        figure.layout = Layout(width = "100%")
        figure_legend = draw_disciplinary_graph_legend(*graph.get_legend_elements())

        # Create a VBox to contain the figure and its legend :
        widgets.append(
            VBox(
                [figure, figure_legend],
                layout = Layout(
                    width = "50%",
                    overflow = "hidden",
                    align_items = "center"
                )
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
        selected_ids = [
            get_card_id_by_name(checkbox.description)
            for checkbox in checkboxes_lists[index]
            if checkbox.value
        ]

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
    checkboxes_lists     = initialize_checkboxes(number_of_groups)
    process_engines      = initialize_process_engines(number_of_groups)
    process_engines_data = compute_process_engines(process_engines, checkboxes_lists)

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
    # Create the update button to update all the figures :
    update_button = Button(
        description = "Calculer",
        button_style = "success",
        style = {
            "font_size": "32px",
            "font_weight": "bold",
            "text_align": "center"
        },
        layout = Layout(
            width = "100%",
            height = "125px",
        )
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

    button_box = HBox(
        [update_button],
        layout = Layout(
            width = "100%",
            height = "175px",
            align_items = "center",
            overflow = "hidden"
        )
    )

    # Create a widget for the title of the reference prospective scenario section :
    prospective_scenario_graphs_title = HTML("<h1 style='margin:50px 0 0 0; text-decoration: underline'>Simulations de la trajectoire des émissions de CO₂ du transport aérien entre 2019 et 2050</h1>")
    prospective_scenario_graphs_title_box = HBox(
        [prospective_scenario_graphs_title],
        layout = Layout(
            width = "100%",
            justify_content = "center",
            overflow = "hidden"
        )
    )

    # Create a widget for the title of the multidisciplinary graphs section :
    multidisciplinary_graphs_title = HTML("<h1 style='margin:50px 0 0 0; text-decoration: underline'>Pourcentage du budget mondial des ressources consommées par le transport aérien entre 2019 et 2050</h1>")
    multidisciplinary_graphs_title_box = HBox(
        [multidisciplinary_graphs_title],
        layout = Layout(
            width = "100%",
            justify_content = "center",
            overflow = "hidden"
        )
    )

    # Create the boxes for the prospective scenario figures :
    reference_prospective_scenario_box = AppLayout(
        center = reference_prospective_scenario_figure,
        layout = Layout(
            width = "100%",
            align_items = "center",
            overflow = "hidden"
        )
    )

    prospective_scenario_boxes = [
        AppLayout(
            left_sidebar = VBox(
                checkboxes_lists[index],
                layout = Layout(
                    margin = "0 15px 0 15px"
                )
            ),
            center = figure,
            layout = Layout(
                width = "100%",
                align_items = "center",
                overflow = "hidden"
            ),
        )
        for index, figure in enumerate(prospective_scenarios_figures)
    ]

    # Create the box for the group comparison prospective scenario figure :
    group_comparison_prospective_scenario_box = AppLayout(
        center = group_comparison_prospective_scenario_figure,
        layout = Layout(
            width = "100%",
            align_items = "center",
            overflow = "hidden"
        )
    )

    # Create the boxes for the multidisciplinary figures (each box contains two figures) :
    if number_of_groups % 2 == 0:
        # If the number of groups is even, we can pair them up (and centrer the reference scenario) :
        multidisciplinary_boxes = [
            HBox(
                [reference_multidisciplinary_figure],
                layout = Layout(
                    width = "100%",
                    justify_content = "space-around",
                    align_items = "flex-start"
                )
            )
        ] + [
            HBox(
                multidisciplinary_figures[index : index + 2],
                layout = Layout(
                    width = "100%",
                    justify_content = "space-around",
                    align_items = "flex-start"
                )
            )
            for index in range(0, len(multidisciplinary_figures), 2)
        ]

    else:
        # If the number of groups is odd, we add the reference scenario to the first box :
        all_multidisciplinary_figures = [reference_multidisciplinary_figure] + multidisciplinary_figures

        multidisciplinary_boxes = [
            HBox(
                all_multidisciplinary_figures[index : index + 2],
                layout = Layout(
                    width = "100%",
                    justify_content = "space-around",
                    align_items = "flex-start"
                )
            )
            for index in range(0, len(all_multidisciplinary_figures), 2)
        ]

    """
    Organize the layout of the interface using a container grid :
    """
    # Create the list of rows for the grid layout :
    rows = [
        explanations,
        button_box,
        prospective_scenario_graphs_title_box,
        reference_prospective_scenario_box,
        *prospective_scenario_boxes,
        group_comparison_prospective_scenario_box,
        multidisciplinary_graphs_title_box,
        *multidisciplinary_boxes
    ]

    # Create the container grid layout with the specified number of rows and one column :
    container = VBox(rows, layout = Layout(width = "100%"))

    return container
