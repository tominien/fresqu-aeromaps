from typing import List

from bqplot import LinearScale
from src.bqplot_figures.prospective_scenario_graph import ProspectiveScenarioGraph, get_prospective_scenario_y_scales
from src.bqplot_figures.multidisciplinary_graph import MultidisciplinaryGraph, get_multidisciplinary_graphs_y_scales

from ipywidgets import Box, VBox, Layout, Checkbox, Button

from src.ui.utils.fresque_aeromaps_UI_constants import (
    CARDS_NAMES,
    DEFAULT_NUMBER_OF_GROUPS,
    BUTTON_BOX_LAYOUT,
    PROSPECTIVE_SCENARIO_BOX_LAYOUT,
    MULTIDISCIPLINARY_BOX_LAYOUT,
    SECTION_VBOX_LAYOUT
)
from src.ui.utils.fresque_aeromaps_UI_widgets import (
    initialize_group_selector,
    initialize_checkboxes_grid,
    draw_explanations,
    draw_group_selector_title,
    draw_group_selector_button,
    draw_checkboxes_grid_title,
    draw_prospective_scenario_graphs_title,
    draw_multidisciplinary_graphs_title,
    draw_update_button
)
from src.ui.utils.fresque_aeromaps_UI_figures import (
    compute_process_engine,
    initialize_process_engine,
    initialize_prospective_scenario_graph,
    initialize_prospective_scenario_group_comparison_graph,
    initialize_multidisciplinary_graph,
    draw_prospective_scenario_graph,
    draw_prospective_scenario_group_comparison_graph,
    draw_multidisciplinary_graph
)




def create_prospective_scenarios_boxes(prospective_scenarios_figures: List[ProspectiveScenarioGraph]) -> VBox:
    """
    Creates a list of boxes containing the prospective scenario figures.

    #### Parameters :
    - `prospective_scenarios_figures (List[ProspectiveScenarioGraph])` : A list of prospective scenario figures to be displayed in boxes.

    #### Returns :
    - `VBox` : A vertical box containing all the prospective scenario figures.
    """
    return VBox(
        [
            figure for figure in prospective_scenarios_figures
        ],
        layout = Layout(**PROSPECTIVE_SCENARIO_BOX_LAYOUT)
    )


def create_multidisciplinary_boxes(
        number_of_groups: int,
        reference_multidisciplinary_figure: MultidisciplinaryGraph,
        multidisciplinary_figures: List[MultidisciplinaryGraph]
    ) -> List[Box]:
    """
    Creates a list of boxes containing the multidisciplinary figures (each box contains two figures).

    #### Parameters :
    - `multidisciplinary_figures (List[MultidisciplinaryGraph])` : A list of multidisciplinary figures to be displayed in boxes.

    #### Returns :
    - `List[Box]` : A list of boxes containing the multidisciplinary figures.
    """
    multidisciplinary_boxes = []

    # If the number of groups is even, we can pair them up (and center the reference scenario) :
    if number_of_groups % 2 == 0:
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

    # If the number of groups is odd, we add the reference scenario to the first box :
    else:
        all_multidisciplinary_figures = [reference_multidisciplinary_figure] + multidisciplinary_figures

        for index in range(0, len(all_multidisciplinary_figures), 2):
            multidisciplinary_boxes.append(
                Box(
                    all_multidisciplinary_figures[index : index + 2],
                    layout = Layout(**MULTIDISCIPLINARY_BOX_LAYOUT)
                )
            )

    return multidisciplinary_boxes


