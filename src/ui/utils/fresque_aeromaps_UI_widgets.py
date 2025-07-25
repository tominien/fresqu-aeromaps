from typing import List, Union

from ipywidgets import Box, VBox, Layout, GridspecLayout, Checkbox, HTML, Label, Button, IntSlider

import markdown

from ui.utils.fresque_aeromaps_UI_constants import (
    CARDS_NAMES,
    DEFAULT_NUMBER_OF_GROUPS,
    MIN_NUMBER_OF_GROUPS,
    MAX_NUMBER_OF_GROUPS,
    get_style_string,
    TITLE_STYLE,
    BUTTON_STYLE,
    GROUP_SELECTOR_STYLE,
    EXPLANATIONS_VBOX_LAYOUT,
    TITLE_BOX_LAYOUT,
    BUTTON_LAYOUT,
    GROUP_SELECTOR_LAYOUT,
    CHECKBOXES_GRID_LAYOUT,
    CHECKBOXES_GRID_CELL_LAYOUT,
    CHECKBOXES_GRID_LABEL_LAYOUT,
    CHECKBOXES_GRID_CHECKBOX_LAYOUT
)

from utils import APPLICATION_EXPLANATIONS_PATH




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


def initialize_group_selector(
        default_value: int = DEFAULT_NUMBER_OF_GROUPS,
        min_value: int = MIN_NUMBER_OF_GROUPS,
        max_value: int = MAX_NUMBER_OF_GROUPS
    ) -> IntSlider:
    """
    Initializes a slider to select the number of groups.

    #### Returns :
    - `IntSlider` : A slider widget to select the number of groups.
    """
    # Create the IntSlider widget :
    slider = IntSlider(
        value = default_value,
        min = min_value,
        max = max_value,
        step = 1,
        description = "Nombre de groupes :",
        continuous_update = False,
        style = GROUP_SELECTOR_STYLE,
        layout = Layout(**GROUP_SELECTOR_LAYOUT)
    )

    return slider


def initialize_checkboxes_grid(
        number_of_groups: int,
        checkboxes_lists: List[List[Checkbox]] 
    ) -> GridspecLayout:
    """
    Initializes the grid layout for the checkboxes and returns it along with a list of lists containing the checkbox widgets.

    #### Arguments :
    - `number_of_groups (int)` : The number of groups to create checkboxes for.
    - `checkboxes_lists (List[List[Checkbox]])` : A list of lists to store the checkbox widgets for each group.

    #### Returns :
    - `GridspecLayout` : The grid layout containing the checkboxes.
    """
    # Check if the checkboxes_lists is in the correct format :
    error_message = "checkboxes_lists must be a list of lists containing Checkbox widgets, with each inner list having the same length as CARDS_NAMES."

    if not isinstance(checkboxes_lists, list) or len(checkboxes_lists) != number_of_groups:
        raise ValueError(error_message)

    for checkboxes_list in checkboxes_lists:
        if not isinstance(checkboxes_list, list) :
            raise ValueError(error_message)
        # Check if each inner list contains Checkbox widgets and has the same length as CARDS_NAMES :
        if len(checkboxes_list) != len(CARDS_NAMES) or not all(isinstance(checkbox, Checkbox) for checkbox in checkboxes_list):
            raise ValueError(error_message)

    # Create a wrapper function to create the checkboxes grid cells :
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
    for index_column in range(2, number_of_columns):
        # Create the label for the group name :
        label = Label(
            value = f"Groupe {index_column - 1}",
            layout = Layout(**CHECKBOXES_GRID_LABEL_LAYOUT)
        )
        grid[0, index_column] = create_cell_checkboxes_grid(label, ["top", "right", "bottom"])
        # Create the checkboxes for each group :
        for index_row, card_name in enumerate(CARDS_NAMES):
            # Create the checkbox for the current group :
            checkbox = checkboxes_lists[index_column - 2][index_row]
            checkbox.indent = False
            checkbox.layout = Layout(**CHECKBOXES_GRID_CHECKBOX_LAYOUT)
            # Create the cell with the checkbox :
            cell = create_cell_checkboxes_grid(checkbox, ["right", "bottom"])
            grid[index_row + 1, index_column] = cell

    return grid


def draw_group_selector_title() -> Box:
    """
    Draws the title for the group number selection slider section.

    #### Returns :
    - `Box` : A box containing the title for the group number selection slider.
    """
    group_selector_title = HTML(f"<div style='margin:50px 0 25px 0; {get_style_string(TITLE_STYLE)}'>Sélection du nombre de groupe</div>")

    return Box(
        [group_selector_title],
        layout = Layout(**TITLE_BOX_LAYOUT)
    )


def draw_group_selector_button() -> Button:
    """
    Draws the button to update the interface based on the selected number of groups.

    #### Returns :
    - `Button` : The button to update the interface.
    """
    return Button(
        description = "Mettre à jour le nombre de groupes",
        button_style = "success",
        style = BUTTON_STYLE,
        layout = Layout(**BUTTON_LAYOUT)
    )


def draw_checkboxes_grid_title() -> Box:
    """
    Draws the title for the checkboxes selection grid section.

    #### Returns :
    - `Box` : A box containing the title for the checkboxes selection grid.
    """
    checkboxes_grid_title = HTML(f"<div style='margin:75px 0 25px 0; {get_style_string(TITLE_STYLE)}'>Sélection des cartes</div>")

    return Box(
        [checkboxes_grid_title],
        layout = Layout(**TITLE_BOX_LAYOUT)
    )


def draw_prospective_scenario_graphs_title() -> Box:
    """
    Draws the title for the prospective scenario graphs section.

    #### Returns :
    - `Box` : A box containing the title for the prospective scenario graphs.
    """
    prospective_scenario_graphs_title = HTML(f"<h1 style='margin:75px 0 0 0; {get_style_string(TITLE_STYLE)}'>Simulations de la trajectoire des émissions de CO₂ du transport aérien entre 2019 et 2050</h1>")

    return Box(
        [prospective_scenario_graphs_title],
        layout = Layout(**TITLE_BOX_LAYOUT)
    )


def draw_multidisciplinary_graphs_title() -> Box:
    """
    Draws the title for the multidisciplinary graphs section.

    #### Returns :
    - `Box` : A box containing the title for the multidisciplinary graphs.
    """
    multidisciplinary_graphs_title = HTML(f"<h1 style='margin:50px 0 0 0; {get_style_string(TITLE_STYLE)}'>Pourcentage du budget mondial des ressources consommées par le transport aérien entre 2019 et 2050</h1>")

    return Box(
        [multidisciplinary_graphs_title],
        layout = Layout(**TITLE_BOX_LAYOUT)
    )


def draw_update_button() -> Button:
    """
    Draws the update button to update all the figures.

    #### Returns :
    - `Button` : The update button.
    """
    return Button(
        description = "Mettre à jour les graphiques",
        button_style = "success",
        style = BUTTON_STYLE,
        layout = Layout(**BUTTON_LAYOUT)
    )