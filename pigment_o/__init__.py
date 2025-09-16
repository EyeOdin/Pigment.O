# Pigment.O is a Krita plugin and it is a Color Picker and Color Mixer and Color Sampler.
# Copyright ( C ) 2020  Ricardo Jeremias.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# ( at your option ) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Imports
from krita import *
from PyQt5 import *
from .picker_docker import *
from .sampler_docker import *

# Information
__version__ = ' 2.0.0 '
__license__ = ' GPLv3+ LGPLv3+ '
__author__ = ' Ricardo Jeremias '
__email__ = ' jeremy6321478@gmail.com '
__url__ = ' https://github.com/EyeOdin '


# Register the docker so Krita can use it!
Application.addDockWidgetFactory( DockWidgetFactory( "pykrita_pigment_o_picker_docker", DockWidgetFactoryBase.DockRight, Picker_Docker ) )
Application.addDockWidgetFactory( DockWidgetFactory( "pykrita_pigment_o_sampler_docker", DockWidgetFactoryBase.DockRight, Sampler_Docker ) )
