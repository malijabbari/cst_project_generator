import settings
import util.constants as constants
import sys

App, Gui, Import, Part, Draft = None, None, None, None, None

try:
    import FreeCAD as App
except ImportError:
    sys.path.append(settings.path_freecad)

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
