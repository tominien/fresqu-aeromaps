from typing import Any, Dict

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
    def draw(self, data: Dict[str, Any]) -> Figure:
        """
        Create and configure the figure based on provided data.

        #### Arguments :
        - `data (Dict[str, Any])` : Raw simulation output data.

        #### Returns :
        - `Figure` : The created figure object.
        """
        ... # Implemented in the subclass.


    @abstractmethod
    def update(self, data: Dict[str, Any]) -> Figure:
        """
        Update the existing figure with new dataset.

        #### Arguments :
        - `data (Dict[str, Any])` : New data to update the figure.

        #### Returns :
        - `Figure` : The updated figure object.
        """
        ... # Implemented in the subclass.