class FresqueAeroMapsUI:
    def __init__(
            self,
            default_number_of_groups: int = DEFAULT_NUMBER_OF_GROUPS
            ) -> None:
        """
        Initializes the Fresque-AeroMaps application main interface.
        To display the interface, you must call the `self.display_interface` method.

        #### Arguments :
        - `default_number_of_groups` : The default number of groups to display in the interface. Default to `DEFAULT_NUMBER_OF_GROUPS`.
        """
        # Check if the default number of groups is valid :
        if not isinstance(default_number_of_groups, int) or not (1 <= default_number_of_groups <= 10):
            raise ValueError("Le nombre de groupes doit être un entier entre 1 et 10.")
        self.number_of_groups = default_number_of_groups

        # Initialize the interface components :
        self._initialize_checkboxes_lists()
        self._initialize_process_engines()
        self._initialize_prospective_scenario_graphs()
        self._initialize_multidisciplinary_graphs()

        # Build the interface sections :
        self._build_explanation_section()
        self._build_group_selector_section()
        self._build_checkboxes_grid_section()
        self._build_prospective_scenario_section()
        self._build_multidisciplinary_section()


    def _compute_process_engines(self, compute_reference_process: bool = False) -> None:
        """
        Computes the process engines data for each group based on the selected checkboxes.

        #### Arguments :
        - `compute_reference_process` : If True, computes the reference process engine data. Default to False.
        """
        # Compute the reference process engine data (if asked) :
        if compute_reference_process:
            self.reference_process_engine_data = compute_process_engine(self.reference_process_engine)

        # Compute each process based on the selected widgets :
        self.process_engines_data = []
        for process_engine, checkboxes in zip(self.process_engines, self.checkboxes_lists):
            self.process_engines_data.append(
                compute_process_engine(process_engine, checkboxes)
            )


    def _initialize_checkboxes_lists(self) -> None:
        """
        Initializes the checkboxes lists for each group.
        """
        self.checkboxes_lists = []
        for _ in range(self.number_of_groups):
            self.checkboxes_lists.append(
                [
                    Checkbox(value = False) for _ in range(len(CARDS_NAMES)) # We don't set the visual elements here (indent and layout), they will be set in the `self._build_checkboxes_grid_section` function.
                ]
            )


    def _update_checkboxes_lists(self, old_number_of_groups: int) -> None:
        """
        Updates the checkboxes lists based on the new number of groups.

        #### Arguments :
        - `old_number_of_groups` : The previous number of groups to update the checkboxes lists.
        """
        # If the number of groups has not changed, do nothing :
        if old_number_of_groups == self.number_of_groups:
            return

        # Update the checkboxes lists based on the new number of groups :
        if self.number_of_groups > old_number_of_groups:
            # Add new checkboxes for the new groups :
            for _ in range(self.number_of_groups - old_number_of_groups):
                self.checkboxes_lists.append(
                    [
                        Checkbox(value = False) for _ in range(len(CARDS_NAMES))
                    ]
                )
        else:
            # Remove checkboxes for the removed groups :
            self.checkboxes_lists = self.checkboxes_lists[:self.number_of_groups]


    def _initialize_process_engines(self) -> None:
        """
        Initializes the process engines used in the interface.

        #### Preconditions :
        - The `self._initialize_checkboxes_lists` function must be called before this function.
        """
        # Initialize the reference process engine :
        self.reference_process_engine = initialize_process_engine()

        # Initialize the process engines for each group :
        self.process_engines = [
            initialize_process_engine() for _ in range(self.number_of_groups)
        ]

        # Compute the reference process engine data and the process engines data for each group :
        self._compute_process_engines(True) # The reference scenario only needs to be computed once.


    def _update_process_engines(self, old_number_of_groups: int) -> None:
        """
        Updates the process engines based on the new number of groups and the checkboxes lists.

        #### Arguments :
        - `old_number_of_groups` : The previous number of groups to update the process engines.
        """
        # If the number of groups has not changed, do nothing :
        if old_number_of_groups == self.number_of_groups:
            return

        # Update the process engines list based on the new number of groups :
        if self.number_of_groups > old_number_of_groups:
            # Add new process engines for the new groups :
            for _ in range(self.number_of_groups - old_number_of_groups):
                self.process_engines.append(initialize_process_engine())
        else:
            # Remove process engines for the removed groups :
            self.process_engines = self.process_engines[:self.number_of_groups]

        # Compute the process engines data for each group (even the old ones) based on the selected checkboxes :
        self._compute_process_engines()


    def _initialize_prospective_scenario_graphs(self) -> None:
        """
        Initializes the prospective scenario graphs used in the interface.

        #### Preconditions :
        - The `self._initialize_process_engines` function must be called before this function.
        """
        # Initialize a shared y-axis for all prospective scenario graphs (make them all share the same scale) :
        min_y, max_y = get_prospective_scenario_y_scales(self.process_engines_data)
        self.prospective_scenario_graphs_shared_y_scale = LinearScale(min = min_y, max = max_y)

        # Initialize the reference prospective scenario graph :
        self.reference_prospective_scenario_graph = initialize_prospective_scenario_graph("Scénario de référence")
        self.reference_prospective_scenario_figure = draw_prospective_scenario_graph(
            self.reference_prospective_scenario_graph,
            self.reference_process_engine_data,
            self.prospective_scenario_graphs_shared_y_scale
        )

        # Initialize the prospective scenario graph for each group :
        self.prospective_scenarios_graphs = [
            initialize_prospective_scenario_graph(f"Scénario du groupe {index + 1}")
            for index in range(self.number_of_groups)
        ]
        self.prospective_scenarios_figures = []
        for prospective_scenario_graph, process_engine_data in zip(self.prospective_scenarios_graphs, self.process_engines_data):
            self.prospective_scenarios_figures.append(
                draw_prospective_scenario_graph(
                    prospective_scenario_graph,
                    process_engine_data,
                    self.prospective_scenario_graphs_shared_y_scale
                )
            )

        # Initialize the group comparison prospective scenario graph :
        self.group_comparison_prospective_scenario_graph = initialize_prospective_scenario_group_comparison_graph(self.number_of_groups)
        self.group_comparison_prospective_scenario_figure = draw_prospective_scenario_group_comparison_graph(
            self.group_comparison_prospective_scenario_graph,
            self.reference_process_engine_data,
            self.process_engines_data,
            self.prospective_scenario_graphs_shared_y_scale
        )


    def _update_prospective_scenario_graphs(self, old_number_of_groups: int) -> None:
        """
        Updates the prospective scenario graphs based on the selected checkboxes and the process engines.

        #### Preconditions :
        - The `self._initialize_prospective_scenario_graphs`, `self._update_checkboxes_lists` and `self._update_process_engines` functions must be called before this function.

        #### Arguments :
        - `old_number_of_groups` : The previous number of groups to update the prospective scenario graphs.
        """
        # If the number of groups has not changed, do nothing :
        if old_number_of_groups == self.number_of_groups:
            return

        # Update the shared y-axis scale for the prospective scenario graphs :
        self.prospective_scenario_graphs_shared_y_scale.min, self.prospective_scenario_graphs_shared_y_scale.max = get_prospective_scenario_y_scales(self.process_engines_data)

        # Update the prospective scenario graphs list based on the new number of groups :
        if self.number_of_groups > old_number_of_groups:
            # Add new prospective scenario graphs for the new groups :
            for index in range(self.number_of_groups - old_number_of_groups):
                new_prospective_scenarios_graph = initialize_prospective_scenario_graph(f"Scénario du groupe {old_number_of_groups + index + 1}")
                self.prospective_scenarios_graphs.append(new_prospective_scenarios_graph)
                self.prospective_scenarios_figures.append(
                    draw_prospective_scenario_graph(
                        new_prospective_scenarios_graph,
                        self.process_engines_data[old_number_of_groups + index],
                        self.prospective_scenario_graphs_shared_y_scale
                    )
                )
        else:
            # Remove prospective scenario graphs for the removed groups :
            self.prospective_scenarios_graphs = self.prospective_scenarios_graphs[:self.number_of_groups]
            self.prospective_scenarios_figures = self.prospective_scenarios_figures[:self.number_of_groups]

        # Update the group comparison prospective scenario graph :
        self.group_comparison_prospective_scenario_graph = initialize_prospective_scenario_group_comparison_graph(self.number_of_groups)
        self.group_comparison_prospective_scenario_figure = draw_prospective_scenario_group_comparison_graph(
            self.group_comparison_prospective_scenario_graph,
            self.reference_process_engine_data,
            self.process_engines_data,
            self.prospective_scenario_graphs_shared_y_scale
        )


    def _initialize_multidisciplinary_graphs(self) -> None:
        """
        Initializes the multidisciplinary graphs used in the interface.

        #### Preconditions :
        - The `self._initialize_process_engines` function must be called before this function.
        """
        # Initialize a shared y-axis for all multidisciplinary graphs (make them all share the same scale) :
        min_y, max_y = get_multidisciplinary_graphs_y_scales(self.process_engines_data)
        self.multidisciplinary_graphs_shared_y_scale = LinearScale(min = min_y, max = max_y)

        # Initialize the reference multidisciplinary graph :
        self.reference_multidisciplinary_graph = initialize_multidisciplinary_graph("Scénario de référence")
        self.reference_multidisciplinary_figure = draw_multidisciplinary_graph(
            self.reference_multidisciplinary_graph,
            self.reference_process_engine_data,
            self.multidisciplinary_graphs_shared_y_scale
        )

        # Initialize the multidisciplinary graph for each group :
        self.multidisciplinary_graphs = [
            initialize_multidisciplinary_graph(f"Scénario du groupe {index + 1}")
            for index in range(self.number_of_groups)
        ]
        self.multidisciplinary_figures = []
        for multidisciplinary_graph, process_engine_data in zip(self.multidisciplinary_graphs, self.process_engines_data):
            self.multidisciplinary_figures.append(
                draw_multidisciplinary_graph(
                    multidisciplinary_graph,
                    process_engine_data,
                    self.multidisciplinary_graphs_shared_y_scale
                )
            )


    def _update_multidisciplinary_graphs(self, old_number_of_groups: int) -> None:
        """
        Updates the multidisciplinary graphs based on the selected checkboxes and the process engines.

        #### Preconditions :
        - The `self._initialize_multidisciplinary_graphs`, `self._update_checkboxes_lists` and `self._update_process_engines` functions must be called before this function.

        #### Arguments :
        - `old_number_of_groups` : The previous number of groups to update the multidisciplinary graphs.
        """
        # If the number of groups has not changed, do nothing :
        if old_number_of_groups == self.number_of_groups:
            return

        # Update the shared y-axis scale for the multidisciplinary graphs :
        self.multidisciplinary_graphs_shared_y_scale.min, self.multidisciplinary_graphs_shared_y_scale.max = get_multidisciplinary_graphs_y_scales(self.process_engines_data)

        # Update the multidisciplinary graphs list based on the new number of groups :
        if self.number_of_groups > old_number_of_groups:
            # Add new multidisciplinary graphs for the new groups :
            for index in range(self.number_of_groups - old_number_of_groups):
                new_multidisciplinary_graph = initialize_multidisciplinary_graph(f"Scénario du groupe {old_number_of_groups + index + 1}")
                self.multidisciplinary_graphs.append(new_multidisciplinary_graph)
                self.multidisciplinary_figures.append(
                    draw_multidisciplinary_graph(
                        new_multidisciplinary_graph,
                        self.process_engines_data[old_number_of_groups + index],
                        self.multidisciplinary_graphs_shared_y_scale
                    )
                )
        else:
            # Remove multidisciplinary graphs for the removed groups :
            self.multidisciplinary_graphs = self.multidisciplinary_graphs[:self.number_of_groups]
            self.multidisciplinary_figures = self.multidisciplinary_figures[:self.number_of_groups]


    def _build_explanation_section(self) -> VBox:
        """
        Builds the explanation section of the interface.

        #### Returns :
        - `VBox` : A vertical box containing the explanation text.
        """
        self.explanation_section = draw_explanations()

        return self.explanation_section


    def _build_group_selector_section(self) -> VBox:
        """
        Builds the group selector section of the interface.

        #### Returns :
        - `VBox` : A vertical box containing the group selector section title and slider.
        """
        # Create the title for the group selector :
        self.group_selector_title = draw_group_selector_title()

        # Initialize the group selector slider :
        self.group_selector = initialize_group_selector(
            default_value = self.number_of_groups
        )

        # Create a button to update the interface based on the selected number of groups :
        self.group_selector_button = draw_group_selector_button()
        self.group_selector_button.on_click(lambda button: self._on_group_selector_change())

        # Create the group selector section :
        self.group_selector_section = VBox(
            [
                self.group_selector_title,
                self.group_selector,
                self.group_selector_button
            ],
            layout = Layout(**SECTION_VBOX_LAYOUT)
        )

        return self.group_selector_section


    def _build_checkboxes_grid_section(self) -> VBox:
        """
        Builds the checkboxes grid section of the interface.

        #### Returns :
        - `VBox` : A vertical box containing the checkboxes grid section title, checkbox grid and update button.
        """
        # Create the title for the checkboxes grid :
        self.checkboxes_grid_title = draw_checkboxes_grid_title()

        # Initialize the checkboxes grid :
        self.checkboxes_grid = initialize_checkboxes_grid(self.number_of_groups, self.checkboxes_lists)

        # Create the update button to update all the figures :
        self.update_button = draw_update_button()
        self.update_button.on_click(lambda button: self._update_figures())

        self.update_button_box = Box(
            [self.update_button],
            layout = Layout(**BUTTON_BOX_LAYOUT)
        )

        # Create the checkboxes grid section :
        self.checkboxes_grid_section = VBox(
            [
                self.checkboxes_grid_title,
                self.checkboxes_grid,
                self.update_button_box
            ],
            layout = Layout(**SECTION_VBOX_LAYOUT)
        )

        return self.checkboxes_grid_section


    def _update_checkboxes_grid_section(self) -> VBox:
        """
        Updates the checkboxes grid section of the interface.
        """
        # Rebuild the checkboxes grid section with the updated checkboxes grid :
        self.checkboxes_grid = initialize_checkboxes_grid(self.number_of_groups, self.checkboxes_lists)

        # Update the checkboxes grid section with the new checkboxes grid :
        self.checkboxes_grid_section.children = [
            self.checkboxes_grid_title,
            self.checkboxes_grid,
            self.update_button_box
        ]

        return self.checkboxes_grid_section


    def _build_prospective_scenario_section(self) -> VBox:
        """
        Builds the prospective scenario section of the interface.

        #### Preconditions :
        - The `self.initialize_prospective_scenario_graphs` function must be called before this function.

        #### Returns :
        - `VBox` : A vertical box containing the prospective scenario graphs title, reference prospective scenario box, prospective scenario boxes and group comparison prospective scenario box.
        """
        # Create a widget for the title of the reference prospective scenario section :
        self.prospective_scenario_graphs_title = draw_prospective_scenario_graphs_title()

        # Create the boxes for the prospective scenario figures :
        self.reference_prospective_scenario_box = Box(
            [self.reference_prospective_scenario_figure],
            layout = Layout(**PROSPECTIVE_SCENARIO_BOX_LAYOUT)
        )

        self.prospective_scenarios_boxes = create_prospective_scenarios_boxes(self.prospective_scenarios_figures)

        # Create the box for the group comparison prospective scenario figure :
        self.group_comparison_prospective_scenario_box = Box(
            [self.group_comparison_prospective_scenario_figure],
            layout = Layout(**PROSPECTIVE_SCENARIO_BOX_LAYOUT)
        )

        # Create the prospective scenario section :
        self.prospective_scenario_section = VBox(
            [
                self.prospective_scenario_graphs_title,
                self.reference_prospective_scenario_box,
                self.prospective_scenarios_boxes,
                self.group_comparison_prospective_scenario_box
            ],
            layout = Layout(**SECTION_VBOX_LAYOUT)
        )

        return self.prospective_scenario_section


    def _update_prospective_scenario_section(self) -> VBox:
        """
        Updates the prospective scenario section of the interface.
        """
        # Rebuild the prospective scenario section with the updated prospective scenario boxes :
        self.prospective_scenarios_boxes = create_prospective_scenarios_boxes(self.prospective_scenarios_figures)

        # Update the prospective scenario section with the new prospective scenario boxes :
        self.group_comparison_prospective_scenario_box = Box(
            [self.group_comparison_prospective_scenario_figure],
            layout = Layout(**PROSPECTIVE_SCENARIO_BOX_LAYOUT)
        )
        self.prospective_scenario_section.children = [
            self.prospective_scenario_graphs_title,
            self.reference_prospective_scenario_box,
            self.prospective_scenarios_boxes,
            self.group_comparison_prospective_scenario_box
        ]

        return self.prospective_scenario_section


    def _build_multidisciplinary_section(self) -> VBox:
        """
        Builds the multidisciplinary section of the interface.

        #### Preconditions :
        - The `self.initialize_multidisciplinary_graphs` function must be called before this function.

        #### Returns :
        - `VBox` : A vertical box containing the multidisciplinary graphs title and multidisciplinary boxes.
        """
        # Create a widget for the title of the multidisciplinary graphs section :
        self.multidisciplinary_graphs_title = draw_multidisciplinary_graphs_title()

        # Create the boxes for the multidisciplinary figures (each box contains two figures) :
        self.multidisciplinary_boxes = create_multidisciplinary_boxes(
            self.number_of_groups,
            self.reference_multidisciplinary_figure,
            self.multidisciplinary_figures
        )

        # Create the multidisciplinary section :
        self.multidisciplinary_section = VBox(
            [
                self.multidisciplinary_graphs_title,
                *self.multidisciplinary_boxes
            ],
            layout = Layout(**SECTION_VBOX_LAYOUT)
        )

        return self.multidisciplinary_section


    def _update_multidisciplinary_section(self) -> VBox:
        """
        Updates the multidisciplinary section of the interface.
        """
        # Rebuild the multidisciplinary section with the updated multidisciplinary boxes :
        self.multidisciplinary_boxes = create_multidisciplinary_boxes(
            self.number_of_groups,
            self.reference_multidisciplinary_figure,
            self.multidisciplinary_figures
        )

        # Update the multidisciplinary section with the new multidisciplinary boxes :
        self.multidisciplinary_section.children = [
            self.multidisciplinary_graphs_title,
            *self.multidisciplinary_boxes
        ]

        return self.multidisciplinary_section


    def _update_figures(self, _button: Button = None) -> None:
        """
        Updates the figures based on the selected checkboxes and the process engines.
        """
        # Compute the process engines data for each group based on the selected checkboxes :
        self._compute_process_engines()

        # Update the figures shared y-axis :
        self.prospective_scenario_graphs_shared_y_scale.min, self.prospective_scenario_graphs_shared_y_scale.max = get_prospective_scenario_y_scales(self.process_engines_data)
        self.multidisciplinary_graphs_shared_y_scale.min, self.multidisciplinary_graphs_shared_y_scale.max = get_multidisciplinary_graphs_y_scales(self.process_engines_data)

        # Update each figure based on the selected checkboxes :
        for index in range(self.number_of_groups):
            self.prospective_scenarios_graphs[index].update(self.process_engines_data[index])
            self.multidisciplinary_graphs[index].update(self.process_engines_data[index])

        self.group_comparison_prospective_scenario_graph.update(
            self.reference_process_engine_data,
            self.process_engines_data
        )


    def _on_group_selector_change(self, _button: Button = None) -> None:
        """
        Handles the change event of the group selector slider.
        """
        # Update the number of groups based on the slider value :
        old_number_of_groups = self.number_of_groups
        self.number_of_groups = self.group_selector.value

        # If the number of groups has not changed, do nothing :
        if old_number_of_groups == self.number_of_groups:
            return

        # Update the checkboxes lists and process engines :
        self._update_checkboxes_lists(old_number_of_groups)
        self._update_process_engines(old_number_of_groups)

        # Update the prospective scenario graphs and multidisciplinary graphs :
        self._update_prospective_scenario_graphs(old_number_of_groups)
        self._update_multidisciplinary_graphs(old_number_of_groups)

        # Rebuild the interface elements impacted by the number of groups change :
        self._update_checkboxes_grid_section()
        self._update_prospective_scenario_section()
        self._update_multidisciplinary_section()


    def display_interface(self) -> VBox:
        """
        Assembles the interface by combining all the sections into a vertical box and returns it.

        #### Returns :
        - `VBox` : A vertical box containing the entire interface layout.
        """
        # Create the container grid layout with the specified number of rows and one column :
        self.interface = VBox(
            [
                self.explanation_section,
                self.group_selector_section,
                self.checkboxes_grid_section,
                self.prospective_scenario_section,
                self.multidisciplinary_section
            ],
            layout = Layout(**SECTION_VBOX_LAYOUT)
        )

        return self.interface
