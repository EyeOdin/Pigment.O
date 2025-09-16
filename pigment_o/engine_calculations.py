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


#region Imports

import math
import sys
from PyQt5 import QtCore
from .engine_constants import *

#endregion


class Geometry():

    #region Init

    def __init__( self ):
        pass

    #endregion
    #region Limiters

    def Limit_Unit( self, value ):
        if value <= 1:
            value = 1
        return value
    def Limit_Float( self, value ):
        if value <= 0:
            value = 0
        if value >= 1:
            value = 1
        return value
    def Limit_Range( self, value, minimum, maximum ):
        if value <= minimum:
            value = minimum
        if value >= maximum:
            value = maximum
        return value
    def Limit_Loop( self, value, limit ):
        if value < 0:
            value = limit
        if value > limit:
            value = 0
        return value
    def Limit_Looper( self, value, limit ):
        while value < 0:
            value += limit
        while value > limit:
            value -= limit
        return value
    def Limit_Error( self, value, error ):
        if ( value > -error and value < error ):
            value = 0
        return value
    def Limit_Angle( self, angle, inter ):
        angle = angle // inter
        even = angle % 2
        if even == 0: # Even
            angle = angle * inter
        else: # Odd
            angle = ( angle + 1 ) * inter
        return angle

    #endregion
    #region LERP

    def Lerp_1D( self, percent, bot, top ):
        lerp = bot + ( ( top - bot ) * percent )
        return lerp
    def Lerp_2D( self, percent, x1, y1, x2, y2 ):
        dx = x2 - x1
        dy = y2 - y1
        lx = x1 + ( dx * percent )
        ly = y1 + ( dy * percent )
        return lx, ly
    def Lerp_3D( self, percent, x1, y1, z1, x2, y2, z2 ):
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        lx = x1 + ( dx * percent )
        ly = y1 + ( dy * percent )
        lz = z1 + ( dz * percent )
        return lx, ly, lz
    def Lerp_List( self, percent, bot, top ):
        lista = []
        for i in range( 0, len( bot ) ):
            lerp = bot[i] + ( ( top[i] - bot[i] ) * percent )
            lista.append( lerp )
        return lista

    #endregion
    #region Range

    def Random_Range( self, range ):
        time = int( QtCore.QTime.currentTime().toString( 'hhmmssms' ) )
        random.seed( time )
        random_value = random.randint( 0, range )
        return random_value

    #endregion
    #region Statistics

    def Stat_Mean( self, lista ):
        length = len( lista )
        add = 0
        for i in range( 0, length ):
            add = add + lista[i]
        mean = add / ( length )
        return mean

    #endregion
    #region Trignometry

    def Trig_2D_Angle_Circle( self, px, py, side, radius, angle ):
        # px - Circle center in X (pixels)
        # py - Circle center in Y (pixels)
        # side - length of the square containning the circle (pixels)
        # radius - how far from the center (0-1)
        # angle - angle delta (0-360)
        circle_x = ( px ) - ( ( side * radius ) * math.cos( math.radians( angle ) ) )
        circle_y = ( py ) - ( ( side * radius ) * math.sin( math.radians( angle ) ) )
        return circle_x, circle_y
    def Trig_2D_Points_Distance( self, x1, y1, x2, y2 ):
        dd = math.sqrt( math.pow( ( x1 - x2 ), 2 ) + math.pow( ( y1 - y2 ), 2 )  )
        return dd
    def Trig_2D_Points_Lines_Angle( self, x1, y1, x2, y2, x3, y3 ):
        v1 = ( x1 - x2, y1 - y2 )
        v2 = ( x3 - x2, y3 - y2 )
        v1_theta = math.atan2( v1[1], v1[0] )
        v2_theta = math.atan2( v2[1], v2[0] )
        angle = ( v2_theta - v1_theta ) * ( 180.0 / math.pi )
        if angle < 0:
            angle += 360.0
        return angle
    def Trig_2D_Points_Lines_Intersection( self, x1, y1, x2, y2, x3, y3, x4, y4 ):
        try:
            xx = ( ( x2 * y1 - x1 * y2 ) * ( x4 - x3 ) - ( x4 * y3 - x3 * y4 ) * ( x2 - x1 ) ) / ( ( x2 - x1 ) * ( y4 - y3 ) - ( x4 - x3 ) * ( y2 - y1 ) )
            yy = ( ( x2 * y1 - x1 * y2 ) * ( y4 - y3 ) - ( x4 * y3 - x3 * y4 ) * ( y2 - y1 ) ) / ( ( x2 - x1 ) * ( y4 - y3 ) - ( x4 - x3 ) * ( y2 - y1 ) )
        except:
            xx = 0
            yy = 0
        return xx, yy
    def Trig_2D_Points_Rotate( self, origin_x, origin_y, dist, angle ):
        cx = origin_x - ( dist * math.cos( math.radians( angle ) ) )
        cy = origin_y - ( dist * math.sin( math.radians( angle ) ) )
        return cx, cy
    def Trig_2D_Triangle_Extrapolation( self, x1, y1, x2, y2, percent_12, percent_23 ):
        hor = x2 - x1
        ver = y2 - y1
        p23_hor = ( percent_23 * hor ) / percent_12
        p23_ver = ( percent_23 * ver ) / percent_12
        x3 = x2 + p23_hor
        y3 = y2 + p23_ver
        return x3, y3
    def Trig_2D_Centroid_Triangle( self, a1, a2, b1, b2, c1, c2 ):
        cx = ( a1 + b1 + c1 ) / 3
        cy = ( a2 + b2 + c2 ) / 3
        return [ cx, cy ]
    def Trig_2D_Centroid_Square( self, a1, a2, b1, b2, c1, c2, d1, d2 ):
        cx = ( a1 + b1 + c1 + d1 ) / 4
        cy = ( a2 + b2 + c2 + d2 ) / 4
        return [ cx, cy ]
    def Trig_2D_Ortogonal_Components(self, x1, y1, x2, y2):
        # x1,y1 is the origin
        delta_x = x2 - x1
        delta_y = y2 - y1
        return [delta_x, delta_y]
    def Trig_3D_Points_Distance( self, x1, y1, z1, x2, y2, z2 ):
        d = math.sqrt( ( x2 - x1 ) ** 2 + ( y2 - y1 ) ** 2 + ( z2 - z1 ) ** 2 )
        return d

    #endregion


