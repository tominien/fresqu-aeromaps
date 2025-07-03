from typing import Dict, List

from crud.crud_cards import get_cards_name, get_card_id_by_name

from core.aeromaps_utils.process_engine import ProcessEngine

from bqplot import Figure
from bqplot_figures.base_graph import BaseGraph
from bqplot_figures.prospective_scenario_graph import ProspectiveScenarioGraph
from bqplot_figures.multidisciplinary_graph import MultidisciplinaryGraph

from ipywidgets import VBox, HBox, Layout, AppLayout, Checkbox, Button, HTML




"""
Etape de refactorisation du code :
    - Mettre à jour le Trello avec les tâches suivantes (et celles déjà faîtes !).
    - Ce qu'il reste à faire (dans ce fichier) :
        - Finir de factoriser `run_graph_v3()`.
        - Mettre sous forme de classe les graphiques `fig_n` et `bar_n` pour chaque groupe.
        - Faire fonctionner de nouveau le bouton "Calculer" pour mettre à jour les graphiques.
        - Retravailler l'interface (positionnement des widgets, des graphiques, etc...).
        - Ajouter des commentaires et de la documentation.
    - Ce qu'il reste à faire (en dehors de ce fichier) :
        - Refactoriser tout le code nouvellement factorisé (créer un agencement BEAUCOUP plus optimal, quitte à coder de nouveau certaines parties), en :
            - Créant, rennomant et supprimant les fichiers actuels.
            - Créant des dossiers.
            - Renommer les CLASSES, FONCTIONS et VARIABLES.
            - Ecrivant des commentaires plus précis.
            - Ext...
        - Supprimer le fichier `temp.ipynb` lorsqu'on aura fini la refactorisation du code.
        - Ajouter Docker.
        - Tester un déploiment du code sur `onready.com` pour vérifier que tout fonctionne correctement (si non, pleurer).
Fin de l'étape de refactorisation du code.
"""




CARDS_NAMES = get_cards_name()


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


def initialize_prospective_scenarios_graphs(number_of_groups: int) -> List[ProspectiveScenarioGraph]:
    """
    Initializes the prospective scenario graphs for each group.

    #### Arguments :
    - `number_of_groups` : The number of groups to create prospective scenario graphs for.

    #### Returns :
    - `List[ProspectiveScenarioGraph]` : A list of prospective scenario graphs for each group.
    """
    return [ProspectiveScenarioGraph(f"Scénario du groupe {index + 1}") for index in range(number_of_groups)]


def initialize_multidisciplinary_graphs(number_of_groups: int) -> List[MultidisciplinaryGraph]:
    """
    Initializes the multidisciplinary graphs for each group.

    #### Arguments :
    - `number_of_groups` : The number of groups to create multidisciplinary graphs for.

    #### Returns :
    - `List[MultidisciplinaryGraph]` : A list of multidisciplinary graphs for each group.
    """
    return [MultidisciplinaryGraph(f"Scénario du groupe {index + 1}") for index in range(number_of_groups)]


def draw_prospective_scenario_graphs(
    prospective_scenarios_graphs: List[ProspectiveScenarioGraph],
    process_engines_data: List[List[dict]]
) -> List[Figure]:
    """
    Draws the prospective scenario graphs for each group.

    #### Parameters :
    - `prospective_scenarios_graphs` : A list of prospective scenario graphs to draw.
    - `process_engines_data` : A list of computed data for each process engine.

    #### Returns :
    - `List[Figure]` : A list of drawn figures for each prospective scenario graph.
    """
    figures = []

    # Draw each prospective scenario graph with the corresponding data :
    for graph, data in zip(prospective_scenarios_graphs, process_engines_data):
        figure            = graph.draw(data)
        figure.fig_margin = {"top": 60, "bottom": 60, "left": 60, "right": 100}
        figures.append(figure)

    return figures


def draw_multidisciplinary_graphs(
    multidisciplinary_graphs: List[MultidisciplinaryGraph],
    process_engines_data: List[List[dict]]
) -> List[Figure]:
    """
    Draws the multidisciplinary graphs for each group.

    #### Parameters :
    - `multidisciplinary_graphs` : A list of multidisciplinary graphs to draw.
    - `process_engines_data` : A list of computed data for each process engine.

    #### Returns :
    - `List[Figure]` : A list of drawn figures for each multidisciplinary graph.
    """
    figures = []

    # Draw each multidisciplinary graph with the corresponding data :
    for graph, data in zip(multidisciplinary_graphs, process_engines_data):
        figure        = graph.draw(data)
        figure.layout = Layout(width = "50%")
        figures.append(figure)

    return figures


