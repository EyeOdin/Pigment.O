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


# Timer Variable
check_timer = 100  # 1000 = 1 SECOND (Zero will Disable checks)

# Numbers
zero = 0
half = 0.5
unit = 1
two = 2
hue_a = 32
cube = 255
render_width = 5000
render_height = 5000
max_val = 16777215
# Luma Coefficients (ITU-R BT.601)
luma_r = 0.299
luma_b = 0.114
luma_g = 1 - luma_r - luma_b # 0.587
luma_pr = 1.402
luma_pb = 1.772
gamma_y = 2.2 # Y (Luma)
gamma_l = 2.4 # linear to standard RGB conversion
# Kelvin
kkk_min_scale = 1000
kkk_half_scale = 6500
kkk_max_scale = 12000
kkk_delta = kkk_max_scale - kkk_min_scale
kkk_half_percent = (kkk_half_scale - kkk_min_scale) / kkk_delta
# Panel
panel = "PANEL"

# Range
krange = {
    # RGB based
    "aaa_1" : 255,
    "rgb_1" : 255, "rgb_2" : 255, "rgb_3" : 255,
    "uvd_1" : 255, "uvd_2" : 255, "uvd_3" : 360,
    "cmy_1" : 255, "cmy_2" : 255, "cmy_3" : 255,
    "cmyk_1": 255, "cmyk_2": 255, "cmyk_3": 255, "cmyk_4": 255,
    "ryb_1" : 255, "ryb_2" : 255, "ryb_3" : 255,
    "yuv_1" : 255, "yuv_2" : 255, "yuv_3" : 255,
    # HUE-RGB Based
    "hsv_1" : 360, "hsv_2" : 255, "hsv_3" : 255,
    "hsl_1" : 360, "hsl_2" : 255, "hsl_3" : 255,
    "hcy_1" : 360, "hcy_2" : 255, "hcy_3" : 255,
    "ard_1" : 360, "ard_2" : 255, "ard_3" : 255,
    # XYZ Based
    "xyz_1" : 255, "xyz_2" : 255, "xyz_3" : 255,
    "xyy_1" : 255, "xyy_2" : 255, "xyy_3" : 255,
    "lab_1" : 256, "lab_2" : 256, "lab_3" : 256,
    # HUE-XYZ Based
    "lch_1" : 255, "lch_2" : 255, "lch_3" : 255,
    }
stops = {
    # RGB based
    "aaa_1" : 4,
    "rgb_1" : 4, "rgb_2" : 4, "rgb_3" : 4,
    "uvd_1" : 4, "uvd_2" : 4, "uvd_3" : 4,
    "cmy_1" : 4, "cmy_2" : 4, "cmy_3" : 4,
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
    # Non Color
    "kkk_1" : 4,
    # Mixers
    "mixer" : 2
    }

# Active Colors
color_neutral = {
    # Details
    "active" : None,
    "hex6" : "#000000",
    # RGB based
    "aaa_1" : 0,
    "rgb_1" : 0, "rgb_2" : 0, "rgb_3" : 0,
    "uvd_1" : 0, "uvd_2" : 0, "uvd_3" : 0,
    "cmy_1" : 0, "cmy_2" : 0, "cmy_3" : 0,
    "cmyk_1": 0, "cmyk_2": 0, "cmyk_3": 0, "cmyk_4": 0,
    "ryb_1" : 0, "ryb_2" : 0, "ryb_3" : 0,
    "yuv_1" : 0, "yuv_2" : 0, "yuv_3" : 0,
    # HUE-RGB Based
    "hue_d" : 0, "hue_a" : 0,
    "hsv_1" : 0, "hsv_2" : 0, "hsv_3" : 0,
    "hsl_1" : 0, "hsl_2" : 0, "hsl_3" : 0,
    "hcy_1" : 0, "hcy_2" : 0, "hcy_3" : 0,
    "ard_1" : 0, "ard_2" : 0, "ard_3" : 0,
    # XYZ Based
    "xyz_1" : 0, "xyz_2" : 0, "xyz_3" : 0,
    "xyy_1" : 0, "xyy_2" : 0, "xyy_3" : 0,
    "lab_1" : 0, "lab_2" : 0, "lab_3" : 0,
    # HUE-XYZ Based
    "lch_1" : 0, "lch_2" : 0, "lch_3" : 0,
    # HTML Name
    "name" : "Black",
    # Kelvin
    "kkk_percent" : kkk_half_percent, # 0.5 %
    "kkk_scale" : kkk_half_scale, # 6500 k
    # Display
    "hex6_d" : "#000000",
    "aaa_d1" : 0,
    "rgb_d1" : 0, "rgb_d2" : 0, "rgb_d3" : 0,
    "cmyk_d1": 0, "cmyk_d2": 0, "cmyk_d3": 0, "cmyk_d4": 0,
    "yuv_d1" : 0, "yuv_d2" : 0, "yuv_d3" : 0,
    "xyz_d1" : 0, "xyz_d2" : 0, "xyz_d3" : 0,
    "lab_d1" : 0, "lab_d2" : 0, "lab_d3" : 0,
    }