class Convert():
    # range 0-1

    #region Init

    def __init__( self ):
        # Modules
        self.geometry = Geometry()
        # Variables
        self.hue = 0
        self.luminosity = "ITU-R BT.709"

    #endregion
    #region Set

    def Set_Document( self, d_cm, d_cd, d_cp ):
        self.d_cm = d_cm
        self.d_cd = d_cd
        self.d_cp = d_cp
    def Set_Hue( self, hue ):
        self.hue = hue
    def Set_Luminosity( self, luminosity ):
        self.luminosity == luminosity
        if self.luminosity == "ITU-R BT.601":
            self.luma_r = 0.299
            self.luma_b = 0.114
            self.luma_g = 1 - self.luma_r - self.luma_b # 0.587
            self.luma_pr = 1.402
            self.luma_pb = 1.772
        if self.luminosity == "ITU-R BT.709":
            self.luma_r = 0.2126
            self.luma_b = 0.0722
            self.luma_g = 1 - self.luma_r - self.luma_b # 0.7152
            self.luma_pr = 1.5748
            self.luma_pb = 1.8556
        if self.luminosity == "ITU-R BT.2020":
            self.luma_r = 0.2627
            self.luma_b = 0.0593
            self.luma_g = 1 - self.luma_r - self.luma_b # 0.678
            self.luma_pr = 0.4969
            self.luma_pb = 0.7910
    def Set_Gamma( self, gamma_y, gamma_l ):
        self.gamma_y = gamma_y
        self.gamma_l = gamma_l
    def Set_Matrix( self, matrix, iluma ):
        # Origin from http://www.brucelindbloom.com/
        # Standard
        if matrix == "sRGB":
            if iluma == "D50": # i=0
                self.m_rgb_xyz = [ [ 0.4360747,  0.3850649,  0.1430804 ], [ 0.2225045,  0.7168786,  0.0606169 ], [ 0.0139322,  0.0971045,  0.7141733 ] ]
                self.m_xyz_rgb = [ [ 3.1338561, -1.6168667, -0.4906146 ], [-0.9787684,  1.9161415,  0.0334540 ], [ 0.0719453, -0.2289914,  1.4052427 ] ]
            if iluma == "D65": # i=1
                self.m_rgb_xyz = [ [ 0.4124564,  0.3575761,  0.1804375 ], [ 0.2126729,  0.7151522,  0.0721750 ], [ 0.0193339,  0.1191920,  0.9503041 ] ]
                self.m_xyz_rgb = [ [ 3.2404542, -1.5371385, -0.4985314 ], [-0.9692660,  1.8760108,  0.0415560 ], [ 0.0556434, -0.2040259,  1.0572252 ] ]
            else:
                iluma = "D65"
        # Professional
        if matrix == "Adobe RGB":
            if iluma == "D50": # i=2
                self.m_rgb_xyz = [ [ 0.6097559,  0.2052401,  0.1492240 ], [ 0.3111242,  0.6256560,  0.0632197 ], [ 0.0194811,  0.0608902,  0.7448387 ] ]
                self.m_xyz_rgb = [ [ 1.9624274, -0.6105343, -0.3413404 ], [-0.9787684,  1.9161415,  0.0334540 ], [ 0.0286869, -0.1406752,  1.3487655 ] ]
            if iluma == "D65": # i=3
                self.m_rgb_xyz = [ [ 0.5767309,  0.1855540,  0.1881852 ], [ 0.2973769,  0.6273491,  0.0752741 ], [ 0.0270343,  0.0706872,  0.9911085 ] ]
                self.m_xyz_rgb = [ [ 2.0413690, -0.5649464, -0.3446944 ], [-0.9692660,  1.8760108,  0.0415560 ], [ 0.0134474, -0.1183897,  1.0154096 ] ]
            else:
                iluma = "D65"
        if matrix == "Apple RGB":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.4755678,  0.3396722,  0.1489800 ], [ 0.2551812,  0.6725693,  0.0722496 ], [ 0.0184697,  0.1133771,  0.6933632 ] ]
                self.m_xyz_rgb = [ [ 2.8510695, -1.3605261, -0.4708281 ], [-1.0927680,  2.0348871,  0.0227598 ], [ 0.1027403, -0.2964984,  1.4510659 ] ]
            if iluma == "D65":
                self.m_rgb_xyz = [ [ 0.4497288,  0.3162486,  0.1844926 ], [ 0.2446525,  0.6720283,  0.0833192 ], [ 0.0251848,  0.1411824,  0.9224628 ] ]
                self.m_xyz_rgb = [ [ 2.9515373, -1.2894116, -0.4738445 ], [-1.0851093,  1.9908566,  0.0372026 ], [ 0.0854934, -0.2694964,  1.0912975 ] ]
            else:
                iluma = "D65"
        if matrix == "Best RGB":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.6326696,  0.2045558,  0.1269946 ], [ 0.2284569,  0.7373523,  0.0341908 ], [ 0.0000000,  0.0095142,  0.8156958 ] ]
                self.m_xyz_rgb = [ [ 1.7552599, -0.4836786, -0.2530000 ], [-0.5441336,  1.5068789,  0.0215528 ], [ 0.0063467, -0.0175761,  1.2256959 ] ]
            else:
                iluma = "D50"
        if matrix == "Beta RGB":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.6712537,  0.1745834,  0.1183829 ], [ 0.3032726,  0.6637861,  0.0329413 ], [ 0.0000000,  0.0407010,  0.7845090 ] ]
                self.m_xyz_rgb = [ [ 1.6832270, -0.4282363, -0.2360185 ], [-0.7710229,  1.7065571,  0.0446900 ], [ 0.0400013, -0.0885376,  1.2723640 ] ]
            else:
                iluma = "D50"
        if matrix == "Bruce RGB":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.4941816,  0.3204834,  0.1495550 ], [ 0.2521531,  0.6844869,  0.0633600 ], [ 0.0157886,  0.0629304,  0.7464909 ] ]
                self.m_xyz_rgb = [ [ 2.6502856, -1.2014485, -0.4289936 ], [-0.9787684,  1.9161415,  0.0334540 ], [ 0.0264570, -0.1361227,  1.3458542 ] ]
            if iluma == "D65":
                self.m_rgb_xyz = [ [ 0.4674162,  0.2944512,  0.1886026 ], [ 0.2410115,  0.6835475,  0.0754410 ], [ 0.0219101,  0.0736128,  0.9933071 ] ]
                self.m_xyz_rgb = [ [ 2.7454669, -1.1358136, -0.4350269 ], [-0.9692660,  1.8760108,  0.0415560 ], [ 0.0112723, -0.1139754,  1.0132541 ] ]
            else:
                iluma = "D65"
        if matrix == "CIE RGB":
            if iluma == "E":
                self.m_rgb_xyz = [ [ 0.4887180,  0.3106803,  0.2006017 ], [ 0.1762044,  0.8129847,  0.0108109 ], [ 0.0000000,  0.0102048,  0.9897952 ] ]
                self.m_xyz_rgb = [ [ 2.3706743, -0.9000405, -0.4706338 ], [-0.5138850,  1.4253036,  0.0885814 ], [ 0.0052982, -0.0146949,  1.0093968 ] ]
        if matrix == "ColorMatch RGB":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.5093439,  0.3209071,  0.1339691 ], [ 0.2748840,  0.6581315,  0.0669845 ], [ 0.0242545,  0.1087821,  0.6921735 ] ]
                self.m_xyz_rgb = [ [ 2.6422874, -1.2234270, -0.3930143 ], [-1.1119763,  2.0590183,  0.0159614 ], [ 0.0821699, -0.2807254,  1.4559877 ] ]
            else:
                iluma = "D50"
        if matrix == "Don RGB 4":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.6457711,  0.1933511,  0.1250978 ], [ 0.2783496,  0.6879702,  0.0336802 ], [ 0.0037113,  0.0179861,  0.8035125 ] ]
                self.m_xyz_rgb = [ [ 1.7603902, -0.4881198, -0.2536126 ], [-0.7126288,  1.6527432,  0.0416715 ], [ 0.0078207, -0.0347411,  1.2447743 ] ]
            else:
                iluma = "D50"
        if matrix == "ECI RGB":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.6502043,  0.1780774,  0.1359384 ], [ 0.3202499,  0.6020711,  0.0776791 ], [ 0.0000000,  0.0678390,  0.7573710 ] ]
                self.m_xyz_rgb = [ [ 1.7827618, -0.4969847, -0.2690101 ], [-0.9593623,  1.9477962, -0.0275807 ], [ 0.0859317, -0.1744674,  1.3228273 ] ]
            else:
                iluma = "D50"
        if matrix == "Ekta Space PS5":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.5938914,  0.2729801,  0.0973485 ], [ 0.2606286,  0.7349465,  0.0044249 ], [ 0.0000000,  0.0419969,  0.7832131 ] ]
                self.m_xyz_rgb = [ [ 2.0043819, -0.7304844, -0.2450052 ], [-0.7110285,  1.6202126,  0.0792227 ], [ 0.0381263, -0.0868780,  1.2725438 ] ]
            else:
                iluma = "D50"
        if matrix == "NTSC RGB":
            if iluma == "C":
                self.m_rgb_xyz = [ [ 0.6068909,  0.1735011,  0.2003480 ], [ 0.2989164,  0.5865990,  0.1144845 ], [ 0.0000000,  0.0660957,  1.1162243 ] ]
                self.m_xyz_rgb = [ [ 1.9099961, -0.5324542, -0.2882091 ], [-0.9846663,  1.9991710, -0.0283082 ], [ 0.0583056, -0.1183781,  0.8975535 ] ]
        if matrix == "PAL/SECAM RGB":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.4552773,  0.3675500,  0.1413926 ], [ 0.2323025,  0.7077956,  0.0599019 ], [ 0.0145457,  0.1049154,  0.7057489 ] ]
                self.m_xyz_rgb = [ [ 2.9603944, -1.4678519, -0.4685105 ], [-0.9787684,  1.9161415,  0.0334540 ], [ 0.0844874, -0.2545973,  1.4216174 ] ]
            if iluma == "D65":
                self.m_rgb_xyz = [ [ 0.4306190,  0.3415419,  0.1783091 ], [ 0.2220379,  0.7066384,  0.0713236 ], [ 0.0201853,  0.1295504,  0.9390944 ] ]
                self.m_xyz_rgb = [ [ 3.0628971, -1.3931791, -0.4757517 ], [-0.9692660,  1.8760108,  0.0415560 ], [ 0.0678775, -0.2288548,  1.0693490 ] ]
            else:
                iluma = "D65"
        if matrix == "ProPhoto RGB":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.7976749,  0.1351917,  0.0313534 ], [ 0.2880402,  0.7118741,  0.0000857 ], [ 0.0000000,  0.0000000,  0.8252100 ] ]
                self.m_xyz_rgb = [ [ 1.3459433, -0.2556075, -0.0511118 ], [-0.5445989,  1.5081673,  0.0205351 ], [ 0.0000000,  0.0000000,  1.2118128 ] ]
            else:
                iluma = "D50"
        if matrix == "SMPTE-C RGB":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.4163290,  0.3931464,  0.1547446 ], [ 0.2216999,  0.7032549,  0.0750452 ], [ 0.0136576,  0.0913604,  0.7201920 ] ]
                self.m_xyz_rgb = [ [ 3.3921940, -1.8264027, -0.5385522 ], [-1.0770996,  2.0213975,  0.0207989 ], [ 0.0723073, -0.2217902,  1.3960932 ] ]
            if iluma == "D65":
                self.m_rgb_xyz = [ [ 0.3935891,  0.3652497,  0.1916313 ], [ 0.2124132,  0.7010437,  0.0865432 ], [ 0.0187423,  0.1119313,  0.9581563 ] ]
                self.m_xyz_rgb = [ [ 3.5053960, -1.7394894, -0.5439640 ], [-1.0690722,  1.9778245,  0.0351722 ], [ 0.0563200, -0.1970226,  1.0502026 ] ]
            else:
                iluma = "D65"
        if matrix == "Wide Gamut RGB":
            if iluma == "D50":
                self.m_rgb_xyz = [ [ 0.7161046,  0.1009296,  0.1471858 ], [ 0.2581874,  0.7249378,  0.0168748 ], [ 0.0000000,  0.0517813,  0.7734287 ] ]
                self.m_xyz_rgb = [ [ 1.4628067, -0.1840623, -0.2743606 ], [-0.5217933,  1.4472381,  0.0677227 ], [ 0.0349342, -0.0968930,  1.2884099 ] ]
            else:
                iluma = "D50"

        # Illuminants
        if iluma == "D50":
            self.ref_x = 0.96422
            self.ref_y = 1.00
            self.ref_z = 0.82521
        if iluma == "D65":
            self.ref_x = 0.95047
            self.ref_y = 1.00
            self.ref_z = 1.08883

    #endregion
    #region Ask

    def Ask_Document( self ):
        return self.d_cm, self.d_cd, self.d_cp
    def Ask_Hue( self ):
        return self.hue
    def Ask_Luma_RGB( self ):
        return self.luma_r, self.luma_b, self.luma_g, self.luma_pr, self.luma_pb
    def Ask_Gamma( self ):
        return self.gamma_y, self.gamma_l
    def Ask_XYZ_Matrix( self ):
        return self.m_rgb_xyz, self.m_xyz_rgb, self.ref_x, self.ref_y, self.ref_z

    #endregion
    #region Links

    # Formulas
    # link : http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
    # Link : https://www.easyrgb.com/en/math.php

    # Pickers
    # link : https://colorizer.org/

    #endregion
    #region Utility

    def Vector_Safe( self, a, b, c ):
        a = self.geometry.Limit_Float( a )
        b = self.geometry.Limit_Float( b )
        c = self.geometry.Limit_Float( c )
        return a, b, c

    def List_Mult_3( self, la, lb ):
        mult = ( la[0] * lb[0] ) + ( la[1] * lb[1] ) + ( la[2] * lb[2] )
        return mult

    #endregion
    #region LERP

    def color_vector( self, mode, color ):
        if mode == "A":
            vector = [ color["aaa_1"] ]
        elif ( mode == "RGB" or mode == None ):
            vector = [ color["rgb_1"], color["rgb_2"], color["rgb_3"] ]
        elif mode == "CMY":
            vector = [ color["cmy_1"], color["cmy_2"], color["cmy_3"] ]
        elif mode == "CMYK":
            vector = [ color["cmyk_1"], color["cmyk_2"], color["cmyk_3"], color["cmyk_4"] ]
        elif mode == "RYB":
            vector = [ color["ryb_1"], color["ryb_2"], color["ryb_3"] ]
        elif mode == "YUV":
            vector = [ color["yuv_1"], color["yuv_2"], color["yuv_3"] ]
        elif mode == "HSV":
            vector = [ color["hsv_1"], color["hsv_2"], color["hsv_3"] ]
        elif mode == "HSL":
            vector = [ color["hsl_1"], color["hsl_2"], color["hsl_3"] ]
        elif mode == "HCY":
            vector = [ color["hcy_1"], color["hcy_2"], color["hcy_3"] ]
        elif mode == "ARD":
            vector = [ color["ard_1"], color["ard_2"], color["ard_3"] ]
        elif mode == "XYZ":
            vector = [ color["xyz_1"], color["xyz_2"], color["xyz_3"] ]
        elif mode == "XYY":
            vector = [ color["xyy_1"], color["xyy_2"], color["xyy_3"] ]
        elif mode == "LAB":
            vector = [ color["lab_1"], color["lab_2"], color["lab_3"] ]
        elif mode == "LCH":
            vector = [ color["lch_1"], color["lch_2"], color["lch_3"] ]
        return vector
    def color_lerp( self, mode, channels, color_a, color_b, factor ):
        color = []
        if channels >= 1:
            hue_rgb = ( "HSV", "HSL", "HCY", "ARD" )
            if mode in hue_rgb: # Circular
                dist_a = color_b[0] - color_a[0]
                if color_a[0] < color_b[0]:
                    dist_b = ( color_b[0] - 1 ) - color_a[0]
                    unit = - 1 / 360
                else:
                    dist_b = ( color_b[0] + 1 ) - color_a[0]
                    unit = 1 / 360
                dist = [ ( abs( dist_a ), dist_a ), ( abs( dist_b + unit ), dist_b ) ]
                d0 = sorted( dist )[0][1] 
                v0 = self.geometry.Limit_Looper( color_a[0] + ( d0 * factor ), 1 )
            else: # Linear
                d0 = color_b[0] - color_a[0]
                v0 = color_a[0] + ( d0 * factor  )
            color.append( v0 )
        if channels >= 2:
            d1 = color_b[1] - color_a[1]
            v1 = color_a[1] + ( d1 * factor  )
            color.append( v1 )
        if channels >= 3:
            hue_xyz = ( "LCH" )
            if mode in hue_xyz: # Circular
                dist_a = color_b[2] - color_a[2]
                if color_a[2] < color_b[2]:
                    dist_b = ( color_b[2] - 1 ) - color_a[2]
                    unit = - 1 / 360
                else:
                    dist_b = ( color_b[2] + 1 ) - color_a[2]
                    unit = 1 / 360
                dist = [ ( abs( dist_a ), dist_a ), ( abs( dist_b + unit ), dist_b ) ]
                d2 = sorted( dist )[0][1] 
                v2 = self.geometry.Limit_Looper( color_a[2] + ( d2 * factor ), 1 )
            else: # Linear
                d2 = color_b[2] - color_a[2]
                v2 = color_a[2] + ( d2 * factor  )
            color.append( v2 )
        if channels >= 4:
            d3 = color_b[3] - color_a[3]
            v3 = color_a[3] + ( d3 * factor  )
            color.append( v3 )
        return color

    def color_convert( self, d_cm, mode, color ):
        # Variables
        aaa = None
        rgb = None
        cmyk = None
        yuv = None
        xyz = None
        lab = None
        self.hue = 0

        # Lists
        list_rgb = [ "A", "RGB", "CMY", "CMYK", "RYB", "YUV", "HSV", "HSL", "HCY", "ARD" ]
        list_xyz = [ "XYZ", "XYY", "LAB", "LCH" ]
        if mode in list_rgb:form = 0
        if mode in list_xyz:form = 1

        # Document
        if d_cm == "A":
            aaa = color
            rgb = self.aaa_to_rgb( color[0] )
            if form == 1:xyz = self.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
        elif ( d_cm == "RGB" or d_cm == None ):
            rgb = color
            if form == 1:xyz = self.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
        elif d_cm == "CMYK":
            cmyk = color
            rgb = self.cmyk_to_rgb( color[0], color[1], color[2], color[3] )
            if form == 1:xyz = self.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
        elif d_cm == "YUV":
            yuv = color
            rgb = self.yuv_to_rgb( yuv[0], yuv[1], yuv[2] )
            if form == 1:xyz = self.rgb_to_xyz( rgb[0], rgb[1], rgb[2] )
        elif d_cm == "XYZ":
            xyz = color
            if form == 0:rgb = self.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
        elif d_cm == "LAB":
            lab = color
            xyz = self.lab_to_xyz( lab[0], lab[1], lab[2] )
            if form == 0:rgb = self.xyz_to_rgb( lab[0], lab[1], lab[2] )

        # Convert
        if mode == "A":
            if aaa == None:cor = self.rgb_to_aaa( rgb[0], rgb[1], rgb[2] )
            else:cor = aaa
        elif ( mode == "RGB" or mode == None ):
            cor = rgb
        elif mode == "CMY":
            cor = self.rgb_to_cmy( rgb[0], rgb[1], rgb[2] )
        elif mode == "CMYK":
            if cmyk == None:cor = self.rgb_to_cmyk( rgb[0], rgb[1], rgb[2], None )
            else:cor = cmyk
        elif mode == "RYB":
            cor = self.rgb_to_ryb( rgb[0], rgb[1], rgb[2] )
        elif mode == "YUV":
            if yuv == None:cor = self.rgb_to_yuv( rgb[0], rgb[1], rgb[2] )
            else:cor = yuv
        elif mode == "HSV":
            cor = self.rgb_to_hsv( rgb[0], rgb[1], rgb[2] )
        elif mode == "HSL":
            cor = self.rgb_to_hsl( rgb[0], rgb[1], rgb[2] )
        elif mode == "HCY":
            cor = self.rgb_to_hcy( rgb[0], rgb[1], rgb[2] )
        elif mode == "ARD":
            cor = self.rgb_to_ard( rgb[0], rgb[1], rgb[2] )
        elif mode == "XYZ":
            cor = xyz
        elif mode == "XYY":
            cor = self.xyz_to_xyy( xyz[0], xyz[1], xyz[2] )
        elif mode == "LAB":
            if lab == None:cor = self.xyz_to_lab( xyz[0], xyz[1], xyz[2] )
            else:cor = lab
        elif mode == "LCH":
            cor = self.xyz_to_lch( xyz[0], xyz[1], xyz[2] )
        return cor

    #endregion
    #region RGB LINEAR

    # AAA
    def rgb_to_aaa( self, r, g, b ):
        aaa = ( self.luma_r * r ) + ( self.luma_g * g ) + ( self.luma_b * b )
        return [aaa]
    def aaa_to_rgb( self, a ):
        r = a
        g = a
        b = a
        return [r, g, b]

    # RGB
    def srgb_to_lrgb( self, sr, sg, sb ):
        n0 = 0.055
        n1 = 1 + n0
        m = 12.92
        value = 0.04045
        if sr <= value: lr = sr / m
        else:           lr = ( ( sr + n0  ) / n1 ) ** gamma_l
        if sg <= value: lg = sg / m
        else:           lg = ( ( sg + n0  ) / n1 ) ** gamma_l
        if sb <= value: lb = sb / m
        else:           lb = ( ( sb + n0  ) / n1 ) ** gamma_l
        return [lr, lg, lb]
    def lrgb_to_srgb( self, lr, lg, lb ):
        n0 = 0.055
        n1 = 1 + n0
        m = 12.92
        value = 0.0031308
        if lr <= value: sr = lr * m
        else:           sr = n1 * lr ** ( 1 / gamma_l  ) - n0
        if lg <= value: sg = lg * m
        else:           sg = n1 * lg ** ( 1 / gamma_l  ) - n0
        if lb <= value: sb = lb * m
        else:           sb = n1 * lb ** ( 1 / gamma_l  ) - n0
        return [sr, sg, sb]
    # UVD
    def rgb_to_uvd( self, r, g, b ):
        # uv range from -1 to +1 ( 0.8 with mask )
        m00 = -0.866025808; m01 = +0.866025808; m02 = -0.0000000000000000961481791
        m10 = +0.500000010; m11 = +0.499999990; m12 = -1.00000000
        m20 = +0.333333497; m21 = +0.333333503; m22 = +0.333333000
        # MatrixInverse * RGB
        u = m00 * r + m01 * g + m02 * b
        v = m10 * r + m11 * g + m12 * b
        d = m20 * r + m21 * g + m22 * b
        m = 0.0000001
        u = self.geometry.Limit_Error( u, m )
        v = self.geometry.Limit_Error( v, m )
        return [u, v, d]
    def uvd_to_rgb( self, u, v, d ):
        m00 = -0.57735;         m01 = +0.333333; m02 = +1
        m10 = +0.57735;         m11 = +0.333333; m12 = +1
        m20 = -0.0000000113021; m21 = -0.666667; m22 = +1
        # Matrix * UVD
        r = m00 * u + m01 * v + m02 * d
        g = m10 * u + m11 * v + m12 * d
        b = m20 * u + m21 * v + m22 * d
        # Correct out of Bound values
        r, g, b = self.Vector_Safe( r, g, b )
        return [r, g, b]

    # CMY
    def rgb_to_cmy( self, r, g, b ):
        c = 1 - r
        m = 1 - g
        y = 1 - b
        return [c, m, y]
    def cmy_to_rgb( self, c, m, y ):
        r = 1 - c
        g = 1 - m
        b = 1 - y
        return [r, g, b]

    # CMYK
    def rgb_to_cmyk( self, r, g, b, key ):
        # key = black from cmyk or key ( if key is None formula is regular )
        q = max( r, g, b )
        if q == 0:
            if key == None:
                c = 0
                m = 0
                y = 0
                k = 1
            else:
                c = 1
                m = 1
                y = 1
                k = key
        else:
            if key == None:
                k = 1 - max( r, g, b ) # Standard Transform
            else:
                k = key # Key is Locked
            ik = 1 - k
            if ik == 0 :
                c = ( r - k  ) / ( k  )
                m = ( g - k  ) / ( k  )
                y = ( b - k  ) / ( k  )
            else:
                c = ( 1 - r - k  ) / ( 1 - k  )
                m = ( 1 - g - k  ) / ( 1 - k  )
                y = ( 1 - b - k  ) / ( 1 - k  )
        return [c, m, y, k]
    def cmyk_to_rgb( self, c, m, y, k ):
        r = ( 1 - c  ) * ( 1 - k  )
        g = ( 1 - m  ) * ( 1 - k  )
        b = ( 1 - y  ) * ( 1 - k  )
        r, g, b = self.Vector_Safe( r, g, b )
        return [r, g, b]
    def rgb_to_k( self, r, g, b ):
        q = max( r, g, b )
        if q == 0:
            k = 1
        else:
            k = 1 - max( r, g, b )
        return k
    def cmyk_to_tic( self, c, m, y, k):
        tic = round( ( c + m + y + k ) * 100 )
        return tic

    # RYB
    def rgb_to_ryb( self, r, g, b ):
        red = r
        green = g
        blue = b
        white  = min( red, green, blue )
        red -= white
        green -= white
        blue -= white
        maxgreen = max( red, green, blue )
        yellow = min( red, green )
        red -= yellow
        green -= yellow
        if ( blue > 0 and green > 0 ):
            blue /= 2
            green /= 2
        yellow += green
        blue += green
        maxyellow = max( red, yellow, blue )
        if maxyellow > 0:
            N = maxgreen / maxyellow
            red *= N
            yellow *= N
            blue *= N
        red += white
        yellow += white
        blue += white
        return [red, yellow, blue]
    def ryb_to_rgb( self, r, y, b ):
        red = r
        yellow = y
        blue = b
        white = min( red, yellow, blue )
        red -= white
        yellow -= white
        blue -= white
        maxyellow = max( red, yellow, blue )
        green = min( yellow, blue )
        yellow -= green
        blue -= green
        if ( blue > 0 and green > 0 ):
            blue *= 2
            green *= 2
        red += yellow
        green += yellow
        maxgreen = max( red, green, blue )
        if maxgreen > 0:
            N = maxyellow / maxgreen
            red *= N
            green *= N
            blue *= N
        red += white
        green += white
        blue += white
        return [red, green, blue]

    # YUV
    def rgb_to_yuv( self, r, g, b ):
        y = self.List_Mult_3( [ self.luma_r                                      , self.luma_g                                      , self.luma_b                                      ], [ r, g, b ] )
        u = self.List_Mult_3( [ -0.5 * ( ( self.luma_r ) / ( 1 - self.luma_b ) ) , -0.5 * ( ( self.luma_g ) / ( 1 - self.luma_b ) ) , +0.5                                             ], [ r, g, b ] )
        v = self.List_Mult_3( [ +0.5                                             , -0.5 * ( ( self.luma_g ) / ( 1 - self.luma_r ) ) , -0.5 * ( ( self.luma_b ) / ( 1 - self.luma_r ) ) ], [ r, g, b ] )
        y, u, v = self.Vector_Safe( y, 0.5 + u, 0.5 + v )
        return [ y, u, v ]
    def yuv_to_rgb( self, y, u, v ):
        u -= 0.5
        v -= 0.5
        if self.luminosity == "ITU-R BT.2020":
            r = self.List_Mult_3( [ +1 , +0                , +1.4746           ], [ y, u, v ] )
            g = self.List_Mult_3( [ +1 , -0.16455312684366 , -0.57135312684366 ], [ y, u, v ] )
            b = self.List_Mult_3( [ +1 , +1.8814           , +0                ], [ y, u, v ] )
        else:
            r = self.List_Mult_3( [ +1 , +0                                                       , 2 - 2 * self.luma_r                                      ], [ y, u, v ] )
            g = self.List_Mult_3( [ +1 , -( self.luma_b / self.luma_g ) * ( 2 - 2 * self.luma_b ) , -( self.luma_r / self.luma_g ) * ( 2 - 2 * self.luma_r ) ], [ y, u, v ] )
            b = self.List_Mult_3( [ +1 , +2 - 2 * self.luma_b                                     , 0                                                        ], [ y, u, v ] )
        r, g, b = self.Vector_Safe( r, g, b )
        return [r,g,b]

    #endregion
    #region RGB HUE

    # HUE RGB
    def rgb_to_hue( self, r, g, b ):
        # In case Krita is in Linear Format
        if self.d_cd != "U8":
            lsl = self.lrgb_to_srgb( r, g, b )
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]

        # sRGB to HSX
        v_min = min( r, g, b  )
        v_max = max( r, g, b  )
        d_max = v_max - v_min
        if d_max == 0:
            h = self.hue
        else:
            d_r = ( ( ( v_max - r  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_g = ( ( ( v_max - g  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_b = ( ( ( v_max - b  ) / 6  ) + ( d_max / 2  )  ) / d_max
            if r == v_max :
                h = d_b - d_g
            elif g == v_max :
                h = ( 1 / 3  ) + d_r - d_b
            elif b == v_max :
                h = ( 2 / 3  ) + d_g - d_r
            h = self.geometry.Limit_Looper( h, 1 )
        return h
    def hue_to_rgb( self, h ):
        vh = h * 6
        if vh == 6 :
            vh = 0
        vi = int( vh  )
        v2 = 1 * ( 1 - 1 * ( vh - vi  )  )
        v3 = 1 * ( 1 - 1 * ( 1 - ( vh - vi  )  )  )
        if vi == 0 :
            r = 1
            g = v3
            b = 0
        elif vi == 1 :
            r = v2
            g = 1
            b = 0
        elif vi == 2 :
            r = 0
            g = 1
            b = v3
        elif vi == 3 :
            r = 0
            g = v2
            b = 1
        elif vi == 4 :
            r = v3
            g = 0
            b = 1
        else:
            r = 1
            g = 0
            b = v2

        # In case Krita is in Linear Format
        if self.d_cd != "U8":
            lsl = self.srgb_to_lrgb( r, g, b )
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        return [r, g, b]
    # HUE Digital-Analog or RGB-RYB
    def hue_to_hue( self, mode, angle ):
        if mode == "DIGITAL":
            hue_d = angle
            hue_a = self.hued_to_huea( angle )
        if mode == "ANALOG":
            hue_d = self.huea_to_hued( angle )
            hue_a = angle
        return hue_d, hue_a
    def hued_to_huea( self, hued ):
        # convertion
        hued = self.geometry.Limit_Looper( hued, 1 )
        for i in range( len( digital_step ) ):
            if hued == digital_step[i]:
                huea = analog_step[i]
        for i in range( len( digital_step )-1 ):
            if ( hued > digital_step[i] and hued < digital_step[i+1] ):
                var = ( hued - digital_step[i] ) / ( digital_step[i+1] - digital_step[i] )
                huea = ( analog_step[i] + ( analog_step[i+1] - analog_step[i] ) * var  )
        return huea
    def huea_to_hued( self, huea ):
        # convertion
        hued = self.geometry.Limit_Looper( huea, 1 )
        for i in range( len( analog_step ) ):
            if huea == analog_step[i]:
                hued = digital_step[i]
        for i in range( len( analog_step )-1 ):
            if ( huea > analog_step[i] and huea < analog_step[i+1] ):
                var = ( huea - analog_step[i] ) / ( analog_step[i+1] - analog_step[i] )
                hued = ( digital_step[i] + ( digital_step[i+1] - digital_step[i] ) * var  )
        return hued
    # Hue YUV
    def uv_to_hue( self, y, u, v, angle ):
        rgb = self.yuv_to_rgb( y, u, v )
        hcy = self.rgb_to_hcy( rgb[0], rgb[1], rgb[2] )
        nrgb = self.hcy_to_rgb( angle, hcy[1], hcy[2] )
        nyuv = self.rgb_to_yuv( nrgb[0], nrgb[1], nrgb[2] )
        ny = y
        nu = nyuv[1]
        nv = nyuv[2]
        return ny, nu, nv

    # HSV
    def rgb_to_hsv( self, r, g, b ):
        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.lrgb_to_srgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]

        # sRGB to HSX
        v_min = min( r, g, b  )
        v_max = max( r, g, b  )
        d_max = v_max - v_min
        v = v_max
        if d_max == 0:
            h = self.hue
            s = 0
        else:
            s = d_max / v_max
            d_r = ( ( ( v_max - r  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_g = ( ( ( v_max - g  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_b = ( ( ( v_max - b  ) / 6  ) + ( d_max / 2  )  ) / d_max
            if r == v_max :
                h = d_b - d_g
            elif g == v_max :
                h = ( 1 / 3  ) + d_r - d_b
            elif b == v_max :
                h = ( 2 / 3  ) + d_g - d_r
            if h < 0 :
                h += 1
            if h > 1 :
                h -= 1
        return [h, s, v]
    def hsv_to_rgb( self, h, s, v ):
        # HSX to sRGB
        if s == 0:
            r = v
            g = v
            b = v
        else:
            vh = h * 6
            if vh == 6 :
                vh = 0
            vi = int( vh  )
            v1 = v * ( 1 - s  )
            v2 = v * ( 1 - s * ( vh - vi  )  )
            v3 = v * ( 1 - s * ( 1 - ( vh - vi  )  )  )
            if vi == 0 :
                r = v
                g = v3
                b = v1
            elif vi == 1 :
                r = v2
                g = v
                b = v1
            elif vi == 2 :
                r = v1
                g = v
                b = v3
            elif vi == 3 :
                r = v1
                g = v2
                b = v
            elif vi == 4 :
                r = v3
                g = v1
                b = v
            else:
                r = v
                g = v1
                b = v2

        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.srgb_to_lrgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]
        return [r, g, b]
    # HSL
    def rgb_to_hsl( self, r, g, b ):
        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.lrgb_to_srgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]

        # sRGB to HSX
        v_min = min( r, g, b  )
        v_max = max( r, g, b  )
        d_max = v_max - v_min
        l = ( v_max + v_min  )/ 2
        if d_max == 0 :
            h = self.hue
            s = 0
        else:
            if l < 0.5 :
                s = d_max / ( v_max + v_min  )
            else:
                s = d_max / ( 2 - v_max - v_min  )
            d_r = ( ( ( v_max - r  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_g = ( ( ( v_max - g  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_b = ( ( ( v_max - b  ) / 6  ) + ( d_max / 2  )  ) / d_max
            if r == v_max :
                h = d_b - d_g
            elif g == v_max:
                h = ( 1 / 3  ) + d_r - d_b
            elif b == v_max:
                h = ( 2 / 3  ) + d_g - d_r
            if h < 0:
                h += 1
            if h > 1:
                h -= 1
        return [h, s, l]
    def hsl_to_rgb( self, h, s, l ):
        if s == 0 :
            r = l
            g = l
            b = l
        else:
            if l < 0.5:
                v2 = l * ( 1 + s  )
            else:
                v2 = ( l + s  ) - ( s * l  )
            v1 = 2 * l - v2
            r = self.hsl_chan( v1, v2, h + ( 1 / 3  )  )
            g = self.hsl_chan( v1, v2, h  )
            b = self.hsl_chan( v1, v2, h - ( 1 / 3  )  )

        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.srgb_to_lrgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]
        return [r, g, b]
    def hsl_chan( self, v1, v2, vh ):
        if vh < 0 :
            vh += 1
        if vh > 1 :
            vh -= 1
        if ( 6 * vh  ) < 1 :
            return ( v1 + ( v2 - v1  ) * 6 * vh  )
        if ( 2 * vh  ) < 1 :
            return ( v2  )
        if ( 3 * vh  ) < 2 :
            return ( v1 + ( v2 - v1  ) * ( ( 2 / 3  ) - vh  ) * 6  )
        return ( v1  )
    # HSY ( Krita version )
    def rgb_to_hsy( self, r, g, b ):
        # In case Krita is NOT in Linear Format
        # if self.d_cd == "U8":
        #     lsl = self.srgb_to_lrgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]

        # sRGB to HSX
        minval = min( r, g, b )
        maxval = max( r, g, b )
        luma = ( self.luma_r * r + self.luma_g * g + self.luma_b * b )
        luma_a = luma
        chroma = maxval - minval
        max_sat = 0.5
        if chroma == 0:
            hue = self.hue
            sat = 0
        else:
            if maxval == r:
                if minval == b:
                    hue = ( g - b ) / chroma
                else:
                    hue = ( g - b ) / chroma + 6
            elif maxval == g:
                hue = ( b - r ) / chroma + 2
            elif maxval == b:
                hue = ( r - g ) / chroma + 4
            hue /= 6
            # segment = 0.166667
            segment = 1 / 6
            if ( hue > 1 or hue < 0 ):
                hue = math.fmod( hue, 1 )
            if ( hue >= 0 * segment and hue < 1 * segment ):
                max_sat = self.luma_r + self.luma_g * ( hue * 6 )
            elif ( hue >= 1 * segment and hue < 2 * segment ):
                max_sat = ( self.luma_g + self.luma_r ) - self.luma_r * ( ( hue - segment ) * 6 )
            elif ( hue >= 2 * segment and hue < 3 * segment ):
                max_sat = self.luma_g + self.luma_b * ( ( hue - 2 * segment ) * 6 )
            elif ( hue >= 3 * segment and hue < 4 * segment ):
                max_sat = ( self.luma_b + self.luma_g ) - self.luma_g * ( ( hue - 3 * segment ) * 6 )
            elif ( hue >= 4 * segment and hue < 5 * segment ):
                max_sat =  ( self.luma_b ) + self.luma_r * ( ( hue - 4 * segment ) * 6 )
            elif ( hue >= 5 * segment and hue <= 1 ):
                max_sat = ( self.luma_r + self.luma_b ) - self.luma_b * ( ( hue - 5 * segment ) * 6 )
            else:
                max_sat = 0.5

            if( max_sat > 1 or max_sat < 0 ):
                max_sat = math.fmod( max_sat, 1 )

            if luma <= max_sat:
                luma_a = ( luma / max_sat ) * 0.5
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5

            if ( chroma > 0 ):
                sat = ( ( chroma / ( 2 * luma_a ) ) if ( luma <= max_sat ) else ( chroma / ( 2 - ( 2 * luma_a ) ) ) )
        if sat <= 0:
            sat = 0
        if luma <= 0:
            luma = 0
        h = hue
        s = sat
        y = luma ** ( 1 / self.gamma_y )
        return [h, s, y]
    def hsy_to_rgb( self, h, s, y ):
        hue = 0
        sat = 0
        luma = 0
        if ( h > 1 or h < 0 ):
            hue = math.fmod( h, 1 )
        else:
            hue = h
        if s < 0:
            sat = 0
        else:
            sat = s
        if y < 0:
            luma = 0
        else:
            luma = y ** ( self.gamma_y )
        # segment = 0.166667
        segment = 1 / 6
        r = 0
        g = 0
        b = 0
        if ( hue >= 0 and hue < segment ):
            max_sat = self.luma_r + ( self.luma_g * ( hue * 6 )  )
            if luma <= max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * 2 * luma_a
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 ) ) * chroma
            r = chroma
            g = x
            b = 0
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        elif ( hue >= ( segment ) and hue < 2 * segment ):
            max_sat = ( self.luma_g + self.luma_r ) - ( self.luma_r * ( hue - segment ) * 6 )
            if luma < max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * ( 2 * luma_a )
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 )  ) * chroma
            r = x
            g = chroma
            b = 0
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        elif ( hue >= 2 * segment and hue < 3 * segment ):
            max_sat = self.luma_g + ( self.luma_b * ( hue - 2 * segment ) * 6 )
            if luma < max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * ( 2 * luma_a )
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 ) ) * chroma
            r = 0
            g = chroma
            b = x
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        elif ( hue >= 3 * segment and hue < 4 * segment ):
            max_sat = ( self.luma_g + self.luma_b ) - ( self.luma_g * ( hue - 3 * segment ) * 6 )
            if luma < max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * ( 2 * luma_a )
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 ) ) * chroma
            r = 0
            g = x
            b = chroma
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        elif ( hue >= 4 * segment and hue < 5 * segment ):
            max_sat = self.luma_b + ( self.luma_r * ( ( hue - 4 * segment ) * 6 ) )
            if luma < max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * ( 2 * luma_a )
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 ) ) * chroma
            r = x
            g = 0
            b = chroma
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        elif ( hue >= 5 * segment and hue <= 1 ):
            max_sat = ( self.luma_b + self.luma_r ) - ( self.luma_b * ( hue - 5 * segment ) * 6 )
            if luma < max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * ( 2 * luma_a )
            else:
                luma_a = ( ( luma-max_sat ) / ( 1-max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 ) ) * chroma
            r = chroma
            g = 0
            b = x
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        else:
            r = 0
            g = 0
            b = 0
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0

        # In case Krita is NOT in Linear Format
        # if self.d_cd == "U8":
        #     lsl = self.lrgb_to_srgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]
        return [r, g, b]
    # HCY ( My Paint Version )
    def rgb_to_hcy( self, r, g, b ):
        # In case Krita is NOT in Linear Format
        # if self.d_cd != "U8": # == vs !=
        #     lsl = self.srgb_to_lrgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]

        # sRGB to HSX
        y = self.luma_r * r + self.luma_g * g + self.luma_b * b
        p = max( r, g, b )
        n = min( r, g, b )
        d = p - n
        if n == p:
            h = self.hue
        elif p == r:
            h = ( g - b ) / d
            if h < 0:
                h += 6.0
        elif p == g:
            h = ( ( b - r ) / d ) + 2.0
        elif p == b:
            h = ( ( r - g ) / d ) + 4.0
        h /= 6.0
        if ( r == g == b or y == 0 or y == 1 ):
            h = self.hue
            c = 0.0
        else:
            c = max( ( y-n ) / y, ( p - y ) / ( 1 - y ) )
        if self.d_cd != "U8": # == vs !=
            y = y**( 1 / self.gamma_y ) # Gama compression of the luma value
        return [h, c, y]
    def hcy_to_rgb( self, h, c, y ):
        if self.d_cd != "U8": # == vs !=
            y = y**( self.gamma_y ) # Gama compression of the luma value
        if c == 0:
            r = y
            g = y
            b = y
        h %= 1.0
        h *= 6.0
        if h < 1:
            th = h
            tm = self.luma_r + self.luma_g * th
        elif h < 2:
            th = 2.0 - h
            tm = self.luma_g + self.luma_r * th
        elif h < 3:
            th = h - 2.0
            tm = self.luma_g + self.luma_b * th
        elif h < 4:
            th = 4.0 - h
            tm = self.luma_b + self.luma_g * th
        elif h < 5:
            th = h - 4.0
            tm = self.luma_b + self.luma_r * th
        else:
            th = 6.0 - h
            tm = self.luma_r + self.luma_b * th
        # Calculate the RGB components in sorted order
        if tm >= y:
            p = y + y * c * ( 1 - tm ) / tm
            o = y + y * c * ( th - tm ) / tm
            n = y - ( y * c )
        else:
            p = y + ( 1 - y ) * c
            o = y + ( 1 - y ) * c * ( th - tm ) / ( 1 - tm )
            n = y - ( 1 - y ) * c * tm / ( 1 - tm )
        # Back to RGB order
        if h < 1:
            r = p
            g = o
            b = n
        elif h < 2:
            r = o
            g = p
            b = n
        elif h < 3:
            r = n
            g = p
            b = o
        elif h < 4:
            r = n
            g = o
            b = p
        elif h < 5:
            r = o
            g = n
            b = p
        else:
            r = p
            g = n
            b = o

        # In case Krita is NOT in Linear Format
        # if self.d_cd != "U8": # == vs !=
        #     lsl = self.lrgb_to_srgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]
        return [r, g, b]

    # ARD
    def rgb_to_ard( self, r, g, b ):
        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.lrgb_to_srgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]

        # Depth
        uvd = self.rgb_to_uvd( r, g, b )
        u = uvd[0]
        v = uvd[1]
        d = uvd[2]
        # Hexagon Depth
        di = d * 3
        if ( di == 0 or di == 1 ):
            a = self.hue
            r = 0
        else:
            # Angle
            a = self.rgb_to_hue( r, g, b )
            # Channel
            O1, O2, O3, O4, O5, O6, C12, C23, C34, C45, C56, C61 = self.uvd_hexagon( d, 1, 0, 1 )
            c = self.ard_channel( d, a, O1, O2, O3, O4, O5, O6, C12, C23, C34, C45, C56, C61 )

            # Ratio
            if ( r == g and g == b and b == r ):
                r = 0
            elif ( r == 0 or g == 0 or b == 0 or r == 1 or g == 1 or b == 1 ):
                r = 1
            else:
                # Neutral Value
                n = ( r + g + b ) / 3 # Ratio = 0
                # Delta
                dr = r - n
                dg = g - n
                db = b - n
                # Ratio Distance
                if c == +1:r = dr / ( 1 - n )
                if c == -1:r = dr / -n
                if c == +2:r = dg / ( 1 - n )
                if c == -2:r = dg / -n
                if c == +3:r = db / ( 1 - n )
                if c == -3:r = db / -n
        # Return
        return [ a, r, d ]
    def ard_to_rgb( self, a, r, d ):
        # Channel
        di = d * 3
        lu = 0
        lv = 0
        if di <= 0:
            r = 0
            g = 0
            b = 0
        elif di >= 3:
            r = 1
            g = 1
            b = 1
        else:
            # Hexagon
            O1, O2, O3, O4, O5, O6, C12, C23, C34, C45, C56, C61 = self.uvd_hexagon( d, 1, 0, 1 )

            # Angle
            hrgb = self.hue_to_rgb( a )
            huvd = self.rgb_to_uvd( hrgb[0], hrgb[1], hrgb[2] )
            acc = self.geometry.Trig_2D_Points_Lines_Angle( huvd[0], huvd[1], 0, 0, C61[0], C61[1] ) / 360

            # Angle
            a01 = self.geometry.Trig_2D_Points_Lines_Angle( O1[0], O1[1], 0, 0, C61[0], C61[1] ) / 360
            a02 = self.geometry.Trig_2D_Points_Lines_Angle( O2[0], O2[1], 0, 0, C61[0], C61[1] ) / 360
            a03 = self.geometry.Trig_2D_Points_Lines_Angle( O3[0], O3[1], 0, 0, C61[0], C61[1] ) / 360
            a04 = self.geometry.Trig_2D_Points_Lines_Angle( O4[0], O4[1], 0, 0, C61[0], C61[1] ) / 360
            a05 = self.geometry.Trig_2D_Points_Lines_Angle( O5[0], O5[1], 0, 0, C61[0], C61[1] ) / 360
            a06 = self.geometry.Trig_2D_Points_Lines_Angle( O6[0], O6[1], 0, 0, C61[0], C61[1] ) / 360
            a12 = self.geometry.Trig_2D_Points_Lines_Angle( C12[0], C12[1], 0, 0, C61[0], C61[1] ) / 360
            a23 = self.geometry.Trig_2D_Points_Lines_Angle( C23[0], C23[1], 0, 0, C61[0], C61[1] ) / 360
            a34 = self.geometry.Trig_2D_Points_Lines_Angle( C34[0], C34[1], 0, 0, C61[0], C61[1] ) / 360
            a45 = self.geometry.Trig_2D_Points_Lines_Angle( C45[0], C45[1], 0, 0, C61[0], C61[1] ) / 360
            a56 = self.geometry.Trig_2D_Points_Lines_Angle( C56[0], C56[1], 0, 0, C61[0], C61[1] ) / 360

            # Depth
            if ( di > 0 and di <= 1):
                if ( acc <= a23 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C61[0], C61[1], C23[0], C23[1] )
                elif ( acc > a23 and acc <= a45 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C23[0], C23[1], C45[0], C45[1] )
                else:
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C45[0], C45[1], C61[0], C61[1] )
            elif ( di > 1 and di < 2):
                if ( acc <= a01 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C61[0], C61[1], O1[0], O1[1] )
                elif ( acc > a01 and acc <= a02 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O1[0], O1[1], O2[0], O2[1] )
                elif ( acc > a02 and acc <= a03 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O2[0], O2[1], O3[0], O3[1] )
                elif ( acc > a03 and acc <= a04 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O3[0], O3[1], O4[0], O4[1] )
                elif ( acc > a04 and acc <= a05 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O4[0], O4[1], O5[0], O5[1] )
                elif ( acc > a05 and acc <= a06 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O5[0], O5[1], O6[0], O6[1] )
                else:
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O6[0], O6[1], C61[0], C61[1] )
            elif ( di >= 2 and di < 3):
                if ( acc <= a12 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C61[0], C61[1], C12[0], C12[1] )
                elif ( acc > a12 and acc <= a34 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C12[0], C12[1], C34[0], C34[1] )
                elif ( acc > a34 and acc <= a56 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C34[0], C34[1], C56[0], C56[1] )
                else:
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C56[0], C56[1], C61[0], C61[1] )
            # UVD Interpolation
            uvd = self.geometry.Lerp_3D( r, 0, 0, d, lu, lv, d )
            rgb = self.uvd_to_rgb( uvd[0], uvd[1], uvd[2] )
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]

        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.srgb_to_lrgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]
        return [r, g, b]
    def uvd_hexagon( self, d, s, o, i ):
        # s = scale
        # o = offset center
        # i = invert Y axis ( panel is inverted )

        # Primaries
        cn = [ 0, 0 ]
        cr = self.rgb_to_uvd( 1, 0, 0 )
        cy = self.rgb_to_uvd( 1, 1, 0 )
        cg = self.rgb_to_uvd( 0, 1, 0 )
        cc = self.rgb_to_uvd( 0, 1, 1 )
        cb = self.rgb_to_uvd( 0, 0, 1 )
        cm = self.rgb_to_uvd( 1, 0, 1 )
        # Single Points
        di = d * 3
        u0 = 0
        u1 = 1
        u2 = 2
        u3 = 3
        if ( di <= u0 or di >= u3 ):
            # Original
            O1 = [ o, o ]
            O2 = [ o, o ]
            O3 = [ o, o ]
            O4 = [ o, o ]
            O5 = [ o, o ]
            O6 = [ o, o ]
            # Complementary
            C12 = [ o, o ]
            C23 = [ o, o ]
            C34 = [ o, o ]
            C45 = [ o, o ]
            C56 = [ o, o ]
            C61 = [ o, o ]
        else:
            # Original
            if ( di >= u0 and di <= u1):
                p = di
                o1_u, o1_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cr[0], cr[1] )
                o2_u, o2_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cg[0], cg[1] )
                o3_u, o3_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cg[0], cg[1] )
                o4_u, o4_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cb[0], cb[1] )
                o5_u, o5_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cb[0], cb[1] )
                o6_u, o6_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cr[0], cr[1] )
            elif ( di > u1 and di < u2):
                p = di - 1
                o1_u, o1_v = self.geometry.Lerp_2D( p, cr[0], cr[1], cy[0], cy[1] )
                o2_u, o2_v = self.geometry.Lerp_2D( p, cg[0], cg[1], cy[0], cy[1] )
                o3_u, o3_v = self.geometry.Lerp_2D( p, cg[0], cg[1], cc[0], cc[1] )
                o4_u, o4_v = self.geometry.Lerp_2D( p, cb[0], cb[1], cc[0], cc[1] )
                o5_u, o5_v = self.geometry.Lerp_2D( p, cb[0], cb[1], cm[0], cm[1] )
                o6_u, o6_v = self.geometry.Lerp_2D( p, cr[0], cr[1], cm[0], cm[1] )
            elif ( di >= u2 and di <= u3):
                p = di - 2
                o1_u, o1_v = self.geometry.Lerp_2D( p, cy[0], cy[1], cn[0], cn[1] )
                o2_u, o2_v = self.geometry.Lerp_2D( p, cy[0], cy[1], cn[0], cn[1] )
                o3_u, o3_v = self.geometry.Lerp_2D( p, cc[0], cc[1], cn[0], cn[1] )
                o4_u, o4_v = self.geometry.Lerp_2D( p, cc[0], cc[1], cn[0], cn[1] )
                o5_u, o5_v = self.geometry.Lerp_2D( p, cm[0], cm[1], cn[0], cn[1] )
                o6_u, o6_v = self.geometry.Lerp_2D( p, cm[0], cm[1], cn[0], cn[1] )
            # Original
            O1 = [ o1_u * s + o, i * o1_v * s + o ]
            O2 = [ o2_u * s + o, i * o2_v * s + o ]
            O3 = [ o3_u * s + o, i * o3_v * s + o ]
            O4 = [ o4_u * s + o, i * o4_v * s + o ]
            O5 = [ o5_u * s + o, i * o5_v * s + o ]
            O6 = [ o6_u * s + o, i * o6_v * s + o ]
            # Complemtary
            C12 = self.geometry.Lerp_2D( 0.5, O1[0], O1[1], O2[0], O2[1] )
            C23 = self.geometry.Lerp_2D( 0.5, O2[0], O2[1], O3[0], O3[1] )
            C34 = self.geometry.Lerp_2D( 0.5, O3[0], O3[1], O4[0], O4[1] )
            C45 = self.geometry.Lerp_2D( 0.5, O4[0], O4[1], O5[0], O5[1] )
            C56 = self.geometry.Lerp_2D( 0.5, O5[0], O5[1], O6[0], O6[1] )
            C61 = self.geometry.Lerp_2D( 0.5, O6[0], O6[1], O1[0], O1[1] ) # Red Hue=0

        # Return
        return O1, O2, O3, O4, O5, O6, C12, C23, C34, C45, C56, C61
    def ard_channel( self, d, a, O1, O2, O3, O4, O5, O6, C12, C23, C34, C45, C56, C61 ):
        # Angle
        a01 = self.geometry.Trig_2D_Points_Lines_Angle( O1[0], O1[1], 0, 0, C61[0], C61[1] ) / 360
        a02 = self.geometry.Trig_2D_Points_Lines_Angle( O2[0], O2[1], 0, 0, C61[0], C61[1] ) / 360
        a03 = self.geometry.Trig_2D_Points_Lines_Angle( O3[0], O3[1], 0, 0, C61[0], C61[1] ) / 360
        a04 = self.geometry.Trig_2D_Points_Lines_Angle( O4[0], O4[1], 0, 0, C61[0], C61[1] ) / 360
        a05 = self.geometry.Trig_2D_Points_Lines_Angle( O5[0], O5[1], 0, 0, C61[0], C61[1] ) / 360
        a06 = self.geometry.Trig_2D_Points_Lines_Angle( O6[0], O6[1], 0, 0, C61[0], C61[1] ) / 360
        a12 = self.geometry.Trig_2D_Points_Lines_Angle( C12[0], C12[1], 0, 0, C61[0], C61[1] ) / 360
        a23 = self.geometry.Trig_2D_Points_Lines_Angle( C23[0], C23[1], 0, 0, C61[0], C61[1] ) / 360
        a34 = self.geometry.Trig_2D_Points_Lines_Angle( C34[0], C34[1], 0, 0, C61[0], C61[1] ) / 360
        a45 = self.geometry.Trig_2D_Points_Lines_Angle( C45[0], C45[1], 0, 0, C61[0], C61[1] ) / 360
        a56 = self.geometry.Trig_2D_Points_Lines_Angle( C56[0], C56[1], 0, 0, C61[0], C61[1] ) / 360
        a61 = 1
        # Channel
        di = d * 3
        if ( di <= 0 or di >= 3 ):
            c = +1
        elif ( di > 0 and di <= 1):
            if ( a <= a23 ):c = -3
            elif ( a > a23 and a <= a45 ):c = -1
            else:c = -2
        elif ( di > 1 and di < 2):
            if ( a <= a01 ):c = +1
            elif ( a > a01 and a <= a02 ):c = -3
            elif ( a > a02 and a <= a03 ):c = +2
            elif ( a > a03 and a <= a04 ):c = -1
            elif ( a > a04 and a <= a05 ):c = +3
            elif ( a > a05 and a <= a06 ):c = -2
            else:c = +1
        elif ( di >= 2 and di < 3):
            if ( a <= a12 ):c = +1
            elif ( a > a12 and a <= a34 ):c = +2
            elif ( a > a34 and a <= a56 ):c = +3
            else:c = +1

        # Return
        return c

    #endregion
    #region XYZ LINEAR

    def rgb_to_xyz( self, r, g, b ):
        lrgb = self.srgb_to_lrgb( r, g, b )
        x = ( lrgb[0] * self.m_rgb_xyz[0][0] ) + ( lrgb[1] * self.m_rgb_xyz[0][1] ) + ( lrgb[2] * self.m_rgb_xyz[0][2] )
        y = ( lrgb[0] * self.m_rgb_xyz[1][0] ) + ( lrgb[1] * self.m_rgb_xyz[1][1] ) + ( lrgb[2] * self.m_rgb_xyz[1][2] )
        z = ( lrgb[0] * self.m_rgb_xyz[2][0] ) + ( lrgb[1] * self.m_rgb_xyz[2][1] ) + ( lrgb[2] * self.m_rgb_xyz[2][2] )
        return [x, y, z]
    def xyz_to_rgb( self, x, y, z ):
        var_r = ( x * self.m_xyz_rgb[0][0] ) + ( y * self.m_xyz_rgb[0][1] ) + ( z * self.m_xyz_rgb[0][2] )
        var_g = ( x * self.m_xyz_rgb[1][0] ) + ( y * self.m_xyz_rgb[1][1] ) + ( z * self.m_xyz_rgb[1][2] )
        var_b = ( x * self.m_xyz_rgb[2][0] ) + ( y * self.m_xyz_rgb[2][1] ) + ( z * self.m_xyz_rgb[2][2] )
        srgb = self.lrgb_to_srgb( var_r, var_g, var_b )
        r, g, b = self.Vector_Safe( srgb[0], srgb[1], srgb[2] )
        return [r, g, b]
    # XYY
    def xyz_to_xyy( self, x, y, z ):
        if ( x == 0 and y == 0 and z == 0 ):
            x1 = 0.31272660439158345
            y2 = 0.3290231524027522
            y3 = y
        else:
            x1 = x / ( x + y + z  )
            y2 = y / ( x + y + z  )
            y3 = y
        return [x1, y2, y3]
    def xyy_to_xyz( self, x1, y2, y3 ):
        if y2 == 0:
            x = 0
            y = 0
            z = 0
        else:
            x = ( x1 * y3  ) / y2
            y = y3
            z = ( ( 1 - x1 - y2 ) * y3 ) / y2
        return [x, y, z]
    def rgb_to_xyy( self, r, g, b ):
        xyz = self.rgb_to_xyz( r, g, b )
        xyy = self.xyz_to_xyy( xyz[0], xyz[1], xyz[2] )
        return [xyy[0], xyy[1], xyy[2]]
    def xyy_to_rgb( self, x, y1, y2 ):
        xyz = self.xyy_to_xyz( x, y1, y2 )
        rgb = self.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
        return [rgb[0], rgb[1], rgb[2]]
    # LAB
    def xyz_to_lab( self, x, y, z ):
        k = 903.3 # Kappa
        e = 0.008856 # Epsilon

        rx = x / self.ref_x
        ry = y / self.ref_y
        rz = z / self.ref_z

        if rx > e: fx = rx**( 1/3 )
        else:      fx = ( k*rx + 16 ) / 116
        if ry > e: fy = ry**( 1/3 )
        else:      fy = ( k*ry + 16 ) / 116
        if rz > e: fz = rz**( 1/3 )
        else:      fz = ( k*rz + 16 ) / 116

        l = ( ( 116 * fy ) - 16 ) / 100
        a = 0.5 + ( fx - fy )
        b = 0.5 + ( fy - fz )

        return [ l, a, b ]
    def lab_to_xyz( self, l, a, b ):
        k = 903.3 # Kappa
        e = 0.008856 # Epsilon

        l = l * 100
        a = a - 0.5
        b = b - 0.5
        fy = ( l + 16  ) / 116
        fx = a + fy
        fz = fy - b

        if fx**3 > e: rx = fx**3
        else:         rx = ( 116 * fx - 16 ) / k
        if l > k*e:   ry = ( ( l + 16 ) / 116 )**3
        else:         ry = l / k
        if fz**3 > e: rz = fz**3
        else:         rz = ( 116 * fz - 16 ) / k

        x = rx * self.ref_x
        y = ry * self.ref_y
        z = rz * self.ref_z

        return [ x, y, z ]
    def rgb_to_lab( self, r, g, b ):
        xyz = self.rgb_to_xyz( r, g, b )
        lab = self.xyz_to_lab( xyz[0], xyz[1], xyz[2] )
        return [ lab[0], lab[1], lab[2] ]
    def lab_to_rgb( self, l, a, b ):
        xyz = self.lab_to_xyz( l, a, b )
        rgb = self.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
        return [ rgb[0], rgb[1], rgb[2] ]

    #endregion
    #region XYZ HUE

    # LCHab
    def lab_to_lch( self, l, a, b ):
        a = ( a - 0.5 ) * 2
        b = ( b - 0.5 ) * 2

        vh = math.atan2( b, a )
        if vh > 0: vh = ( vh / math.pi ) * 180
        else:      vh = 360 - ( abs( vh ) / math.pi ) * 180
        c = math.sqrt( a**2 + b**2 )
        h = vh / 360

        l, c, h = self.Vector_Safe( l, c, h )
        return [ l, c, h ]
    def lch_to_lab( self, l, c, h ):
        vh = h * 360

        a = math.cos( math.radians( vh ) ) * c
        b = math.sin( math.radians( vh ) ) * c

        a = a / 2 + 0.5
        b = b / 2 + 0.5

        l, a, b = self.Vector_Safe( l, a, b )
        return [ l, a, b ]
    def xyz_to_lch( self, x, y, z ):
        lab = self.xyz_to_lab( x, y, z )
        lch = self.lab_to_lch( lab[0], lab[1], lab[2] )
        return [ lch[0], lch[1], lch[2] ]
    def lch_to_xyz( self, l, c, h ):
        lab = self.lch_to_lab( l, c, h )
        xyz = self.lab_to_xyz( lab[0], lab[1], lab[2] )
        return [ xyz[0], xyz[1], xyz[2] ]
    def rgb_to_lch( self, r, g, b ):
        xyz = self.rgb_to_xyz( r, g, b )
        lab = self.xyz_to_lab( xyz[0], xyz[1], xyz[2] )
        lch = self.lab_to_lch( lab[0], lab[1], lab[2] )
        return [ lch[0], lch[1], lch[2] ]
    def lch_to_rgb( self, l, c, h ):
        lab = self.lch_to_lab( l, c, h )
        xyz = self.lab_to_xyz( lab[0], lab[1], lab[2] )
        rgb = self.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
        return [ rgb[0], rgb[1], rgb[2] ]

    #endregion
    #region Non-Color

    # KELVIN ( not physical based )
    def kkk_percent_to_scale( self, percent ):
        scale = int( ( percent * kkk_delta ) + kkk_min_scale )
        return scale
    def kkk_scale_to_percent( self, scale ):
        percent = ( scale - kkk_min_scale ) / kkk_delta
        return percent

    def kkk_to_rgb( self, temp, lut ):
        # Entry
        entry = self.search_entry( temp, lut )
        # RGB
        r = lut[entry][0]
        g = lut[entry][1]
        b = lut[entry][2]
        # Return
        return [r, g, b]
    def kkk_to_cd( self, temp, lut ):
        # Entry
        entry = self.search_entry( temp, lut )
        # Class and Discription
        c = lut[entry][0]
        d = lut[entry][1]
        # Return
        return [c, d]
    def search_entry( self, temp, lut ):
        # Variables
        key = list( lut.keys() )
        length = len( key )
        # Search
        entry = key[0]
        if ( temp > key[0] ):
            for i in range( 0, length ):
                key_i = key[i]
                if temp < key_i:
                    entry = key[i-1]
                    break
                if temp == key_i:
                    entry = key_i
                    break
                entry = key_i
        return entry

    #endregion
    #region HEX

    def rgb_to_hex6( self, r, g, b ):
        hex1 = str( hex( int( r * 255 )  )  )[2:4].zfill( 2 )
        hex2 = str( hex( int( g * 255 )  )  )[2:4].zfill( 2 )
        hex3 = str( hex( int( b * 255 )  )  )[2:4].zfill( 2 )
        hex_code = str( "#" + hex1 + hex2 + hex3  )
        return hex_code
    def hex6_to_rgb( self, hex_code ):
        # Hexadecimal
        hex1 = int( format( int( hex_code[1:3],16 ),'02d' ) )
        hex2 = int( format( int( hex_code[3:5],16 ),'02d' ) )
        hex3 = int( format( int( hex_code[5:7],16 ),'02d' ) )
        # Range
        r = hex1 / 255
        g = hex2 / 255
        b = hex3 / 255
        rgb = [r, g, b]
        return rgb
    def hex6_to_name( self, hex_code, color_names ):
        search = color_names.get( hex_code )
        if search == None:
            name = ""
        else:
            name = search[0]
        return name

    def hex3_to_rgb( self, hex_code ):
        # Parse
        hex1 = hex_code[1:2]
        hex2 = hex_code[2:3]
        hex3 = hex_code[3:4]
        # Hexadecimal
        hex1 = int( format( int( hex1+hex1 ,16 ),'02d' ) )
        hex2 = int( format( int( hex2+hex2 ,16 ),'02d' ) )
        hex3 = int( format( int( hex3+hex3 ,16 ),'02d' ) )
        # Range
        r = hex1 / 255
        g = hex2 / 255
        b = hex3 / 255
        rgb = [r, g, b]

        return rgb

    #endregion


