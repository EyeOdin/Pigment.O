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
import copy


# Main
DOCKER_NAME = "Pigment.O"
DOCKER_PICKER = "Pigment.O Picker"
DOCKER_SAMPLER = "Pigment.O Sampler"

# Harmony
harmony_5 = "ANALOGOUS"
harmony_4 = "TETRADIC"
harmony_3 = "TRIADIC"
harmony_2 = "COMPLEMENTARY"
harmony_1 = "MONOCHROMATIC"

# Panel
panel_fill    = "Display : Fill"
panel_square  = "Selector : Square"
panel_hue     = "Selector : Hue"
panel_gamut   = "Selector : Gamut"
panel_hexagon = "Selector : Hexagon"
panel_luma    = "Selector : Luma"
panel_plane   = "Mixer : Plane"
panel_mask    = "Mixer : Mask"

# Timer Variable
check_timer = 100  # 1000 = 1 SECOND (Zero will Disable checks)
# Numbers
qt_max = 16777215
render_width = 500
render_height = 500
pin_range = 20

# Circle
circle_digital = [ 0, 60, 120, 180, 240, 300, 360 ]
circle_analog = [ 0, 122, 165, 218, 275, 330, 360 ]
circle_hexagon = [ 30, 90, 150, 210, 270, 330 ]
hue_a = 32
delta_a = 0.314

# Gamma
gamma_y = 2.2 # Y (Luma)
gamma_l = 2.4 # linear to standard RGB conversion

# RYB angle conversion stops
digital_step = [ 0, 35/360,  60/360, 120/360, 180/360, 240/360, 300/360, 1 ]
analog_step  = [ 0, 60/360, 122/360, 165/360, 218/360, 275/360, 330/360, 1 ]

# Kelvin
kelvin_min = 1000
kelvin_half = 6500
kelvin_max = 12000
kelvin_delta = kelvin_max - kelvin_min
# Kelvin Table
kelvin_illuminants = {
    # Temperature : Class, Discription
    1000 : ["", ""],
    2724 : ["LED-V1", "phosphor-converted violet"],
    2733 : ["LED-B1", "phosphor-converted blue"],
    2840 : ["LED-RGB1", "mixing of red, green, and blue LEDs"],
    2851 : ["LED-BH1", "mixing of phosphor-converted blue LED and red LED (blue-hybrid)"],
    2856 : ["A", "incandescent / tungsten"],
    2940 : ["F4", "warm white fluorescent"],
    2998 : ["LED-B2", "phosphor-converted blue"],
    3000 : ["F12", "Philips TL83, Ultralume 30"],
    3450 : ["F3", "white fluorescent"],
    4000 : ["F11", "Philips TL84, Ultralume 40"],
    4070 : ["LED-V2", "phosphor-converted violet"],
    4103 : ["LED-B3", "phosphor-converted blue"],
    4150 : ["F6 / F9", "light white fluorescent / cool white deluxe fluorescent"],
    4230 : ["F2", "cool white fluorescent"],
    4874 : ["B", "obsolete, direct sunlight at noon"],
    5000 : ["F8 / F10", "D50 simulator, Sylvania F40 Design 50 / Philips TL85, Ultralume 50"],
    5003 : ["D50","horizon light, ICC profile PCS"],
    5109 : ["LED-B4", "phosphor-converted blue"],
    5454 : ["E", "equal energy"],
    5503 : ["D55", "mid-morning / mid-afternoon daylight"],
    6350 : ["F5", "daylight fluorescent"],
    6430 : ["F1", "daylight fluorescent"],
    6500 : ["F7", "D65 simulator, daylight simulator"],
    6504 : ["D65", "noon daylight: television, sRGB color space"],
    6598 : ["LED-B5", "phosphor-converted blue"],
    6774 : ["C", "obsolete, average / North sky daylight"],
    7504 : ["D75", "North sky daylight"],
    9305 : ["D93", "high-efficiency blue phosphor monitors, BT.2035"],
    12000 : ["", ""],
    }