color_true = color_neutral.copy()
color_false = color_neutral.copy()
color_true["active"] = True
color_false["active"] = False

# Foreground and Background
kac = color_true.copy()
kbc = color_true.copy()
# Harmony Colors
har_01 = color_true.copy()
har_02 = color_true.copy()
har_03 = color_true.copy()
har_04 = color_true.copy()
har_05 = color_true.copy()

# RYB angle conversion stops
digital_step = [ 0, 35/360,  60/360, 120/360, 180/360, 240/360, 300/360, 1 ]
analog_step  = [ 0, 60/360, 122/360, 165/360, 218/360, 275/360, 330/360, 1 ]

# Kelvin Table
kelvin_rgb = {
    1000 : [255 / cube,  56 / cube,   0 / cube],
    1100 : [255 / cube,  71 / cube,   0 / cube],
    1200 : [255 / cube,  83 / cube,   0 / cube],
    1300 : [255 / cube,  93 / cube,   0 / cube],
    1400 : [255 / cube, 101 / cube,   0 / cube],
    1500 : [255 / cube, 109 / cube,   0 / cube],
    1600 : [255 / cube, 115 / cube,   0 / cube],
    1700 : [255 / cube, 121 / cube,   0 / cube],
    1800 : [255 / cube, 126 / cube,   0 / cube],
    1900 : [255 / cube, 131 / cube,   0 / cube],
    2000 : [255 / cube, 138 / cube,  18 / cube],
    2100 : [255 / cube, 142 / cube,  33 / cube],
    2200 : [255 / cube, 147 / cube,  44 / cube],
    2300 : [255 / cube, 152 / cube,  54 / cube],
    2400 : [255 / cube, 157 / cube,  63 / cube],
    2500 : [255 / cube, 161 / cube,  72 / cube],
    2600 : [255 / cube, 165 / cube,  79 / cube],
    2700 : [255 / cube, 169 / cube,  87 / cube],
    2800 : [255 / cube, 173 / cube,  94 / cube],
    2900 : [255 / cube, 177 / cube, 101 / cube],
    3000 : [255 / cube, 180 / cube, 107 / cube],
    3100 : [255 / cube, 184 / cube, 114 / cube],
    3200 : [255 / cube, 187 / cube, 120 / cube],
    3300 : [255 / cube, 190 / cube, 126 / cube],
    3400 : [255 / cube, 193 / cube, 132 / cube],
    3500 : [255 / cube, 196 / cube, 137 / cube],
    3600 : [255 / cube, 199 / cube, 143 / cube],
    3700 : [255 / cube, 201 / cube, 148 / cube],
    3800 : [255 / cube, 204 / cube, 153 / cube],
    3900 : [255 / cube, 206 / cube, 159 / cube],
    4000 : [255 / cube, 209 / cube, 163 / cube],
    4100 : [255 / cube, 211 / cube, 168 / cube],
    4200 : [255 / cube, 213 / cube, 173 / cube],
    4300 : [255 / cube, 215 / cube, 177 / cube],
    4400 : [255 / cube, 217 / cube, 182 / cube],
    4500 : [255 / cube, 219 / cube, 186 / cube],
    4600 : [255 / cube, 221 / cube, 190 / cube],
    4700 : [255 / cube, 223 / cube, 194 / cube],
    4800 : [255 / cube, 225 / cube, 198 / cube],
    4900 : [255 / cube, 227 / cube, 202 / cube],
    5000 : [255 / cube, 228 / cube, 206 / cube],
    5100 : [255 / cube, 230 / cube, 210 / cube],
    5200 : [255 / cube, 232 / cube, 213 / cube],
    5300 : [255 / cube, 233 / cube, 217 / cube],
    5400 : [255 / cube, 235 / cube, 220 / cube],
    5500 : [255 / cube, 236 / cube, 224 / cube],
    5600 : [255 / cube, 238 / cube, 227 / cube],
    5700 : [255 / cube, 239 / cube, 230 / cube],
    5800 : [255 / cube, 240 / cube, 233 / cube],
    5900 : [255 / cube, 242 / cube, 236 / cube],
    6000 : [255 / cube, 243 / cube, 239 / cube],
    6100 : [255 / cube, 244 / cube, 242 / cube],
    6200 : [255 / cube, 245 / cube, 245 / cube],
    6300 : [255 / cube, 246 / cube, 247 / cube],
    6400 : [255 / cube, 248 / cube, 251 / cube],
    6500 : [255 / cube, 255 / cube, 255 / cube], # 6500 : [255 / cube, 249 / cube, 253 / cube],
    6600 : [254 / cube, 249 / cube, 255 / cube],
    6700 : [252 / cube, 247 / cube, 255 / cube],
    6800 : [249 / cube, 246 / cube, 255 / cube],
    6900 : [247 / cube, 245 / cube, 255 / cube],
    7000 : [245 / cube, 243 / cube, 255 / cube],
    7100 : [243 / cube, 242 / cube, 255 / cube],
    7200 : [240 / cube, 241 / cube, 255 / cube],
    7300 : [239 / cube, 240 / cube, 255 / cube],
    7400 : [237 / cube, 239 / cube, 255 / cube],
    7500 : [235 / cube, 238 / cube, 255 / cube],
    7600 : [233 / cube, 237 / cube, 255 / cube],
    7700 : [231 / cube, 236 / cube, 255 / cube],
    7800 : [230 / cube, 235 / cube, 255 / cube],
    7900 : [228 / cube, 234 / cube, 255 / cube],
    8000 : [227 / cube, 233 / cube, 255 / cube],
    8100 : [225 / cube, 232 / cube, 255 / cube],
    8200 : [224 / cube, 231 / cube, 255 / cube],
    8300 : [222 / cube, 230 / cube, 255 / cube],
    8400 : [221 / cube, 230 / cube, 255 / cube],
    8500 : [220 / cube, 229 / cube, 255 / cube],
    8600 : [218 / cube, 229 / cube, 255 / cube],
    8700 : [217 / cube, 227 / cube, 255 / cube],
    8800 : [216 / cube, 227 / cube, 255 / cube],
    8900 : [215 / cube, 226 / cube, 255 / cube],
    9000 : [214 / cube, 225 / cube, 255 / cube],
    9100 : [212 / cube, 225 / cube, 255 / cube],
    9200 : [211 / cube, 224 / cube, 255 / cube],
    9300 : [210 / cube, 223 / cube, 255 / cube],
    9400 : [209 / cube, 223 / cube, 255 / cube],
    9500 : [208 / cube, 222 / cube, 255 / cube],
    9600 : [207 / cube, 221 / cube, 255 / cube],
    9700 : [207 / cube, 221 / cube, 255 / cube],
    9800 : [207 / cube, 220 / cube, 255 / cube],
    9900 : [206 / cube, 220 / cube, 255 / cube],
    10000 : [206 / cube, 218 / cube, 255 / cube],
    10100 : [206 / cube, 218 / cube, 255 / cube],
    10200 : [205 / cube, 217 / cube, 255 / cube],
    10300 : [205 / cube, 217 / cube, 255 / cube],
    10400 : [204 / cube, 216 / cube, 255 / cube],
    10500 : [204 / cube, 216 / cube, 255 / cube],
    10600 : [203 / cube, 215 / cube, 255 / cube],
    10700 : [202 / cube, 215 / cube, 255 / cube],
    10800 : [202 / cube, 214 / cube, 255 / cube],
    10900 : [201 / cube, 214 / cube, 255 / cube],
    11000 : [200 / cube, 213 / cube, 255 / cube],
    11100 : [200 / cube, 213 / cube, 255 / cube],
    11200 : [199 / cube, 212 / cube, 255 / cube],
    11300 : [198 / cube, 212 / cube, 255 / cube],
    11400 : [198 / cube, 212 / cube, 255 / cube],
    11500 : [197 / cube, 211 / cube, 255 / cube],
    11600 : [197 / cube, 211 / cube, 255 / cube],
    11700 : [197 / cube, 210 / cube, 255 / cube],
    11800 : [196 / cube, 210 / cube, 255 / cube],
    11900 : [195 / cube, 210 / cube, 255 / cube],
    12000 : [195 / cube, 209 / cube, 255 / cube],
    }
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
    "A" : [2856, 109.850, 100.000, 35.585,],
    "B" : [4874, 99.0927, 100.000, 85.313,],
    "C" : [6774, 98.074, 100.000, 118.232,],
    "D50" : [5003, 96.422, 100.000, 82.521,],
    "D55" : [5503, 95.682, 100.000, 92.149,],
    "D65" : [6504, 95.047, 100.000, 108.883,],
    "D75" : [7504, 94.972, 100.000, 122.638,],
    "E" : [5454, 100.000, 100.000, 100.000,],
    "F1" : [6430, 92.834, 100.000, 103.665,],
    "F2" : [4230, 99.187, 100.000, 67.395,],
    "F3" : [3450, 103.754, 100.000, 49.861,],
    "F4" : [2940, 109.147, 100.000, 38.813,],
    "F5" : [6350, 90.872, 100.000, 98.723,],
    "F6" : [4150, 97.309, 100.000, 60.191,],
    "F7" : [6500, 95.044, 100.000, 108.755,],
    "F8" : [5000, 96.413, 100.000, 82.333,],
    "F9" : [4150, 100.365, 100.000, 67.868,],
    "F10" : [5000, 96.174, 100.000, 81.712,],
    "F11" : [4000, 100.966, 100.000, 64.370,],
    "F12" : [3000, 108.046, 100.000, 39.228,],
    }