class Analyse():

    #region Numbers

    # Bytes
    def Bytes_to_Integer( self, byte_array, d_cd ):
        # converts byte data to numerical data
        # byte_data - information read from a document
        # d_cd - document color depth

        # Byte Order
        byte_order = sys.byteorder
        # Bit Depth
        num_array = []
        if ( d_cd == "U8" or d_cd == None ):
            for i in range( 0, len( byte_array ) ):
                byte = byte_array.at( i )
                num = int.from_bytes( byte, byte_order )
                num_array.append( num )
        elif ( d_cd == "U16" or d_cd == "F16" ):
            for i in range( 0, len( byte_array ), 2 ):
                b1 = byte_array.at( i )
                b2 = byte_array.at( i+1 )
                byte = b1 + b2
                num = int.from_bytes( byte, byte_order )
                num_array.append( num )
        elif d_cd == "F32":
            for i in range( 0, len( byte_array ), 4 ):
                b1 = byte_array.at( i )
                b2 = byte_array.at( i+1 )
                b3 = byte_array.at( i+2 )
                b4 = byte_array.at( i+3 )
                byte = b1 + b2 + b3 + b4
                num = int.from_bytes( byte, byte_order )
                num_array.append( num )
        # Return
        return num_array
    def Integer_to_Bytes( self, num_array, d_cd ):
        # converts numbers to byte data
        # num_data - information previously calculated
        # d_cd - document color depth

        # Byte Order
        byte_order = sys.byteorder
        # Bit Depth
        if d_cd == "U8":
            k = 1
        elif ( d_cd == "U16" or d_cd == "F16" ):
            k = 2
        elif d_cd == "F32":
            k = 4

        # Conversion to Bytes
        byte_array = bytearray( num_array )
        return byte_array
    # Pixels
    def Numbers_on_Pixel( self, d_cm, d_cd, index, num_array ):
        # reads the numerical data from a pixel with a given index

        # Variables
        if d_cd == "U8": # BGR
            k = 255
        elif d_cd == "U16":
            k = 65535
        elif d_cd == "F16":
            # k = 65535
            k = 15360
        elif d_cd == "F32":
            # k = 4294836225
            k = 1065353216
        # Color Model and Depth
        byte_list = []
        if d_cm == "A":
            pixel = index * 2
            if d_cd == "U8":
                n0 = num_array[pixel + 0] # Gray
                n1 = num_array[pixel + 1] # Alpha
            if d_cd == "U16":
                n0 = num_array[pixel + 0] # Gray
                n1 = num_array[pixel + 1] # Alpha
            if d_cd == "F16":
                pass
            if d_cd == "F32":
                pass
            byte_list = [n0, n1]
        elif ( d_cm == "RGB" or d_cm == None ):
            pixel = index * 4
            if d_cd == "U8": # BGR
                n0 = num_array[pixel + 2] # Red
                n1 = num_array[pixel + 1] # Green
                n2 = num_array[pixel + 0] # Blue
                n3 = num_array[pixel + 3] # Alpha
            if d_cd == "U16": # BGR
                n0 = num_array[pixel + 2] # Red
                n1 = num_array[pixel + 1] # Green
                n2 = num_array[pixel + 0] # Blue
                n3 = num_array[pixel + 3] # Alpha
            if d_cd == "F16":
                pass
            if d_cd == "F32":
                pass
            byte_list = [n0, n1, n2, n3]
        elif d_cm == "CMYK":
            pixel = index * 5
            if d_cd == "U8":
                n0 = num_array[pixel + 0] # Cyan
                n1 = num_array[pixel + 1] # Magenta
                n2 = num_array[pixel + 2] # Yellow
                n3 = num_array[pixel + 3] # Key
                n4 = num_array[pixel + 4] # Alpha
            if d_cd == "U16":
                n0 = num_array[pixel + 0] # Cyan
                n1 = num_array[pixel + 1] # Magenta
                n2 = num_array[pixel + 2] # Yellow
                n3 = num_array[pixel + 3] # Key
                n4 = num_array[pixel + 4] # Alpha
            if d_cd == "F32":
                pass
            byte_list = [n0, n1, n2, n3, n4]
        elif d_cm == "YUV":
            pixel = index * 4
            if d_cd == "U8":
                n0 = num_array[pixel + 0] # Luma
                n1 = num_array[pixel + 1] # Cb
                n2 = num_array[pixel + 2] # Cr
                n3 = num_array[pixel + 3] # Alpha
            if d_cd == "U16":
                n0 = num_array[pixel + 0] # Luma
                n1 = num_array[pixel + 1] # Cb
                n2 = num_array[pixel + 2] # Cr
                n3 = num_array[pixel + 3] # Alpha
            if d_cd == "F32":
                pass
            byte_list = [n0, n1, n2, n3]
        elif d_cm == "XYZ":
            pixel = index * 4
            if d_cd == "U8":
                n0 = num_array[pixel + 0] # X
                n1 = num_array[pixel + 1] # Y
                n2 = num_array[pixel + 2] # Z
                n3 = num_array[pixel + 3] # Alpha
            if d_cd == "U16":
                n0 = num_array[pixel + 0] # X
                n1 = num_array[pixel + 1] # Y
                n2 = num_array[pixel + 2] # Z
                n3 = num_array[pixel + 3] # Alpha
            if d_cd == "F16":
                pass
            if d_cd == "F32":
                pass
            byte_list = [n0, n1, n2, n3]
        elif d_cm == "LAB":
            pixel = index * 4
            if d_cd == "U8":
                n0 = num_array[pixel + 0] # Lightness*
                n1 = num_array[pixel + 1] # A*
                n2 = num_array[pixel + 2] # 1*
                n3 = num_array[pixel + 3] # Alpha
            if d_cd == "U16":
                n0 = num_array[pixel + 0] # Lightness*
                n1 = num_array[pixel + 1] # A*
                n2 = num_array[pixel + 2] # 1*
                n3 = num_array[pixel + 3] # Alpha
            if d_cd == "F32":
                pass
            byte_list = [n0, n1, n2, n3]
        return byte_list
    # Total Ink Coverage
    def Total_Ink_Coverage( self, invert, tic, limit, c0, c1, c2, bw, cor ):
        p = tic - limit
        if ( invert == False and tic > limit ):
            value = p / ( 400 - limit )
            cor = True
            t0 = c0
            t1 = c1
            t2 = c2
            tw = value
        elif ( invert == True and tic < limit ):
            value = p / ( 0 - limit )
            cor = True
            t0 = c0
            t1 = c1
            t2 = c2
            tw = value
        else:
            t0 = bw
            t1 = bw
            t2 = bw
            tw = 0
        return t0, t1, t2, tw, cor

    #endregion
    #region Selector

    def Selector_Linear( self, num, pa, pb, pc, pd ):
        # Intervals
        int_bc = num >= pb and num <= pc
        int_ab = num >= pa and num <  pb
        int_cd = num <= pd and num >  pc
        # Logic
        if int_bc == True:
            select = 1
        elif int_ab == True:
            dt = abs( pb - pa )
            da = abs( num - pa )
            if da > 0: select = da / dt
            else:      select = 0
        elif int_cd == True:
            dt = abs( pc - pd )
            db = abs( num - pd )
            if db > 0: select = db / dt
            else:      select = 0
        else:
            select = 0
        # Return
        return select
    def Selector_Circular( self, num, pa, pb, pc, pd ):
        # Points
        pan = pa
        if pb < pan:    pbn = pb + 1
        else:           pbn = pb
        if pc < pbn:    pcn = pc + 1
        else:           pcn = pc
        if pd < pcn:    pdn = pd + 1
        else:           pdn = pd

        pal = pan - 1
        pbl = pbn - 1
        pcl = pcn - 1
        pdl = pdn - 1

        # Intervals
        int_bc_n = pbn <= num <= pcn
        int_ab_n = pan <= num <  pbn
        int_cd_n = pcn <  num <= pdn

        int_bc_l = pbl <= num <= pcl
        int_ab_l = pal <= num <  pbl
        int_cd_l = pcl <  num <= pdl

        # Logic
        if pa == pb == pc == pd:
            select = 1
        elif ( int_bc_n == True or int_bc_l == True ):
            select = 1
        elif ( int_ab_n == True or int_ab_l == True ):
            if int_ab_n == True:
                dt = abs( pbn - pan )
                da = abs( num - pan )
                if da > 0: select = da / dt
                else:      select = 0
            if int_ab_l == True:
                dt = abs( pbl - pal )
                da = abs( num - pal )
                if da > 0: select = da / dt
                else:      select = 0
        elif ( int_cd_n == True or int_cd_l == True ):
            if int_cd_n == True:
                dt = abs( pcn - pdn )
                db = abs( num - pdn )
                if db > 0: select = db / dt
                else:      select = 0
            if int_cd_l == True:
                dt = abs( pcl - pdl )
                db = abs( num - pdl )
                if db > 0: select = db / dt
                else:      select = 0
        else:
            select = 0

        # Return
        return select

    #endregion


