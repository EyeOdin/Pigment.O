# Imports
from krita import *
from PyQt5 import *
from .pigment_o_docker import *

# Information
__version__ = ' 2.0.0 '
__license__ = ' GPLv3+ LGPLv3+ '
__author__ = ' Ricardo Jeremias '
__email__ = ' jeremy6321478@gmail.com '
__url__ = ' https://github.com/EyeOdin '

# Name the Python Script for the program
DOCKER_ID = "pykrita_pigment_o_docker"

# Register the docker so Krita can use it!
Application.addDockWidgetFactory( DockWidgetFactory( DOCKER_ID, DockWidgetFactoryBase.DockRight, PigmentO_Docker ) )