kelvin_xyz_1964 = {
    # Illuminant - CIE*1964 ( X - Y - Z )
    "A" : [2856, 111.144, 100.000, 35.200],
    "B" : [4874, 99.178, 100.000, 84.3493],
    "C" : [6774, 97.285, 100.000, 116.145],
    "D50" : [5003, 96.720, 100.000, 81.427],
    "D55" : [5503, 95.799, 100.000, 90.926],
    "D65" : [6504, 94.811, 100.000, 107.304],
    "D75" : [7504, 94.416, 100.000, 120.641],
    "E" : [5454, 100.000, 100.000, 100.000],
    "F1" : [6430, 94.791, 100.000, 103.191],
    "F2" : [4230, 103.280, 100.000, 69.026],
    "F3" : [3450, 108.968, 100.000, 51.965],
    "F4" : [2940, 114.961, 100.000, 40.963],
    "F5" : [6350, 93.369, 100.000, 98.636],
    "F6" : [4150, 102.148, 100.000, 62.074],
    "F7" : [6500, 95.792, 100.000, 107.687],
    "F8" : [5000, 97.115, 100.000, 81.135],
    "F9" : [4150, 102.116, 100.000, 67.826],
    "F10" : [5000, 99.001, 100.000, 83.134],
    "F11" : [4000, 103.866, 100.000, 65.627],
    "F12" : [3000, 111.428, 100.000, 40.353],
    }
kelvin = { "class" : kelvin_illuminants[6500][0], "description" : kelvin_illuminants[6500][1] }

# Fill
fill = { "active" : False, "node_uid" : None, "alphalock_before" : False }

# Selection
selection = {
    # State
    "active" : False,
    "mode" : "LINEAR",
    # Markers
    "l0" : 0.2,
    "l1" : 0.1,
    "r1" : 0.1,
    "r0" : 0.2,
    }
sele_1_var = selection.copy()
sele_2_var = selection.copy()
sele_3_var = selection.copy()
sele_4_var = selection.copy()