"""
class Colour():

    #region RGB LINEAR

    # AAA
    def rgb_to_aaa( self, r, g, b ):
        aaa = ( self.luma_r * r ) + ( self.luma_g * g ) + ( self.luma_b * b )
        return [aaa]
    def aaa_to_rgb( self, a ):
        r = a
        g = a
        b = a
        return [r, g, b]

    # RGB
    def srgb_to_lrgb( self, sr, sg, sb ):
        n0 = 0.055
        n1 = 1 + n0
        m = 12.92
        value = 0.04045
        if sr <= value: lr = sr / m
        else:           lr = ( ( sr + n0  ) / n1 ) ** gamma_l
        if sg <= value: lg = sg / m
        else:           lg = ( ( sg + n0  ) / n1 ) ** gamma_l
        if sb <= value: lb = sb / m
        else:           lb = ( ( sb + n0  ) / n1 ) ** gamma_l
        return [lr, lg, lb]
    def lrgb_to_srgb( self, lr, lg, lb ):
        n0 = 0.055
        n1 = 1 + n0
        m = 12.92
        value = 0.0031308
        if lr <= value: sr = lr * m
        else:           sr = n1 * lr ** ( 1 / gamma_l  ) - n0
        if lg <= value: sg = lg * m
        else:           sg = n1 * lg ** ( 1 / gamma_l  ) - n0
        if lb <= value: sb = lb * m
        else:           sb = n1 * lb ** ( 1 / gamma_l  ) - n0
        return [sr, sg, sb]
    # UVD
    def rgb_to_uvd( self, r, g, b ):
        # uv range from -1 to +1 ( 0.8 with mask )
        m00 = -0.866025808; m01 = +0.866025808; m02 = -0.0000000000000000961481791
        m10 = +0.500000010; m11 = +0.499999990; m12 = -1.00000000
        m20 = +0.333333497; m21 = +0.333333503; m22 = +0.333333000
        # MatrixInverse * RGB
        u = m00 * r + m01 * g + m02 * b
        v = m10 * r + m11 * g + m12 * b
        d = m20 * r + m21 * g + m22 * b
        m = 0.0000001
        u = self.geometry.Limit_Error( u, m )
        v = self.geometry.Limit_Error( v, m )
        return [u, v, d]
    def uvd_to_rgb( self, u, v, d ):
        m00 = -0.57735;         m01 = +0.333333; m02 = +1
        m10 = +0.57735;         m11 = +0.333333; m12 = +1
        m20 = -0.0000000113021; m21 = -0.666667; m22 = +1
        # Matrix * UVD
        r = m00 * u + m01 * v + m02 * d
        g = m10 * u + m11 * v + m12 * d
        b = m20 * u + m21 * v + m22 * d
        # Correct out of Bound values
        r, g, b = self.Vector_Safe( r, g, b )
        return [r, g, b]

    # CMY
    def rgb_to_cmy( self, r, g, b ):
        c = 1 - r
        m = 1 - g
        y = 1 - b
        return [c, m, y]
    def cmy_to_rgb( self, c, m, y ):
        r = 1 - c
        g = 1 - m
        b = 1 - y
        return [r, g, b]

    # CMYK
    def rgb_to_cmyk( self, r, g, b, key ):
        # key = black from cmyk or key ( if key is None formula is regular )
        q = max( r, g, b )
        if q == 0:
            if key == None:
                c = 0
                m = 0
                y = 0
                k = 1
            else:
                c = 1
                m = 1
                y = 1
                k = key
        else:
            if key == None:
                k = 1 - max( r, g, b ) # Standard Transform
            else:
                k = key # Key is Locked
            ik = 1 - k
            if ik == 0 :
                c = ( r - k  ) / ( k  )
                m = ( g - k  ) / ( k  )
                y = ( b - k  ) / ( k  )
            else:
                c = ( 1 - r - k  ) / ( 1 - k  )
                m = ( 1 - g - k  ) / ( 1 - k  )
                y = ( 1 - b - k  ) / ( 1 - k  )
        return [c, m, y, k]
    def cmyk_to_rgb( self, c, m, y, k ):
        r = ( 1 - c  ) * ( 1 - k  )
        g = ( 1 - m  ) * ( 1 - k  )
        b = ( 1 - y  ) * ( 1 - k  )
        r, g, b = self.Vector_Safe( r, g, b )
        return [r, g, b]
    def rgb_to_k( self, r, g, b ):
        q = max( r, g, b )
        if q == 0:
            k = 1
        else:
            k = 1 - max( r, g, b )
        return k
    def cmyk_to_tic( self, c, m, y, k):
        tic = round( ( c + m + y + k ) * 100 )
        return tic

    # RYB
    def rgb_to_ryb( self, r, g, b ):
        red = r
        green = g
        blue = b
        white  = min( red, green, blue )
        red -= white
        green -= white
        blue -= white
        maxgreen = max( red, green, blue )
        yellow = min( red, green )
        red -= yellow
        green -= yellow
        if ( blue > 0 and green > 0 ):
            blue /= 2
            green /= 2
        yellow += green
        blue += green
        maxyellow = max( red, yellow, blue )
        if maxyellow > 0:
            N = maxgreen / maxyellow
            red *= N
            yellow *= N
            blue *= N
        red += white
        yellow += white
        blue += white
        return [red, yellow, blue]
    def ryb_to_rgb( self, r, y, b ):
        red = r
        yellow = y
        blue = b
        white = min( red, yellow, blue )
        red -= white
        yellow -= white
        blue -= white
        maxyellow = max( red, yellow, blue )
        green = min( yellow, blue )
        yellow -= green
        blue -= green
        if ( blue > 0 and green > 0 ):
            blue *= 2
            green *= 2
        red += yellow
        green += yellow
        maxgreen = max( red, green, blue )
        if maxgreen > 0:
            N = maxyellow / maxgreen
            red *= N
            green *= N
            blue *= N
        red += white
        green += white
        blue += white
        return [red, green, blue]

    # YUV
    def rgb_to_yuv( self, r, g, b ):
        y = self.List_Mult_3( [ self.luma_r                                      , self.luma_g                                      , self.luma_b                                      ], [ r, g, b ] )
        u = self.List_Mult_3( [ -0.5 * ( ( self.luma_r ) / ( 1 - self.luma_b ) ) , -0.5 * ( ( self.luma_g ) / ( 1 - self.luma_b ) ) , +0.5                                             ], [ r, g, b ] )
        v = self.List_Mult_3( [ +0.5                                             , -0.5 * ( ( self.luma_g ) / ( 1 - self.luma_r ) ) , -0.5 * ( ( self.luma_b ) / ( 1 - self.luma_r ) ) ], [ r, g, b ] )
        y, u, v = self.Vector_Safe( y, 0.5 + u, 0.5 + v )
        return [ y, u, v ]
    def yuv_to_rgb( self, y, u, v ):
        u -= 0.5
        v -= 0.5
        if self.luminosity == "ITU-R BT.2020":
            r = self.List_Mult_3( [ +1 , +0                , +1.4746           ], [ y, u, v ] )
            g = self.List_Mult_3( [ +1 , -0.16455312684366 , -0.57135312684366 ], [ y, u, v ] )
            b = self.List_Mult_3( [ +1 , +1.8814           , +0                ], [ y, u, v ] )
        else:
            r = self.List_Mult_3( [ +1 , +0                                                       , 2 - 2 * self.luma_r                                      ], [ y, u, v ] )
            g = self.List_Mult_3( [ +1 , -( self.luma_b / self.luma_g ) * ( 2 - 2 * self.luma_b ) , -( self.luma_r / self.luma_g ) * ( 2 - 2 * self.luma_r ) ], [ y, u, v ] )
            b = self.List_Mult_3( [ +1 , +2 - 2 * self.luma_b                                     , 0                                                        ], [ y, u, v ] )
        r, g, b = self.Vector_Safe( r, g, b )
        return [r,g,b]

    #endregion
    #region RGB HUE

    # HUE RGB
    def rgb_to_hue( self, r, g, b ):
        # In case Krita is in Linear Format
        if self.d_cd != "U8":
            lsl = self.lrgb_to_srgb( r, g, b )
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]

        # sRGB to HSX
        v_min = min( r, g, b  )
        v_max = max( r, g, b  )
        d_max = v_max - v_min
        if d_max == 0:
            h = self.hue
        else:
            d_r = ( ( ( v_max - r  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_g = ( ( ( v_max - g  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_b = ( ( ( v_max - b  ) / 6  ) + ( d_max / 2  )  ) / d_max
            if r == v_max :
                h = d_b - d_g
            elif g == v_max :
                h = ( 1 / 3  ) + d_r - d_b
            elif b == v_max :
                h = ( 2 / 3  ) + d_g - d_r
            h = self.geometry.Limit_Looper( h, 1 )
        return h
    def hue_to_rgb( self, h ):
        vh = h * 6
        if vh == 6 :
            vh = 0
        vi = int( vh  )
        v2 = 1 * ( 1 - 1 * ( vh - vi  )  )
        v3 = 1 * ( 1 - 1 * ( 1 - ( vh - vi  )  )  )
        if vi == 0 :
            r = 1
            g = v3
            b = 0
        elif vi == 1 :
            r = v2
            g = 1
            b = 0
        elif vi == 2 :
            r = 0
            g = 1
            b = v3
        elif vi == 3 :
            r = 0
            g = v2
            b = 1
        elif vi == 4 :
            r = v3
            g = 0
            b = 1
        else:
            r = 1
            g = 0
            b = v2

        # In case Krita is in Linear Format
        if self.d_cd != "U8":
            lsl = self.srgb_to_lrgb( r, g, b )
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        return [r, g, b]
    # HUE Digital-Analog or RGB-RYB
    def hue_to_hue( self, mode, angle ):
        if mode == "DIGITAL":
            hue_d = angle
            hue_a = self.hued_to_huea( angle )
        if mode == "ANALOG":
            hue_d = self.huea_to_hued( angle )
            hue_a = angle
        return hue_d, hue_a
    def hued_to_huea( self, hued ):
        # convertion
        hued = self.geometry.Limit_Looper( hued, 1 )
        for i in range( len( digital_step ) ):
            if hued == digital_step[i]:
                huea = analog_step[i]
        for i in range( len( digital_step )-1 ):
            if ( hued > digital_step[i] and hued < digital_step[i+1] ):
                var = ( hued - digital_step[i] ) / ( digital_step[i+1] - digital_step[i] )
                huea = ( analog_step[i] + ( analog_step[i+1] - analog_step[i] ) * var  )
        return huea
    def huea_to_hued( self, huea ):
        # convertion
        hued = self.geometry.Limit_Looper( huea, 1 )
        for i in range( len( analog_step ) ):
            if huea == analog_step[i]:
                hued = digital_step[i]
        for i in range( len( analog_step )-1 ):
            if ( huea > analog_step[i] and huea < analog_step[i+1] ):
                var = ( huea - analog_step[i] ) / ( analog_step[i+1] - analog_step[i] )
                hued = ( digital_step[i] + ( digital_step[i+1] - digital_step[i] ) * var  )
        return hued
    # Hue YUV
    def uv_to_hue( self, y, u, v, angle ):
        rgb = self.yuv_to_rgb( y, u, v )
        hcy = self.rgb_to_hcy( rgb[0], rgb[1], rgb[2] )
        nrgb = self.hcy_to_rgb( angle, hcy[1], hcy[2] )
        nyuv = self.rgb_to_yuv( nrgb[0], nrgb[1], nrgb[2] )
        ny = y
        nu = nyuv[1]
        nv = nyuv[2]
        return ny, nu, nv

    # HSV
    def rgb_to_hsv( self, r, g, b ):
        # sRGB to HSX
        v_min = min( r, g, b  )
        v_max = max( r, g, b  )
        d_max = v_max - v_min
        v = v_max
        if d_max == 0:
            h = self.hue
            s = 0
        else:
            s = d_max / v_max
            d_r = ( ( ( v_max - r  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_g = ( ( ( v_max - g  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_b = ( ( ( v_max - b  ) / 6  ) + ( d_max / 2  )  ) / d_max
            if r == v_max :
                h = d_b - d_g
            elif g == v_max :
                h = ( 1 / 3  ) + d_r - d_b
            elif b == v_max :
                h = ( 2 / 3  ) + d_g - d_r
            if h < 0 :
                h += 1
            if h > 1 :
                h -= 1
        return [h, s, v]
    def hsv_to_rgb( self, h, s, v ):
        # HSX to sRGB
        if s == 0:
            r = v
            g = v
            b = v
        else:
            vh = h * 6
            if vh == 6 :
                vh = 0
            vi = int( vh  )
            v1 = v * ( 1 - s  )
            v2 = v * ( 1 - s * ( vh - vi  )  )
            v3 = v * ( 1 - s * ( 1 - ( vh - vi  )  )  )
            if vi == 0 :
                r = v
                g = v3
                b = v1
            elif vi == 1 :
                r = v2
                g = v
                b = v1
            elif vi == 2 :
                r = v1
                g = v
                b = v3
            elif vi == 3 :
                r = v1
                g = v2
                b = v
            elif vi == 4 :
                r = v3
                g = v1
                b = v
            else:
                r = v
                g = v1
                b = v2

        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.srgb_to_lrgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]
        return [r, g, b]
    # HSL
    def rgb_to_hsl( self, r, g, b ):
        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.lrgb_to_srgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]

        # sRGB to HSX
        v_min = min( r, g, b  )
        v_max = max( r, g, b  )
        d_max = v_max - v_min
        l = ( v_max + v_min  )/ 2
        if d_max == 0 :
            h = self.hue
            s = 0
        else:
            if l < 0.5 :
                s = d_max / ( v_max + v_min  )
            else:
                s = d_max / ( 2 - v_max - v_min  )
            d_r = ( ( ( v_max - r  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_g = ( ( ( v_max - g  ) / 6  ) + ( d_max / 2  )  ) / d_max
            d_b = ( ( ( v_max - b  ) / 6  ) + ( d_max / 2  )  ) / d_max
            if r == v_max :
                h = d_b - d_g
            elif g == v_max:
                h = ( 1 / 3  ) + d_r - d_b
            elif b == v_max:
                h = ( 2 / 3  ) + d_g - d_r
            if h < 0:
                h += 1
            if h > 1:
                h -= 1
        return [h, s, l]
    def hsl_to_rgb( self, h, s, l ):
        if s == 0 :
            r = l
            g = l
            b = l
        else:
            if l < 0.5:
                v2 = l * ( 1 + s  )
            else:
                v2 = ( l + s  ) - ( s * l  )
            v1 = 2 * l - v2
            r = self.hsl_chan( v1, v2, h + ( 1 / 3  )  )
            g = self.hsl_chan( v1, v2, h  )
            b = self.hsl_chan( v1, v2, h - ( 1 / 3  )  )

        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.srgb_to_lrgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]
        return [r, g, b]
    def hsl_chan( self, v1, v2, vh ):
        if vh < 0 :
            vh += 1
        if vh > 1 :
            vh -= 1
        if ( 6 * vh  ) < 1 :
            return ( v1 + ( v2 - v1  ) * 6 * vh  )
        if ( 2 * vh  ) < 1 :
            return ( v2  )
        if ( 3 * vh  ) < 2 :
            return ( v1 + ( v2 - v1  ) * ( ( 2 / 3  ) - vh  ) * 6  )
        return ( v1  )
    # HSY ( Krita version )
    def rgb_to_hsy( self, r, g, b ):
        # In case Krita is NOT in Linear Format
        # if self.d_cd == "U8":
        #     lsl = self.srgb_to_lrgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]

        # sRGB to HSX
        minval = min( r, g, b )
        maxval = max( r, g, b )
        luma = ( self.luma_r * r + self.luma_g * g + self.luma_b * b )
        luma_a = luma
        chroma = maxval - minval
        max_sat = 0.5
        if chroma == 0:
            hue = self.hue
            sat = 0
        else:
            if maxval == r:
                if minval == b:
                    hue = ( g - b ) / chroma
                else:
                    hue = ( g - b ) / chroma + 6
            elif maxval == g:
                hue = ( b - r ) / chroma + 2
            elif maxval == b:
                hue = ( r - g ) / chroma + 4
            hue /= 6
            # segment = 0.166667
            segment = 1 / 6
            if ( hue > 1 or hue < 0 ):
                hue = math.fmod( hue, 1 )
            if ( hue >= 0 * segment and hue < 1 * segment ):
                max_sat = self.luma_r + self.luma_g * ( hue * 6 )
            elif ( hue >= 1 * segment and hue < 2 * segment ):
                max_sat = ( self.luma_g + self.luma_r ) - self.luma_r * ( ( hue - segment ) * 6 )
            elif ( hue >= 2 * segment and hue < 3 * segment ):
                max_sat = self.luma_g + self.luma_b * ( ( hue - 2 * segment ) * 6 )
            elif ( hue >= 3 * segment and hue < 4 * segment ):
                max_sat = ( self.luma_b + self.luma_g ) - self.luma_g * ( ( hue - 3 * segment ) * 6 )
            elif ( hue >= 4 * segment and hue < 5 * segment ):
                max_sat =  ( self.luma_b ) + self.luma_r * ( ( hue - 4 * segment ) * 6 )
            elif ( hue >= 5 * segment and hue <= 1 ):
                max_sat = ( self.luma_r + self.luma_b ) - self.luma_b * ( ( hue - 5 * segment ) * 6 )
            else:
                max_sat = 0.5

            if( max_sat > 1 or max_sat < 0 ):
                max_sat = math.fmod( max_sat, 1 )

            if luma <= max_sat:
                luma_a = ( luma / max_sat ) * 0.5
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5

            if ( chroma > 0 ):
                sat = ( ( chroma / ( 2 * luma_a ) ) if ( luma <= max_sat ) else ( chroma / ( 2 - ( 2 * luma_a ) ) ) )
        if sat <= 0:
            sat = 0
        if luma <= 0:
            luma = 0
        h = hue
        s = sat
        y = luma ** ( 1 / self.gamma_y )
        return [h, s, y]
    def hsy_to_rgb( self, h, s, y ):
        hue = 0
        sat = 0
        luma = 0
        if ( h > 1 or h < 0 ):
            hue = math.fmod( h, 1 )
        else:
            hue = h
        if s < 0:
            sat = 0
        else:
            sat = s
        if y < 0:
            luma = 0
        else:
            luma = y ** ( self.gamma_y )
        # segment = 0.166667
        segment = 1 / 6
        r = 0
        g = 0
        b = 0
        if ( hue >= 0 and hue < segment ):
            max_sat = self.luma_r + ( self.luma_g * ( hue * 6 )  )
            if luma <= max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * 2 * luma_a
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 ) ) * chroma
            r = chroma
            g = x
            b = 0
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        elif ( hue >= ( segment ) and hue < 2 * segment ):
            max_sat = ( self.luma_g + self.luma_r ) - ( self.luma_r * ( hue - segment ) * 6 )
            if luma < max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * ( 2 * luma_a )
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 )  ) * chroma
            r = x
            g = chroma
            b = 0
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        elif ( hue >= 2 * segment and hue < 3 * segment ):
            max_sat = self.luma_g + ( self.luma_b * ( hue - 2 * segment ) * 6 )
            if luma < max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * ( 2 * luma_a )
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 ) ) * chroma
            r = 0
            g = chroma
            b = x
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        elif ( hue >= 3 * segment and hue < 4 * segment ):
            max_sat = ( self.luma_g + self.luma_b ) - ( self.luma_g * ( hue - 3 * segment ) * 6 )
            if luma < max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * ( 2 * luma_a )
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 ) ) * chroma
            r = 0
            g = x
            b = chroma
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        elif ( hue >= 4 * segment and hue < 5 * segment ):
            max_sat = self.luma_b + ( self.luma_r * ( ( hue - 4 * segment ) * 6 ) )
            if luma < max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * ( 2 * luma_a )
            else:
                luma_a = ( ( luma-max_sat ) / ( 1 - max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 ) ) * chroma
            r = x
            g = 0
            b = chroma
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        elif ( hue >= 5 * segment and hue <= 1 ):
            max_sat = ( self.luma_b + self.luma_r ) - ( self.luma_b * ( hue - 5 * segment ) * 6 )
            if luma < max_sat:
                luma_a = ( luma / max_sat ) * 0.5
                chroma = sat * ( 2 * luma_a )
            else:
                luma_a = ( ( luma-max_sat ) / ( 1-max_sat ) * 0.5 ) + 0.5
                chroma = sat * ( 2 - 2 * luma_a )
            fract = hue * 6
            x = ( 1 - abs( math.fmod( fract, 2 ) - 1 ) ) * chroma
            r = chroma
            g = 0
            b = x
            m = luma - ( ( self.luma_r * r ) + ( self.luma_b * b ) + ( self.luma_g * g ) )
            r += m
            g += m
            b += m
        else:
            r = 0
            g = 0
            b = 0
        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0

        # In case Krita is NOT in Linear Format
        # if self.d_cd == "U8":
        #     lsl = self.lrgb_to_srgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]
        return [r, g, b]
    # HCY ( My Paint Version )
    def rgb_to_hcy( self, r, g, b ):
        # In case Krita is NOT in Linear Format
        # if self.d_cd != "U8": # == vs !=
        #     lsl = self.srgb_to_lrgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]

        # sRGB to HSX
        y = self.luma_r * r + self.luma_g * g + self.luma_b * b
        p = max( r, g, b )
        n = min( r, g, b )
        d = p - n
        if n == p:
            h = self.hue
        elif p == r:
            h = ( g - b ) / d
            if h < 0:
                h += 6.0
        elif p == g:
            h = ( ( b - r ) / d ) + 2.0
        elif p == b:
            h = ( ( r - g ) / d ) + 4.0
        h /= 6.0
        if ( r == g == b or y == 0 or y == 1 ):
            h = self.hue
            c = 0.0
        else:
            c = max( ( y-n ) / y, ( p - y ) / ( 1 - y ) )
        if self.d_cd != "U8": # == vs !=
            y = y**( 1 / self.gamma_y ) # Gama compression of the luma value
        return [h, c, y]
    def hcy_to_rgb( self, h, c, y ):
        if self.d_cd != "U8": # == vs !=
            y = y**( self.gamma_y ) # Gama compression of the luma value
        if c == 0:
            r = y
            g = y
            b = y
        h %= 1.0
        h *= 6.0
        if h < 1:
            th = h
            tm = self.luma_r + self.luma_g * th
        elif h < 2:
            th = 2.0 - h
            tm = self.luma_g + self.luma_r * th
        elif h < 3:
            th = h - 2.0
            tm = self.luma_g + self.luma_b * th
        elif h < 4:
            th = 4.0 - h
            tm = self.luma_b + self.luma_g * th
        elif h < 5:
            th = h - 4.0
            tm = self.luma_b + self.luma_r * th
        else:
            th = 6.0 - h
            tm = self.luma_r + self.luma_b * th
        # Calculate the RGB components in sorted order
        if tm >= y:
            p = y + y * c * ( 1 - tm ) / tm
            o = y + y * c * ( th - tm ) / tm
            n = y - ( y * c )
        else:
            p = y + ( 1 - y ) * c
            o = y + ( 1 - y ) * c * ( th - tm ) / ( 1 - tm )
            n = y - ( 1 - y ) * c * tm / ( 1 - tm )
        # Back to RGB order
        if h < 1:
            r = p
            g = o
            b = n
        elif h < 2:
            r = o
            g = p
            b = n
        elif h < 3:
            r = n
            g = p
            b = o
        elif h < 4:
            r = n
            g = o
            b = p
        elif h < 5:
            r = o
            g = n
            b = p
        else:
            r = p
            g = n
            b = o

        # In case Krita is NOT in Linear Format
        # if self.d_cd != "U8": # == vs !=
        #     lsl = self.lrgb_to_srgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]
        return [r, g, b]

    # ARD
    def rgb_to_ard( self, r, g, b ):
        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.lrgb_to_srgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]

        # Depth
        uvd = self.rgb_to_uvd( r, g, b )
        u = uvd[0]
        v = uvd[1]
        d = uvd[2]
        # Hexagon Depth
        di = d * 3
        if ( di == 0 or di == 1 ):
            a = self.hue
            r = 0
        else:
            # Angle
            a = self.rgb_to_hue( r, g, b )
            # Channel
            O1, O2, O3, O4, O5, O6, C12, C23, C34, C45, C56, C61 = self.uvd_hexagon( d, 1, 0, 1 )
            c = self.ard_channel( d, a, O1, O2, O3, O4, O5, O6, C12, C23, C34, C45, C56, C61 )

            # Ratio
            if ( r == g and g == b and b == r ):
                r = 0
            elif ( r == 0 or g == 0 or b == 0 or r == 1 or g == 1 or b == 1 ):
                r = 1
            else:
                # Neutral Value
                n = ( r + g + b ) / 3 # Ratio = 0
                # Delta
                dr = r - n
                dg = g - n
                db = b - n
                # Ratio Distance
                if c == +1:r = dr / ( 1 - n )
                if c == -1:r = dr / -n
                if c == +2:r = dg / ( 1 - n )
                if c == -2:r = dg / -n
                if c == +3:r = db / ( 1 - n )
                if c == -3:r = db / -n
        # Return
        return [ a, r, d ]
    def ard_to_rgb( self, a, r, d ):
        # Channel
        di = d * 3
        lu = 0
        lv = 0
        if di <= 0:
            r = 0
            g = 0
            b = 0
        elif di >= 3:
            r = 1
            g = 1
            b = 1
        else:
            # Hexagon
            O1, O2, O3, O4, O5, O6, C12, C23, C34, C45, C56, C61 = self.uvd_hexagon( d, 1, 0, 1 )

            # Angle
            hrgb = self.hue_to_rgb( a )
            huvd = self.rgb_to_uvd( hrgb[0], hrgb[1], hrgb[2] )
            acc = self.geometry.Trig_2D_Points_Lines_Angle( huvd[0], huvd[1], 0, 0, C61[0], C61[1] ) / 360

            # Angle
            a01 = self.geometry.Trig_2D_Points_Lines_Angle( O1[0], O1[1], 0, 0, C61[0], C61[1] ) / 360
            a02 = self.geometry.Trig_2D_Points_Lines_Angle( O2[0], O2[1], 0, 0, C61[0], C61[1] ) / 360
            a03 = self.geometry.Trig_2D_Points_Lines_Angle( O3[0], O3[1], 0, 0, C61[0], C61[1] ) / 360
            a04 = self.geometry.Trig_2D_Points_Lines_Angle( O4[0], O4[1], 0, 0, C61[0], C61[1] ) / 360
            a05 = self.geometry.Trig_2D_Points_Lines_Angle( O5[0], O5[1], 0, 0, C61[0], C61[1] ) / 360
            a06 = self.geometry.Trig_2D_Points_Lines_Angle( O6[0], O6[1], 0, 0, C61[0], C61[1] ) / 360
            a12 = self.geometry.Trig_2D_Points_Lines_Angle( C12[0], C12[1], 0, 0, C61[0], C61[1] ) / 360
            a23 = self.geometry.Trig_2D_Points_Lines_Angle( C23[0], C23[1], 0, 0, C61[0], C61[1] ) / 360
            a34 = self.geometry.Trig_2D_Points_Lines_Angle( C34[0], C34[1], 0, 0, C61[0], C61[1] ) / 360
            a45 = self.geometry.Trig_2D_Points_Lines_Angle( C45[0], C45[1], 0, 0, C61[0], C61[1] ) / 360
            a56 = self.geometry.Trig_2D_Points_Lines_Angle( C56[0], C56[1], 0, 0, C61[0], C61[1] ) / 360

            # Depth
            if ( di > 0 and di <= 1):
                if ( acc <= a23 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C61[0], C61[1], C23[0], C23[1] )
                elif ( acc > a23 and acc <= a45 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C23[0], C23[1], C45[0], C45[1] )
                else:
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C45[0], C45[1], C61[0], C61[1] )
            elif ( di > 1 and di < 2):
                if ( acc <= a01 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C61[0], C61[1], O1[0], O1[1] )
                elif ( acc > a01 and acc <= a02 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O1[0], O1[1], O2[0], O2[1] )
                elif ( acc > a02 and acc <= a03 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O2[0], O2[1], O3[0], O3[1] )
                elif ( acc > a03 and acc <= a04 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O3[0], O3[1], O4[0], O4[1] )
                elif ( acc > a04 and acc <= a05 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O4[0], O4[1], O5[0], O5[1] )
                elif ( acc > a05 and acc <= a06 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O5[0], O5[1], O6[0], O6[1] )
                else:
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, O6[0], O6[1], C61[0], C61[1] )
            elif ( di >= 2 and di < 3):
                if ( acc <= a12 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C61[0], C61[1], C12[0], C12[1] )
                elif ( acc > a12 and acc <= a34 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C12[0], C12[1], C34[0], C34[1] )
                elif ( acc > a34 and acc <= a56 ):
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C34[0], C34[1], C56[0], C56[1] )
                else:
                    lu, lv = self.geometry.Trig_2D_Points_Lines_Intersection( huvd[0], huvd[1], 0, 0, C56[0], C56[1], C61[0], C61[1] )
            # UVD Interpolation
            uvd = self.geometry.Lerp_3D( r, 0, 0, d, lu, lv, d )
            rgb = self.uvd_to_rgb( uvd[0], uvd[1], uvd[2] )
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]

        # In case Krita is in Linear Format
        # if self.d_cd != "U8":
        #     lsl = self.srgb_to_lrgb( r, g, b )
        #     r = lsl[0]
        #     g = lsl[1]
        #     b = lsl[2]
        return [r, g, b]
    def uvd_hexagon( self, d, s, o, i ):
        # s = scale
        # o = offset center
        # i = invert Y axis ( panel is inverted )

        # Primaries
        cn = [ 0, 0 ]
        cr = self.rgb_to_uvd( 1, 0, 0 )
        cy = self.rgb_to_uvd( 1, 1, 0 )
        cg = self.rgb_to_uvd( 0, 1, 0 )
        cc = self.rgb_to_uvd( 0, 1, 1 )
        cb = self.rgb_to_uvd( 0, 0, 1 )
        cm = self.rgb_to_uvd( 1, 0, 1 )
        # Single Points
        di = d * 3
        u0 = 0
        u1 = 1
        u2 = 2
        u3 = 3
        if ( di <= u0 or di >= u3 ):
            # Original
            O1 = [ o, o ]
            O2 = [ o, o ]
            O3 = [ o, o ]
            O4 = [ o, o ]
            O5 = [ o, o ]
            O6 = [ o, o ]
            # Complementary
            C12 = [ o, o ]
            C23 = [ o, o ]
            C34 = [ o, o ]
            C45 = [ o, o ]
            C56 = [ o, o ]
            C61 = [ o, o ]
        else:
            # Original
            if ( di >= u0 and di <= u1):
                p = di
                o1_u, o1_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cr[0], cr[1] )
                o2_u, o2_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cg[0], cg[1] )
                o3_u, o3_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cg[0], cg[1] )
                o4_u, o4_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cb[0], cb[1] )
                o5_u, o5_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cb[0], cb[1] )
                o6_u, o6_v = self.geometry.Lerp_2D( p, cn[0], cn[1], cr[0], cr[1] )
            elif ( di > u1 and di < u2):
                p = di - 1
                o1_u, o1_v = self.geometry.Lerp_2D( p, cr[0], cr[1], cy[0], cy[1] )
                o2_u, o2_v = self.geometry.Lerp_2D( p, cg[0], cg[1], cy[0], cy[1] )
                o3_u, o3_v = self.geometry.Lerp_2D( p, cg[0], cg[1], cc[0], cc[1] )
                o4_u, o4_v = self.geometry.Lerp_2D( p, cb[0], cb[1], cc[0], cc[1] )
                o5_u, o5_v = self.geometry.Lerp_2D( p, cb[0], cb[1], cm[0], cm[1] )
                o6_u, o6_v = self.geometry.Lerp_2D( p, cr[0], cr[1], cm[0], cm[1] )
            elif ( di >= u2 and di <= u3):
                p = di - 2
                o1_u, o1_v = self.geometry.Lerp_2D( p, cy[0], cy[1], cn[0], cn[1] )
                o2_u, o2_v = self.geometry.Lerp_2D( p, cy[0], cy[1], cn[0], cn[1] )
                o3_u, o3_v = self.geometry.Lerp_2D( p, cc[0], cc[1], cn[0], cn[1] )
                o4_u, o4_v = self.geometry.Lerp_2D( p, cc[0], cc[1], cn[0], cn[1] )
                o5_u, o5_v = self.geometry.Lerp_2D( p, cm[0], cm[1], cn[0], cn[1] )
                o6_u, o6_v = self.geometry.Lerp_2D( p, cm[0], cm[1], cn[0], cn[1] )
            # Original
            O1 = [ o1_u * s + o, i * o1_v * s + o ]
            O2 = [ o2_u * s + o, i * o2_v * s + o ]
            O3 = [ o3_u * s + o, i * o3_v * s + o ]
            O4 = [ o4_u * s + o, i * o4_v * s + o ]
            O5 = [ o5_u * s + o, i * o5_v * s + o ]
            O6 = [ o6_u * s + o, i * o6_v * s + o ]
            # Complemtary
            C12 = self.geometry.Lerp_2D( 0.5, O1[0], O1[1], O2[0], O2[1] )
            C23 = self.geometry.Lerp_2D( 0.5, O2[0], O2[1], O3[0], O3[1] )
            C34 = self.geometry.Lerp_2D( 0.5, O3[0], O3[1], O4[0], O4[1] )
            C45 = self.geometry.Lerp_2D( 0.5, O4[0], O4[1], O5[0], O5[1] )
            C56 = self.geometry.Lerp_2D( 0.5, O5[0], O5[1], O6[0], O6[1] )
            C61 = self.geometry.Lerp_2D( 0.5, O6[0], O6[1], O1[0], O1[1] ) # Red Hue=0

        # Return
        return O1, O2, O3, O4, O5, O6, C12, C23, C34, C45, C56, C61
    def ard_channel( self, d, a, O1, O2, O3, O4, O5, O6, C12, C23, C34, C45, C56, C61 ):
        # Angle
        a01 = self.geometry.Trig_2D_Points_Lines_Angle( O1[0], O1[1], 0, 0, C61[0], C61[1] ) / 360
        a02 = self.geometry.Trig_2D_Points_Lines_Angle( O2[0], O2[1], 0, 0, C61[0], C61[1] ) / 360
        a03 = self.geometry.Trig_2D_Points_Lines_Angle( O3[0], O3[1], 0, 0, C61[0], C61[1] ) / 360
        a04 = self.geometry.Trig_2D_Points_Lines_Angle( O4[0], O4[1], 0, 0, C61[0], C61[1] ) / 360
        a05 = self.geometry.Trig_2D_Points_Lines_Angle( O5[0], O5[1], 0, 0, C61[0], C61[1] ) / 360
        a06 = self.geometry.Trig_2D_Points_Lines_Angle( O6[0], O6[1], 0, 0, C61[0], C61[1] ) / 360
        a12 = self.geometry.Trig_2D_Points_Lines_Angle( C12[0], C12[1], 0, 0, C61[0], C61[1] ) / 360
        a23 = self.geometry.Trig_2D_Points_Lines_Angle( C23[0], C23[1], 0, 0, C61[0], C61[1] ) / 360
        a34 = self.geometry.Trig_2D_Points_Lines_Angle( C34[0], C34[1], 0, 0, C61[0], C61[1] ) / 360
        a45 = self.geometry.Trig_2D_Points_Lines_Angle( C45[0], C45[1], 0, 0, C61[0], C61[1] ) / 360
        a56 = self.geometry.Trig_2D_Points_Lines_Angle( C56[0], C56[1], 0, 0, C61[0], C61[1] ) / 360
        a61 = 1
        # Channel
        di = d * 3
        if ( di <= 0 or di >= 3 ):
            c = +1
        elif ( di > 0 and di <= 1):
            if ( a <= a23 ):c = -3
            elif ( a > a23 and a <= a45 ):c = -1
            else:c = -2
        elif ( di > 1 and di < 2):
            if ( a <= a01 ):c = +1
            elif ( a > a01 and a <= a02 ):c = -3
            elif ( a > a02 and a <= a03 ):c = +2
            elif ( a > a03 and a <= a04 ):c = -1
            elif ( a > a04 and a <= a05 ):c = +3
            elif ( a > a05 and a <= a06 ):c = -2
            else:c = +1
        elif ( di >= 2 and di < 3):
            if ( a <= a12 ):c = +1
            elif ( a > a12 and a <= a34 ):c = +2
            elif ( a > a34 and a <= a56 ):c = +3
            else:c = +1

        # Return
        return c

    #endregion
    #region XYZ LINEAR

    def rgb_to_xyz( self, r, g, b ):
        lrgb = self.srgb_to_lrgb( r, g, b )
        x = ( lrgb[0] * self.m_rgb_xyz[0][0] ) + ( lrgb[1] * self.m_rgb_xyz[0][1] ) + ( lrgb[2] * self.m_rgb_xyz[0][2] )
        y = ( lrgb[0] * self.m_rgb_xyz[1][0] ) + ( lrgb[1] * self.m_rgb_xyz[1][1] ) + ( lrgb[2] * self.m_rgb_xyz[1][2] )
        z = ( lrgb[0] * self.m_rgb_xyz[2][0] ) + ( lrgb[1] * self.m_rgb_xyz[2][1] ) + ( lrgb[2] * self.m_rgb_xyz[2][2] )
        return [x, y, z]
    def xyz_to_rgb( self, x, y, z ):
        var_r = ( x * self.m_xyz_rgb[0][0] ) + ( y * self.m_xyz_rgb[0][1] ) + ( z * self.m_xyz_rgb[0][2] )
        var_g = ( x * self.m_xyz_rgb[1][0] ) + ( y * self.m_xyz_rgb[1][1] ) + ( z * self.m_xyz_rgb[1][2] )
        var_b = ( x * self.m_xyz_rgb[2][0] ) + ( y * self.m_xyz_rgb[2][1] ) + ( z * self.m_xyz_rgb[2][2] )
        srgb = self.lrgb_to_srgb( var_r, var_g, var_b )
        r, g, b = self.Vector_Safe( srgb[0], srgb[1], srgb[2] )
        return [r, g, b]
    # XYY
    def xyz_to_xyy( self, x, y, z ):
        if ( x == 0 and y == 0 and z == 0 ):
            x1 = 0.31272660439158345
            y2 = 0.3290231524027522
            y3 = y
        else:
            x1 = x / ( x + y + z  )
            y2 = y / ( x + y + z  )
            y3 = y
        return [x1, y2, y3]
    def xyy_to_xyz( self, x1, y2, y3 ):
        if y2 == 0:
            x = 0
            y = 0
            z = 0
        else:
            x = ( x1 * y3  ) / y2
            y = y3
            z = ( ( 1 - x1 - y2 ) * y3 ) / y2
        return [x, y, z]
    def rgb_to_xyy( self, r, g, b ):
        xyz = self.rgb_to_xyz( r, g, b )
        xyy = self.xyz_to_xyy( xyz[0], xyz[1], xyz[2] )
        return [xyy[0], xyy[1], xyy[2]]
    def xyy_to_rgb( self, x, y1, y2 ):
        xyz = self.xyy_to_xyz( x, y1, y2 )
        rgb = self.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
        return [rgb[0], rgb[1], rgb[2]]
    # LAB
    def xyz_to_lab( self, x, y, z ):
        k = 903.3 # Kappa
        e = 0.008856 # Epsilon

        rx = x / self.ref_x
        ry = y / self.ref_y
        rz = z / self.ref_z

        if rx > e: fx = rx**( 1/3 )
        else:      fx = ( k*rx + 16 ) / 116
        if ry > e: fy = ry**( 1/3 )
        else:      fy = ( k*ry + 16 ) / 116
        if rz > e: fz = rz**( 1/3 )
        else:      fz = ( k*rz + 16 ) / 116

        l = ( ( 116 * fy ) - 16 ) / 100
        a = 0.5 + ( fx - fy )
        b = 0.5 + ( fy - fz )

        return [ l, a, b ]
    def lab_to_xyz( self, l, a, b ):
        k = 903.3 # Kappa
        e = 0.008856 # Epsilon

        l = l * 100
        a = a - 0.5
        b = b - 0.5
        fy = ( l + 16  ) / 116
        fx = a + fy
        fz = fy - b

        if fx**3 > e: rx = fx**3
        else:         rx = ( 116 * fx - 16 ) / k
        if l > k*e:   ry = ( ( l + 16 ) / 116 )**3
        else:         ry = l / k
        if fz**3 > e: rz = fz**3
        else:         rz = ( 116 * fz - 16 ) / k

        x = rx * self.ref_x
        y = ry * self.ref_y
        z = rz * self.ref_z

        return [ x, y, z ]
    def rgb_to_lab( self, r, g, b ):
        xyz = self.rgb_to_xyz( r, g, b )
        lab = self.xyz_to_lab( xyz[0], xyz[1], xyz[2] )
        return [ lab[0], lab[1], lab[2] ]
    def lab_to_rgb( self, l, a, b ):
        xyz = self.lab_to_xyz( l, a, b )
        rgb = self.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
        return [ rgb[0], rgb[1], rgb[2] ]

    #endregion
    #region XYZ HUE

    # LCHab
    def lab_to_lch( self, l, a, b ):
        a = ( a - 0.5 ) * 2
        b = ( b - 0.5 ) * 2

        vh = math.atan2( b, a )
        if vh > 0: vh = ( vh / math.pi ) * 180
        else:      vh = 360 - ( abs( vh ) / math.pi ) * 180
        c = math.sqrt( a**2 + b**2 )
        h = vh / 360

        l, c, h = self.Vector_Safe( l, c, h )
        return [ l, c, h ]
    def lch_to_lab( self, l, c, h ):
        vh = h * 360

        a = math.cos( math.radians( vh ) ) * c
        b = math.sin( math.radians( vh ) ) * c

        a = a / 2 + 0.5
        b = b / 2 + 0.5

        l, a, b = self.Vector_Safe( l, a, b )
        return [ l, a, b ]
    def xyz_to_lch( self, x, y, z ):
        lab = self.xyz_to_lab( x, y, z )
        lch = self.lab_to_lch( lab[0], lab[1], lab[2] )
        return [ lch[0], lch[1], lch[2] ]
    def lch_to_xyz( self, l, c, h ):
        lab = self.lch_to_lab( l, c, h )
        xyz = self.lab_to_xyz( lab[0], lab[1], lab[2] )
        return [ xyz[0], xyz[1], xyz[2] ]
    def rgb_to_lch( self, r, g, b ):
        xyz = self.rgb_to_xyz( r, g, b )
        lab = self.xyz_to_lab( xyz[0], xyz[1], xyz[2] )
        lch = self.lab_to_lch( lab[0], lab[1], lab[2] )
        return [ lch[0], lch[1], lch[2] ]
    def lch_to_rgb( self, l, c, h ):
        lab = self.lch_to_lab( l, c, h )
        xyz = self.lab_to_xyz( lab[0], lab[1], lab[2] )
        rgb = self.xyz_to_rgb( xyz[0], xyz[1], xyz[2] )
        return [ rgb[0], rgb[1], rgb[2] ]

    #endregion
    #region Convert

    def convert( self, input_space="RGB", input_bit="8I", v1=0, v2=0, v3=0, v4=0, output_space="RGB", output_bit="8I" ):
        # Input Variations
        # input/output space = AAA RGB CMY CMYK RYB YUV HSV HSL HCY ARD XYZ XYY LAB LCH
        # input/output bit = 8I 16I 16F 32F
        # v1 v2 v3 v4 = -1 0 1

        # "RGB_8I_255_255_255"
        # "RGB_16I_65535_65535_65535"
        # "RGB_16F_1.0_1.0_1.0"
        # "RGB_32F_1.0_1.0_1.0"

        # Bit Depth Input
        if input_bit == "8I":   input_depth = 255
        if input_bit == "16I":  input_depth = 65535
        if input_bit == "16F":  input_depth = 1
        if input_bit == "32F":  input_depth = 1
        # Bit Depth Output
        if output_bit == "8I":  output_depth = 255
        if output_bit == "16I": output_depth = 65535
        if output_bit == "16F": output_depth = 1
        if output_bit == "32F": output_depth = 1

        # Color Space
        if input_space == "AAA":
            pass
        if input_space == "RGB":

            if output_space == "AAA":
                aaa = self.rgb_to_aaa( v1, v2, v3 )
                return aaa
            if output_space == "RGB":
                rgb = [ v1, v2, v3 ]
                return rgb
            if output_space == "CMY":
                cmy = self.rgb_to_cmy( v1, v2, v3 )
                return cmy
            if output_space == "CMYK":
                cmyk = self.rgb_to_cmyk( v1, v2, v3 )
                return cmyk
            if output_space == "RYB":
                ryb = self.rgb_to_ryb( v1, v2, v3 )
                return ryb
            if output_space == "YUV":
                yuv = self.rgb_to_yuv( v1, v2, v3 )
                return yuv
            if output_space == "HSV":
                hsv = self.rgb_to_hsv( v1, v2, v3 )
                return hsv
            if output_space == "HSL":
                hsl = self.rgb_to_hsl( v1, v2, v3 )
                return hsl
            if output_space == "HCY":
                hcy = self.rgb_to_hcy( v1, v2, v3 )
                return hcy
            if output_space == "ARD":
                ard = self.rgb_to_ard( v1, v2, v3 )
                return ard
            if output_space == "XYZ":
                xyz = self.rgb_to_xyz( v1, v2, v3 )
                return xyz
            if output_space == "XYY":
                xyz = self.rgb_to_xyz( v1, v2, v3 )
                xyy = self.rgb_to_xyy( xyz[0], xyz[1], xyz[2] )
                return xyy
            if output_space == "LAB":
                xyz = self.rgb_to_xyz( v1, v2, v3 )
                lab = self.rgb_to_lab( xyz[0], xyz[1], xyz[2] )
                return lab
            if output_space == "LCH":
                xyz = self.rgb_to_xyz( v1, v2, v3 )
                lch = self.rgb_to_lch( xyz[0], xyz[1], xyz[2] )
                return lch

        if input_space == "CMY":
            pass
        if input_space == "CMYK":
            pass
        if input_space == "RYB":
            pass
        if input_space == "YUV":
            pass

        if input_space == "HSV":
            pass
        if input_space == "HSL":
            pass
        if input_space == "HCY":
            pass
        if input_space == "ARD":
            pass

        if input_space == "XYZ":
            pass
        if input_space == "XYY":
            pass
        if input_space == "LAB":
            pass
        if input_space == "LCH":
            pass
        

    #endregion
    cor_neutral = {
        # State
        "active" : None,
        # Hue
        "hue_d" : 0,
        "hue_a" : 0,
        # HEX Code
        "hex_aaa" : "#00",
        "hex_rgb" : "#000000",
        "hex_cmyk" : "#000000ff",
        "hex_yuv" : "#000000",
        "hex_xyz" : "#000000",
        "hex_lab" : "#008080",
        # Kelvin
        'kkk_percent': 0.5,
        'kkk_scale': 6500,
        # Name
        "name" : "Black",
        }

    kac={
        'active': True,
        'hex6': '#000000',
        'aaa_1': 0.0, 'rgb_1': 0, 'rgb_2': 0, 'rgb_3': 0,
        'uvd_1': 0, 'uvd_2': 0, 'uvd_3': 0.0,
        'cmy_1': 1, 'cmy_2': 1, 'cmy_3': 1,
        'cmyk_1': 0, 'cmyk_2': 0, 'cmyk_3': 0, 'cmyk_4': 1,
        'ryb_1': 0, 'ryb_2': 0, 'ryb_3': 0,
        'yuv_1': 0, 'yuv_2': 0.5, 'yuv_3': 0.5,
        'hue_d': 0.9190479505515416, 'hue_a': 0.9595239752757708,
        'hsv_1': 0.9190479505515416, 'hsv_2': 0, 'hsv_3': 0,
        'hsl_1': 0.9190479505515416, 'hsl_2': 0, 'hsl_3': 0, 
        'hcy_1': 0.9190479505515416, 'hcy_2': 0.0, 'hcy_3': 0.0, 
        'ard_1': 0.9190479505515416, 'ard_2': 0, 'ard_3': 0.0, 
        'xyz_1': 0.0, 'xyz_2': 0.0, 'xyz_3': 0.0, 
        'xyy_1': 0.31272660439158345, 'xyy_2': 0.3290231524027522, 
        'xyy_3': 0.0, 'lab_1': 0.0, 'lab_2': 0.5, 'lab_3': 0.5, 
        'lch_1': 0, 'lch_2': 0, 'lch_3': 1, 
        'name': 'Black', 
        'kkk_percent': 0.5, 'kkk_scale': 6500, 
        'hex6_d': '#000000', 
        'aaa_d1': 1.0, 
        'rgb_d1': 0.0, 'rgb_d2': 0.0, 'rgb_d3': 0.0, 
        'cmyk_d1': 0, 'cmyk_d2': 0, 'cmyk_d3': 0, 'cmyk_d4': 0, 
        'yuv_d1': 0, 'yuv_d2': 0, 'yuv_d3': 0, 
        'xyz_d1': 0, 'xyz_d2': 0, 'xyz_d3': 0, 
        'lab_d1': 0, 'lab_d2': 0, 'lab_d3': 0
        }

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

"""