def update_figures(
    _button:         Button,
    number_of_groups: int,
    process_engines: List[ProcessEngine],
    checkboxes_lists:   List[List[Checkbox]],
    graphs:          Dict[str, List[BaseGraph]]
) -> None:
    """
    Updates the figures based on the selected checkboxes and the process engines.

    #### Arguments :
    - `_button` : The button that triggered the update (not used in this function).
    - `number_of_groups` : The number of groups to update the figures for.
    - `process_engines` : A list of process engines to compute the new data.
    - `checkboxes_lists` : A list of lists containing the checkbox widgets for each group.
    - `graphs` : A dictionary containing the prospective scenario graphs and multidisciplinary graphs.

    #### Returns :
    - `None` : This function does not return anything, it updates the graphs in place
    """
    # Get each type of graph from the dictionary :
    prospective_scenario_graphs = graphs["prospective_scenarios_graphs"]
    multidisciplinary_graphs    = graphs["multidisciplinary_graphs"]

    # Update each graph based on the selected widgets :
    for index in range(number_of_groups):
        # Get the selected card IDs for the current group :
        selected_ids = [
            get_card_id_by_name(checkbox.description)
            for checkbox in checkboxes_lists[index]
            if checkbox.value
        ]

        # Compute the new data for the current process engine :
        new_data = process_engines[index].compute(
            tuple(selected_ids) if selected_ids else None
        )

        # Update the corresponding graphs with the new data :
        prospective_scenario_graphs[index].update(new_data)
        multidisciplinary_graphs[index].update(new_data)


def draw_interface(number_of_groups: int) -> VBox:
    """
    Draws the main interface of the notebook with all the graphs and widgets.

    #### Arguments :
    - `number_of_groups` : The number of groups to create the interface for. Must be an interger between 1 and 10.

    #### Returns :
    - `VBox` : A vertical box containing the layout of the interface with all the graphs and widgets.
    """
    # Check if the number of groups is valid :
    if not isinstance(number_of_groups, int) or not (1 <= number_of_groups <= 10):
        raise ValueError("Le nombre de groupes doit être un entier entre 1 et 10.")

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
    # Initialize the reference prospective scenario graph :
    reference_prospective_scenario_graph             = ProspectiveScenarioGraph("Scénario de référence")
    reference_prospective_scenario_figure            = reference_prospective_scenario_graph.draw(reference_process_engine_data)
    reference_prospective_scenario_figure.fig_margin = {"top": 60, "bottom": 60, "left": 60, "right": 100}

    # Initialize the prospective scenario graph for each group :
    prospective_scenarios_graphs  = initialize_prospective_scenarios_graphs(number_of_groups)
    prospective_scenarios_figures = draw_prospective_scenario_graphs(
        prospective_scenarios_graphs,
        process_engines_data
    )

    """
    Multidisciplinary graphs initialization :
    """
    # Initialize the reference multidisciplinary graph :
    reference_multidisciplinary_graph         = MultidisciplinaryGraph("Scénario de référence")
    reference_multidisciplinary_figure        = reference_multidisciplinary_graph.draw(reference_process_engine_data)
    reference_multidisciplinary_figure.layout = Layout(width = "50%")

    # Initialize the multidisciplinary graph for each group :
    multidisciplinary_graphs  = initialize_multidisciplinary_graphs(number_of_groups)
    multidisciplinary_figures = draw_multidisciplinary_graphs(
        multidisciplinary_graphs,
        process_engines_data
    )

    """
    Plot the figures in a grid layout :
    """
    # Create the boxes for the prospective scenario figures :
    reference_prospective_scenario_box = AppLayout(
        center = reference_prospective_scenario_figure,
        align_items = "center",
        width = "100%"
    )

    prospective_scenario_boxes = [
        AppLayout(
            left_sidebar = VBox(checkboxes_lists[index]),
            center = figure,
            align_items = "center",
            width = "100%"
        )
        for index, figure in enumerate(prospective_scenarios_figures)
    ]

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

    # Create the update button to update all the figures :
    update_button = Button(
        description = "Calculer",
        button_style = "success",
        layout = Layout(
            width = "100%",
            height = "125px",
        )
    )
    update_button.on_click(
        lambda button: update_figures(
            button,
            number_of_groups,
            process_engines,
            checkboxes_lists,
            {
                "prospective_scenarios_graphs": prospective_scenarios_graphs,
                "multidisciplinary_graphs": multidisciplinary_graphs
            }
        )
    )

    button_box = HBox(
        [update_button],
        layout = Layout(
            width = "100%",
            height = "175px",
            align_items = "center"
        )
    )

    # Create a widget for the title of the reference prospective scenario section :
    prospective_scenario_graphs_title = HTML("<h3 style='margin:0'>Simulations de l'évolution des émissions de CO₂ du transport aérien sur la période 2019-2050</h3>")
    prospective_scenario_graphs_title_box = HBox(
        [prospective_scenario_graphs_title],
        layout = Layout(
            width = "100%",
            justify_content = "center",
            align_items = "center"
        )
    )

    # Create a widget for the title of the multidisciplinary graphs section :
    multidisciplinary_graphs_title = HTML("<h3 style='margin:0'>Pourcentages du budget des ressources mondiales utilisés par le transport aérien sur la période 2019-2050</h3>")
    multidisciplinary_graphs_title_box = HBox(
        [multidisciplinary_graphs_title],
        layout = Layout(
            width = "100%",
            justify_content = "center",
            align_items = "center"
        )
    )

    """
    Organize the layout of the interface using a container grid :
    """
    # Create the list of rows for the grid layout :
    rows = [
        prospective_scenario_graphs_title_box,
        reference_prospective_scenario_box,
        *prospective_scenario_boxes,
        button_box,
        multidisciplinary_graphs_title_box,
        *multidisciplinary_boxes
    ]

    # Create the container grid layout with the specified number of rows and one column :
    container = VBox(rows, layout = Layout(width="100%"))

    return container
