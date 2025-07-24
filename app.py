import panel
from panel.template import BootstrapTemplate

# Load the Python Path from the .env file :
import os
import sys
from dotenv import load_dotenv

load_dotenv()

ROOT_DIRECTORY = os.path.dirname(__file__)
SRC_DIRECTORY  = os.getenv("PYTHONPATH", os.path.join(ROOT_DIRECTORY, "src"))
if SRC_DIRECTORY not in sys.path:
    sys.path.append(SRC_DIRECTORY)

# Set up the Panel application with the necessary imports and configurations :
panel.extension(
    "ipywidgets", # Load the Panel and IPyWidgets extensions.
    raw_css = [
        """
        #header {
            display: none !important;
            height: 0 !important;
            padding: 0 !important;
            visibility: hidden !important;
        }
        """
    ]
)

from ui.fresque_aeromaps_UI import FresqueAeroMapsUI

from utils import APPLICATION_ICON_PATH




def create_application_view() -> BootstrapTemplate:
    """
    Creates the Panel application view for the Fresqu'AéroMaps interface.

    #### Returns :
    - `BootstrapTemplate`: A Panel Bootstrap template containing the application view.
    """
    # Draw the interface :
    application = FresqueAeroMapsUI()
    interface = application.display_interface()

    # Create the Panel application view :
    app_view = panel.panel(interface, sizing_mode = "stretch_both")

    template = BootstrapTemplate(
        main = app_view,
        title = "Fresqu'AéroMaps",
        favicon = APPLICATION_ICON_PATH
    )

    return template.servable()


# Launch the Panel server with the application view :
create_application_view()
