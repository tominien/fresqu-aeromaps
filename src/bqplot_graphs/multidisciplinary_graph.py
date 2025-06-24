from .base_graph import BaseGraph




class MultidisciplinaryGraph(BaseGraph):
    """
    Graph class for multidisciplinary data visualization.

    Implements the `draw()` and `update()` methods.

    #### Arguments :
    - `figure_title (str)` : Title of the figure.
    """
    def __init__(self, figure_title: str) -> None:
        super().__init__()
        self.figure_title = figure_title
