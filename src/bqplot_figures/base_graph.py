from typing import List, Dict, Tuple, Any

from abc import ABC, abstractmethod

from bqplot import Figure




class BaseGraph(ABC):
    """
    Abstract interface for any type of graph component.

    Subclasses must implement:
    - `draw(data)` : To create the initial figure.
    - `update(data)` : To update the figure with new data.

    #### Attributes :
    - `figure (Figure)` : The figure instance.
    """
    def __init__(self) -> None:
        self.figure: Figure = None


    @property
    def get_figure(self) -> Figure:
        """
        Returns the current figure instance.

        #### Returns :
        - `Figure` : The current figure object.
        """
        return self.figure


    @abstractmethod
    def draw(
            self,
            process_data: Dict[str, Any],
            override: bool = False
        ) -> Figure:
        """
        Create **initial** figure.

        If the figure is already drawn and you just want to update the data, it is recommended to use the `update()` method instead.
        This method will not redraw the figure but will update the lines' data only.

        However, if you want to redraw the figure completely, you can set `override = True` to force a redraw.
        This action takes more time and resources to execute.

        #### Arguments :
        - `process_data (Dict[str, Any])` : Data dictionary containing the necessary data for plotting the initial graph.
        - `override (bool)` : If `True`, forces a redraw of the figure, even if it has already been drawn. Defaults to `False`.

        #### Returns :
        - `Figure` : The initial figure with historical, prospective, and aspects areas plotted.
        """
        # Check is the figure is already drawn and if override is set to False :
        if self.figure is not None and not override :
            return self.update(process_data)

        ... # Implemented in the subclass.


    @abstractmethod
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

        ... # Implemented in the subclass.

    @abstractmethod
    def get_legend_elements(self) -> Tuple[List[str], List[str]]:
        """
        Get the legend elements of the figure.
        Allows to retrieve the colors and labels of the graph's legend to create a custom legend.

        #### Returns :
        - `Tuple[List[str], List[str]]` : A tuple containing two lists:
            - The first list contains the colors of the legend elements.
            - The second list contains the labels of the legend elements.
        """
        # Check if the figure is already drawn :
        if not self.figure:
            raise ValueError("The figure is not drawn yet. Please call the `draw()` method first.")

        ... # Implemented in the subclass.
