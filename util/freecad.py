import settings
import util.constants as constants
import sys

App, Gui, Import, Part, Draft = None, None, None, None, None

try:
    import FreeCAD as App
except ImportError:
    if settings.is_running_on_desktop:
        sys.path.append(settings.path_freecad_desktop)
    else:
        sys.path.append(settings.path_freecad_server)

import FreeCAD as App
import FreeCADGui as Gui
import Import
import Part
import Draft

# setup with GUI or not, NOTE: I couldn't get the GUI working properly
if not constants.setup_with_gui:
    Gui.setupWithoutGUI()
else:
    Gui.showMainWindow()
