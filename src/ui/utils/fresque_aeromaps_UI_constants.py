from typing import Dict

from crud.crud_cards import get_cards_name




# Define the general constants:
CARDS_NAMES = get_cards_name()

DEFAULT_NUMBER_OF_GROUPS = 3
MIN_NUMBER_OF_GROUPS = 1
MAX_NUMBER_OF_GROUPS = 10

# Define the FresqueAeroMaps application graphs colors:
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

# Define the FresqueAeroMaps application HTML styles:
def get_style_string(styles: Dict[str, str]) -> str:
    """
    Converts a dictionary of styles to a string format for HTML.
    
    #### Arguments:
    - `styles (Dict[str, str])`: A dictionary where keys are CSS properties and values are their corresponding values.
    
    #### Returns:
    - `str`: A string representation of the styles.
    """
    return "; ".join(f"{key}: {value}" for key, value in styles.items()).replace("_", "-")

TITLE_STYLE = {
    "font_size": "24px",
    "font_weight": "bold",
    "text_decoration": "underline",
    "text_align": "center"
}

GROUP_SELECTOR_STYLE = {
    "description_width": "initial",
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

# Define the FresqueAeroMaps application layouts:
EXPLANATIONS_VBOX_LAYOUT = {
    "width": "100%"
}

GROUP_SELECTOR_LAYOUT = {
    "width": "98%", # I did not put 100% because the description and group number values are truncated by the scrollbar if it is displayed.
    "margin": "0 auto"
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
    "margin": "10px 0 0 0"
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
    "width": "100%",
    "display": "flex",
    "justify_content": "center"
}

BUTTON_LAYOUT = {
    "width": "100%",
    "height": "125px",
    "margin": "25px 0 0 0",
}

BUTTON_BOX_LAYOUT = {
    "width": "100%",
    "height": "150px",
    "align_items": "center",
    "justify_content": "center"
}

PROSPECTIVE_SCENARIO_BOX_LAYOUT = {
    "width": "100%",
    "display": "flex",
    "justify_content": "center",
    "align_items": "center",
    "overflow": "hidden"
}

PROSPECTIVE_SCENARIO_GRAPH_LAYOUT = {
    "width": "100%"
}

MULTIDISCIPLINARY_BOX_LAYOUT = {
    "width": "100%",
    "display": "flex",
    "flex_flow": "row nowrap",
    "justify_content": "space-around",
    "align_items": "flex-start"
}

MULTIDISCIPLINARY_LEGEND_HBOX_LAYOUT = {
    "width": "100%",
    "justify_content": "center",
    "margin": "-12px 0 0 0"
}

MULTIDISCIPLINARY_GRAPH_AND_LEGEND_VBOX_LAYOUT = {
    "width": "50%",
    "align_items": "center",
    "overflow": "hidden"
}

SECTION_VBOX_LAYOUT = {
    "width": "100%",
    "align_items": "center",
    "overflow": "hidden"
}