kelvin_xyz_1931 = {
    # Illuminant - Kelvin - CIE*1931 ( X - Y - Z )
    "A"   : [2856, 109.850, 100.000, 35.585,],
    "B"   : [4874, 99.0927, 100.000, 85.313,],
    "C"   : [6774, 98.074, 100.000, 118.232,],
    "D50" : [5003, 96.422, 100.000, 82.521,],
    "D55" : [5503, 95.682, 100.000, 92.149,],
    "D65" : [6504, 95.047, 100.000, 108.883,],
    "D75" : [7504, 94.972, 100.000, 122.638,],
    "E"   : [5454, 100.000, 100.000, 100.000,],
    "F1"  : [6430, 92.834, 100.000, 103.665,],
    "F2"  : [4230, 99.187, 100.000, 67.395,],
    "F3"  : [3450, 103.754, 100.000, 49.861,],
    "F4"  : [2940, 109.147, 100.000, 38.813,],
    "F5"  : [6350, 90.872, 100.000, 98.723,],
    "F6"  : [4150, 97.309, 100.000, 60.191,],
    "F7"  : [6500, 95.044, 100.000, 108.755,],
    "F8"  : [5000, 96.413, 100.000, 82.333,],
    "F9"  : [4150, 100.365, 100.000, 67.868,],
    "F10" : [5000, 96.174, 100.000, 81.712,],
    "F11" : [4000, 100.966, 100.000, 64.370,],
    "F12" : [3000, 108.046, 100.000, 39.228,],
    }
kelvin_xyz_1964 = {
    # Illuminant - Kelvin - CIE*1964 ( X - Y - Z )
    "A"   : [2856, 111.144, 100.000, 35.200],
    "B"   : [4874, 99.178, 100.000, 84.3493],
    "C"   : [6774, 97.285, 100.000, 116.145],
    "D50" : [5003, 96.720, 100.000, 81.427],
    "D55" : [5503, 95.799, 100.000, 90.926],
    "D65" : [6504, 94.811, 100.000, 107.304],
    "D75" : [7504, 94.416, 100.000, 120.641],
    "E"   : [5454, 100.000, 100.000, 100.000],
    "F1"  : [6430, 94.791, 100.000, 103.191],
    "F2"  : [4230, 103.280, 100.000, 69.026],
    "F3"  : [3450, 108.968, 100.000, 51.965],
    "F4"  : [2940, 114.961, 100.000, 40.963],
    "F5"  : [6350, 93.369, 100.000, 98.636],
    "F6"  : [4150, 102.148, 100.000, 62.074],
    "F7"  : [6500, 95.792, 100.000, 107.687],
    "F8"  : [5000, 97.115, 100.000, 81.135],
    "F9"  : [4150, 102.116, 100.000, 67.826],
    "F10" : [5000, 99.001, 100.000, 83.134],
    "F11" : [4000, 103.866, 100.000, 65.627],
    "F12" : [3000, 111.428, 100.000, 40.353],
    }

# Channels
color_view = {
    # RGB based
    "gray" : False,
    "srgb" : False,
    "lrgb" : False,
    "cmyk" : False,
    "ryb"  : False,
    "yuv"  : False,
    # HUE-RGB Based
    "hsv"  : True,
    "hsl"  : False,
    "hcy"  : False,
    "ard"  : False,
    # XYZ Based
    "xyz"  : False,
    "xyy"  : False,
    "lab"  : False,
    # HUE-XYZ Based
    "lch"  : False,
    # Mixer
    "kelvin" : False,
    "pole" : False,
    "linear" : True,
    # Display
    "hex6" : False,
    "sum4" : False,
    }
color_range = {
    # RGB based
    "gray_1": 255,
    "srgb_1": 255, "srgb_2": 255, "srgb_3": 255,
    "lrgb_1": 255, "lrgb_2": 255, "lrgb_3": 255,
    "cmyk_1": 255, "cmyk_2": 255, "cmyk_3": 255, "cmyk_4": 255,
    "ryb_1" : 255, "ryb_2" : 255, "ryb_3" : 255,
    "yuv_1" : 255, "yuv_2" : 255, "yuv_3" : 255,
    # HUE-RGB Based
    "hsv_1" : 360, "hsv_2" : 255, "hsv_3" : 255,
    "hsl_1" : 360, "hsl_2" : 255, "hsl_3" : 255,
    "hcy_1" : 360, "hcy_2" : 255, "hcy_3" : 255,
    "ard_1" : 360, "ard_2" : 255, "ard_3" : 360,
    # XYZ Based
    "xyz_1" : 255, "xyz_2" : 255, "xyz_3" : 255,
    "xyy_1" : 255, "xyy_2" : 255, "xyy_3" : 255,
    "lab_1" : 255, "lab_2" : 255, "lab_3" : 255, # 256 ?
    # HUE-XYZ Based
    "lch_1" : 255, "lch_2" : 255, "lch_3" : 255,
    # Non Color
    "uvd_1" : 360, "uvd_2" : 255, "uvd_3" : 360,
    }
color_mark = {
    # RGB based
    "gray_1": 4,
    "srgb_1": 4, "srgb_2": 4, "srgb_3": 4,
    "lrgb_1": 4, "lrgb_2": 4, "lrgb_3": 4,
    "cmyk_1": 4, "cmyk_2": 4, "cmyk_3": 4, "cmyk_4": 4,
    "ryb_1" : 4, "ryb_2" : 4, "ryb_3" : 4,
    "yuv_1" : 4, "yuv_2" : 4, "yuv_3" : 4,
    # HUE-RGB Based
    "hsv_1" : 6, "hsv_2" : 4, "hsv_3" : 4,
    "hsl_1" : 6, "hsl_2" : 4, "hsl_3" : 4,
    "hcy_1" : 6, "hcy_2" : 4, "hcy_3" : 4,
    "ard_1" : 6, "ard_2" : 4, "ard_3" : 6,
    # XYZ Based
    "xyz_1" : 4, "xyz_2" : 4, "xyz_3" : 4,
    "xyy_1" : 4, "xyy_2" : 4, "xyy_3" : 4,
    "lab_1" : 4, "lab_2" : 4, "lab_3" : 4,
    # HUE-XYZ Based
    "lch_1" : 4, "lch_2" : 4, "lch_3" : 6,
    # Mixer
    "kelvin" : 4,
    "pole" : 4,
    "linear" : 4,
    }
# Color Object
color_neutral = {
    # Details
    "active" : None,
    # Description
    "display" : "#000000",
    "hex6" : "#000000",
    "sum4" : 0,
    "name" : "Black",
    # RGB linear
    "gray_1": 0.00,
    "srgb_1": 0.00, "srgb_2": 0.00, "srgb_3": 0.00,
    "lrgb_1": 0.00, "lrgb_2": 0.00, "lrgb_3": 0.00,
    "cmyk_1": 0.00, "cmyk_2": 0.00, "cmyk_3": 0.00, "cmyk_4": 1.00,
    "ryb_1" : 0.00, "ryb_2" : 0.00, "ryb_3" : 0.00,
    "yuv_1" : 0.00, "yuv_2" : 0.50, "yuv_3" : 0.50,
    # RGB Hue
    "hue_d" : 0.00, "hue_a" : 0.00,
    "hsv_1" : 0.00, "hsv_2" : 0.00, "hsv_3" : 0.00,
    "hsl_1" : 0.00, "hsl_2" : 0.00, "hsl_3" : 0.00,
    "hcy_1" : 0.00, "hcy_2" : 0.00, "hcy_3" : 0.00,
    "ard_1" : 0.00, "ard_2" : 0.00, "ard_3" : 0.00,
    # XYZ Linear
    "xyz_1" : 0.00, "xyz_2" : 0.00, "xyz_3" : 0.00,
    "xyy_1" : 0.31, "xyy_2" : 0.33, "xyy_3" : 0.00,
    "lab_1" : 0.00, "lab_2" : 0.50, "lab_3" : 0.50,
    "luv_1" : 0.00, "luv_2" : 0.00, "luv_3" : 0.00,
    # XYZ Hue
    "lch_1" : 0.00, "lch_2" : 0.00, "lch_3" : 0.00,
    # Other
    "uvd_1" : 0.00, "uvd_2" : 0.00, "uvd_3" : 0.00,
    }
# Colors
color_true = copy.deepcopy( color_neutral )
color_false = copy.deepcopy( color_neutral )
color_true["active"]  = True
color_false["active"] = False
# Foreground and Background
kfc = copy.deepcopy( color_true )
kbc = copy.deepcopy( color_true )
mix = copy.deepcopy( color_true )
# Harmony Colors
har_01 = copy.deepcopy( color_true )
har_02 = copy.deepcopy( color_true )
har_03 = copy.deepcopy( color_true )
har_04 = copy.deepcopy( color_true )
har_05 = copy.deepcopy( color_true )
