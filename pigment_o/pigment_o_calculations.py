# Pigment.O is a Krita plugin and it is a Color Picker and Color Mixer.
# Copyright (C) 2020  Ricardo Jeremias.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#\\ Imports ####################################################################
import math

#//

class color():

    #\\ Adjust #################################################################
    def Set_Document(d_cm_, d_cd_, d_cp_):
        d_cm = d_cm_
        d_cd = d_cd_
        d_cp = d_cp_
    def Set_Angle_Live(angle_live_):
        angle_live = angle_live_
    def Set_Luma_RGB(luminosity):
        if luminosity == "ITU-R BT.601":
            luma_r = 0.299
            luma_b = 0.114
            luma_g = 1 - luma_r - luma_b # 0.587
            luma_pr = 1.402
            luma_pb = 1.772
        if luminosity == "ITU-R BT.709":
            luma_r = 0.2126
            luma_b = 0.0722
            luma_g = 1 - luma_r - luma_b # 0.7152
            luma_pr = 1.5748
            luma_pb = 1.8556
        if luminosity == "ITU-R BT.2020":
            luma_r = 0.2627
            luma_b = 0.0593
            luma_g = 1 - luma_r - luma_b # 0.678
            luma_pr = 0.4969
            luma_pb = 0.7910
    def Set_Gamma(gamma_y_, gamma_l_):
        gamma_y = gamma_y_
        gamma_l = gamma_l_
    def Set_XYZ_Matrix(xyz_matrix, xyz_iluma):
        if matrix == "sRGB":
            if iluma == "D50": # i=0
                m_rgb_xyz = [
                [0.4360747,  0.3850649,  0.1430804],
                [0.2225045,  0.7168786,  0.0606169],
                [0.0139322,  0.0971045,  0.7141733]
                ]
                m_xyz_rgb = [
                [ 3.1338561, -1.6168667, -0.4906146],
                [-0.9787684,  1.9161415,  0.0334540],
                [ 0.0719453, -0.2289914,  1.4052427]
                ]
            if iluma == "D65": # i=1
                m_rgb_xyz = [
                [0.4124564,  0.3575761,  0.1804375],
                [0.2126729,  0.7151522,  0.0721750],
                [0.0193339,  0.1191920,  0.9503041]
                ]
                m_xyz_rgb = [
                [ 3.2404542, -1.5371385, -0.4985314],
                [-0.9692660,  1.8760108,  0.0415560],
                [ 0.0556434, -0.2040259,  1.0572252]
                ]

        if matrix == "Adobe RGB":
            if iluma == "D50": # i=2
                m_rgb_xyz = [
                [0.6097559,  0.2052401,  0.1492240],
                [0.3111242,  0.6256560,  0.0632197],
                [0.0194811,  0.0608902,  0.7448387]
                ]
                m_xyz_rgb = [
                [ 1.9624274, -0.6105343, -0.3413404],
                [-0.9787684,  1.9161415,  0.0334540],
                [ 0.0286869, -0.1406752,  1.3487655]
                ]
            if iluma == "D65": # i=3
                m_rgb_xyz = [
                [ 0.5767309,  0.1855540,  0.1881852],
                [ 0.2973769,  0.6273491,  0.0752741],
                [ 0.0270343,  0.0706872,  0.9911085]
                ]
                m_xyz_rgb = [
                [ 2.0413690, -0.5649464, -0.3446944],
                [-0.9692660,  1.8760108,  0.0415560],
                [ 0.0134474, -0.1183897,  1.0154096]
                ]
        if matrix == "Apple RGB":
            if iluma == "D50":
                m_rgb_xyz = [
                [0.4755678, 0.3396722,  0.1489800],
                [0.2551812, 0.6725693,  0.0722496],
                [0.0184697, 0.1133771,  0.6933632]
                ]
                m_xyz_rgb = [
                [ 2.8510695, -1.3605261, -0.4708281],
                [-1.0927680,  2.0348871,  0.0227598],
                [ 0.1027403, -0.2964984,  1.4510659]
                ]
            if iluma == "D65":
                m_rgb_xyz = [
                [0.4497288,  0.3162486,  0.1844926],
                [0.2446525,  0.6720283,  0.0833192],
                [0.0251848,  0.1411824,  0.9224628]
                ]
                m_xyz_rgb = [
                [ 2.9515373, -1.2894116, -0.4738445],
                [-1.0851093,  1.9908566,  0.0372026],
                [ 0.0854934, -0.2694964,  1.0912975]
                ]
        if matrix == "Best RGB":
            if iluma == "D50":
                m_rgb_xyz = [
                [0.6326696,  0.2045558,  0.1269946],
                [0.2284569,  0.7373523,  0.0341908],
                [0.0000000,  0.0095142,  0.8156958]
                ]
                m_xyz_rgb = [
                [ 1.7552599, -0.4836786, -0.2530000],
                [-0.5441336,  1.5068789,  0.0215528],
                [ 0.0063467, -0.0175761,  1.2256959]
                ]
            else:
                iluma = "D50"
        if matrix == "Beta RGB":
            if iluma == "D50":
                m_rgb_xyz = [
                [ 0.6712537,  0.1745834,  0.1183829],
                [ 0.3032726,  0.6637861,  0.0329413],
                [ 0.0000000,  0.0407010,  0.7845090]
                ]
                m_xyz_rgb = [
                [ 1.6832270, -0.4282363, -0.2360185],
                [-0.7710229,  1.7065571,  0.0446900],
                [ 0.0400013, -0.0885376,  1.2723640]
                ]
            else:
                iluma = "D50"
        if matrix == "Bruce RGB":
            if iluma == "D50":
                m_rgb_xyz = [
                [ 0.4941816,  0.3204834,  0.1495550],
                [ 0.2521531,  0.6844869,  0.0633600],
                [ 0.0157886,  0.0629304,  0.7464909]
                ]
                m_xyz_rgb = [
                [ 2.6502856, -1.2014485, -0.4289936],
                [-0.9787684,  1.9161415,  0.0334540],
                [ 0.0264570, -0.1361227,  1.3458542]
                ]
            if iluma == "D65":
                m_rgb_xyz = [
                [ 0.4674162,  0.2944512,  0.1886026],
                [ 0.2410115,  0.6835475,  0.0754410],
                [ 0.0219101,  0.0736128,  0.9933071]
                ]
                m_xyz_rgb = [
                [ 2.7454669, -1.1358136, -0.4350269],
                [-0.9692660,  1.8760108,  0.0415560],
                [ 0.0112723, -0.1139754,  1.0132541]
                ]
        # CIE RGB
        if matrix == "ColorMatch RGB":
            if iluma == "D50":
                m_rgb_xyz = [
                [ 0.5093439,  0.3209071,  0.1339691],
                [ 0.2748840,  0.6581315,  0.0669845],
                [ 0.0242545,  0.1087821,  0.6921735]
                ]
                m_xyz_rgb = [
                [ 2.6422874, -1.2234270, -0.3930143],
                [-1.1119763,  2.0590183,  0.0159614],
                [ 0.0821699, -0.2807254,  1.4559877]
                ]
            else:
                iluma = "D50"
        if matrix == "Don RGB 4":
            if iluma == "D50":
                m_rgb_xyz = [
                [ 0.6457711,  0.1933511,  0.1250978],
                [ 0.2783496,  0.6879702,  0.0336802],
                [ 0.0037113,  0.0179861,  0.8035125],
                ]
                m_xyz_rgb = [
                [ 1.7603902, -0.4881198, -0.2536126],
                [-0.7126288,  1.6527432,  0.0416715],
                [ 0.0078207, -0.0347411,  1.2447743],
                ]
            else:
                iluma = "D50"
        if matrix == "ECI RGB":
            if iluma == "D50":
                m_rgb_xyz = [
                [ 0.6502043,  0.1780774,  0.1359384],
                [ 0.3202499,  0.6020711,  0.0776791],
                [ 0.0000000,  0.0678390,  0.7573710]
                ]
                m_xyz_rgb = [
                [ 1.7827618, -0.4969847, -0.2690101],
                [-0.9593623,  1.9477962, -0.0275807],
                [ 0.0859317, -0.1744674,  1.3228273]
                ]
            else:
                iluma = "D50"
        if matrix == "Ekta Space PS5":
            if iluma == "D50":
                m_rgb_xyz = [
                [ 0.5938914,  0.2729801,  0.0973485],
                [ 0.2606286,  0.7349465,  0.0044249],
                [ 0.0000000,  0.0419969,  0.7832131]
                ]
                m_xyz_rgb = [
                [ 2.0043819, -0.7304844, -0.2450052],
                [-0.7110285,  1.6202126,  0.0792227],
                [ 0.0381263, -0.0868780,  1.2725438]
                ]
            else:
                iluma = "D50"
        # NTSC RGB
        if matrix == "PAL/SECAM RGB":
            if iluma == "D50":
                m_rgb_xyz = [
                [ 0.4552773,  0.3675500,  0.1413926],
                [ 0.2323025,  0.7077956,  0.0599019],
                [ 0.0145457,  0.1049154,  0.7057489]
                ]
                m_xyz_rgb = [
                [ 2.9603944, -1.4678519, -0.4685105],
                [-0.9787684,  1.9161415,  0.0334540],
                [ 0.0844874, -0.2545973,  1.4216174]
                ]
            if iluma == "D65":
                m_rgb_xyz = [
                [ 0.4306190,  0.3415419,  0.1783091],
                [ 0.2220379,  0.7066384,  0.0713236],
                [ 0.0201853,  0.1295504,  0.9390944]
                ]
                m_xyz_rgb = [
                [ 3.0628971, -1.3931791, -0.4757517],
                [-0.9692660,  1.8760108,  0.0415560],
                [ 0.0678775, -0.2288548,  1.0693490]
                ]
        if matrix == "ProPhoto RGB":
            if iluma == "D50":
                m_rgb_xyz = [
                [0.7976749, 0.1351917, 0.0313534],
                [0.2880402, 0.7118741, 0.0000857],
                [0.0000000, 0.0000000, 0.8252100]
                ]
                m_xyz_rgb = [
                [ 1.3459433, -0.2556075, -0.0511118],
                [-0.5445989,  1.5081673,  0.0205351],
                [ 0.0000000,  0.0000000,  1.2118128]
                ]
            else:
                iluma = "D50"
        if matrix == "SMPTE-C RGB":
            if iluma == "D50":
                m_rgb_xyz = [
                [ 0.4163290,  0.3931464,  0.1547446],
                [ 0.2216999,  0.7032549,  0.0750452],
                [ 0.0136576,  0.0913604,  0.7201920]
                ]
                m_xyz_rgb = [
                [ 3.3921940, -1.8264027, -0.5385522],
                [-1.0770996,  2.0213975,  0.0207989],
                [ 0.0723073, -0.2217902,  1.3960932]
                ]
            if iluma == "D65":
                m_rgb_xyz = [
                [ 0.3935891,  0.3652497,  0.1916313],
                [ 0.2124132,  0.7010437,  0.0865432],
                [ 0.0187423,  0.1119313,  0.9581563]
                ]
                m_xyz_rgb = [
                [ 3.5053960, -1.7394894, -0.5439640],
                [-1.0690722,  1.9778245,  0.0351722],
                [ 0.0563200, -0.1970226,  1.0502026]
                ]
        if matrix == "Wide Gamut RGB":
            if iluma == "D50":
                m_rgb_xyz = [
                [ 0.7161046,  0.1009296,  0.1471858],
                [ 0.2581874,  0.7249378,  0.0168748],
                [ 0.0000000,  0.0517813,  0.7734287]
                ]
                m_xyz_rgb = [
                [ 1.4628067, -0.1840623, -0.2743606],
                [-0.5217933,  1.4472381,  0.0677227],
                [ 0.0349342, -0.0968930,  1.2884099]
                ]
            else:
                iluma = "D50"

        # Illuminants
        if iluma == "D50":
            ref_x = 0.96422
            ref_y = 1.00
            ref_z = 0.82521
        if iluma == "D65":
            ref_x = 0.95047
            ref_y = 1.00
            ref_z = 1.08883

    #//
    #\\ RGB ####################################################################
    # Gray Contrast
    def gc(r, g, b):
        value = rgb_to_aaa(r, g, b)[0]
        if value <= 0.3:
            gc = ( 1 - value )
        elif value >= 0.7:
            gc = ( 1 - value )
        else:
            gc = ( value - 0.3 )
        return gc
    # AAA
    def rgb_to_aaa(r, g, b):
        aaa = (luma_r*r) + (luma_g*g) + (luma_b*b)
        return [aaa]
    # RGB
    def srgb_to_lrgb(sr, sg, sb):
        n = 0.055
        m = 12.92
        if sr > 0.04045:
            lr = ( ( sr + n ) / ( 1 + n ) ) ** gamma_l
        else:
            lr = sr / m
        if sg > 0.04045:
            lg = ( ( sg + n ) / ( 1 + n ) ) ** gamma_l
        else:
            lg = sg / m
        if sb > 0.04045:
            lb = ( ( sb + n ) / ( 1 + n ) ) ** gamma_l
        else:
            lb = sb / m
        return [lr, lg, lb]
    def lrgb_to_srgb(lr, lg, lb):
        n = 0.055
        m = 12.92
        if lr > 0.0031308:
            sr = (( 1 + n ) * lr ** ( 1 / gamma_l )) - n
        else:
            sr = m * lr
        if lg > 0.0031308:
            sg = (( 1 + n ) * lg ** ( 1 / gamma_l )) - n
        else:
            sg = m * lg
        if lb > 0.0031308:
            sb = (( 1 + n ) * lb ** ( 1 / gamma_l )) - n
        else:
            sb = m * lb
        return [sr, sg, sb]
    # CMY
    def rgb_to_cmy(r, g, b):
        c = 1 - r
        m = 1 - g
        y = 1 - b
        return [c, m, y]
    def cmy_to_rgb(c, m, y):
        r = 1 - c
        g = 1 - m
        b = 1 - y
        return [r, g, b]
    # CMYK
    def rgb_to_cmyk(r, g, b):
        q = max(r, g, b)
        if q == 0:
            if cmyk_lock == False:
                c = 0
                m = 0
                y = 0
                k = 1
            if cmyk_lock == True:
                c = 1
                m = 1
                y = 1
                k = cmyk_4
        else:
            if cmyk_lock == False:
                k = 1 - max(r, g, b) # Standard Transform
            else:
                k = cmyk_4 # Key is Locked
            ik = 1 - k
            if ik == 0 :
                c = ( r - k ) / ( k )
                m = ( g - k ) / ( k )
                y = ( b - k ) / ( k )
            else:
                c = ( 1 - r - k ) / ( 1 - k )
                m = ( 1 - g - k ) / ( 1 - k )
                y = ( 1 - b - k ) / ( 1 - k )
        return [c, m, y, k]
    def cmyk_to_rgb(c, m, y, k):
        r = ( 1 - c ) * ( 1 - k )
        g = ( 1 - m ) * ( 1 - k )
        b = ( 1 - y ) * ( 1 - k )
        return [r, g, b]
    # RYB
    def rgb_to_ryb(r, g, b):
        red = r
        green = g
        blue = b
        white  = min(red, green, blue)
        red -= white
        green -= white
        blue -= white
        maxgreen = max(red, green, blue)
        yellow = min(red, green)
        red -= yellow
        green -= yellow
        if (blue > 0 and green > 0):
            blue /= 2
            green /= 2
        yellow += green
        blue += green
        maxyellow = max(red, yellow, blue)
        if maxyellow > 0:
            N = maxgreen / maxyellow
            red *= N
            yellow *= N
            blue *= N
        red += white
        yellow += white
        blue += white
        return [red, yellow, blue]
    def ryb_to_rgb(r, y, b):
        red = r
        yellow = y
        blue = b
        white = min(red, yellow, blue)
        red -= white
        yellow -= white
        blue -= white
        maxyellow = max(red, yellow, blue)
        green = min(yellow, blue)
        yellow -= green
        blue -= green
        if (blue > 0 and green > 0):
            blue *= 2
            green *= 2
        red += yellow
        green += yellow
        maxgreen = max(red, green, blue)
        if maxgreen > 0:
            N = maxyellow / maxgreen
            red *= N
            green *= N
            blue *= N
        red += white
        green += white
        blue += white
        return [red, green, blue]
    # RYB HUE Conversion
    def hcmy_to_hryb(hcmy):
        hcmy = Math_1D_Loop(hcmy)
        for i in range(len(cmy_step)):
            if hcmy == cmy_step[i]:
                hryb = ryb_step[i]
        for i in range(len(cmy_step)-1):
            if (hcmy > cmy_step[i] and hcmy < cmy_step[i+1]):
                var = (hcmy - cmy_step[i]) / (cmy_step[i+1] - cmy_step[i])
                hryb = ( ryb_step[i] + (ryb_step[i+1] - ryb_step[i]) * var )
        return hryb
    def hryb_to_hcmy(hryb):
        hcmy = Math_1D_Loop(hryb)
        for i in range(len(ryb_step)):
            if hryb == ryb_step[i]:
                hcmy = cmy_step[i]
        for i in range(len(ryb_step)-1):
            if (hryb > ryb_step[i] and hryb < ryb_step[i+1]):
                var = (hryb - ryb_step[i]) / (ryb_step[i+1] - ryb_step[i])
                hcmy = ( cmy_step[i] + (cmy_step[i+1] - cmy_step[i]) * var )
        return hcmy
    # YUV
    def rgb_to_yuv(r, g, b):
        y = luma_r*r + luma_g*g + luma_b*b
        pb = 0.5 + (0.5 * ((b - y) / (1 - luma_b))) # Chroma Blue - " 0.5 + " is the slider adjustment offset
        pr = 0.5 + (0.5 * ((r - y) / (1 - luma_r))) # Chroma Red - " 0.5 + " is the slider adjustment offset
        return [y, pb, pr]
    def yuv_to_rgb(y, pb, pr):
        pb = pb - 0.5 # slider adjustment offset
        pr = pr - 0.5 # slider adjustment offset
        r = luma_pr * pr + y
        g = (-0.344136286201022) * pb + (-0.714136286201022) * pr + y
        b = luma_pb * pb + y
        r = Math_1D_Limit(r)
        g = Math_1D_Limit(g)
        b = Math_1D_Limit(b)
        return [r, g, b]
    # KELVIN (not physical)
    def kkk_to_rgb(k):
        for i in range(len(kelvin_rgb)):
            # detect list entry
            if (k == kelvin_rgb[i][0] or (k > kelvin_rgb[i][0] and k < kelvin_rgb[i+1][0])):
                # 1 value for that step
                r = kelvin_rgb[i][1] / 255
                g = kelvin_rgb[i][2] / 255
                b = kelvin_rgb[i][3] / 255
        return [r, g, b]

    #//
    #\\ RGB HUE ################################################################
    # UVD
    def rgb_to_uvd(r, g, b):
        # uv range from -1 to 1 (0.8 with mask)
        # MatrixInverse * RGB
        MatrixInv = [[-0.866025808, 0.866025808, -0.0000000000000000961481791],
                     [ 0.500000010, 0.499999990, -1.00000000],
                     [ 0.333333497, 0.333333503,  0.333333000]]
        u = MatrixInv[0][0]*r + MatrixInv[0][1]*g + MatrixInv[0][2]*b
        v = MatrixInv[1][0]*r + MatrixInv[1][1]*g + MatrixInv[1][2]*b
        d = MatrixInv[2][0]*r + MatrixInv[2][1]*g + MatrixInv[2][2]*b
        m = 0.0000001
        if (u > -m and u < m):
            u = 0
        if (v > -m and v < m):
            v = 0
        return [u, v, d]
    def uvd_to_rgb(u, v, d):
        # Matrix * UVD
        Matrix = [[-0.57735,          0.333333, 1],
                  [ 0.57735,          0.333333, 1],
                  [-0.0000000113021, -0.666667, 1]]
        r = Matrix[0][0]*u + Matrix[0][1]*v + Matrix[0][2]*d
        g = Matrix[1][0]*u + Matrix[1][1]*v + Matrix[1][2]*d
        b = Matrix[2][0]*u + Matrix[2][1]*v + Matrix[2][2]*d
        # Correct out of Bound values
        r = Math_1D_Limit(r)
        g = Math_1D_Limit(g)
        b = Math_1D_Limit(b)
        return [r, g, b]
    def uvd_hexagon_origins(d):
        # Values
        w1 = 0.8660253882408142
        h1 = 0.5000000596046448
        h2 = 1
        diagonal = d * 3
        delta1 = diagonal
        delta2 = diagonal - 1
        delta3 = diagonal - 2
        # Single Points
        if diagonal <= 0.0:
            O1 = [0, 0]
            O2 = [0, 0]
            O3 = [0, 0]
            O4 = [0, 0]
            O5 = [0, 0]
            O6 = [0, 0]
        elif (diagonal > 0.0 and diagonal <= 1.0):
            O1 = [0 + 0,           0 - (h2*delta1)]  # -1 exception to not be zero area
            O2 = [0 + (w1*delta1), 0 + (h1*delta1)]
            O3 = [0 + (w1*delta1), 0 + (h1*delta1)]
            O4 = [0 - (w1*delta1), 0 + (h1*delta1)]
            O5 = [0 - (w1*delta1), 0 + (h1*delta1)]
            O6 = [0 + 0,           0 - (h2*delta1)]  # -1 exception to not be zero area
        elif (diagonal > 1.0 and diagonal < 2.0):
            O1 = [ 0  + (w1*delta2), -h2 + (h1*delta2)]
            O2 = [ w1 + 0,            h1 - (h2*delta2)]
            O3 = [ w1 - (w1*delta2),  h1 + (h1*delta2)]
            O4 = [-w1 + (w1*delta2),  h1 + (h1*delta2)]
            O5 = [-w1 + 0,            h1 - (h2*delta2)]
            O6 = [  0 - (w1*delta2), -h2 + (h1*delta2)]
        elif (diagonal >= 2.0 and diagonal < 3.0):
            O1 = [ w1 - (w1*delta3), -h1 + (h1*delta3)]
            O2 = [ w1 - (w1*delta3), -h1 + (h1*delta3)]
            O3 = [ 0  + 0,            h2 - (h2*delta3)]
            O4 = [ 0  + 0,            h2 - (h2*delta3)]
            O5 = [-w1 + (w1*delta3), -h1 + (h1*delta3)]
            O6 = [-w1 + (w1*delta3), -h1 + (h1*delta3)]
        elif diagonal >= 3.0:
            O1 = [0, 0]
            O2 = [0, 0]
            O3 = [0, 0]
            O4 = [0, 0]
            O5 = [0, 0]
            O6 = [0, 0]
        # Composed Points
        OCC = [0, 0]
        O12 = [O1[0] + ((O2[0] - O1[0]) / 2), O1[1] + ((O2[1] - O1[1]) / 2)]
        O23 = [O2[0] + ((O3[0] - O2[0]) / 2), O2[1] + ((O3[1] - O2[1]) / 2)]
        O34 = [O3[0] + ((O4[0] - O3[0]) / 2), O3[1] + ((O4[1] - O3[1]) / 2)]
        O45 = [O4[0] + ((O5[0] - O4[0]) / 2), O4[1] + ((O5[1] - O4[1]) / 2)]
        O56 = [O5[0] + ((O6[0] - O5[0]) / 2), O5[1] + ((O6[1] - O5[1]) / 2)]
        O61 = [O6[0] + ((O1[0] - O6[0]) / 2), O6[1] + ((O1[1] - O6[1]) / 2)]
        # Angle to Red Axis as Origin
        REDAXIS = Math_2D_Points_Lines_Angle(10, 0, 0, 0, O45[0], O45[1])
        # Return
        return O1,O2,O3,O4,O5,O6,OCC,O12,O23,O34,O45,O56,O61
    def uvd_to_ard(u, v, d):
        # Update Origin Points
        uvd_hexagon_origins(d)
        # Correct UV values
        u = round(u,15)
        v = round(v,15)
        # Angle
        if (u == 0 and v == 0):
            arc=0
            a=0
        else:
            arc = Math_2D_Points_Lines_Angle(u,v, 0,0, O45[0],O45[1]) # range 0 to 360
            a = arc / 360 # range 0 to 1
        # User Value
        user = Math_2D_Points_Distance(0, 0, u, v)
        # Total Value
        diagonal = d * 3
        if diagonal <= 0:
            a = angle_live
            total = 1
        elif (diagonal > 0 and diagonal <= 1):
            # Angles according to O45(RED) as Origin
            AR = 0 # RED
            AG = Math_2D_Points_Lines_Angle(O23[0], O23[1], 0, 0, O45[0], O45[1]) # GREEN
            AB = Math_2D_Points_Lines_Angle(O61[0], O61[1], 0, 0, O45[0], O45[1]) # BLUE
            # Certain
            if arc == AR:
                total = Math_2D_Points_Distance(0, 0, O45[0], O45[1])
            elif arc == AG:
                total = Math_2D_Points_Distance(0, 0, O23[0], O23[1])
            elif arc == AB:
                total = Math_2D_Points_Distance(0, 0, O61[0], O61[1])
            # Intervals
            elif (arc > AR and arc < AG):
                inter = list(Math_2D_Points_Lines_Intersection(O3[0], O3[1], O4[0], O4[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AG and arc < AB):
                inter = list(Math_2D_Points_Lines_Intersection(O1[0], O1[1], O2[0], O2[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AB or arc < AR):
                inter = list(Math_2D_Points_Lines_Intersection(O5[0], O5[1], O6[0], O6[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif (diagonal > 1 and diagonal < 2):
            # Angles according to O45(RED) as Origin
            A1 = Math_2D_Points_Lines_Angle(O1[0], O1[1], 0, 0, O45[0], O45[1]) # O1
            A2 = Math_2D_Points_Lines_Angle(O2[0], O2[1], 0, 0, O45[0], O45[1]) # O2
            A3 = Math_2D_Points_Lines_Angle(O3[0], O3[1], 0, 0, O45[0], O45[1]) # O3
            A4 = Math_2D_Points_Lines_Angle(O4[0], O4[1], 0, 0, O45[0], O45[1]) # O4
            A5 = Math_2D_Points_Lines_Angle(O5[0], O5[1], 0, 0, O45[0], O45[1]) # O5
            A6 = Math_2D_Points_Lines_Angle(O6[0], O6[1], 0, 0, O45[0], O45[1]) # O6
            # Certain
            if arc == A1:
                total = Math_2D_Points_Distance(0, 0, O1[0], O1[1])
            elif arc == A2:
                total = Math_2D_Points_Distance(0, 0, O2[0], O2[1])
            elif arc == A3:
                total = Math_2D_Points_Distance(0, 0, O3[0], O3[1])
            elif arc == A4:
                total = Math_2D_Points_Distance(0, 0, O4[0], O4[1])
            elif arc == A5:
                total = Math_2D_Points_Distance(0, 0, O5[0], O5[1])
            elif arc == A6:
                total = Math_2D_Points_Distance(0, 0, O6[0], O6[1])
            # Intervals
            elif (arc > A4 and arc < A3): # 0
                inter = list(Math_2D_Points_Lines_Intersection(O4[0], O4[1], O3[0], O3[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A3 and arc < A2): # 60
                inter = list(Math_2D_Points_Lines_Intersection(O3[0], O3[1], O2[0], O2[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A2 and arc < A1): # 120
                inter = list(Math_2D_Points_Lines_Intersection(O2[0], O2[1], O1[0], O1[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A1 and arc < A6): # 180
                inter = list(Math_2D_Points_Lines_Intersection(O1[0], O1[1], O6[0], O6[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A6 and arc < A5): # 240
                inter = list(Math_2D_Points_Lines_Intersection(O6[0], O6[1], O5[0], O5[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A5 or arc < A4): # 300
                inter = list(Math_2D_Points_Lines_Intersection(O5[0], O5[1], O4[0], O4[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif (diagonal >= 2 and diagonal < 3):
            # Angles according to O45(RED) as Origin
            AY = Math_2D_Points_Lines_Angle(O34[0], O34[1], 0, 0, O45[0], O45[1]) # YELLOW
            AC = Math_2D_Points_Lines_Angle(O12[0], O12[1], 0, 0, O45[0], O45[1]) # CYAN
            AM = Math_2D_Points_Lines_Angle(O56[0], O56[1], 0, 0, O45[0], O45[1]) # MAGENTA
            # Certain
            if arc == AY:
                total = Math_2D_Points_Distance(0, 0, O34[0], O34[1])
            elif arc == AC:
                total = Math_2D_Points_Distance(0, 0, O12[0], O12[1])
            elif arc == AM:
                total = Math_2D_Points_Distance(0, 0, O56[0], O56[1])
            # Intervals
            elif (arc > AY and arc < AC):
                inter = list(Math_2D_Points_Lines_Intersection(O2[0], O2[1], O3[0], O3[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AC and arc < AM):
                inter = list(Math_2D_Points_Lines_Intersection(O1[0], O1[1], O6[0], O6[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AM or arc < AY):
                inter = list(Math_2D_Points_Lines_Intersection(O4[0], O4[1], O5[0], O5[1], 0, 0, u, v))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif diagonal >= 3:
            a = angle_live
            total = 1
        # Percentual Value of the distance from the center to the outside
        try:
            ratio = user / total
        except:
            ratio = user
        r = ratio
        # Correct out of Bound values
        a = Math_1D_Limit(a)
        r = Math_1D_Limit(r)
        d = Math_1D_Limit(d)
        return [a, r, d]
    def ard_to_uvd(a, r, d):
        # Update Origin Points
        uvd_hexagon_origins(d)
        # Angle according to normal zero axis +U right and counter clockwise
        a360 = a * 360
        arc = a360 - REDAXIS
        if a360 < REDAXIS:
            arc = (360 - REDAXIS) + a360
        # Intersection Vector line Point
        ucos =  math.cos(math.radians(arc))
        vsin = -math.sin(math.radians(arc))
        # Diagonal Depth
        diagonal = d * 3
        if diagonal <= 0:
            total = 1
        elif (diagonal > 0 and diagonal <= 1):
            # Angles according to +U(UVD) as Origin
            AR = Math_2D_Points_Lines_Angle(O45[0], O45[1], 0, 0, 1, 0) # RED
            AG = Math_2D_Points_Lines_Angle(O23[0], O23[1], 0, 0, 1, 0) # GREEN
            AB = Math_2D_Points_Lines_Angle(O61[0], O61[1], 0, 0, 1, 0) # BLUE
            # Certain
            if arc == AR: # RED
                total = Math_2D_Points_Distance(0, 0, O45[0], O45[1])
            elif arc == AG: # GREEN
                total = Math_2D_Points_Distance(0, 0, O23[0], O23[1])
            elif arc == AB: # BLUE
                total = Math_2D_Points_Distance(0, 0, O61[0], O61[1])
            # Intervals
            elif (arc > AR and arc < AG):
                inter = list(Math_2D_Points_Lines_Intersection(O3[0], O3[1], O4[0], O4[1], 0, 0, ucos, vsin))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AG or arc < AB):
                inter = list(Math_2D_Points_Lines_Intersection(O1[0], O1[1], O2[0], O2[1], 0, 0, ucos, vsin))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AB and arc < AR):
                inter = list(Math_2D_Points_Lines_Intersection(O5[0], O5[1], O6[0], O6[1], 0, 0, ucos, vsin))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif (diagonal > 1 and diagonal < 2):
            # Angles according to +U(UVD) as Origin
            A1 = Math_2D_Points_Lines_Angle(O1[0], O1[1], 0, 0, 1, 0) # P1
            A2 = Math_2D_Points_Lines_Angle(O2[0], O2[1], 0, 0, 1, 0) # P2
            A3 = Math_2D_Points_Lines_Angle(O3[0], O3[1], 0, 0, 1, 0) # P3
            A4 = Math_2D_Points_Lines_Angle(O4[0], O4[1], 0, 0, 1, 0) # P4
            A5 = Math_2D_Points_Lines_Angle(O5[0], O5[1], 0, 0, 1, 0) # P5
            A6 = Math_2D_Points_Lines_Angle(O6[0], O6[1], 0, 0, 1, 0) # P6
            # Certain
            if arc == A1:
                total = Math_2D_Points_Distance(0, 0, O1[0], O1[1])
            elif arc == A2:
                total = Math_2D_Points_Distance(0, 0, O2[0], O2[1])
            elif arc == A3:
                total = Math_2D_Points_Distance(0, 0, O3[0], O3[1])
            elif arc == A4:
                total = Math_2D_Points_Distance(0, 0, O4[0], O4[1])
            elif arc == A5:
                total = Math_2D_Points_Distance(0, 0, O5[0], O5[1])
            elif arc == A6:
                total = Math_2D_Points_Distance(0, 0, O6[0], O6[1])
            # Intervals
            elif (arc > A1 and arc < A6): # 180
                inter = list(Math_2D_Points_Lines_Intersection(O1[0], O1[1], O6[0], O6[1], 0, 0, ucos, vsin))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A6 and arc < A5): # 240
                inter = list(Math_2D_Points_Lines_Intersection(O6[0], O6[1], O5[0], O5[1], 0, 0, ucos, vsin))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A5 and arc < A4): # 300
                inter = list(Math_2D_Points_Lines_Intersection(O5[0], O5[1], O4[0], O4[1], 0, 0, ucos, vsin))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > A4 and arc < A3): # 0
                inter = list(Math_2D_Points_Lines_Intersection(O4[0], O4[1], O3[0], O3[1], 0, 0, ucos, vsin))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            # Desambiguiation due to A2 crossing the Origin Axis
            elif A2 < 180:
                if (arc > A3 or arc < A2): # 60 OR
                    inter = list(Math_2D_Points_Lines_Intersection(O3[0], O3[1], O2[0], O2[1], 0, 0, ucos, vsin))
                    total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
                if (arc > A2 and arc < A1): # 120 AND
                    inter = list(Math_2D_Points_Lines_Intersection(O2[0], O2[1], O1[0], O1[1], 0, 0, ucos, vsin))
                    total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif A2 > 180:
                if (arc > A3 and arc < A2): # 60 AND
                    inter = list(Math_2D_Points_Lines_Intersection(O3[0], O3[1], O2[0], O2[1], 0, 0, ucos, vsin))
                    total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
                if (arc > A2 or arc < A1): # 120 OR
                    inter = list(Math_2D_Points_Lines_Intersection(O2[0], O2[1], O1[0], O1[1], 0, 0, ucos, vsin))
                    total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif (diagonal >= 2 and diagonal < 3):
            # Angles according to +U(UVD) as Origin
            AY = Math_2D_Points_Lines_Angle(O34[0], O34[1], 0, 0, 1, 0) # YELLOW
            AC = Math_2D_Points_Lines_Angle(O12[0], O12[1], 0, 0, 1, 0) # CYAN
            AM = Math_2D_Points_Lines_Angle(O56[0], O56[1], 0, 0, 1, 0) # MAGENTA
            # Certain
            if arc == AY:
                total = Math_2D_Points_Distance(0, 0, O34[0], O34[1])
            elif arc == AC:
                total = Math_2D_Points_Distance(0, 0, O12[0], O12[1])
            elif arc == AM:
                total = Math_2D_Points_Distance(0, 0, O56[0], O56[1])
            # Intervals
            elif (arc > AY or arc < AC):
                inter = list(Math_2D_Points_Lines_Intersection(O2[0], O2[1], O3[0], O3[1], 0, 0, ucos, vsin))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AC and arc < AM):
                inter = list(Math_2D_Points_Lines_Intersection(O1[0], O1[1], O6[0], O6[1], 0, 0, ucos, vsin))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
            elif (arc > AM and arc < AY):
                inter = list(Math_2D_Points_Lines_Intersection(O4[0], O4[1], O5[0], O5[1], 0, 0, ucos, vsin))
                total = Math_2D_Points_Distance(0, 0, inter[0], inter[1])
        elif diagonal >= 3:
            total = 1
        # User Distance to Center
        user = r * total
        u = user * math.cos(math.radians(arc))
        v = user * -math.sin(math.radians(arc))
        # Correct UV for D extreme value
        if (d==0 or d==1):
            u = 0
            v = 0
        return [u, v, d]
    # ARD
    def rgb_to_ard(r, g, b):
        uvd = rgb_to_uvd(r, g, b)
        ard = uvd_to_ard(uvd[0], uvd[1], uvd[2])
        a = ard[0]
        r = ard[1]
        d = ard[2]
        if r == 0:
            a = angle_live
        return [a, r, d]
    def ard_to_rgb(a, r, d):
        uvd = ard_to_uvd(a, r, d)
        rgb = uvd_to_rgb(uvd[0], uvd[1], uvd[2])
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return [r, g, b]
    # HUE
    def rgb_to_hue(r, g, b):
        maxc = max(r, g, b)
        minc = min(r, g, b)
        if minc == maxc:
            # return [0.0]
            return [angle_live]
        rc = (maxc-r) / (maxc-minc)
        gc = (maxc-g) / (maxc-minc)
        bc = (maxc-b) / (maxc-minc)
        if r == maxc:
            h = bc-gc
        elif g == maxc:
            h = 2.0 + rc - bc
        else:
            h = 4.0 + gc - rc
        h = ( h / 6.0 ) % 1.0
        return [h]
    def hue_to_rgb(h):
        vh = h * 6
        if vh == 6 :
            vh = 0
        vi = int( vh )
        v2 = 1 * ( 1 - 1 * ( vh - vi ) )
        v3 = 1 * ( 1 - 1 * ( 1 - ( vh - vi ) ) )
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
        return [r, g, b]
    # HSI ????????????????????????????????????????????????????
    def rgb_to_hsi_old(r, g, b):
        # In case Krita is in Linear Format
        if d_cd != "U8":
            lsl = lrgb_to_srgb(r, g, b)
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        # sRGB to HSX
        i = (r + g + b) / 3
        m = min(r,g,b)
        s = 1 - (3/(r+g+b))*m
        if g > b:
            h = math.acos( ((r-g)+(r-b)) / ((r-g)**2+((r-b)(g-b)))**0.5 )
        else:
            h = 360 - h
        h = h / 360
        return [h, s, i]
    def hsi_to_rgb_old(h, s, i):
        # HSX to sRGB
        hue = h * 6
        z = (1 - abs(math.fmod(hue, 2) - 1) ) * s
        c = (3 * i * s) / (1 + z)
        x = c * z
        if (hue >= 0 and hue < 1):
            r = c
            g = x
            b = 0
        elif (hue >= 1 and hue < 2):
            r = x
            g = c
            b = 0
        elif (hue >= 2 and hue < 3):
            r = 0
            g = c
            b = x
        elif (hue >= 3 and hue < 4):
            r = 0
            g = x
            b = c
        elif (hue >= 4 and hue < 5):
            r = x
            g = 0
            b = c
        elif (hue >= 5 and hue <= 6):
            r = c
            g = 0
            b = x
        else:
            r = 0
            g = 0
            b = 0
        m = i * ( 1 - s )
        r = r + m
        g = g + m
        b = b + m
        # In case Krita is in Linear Format
        if d_cd != "U8":
            lsl = srgb_to_lrgb(r, g, b)
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        return [r, g, b]

    def rgb_to_hsi(r, g, b):
        return [h, s, i]
    def hsi_to_rgb(h, s, i):
        return [r, g, b]

    # HSV
    def rgb_to_hsv(r, g, b):
        # In case Krita is in Linear Format
        if d_cd != "U8":
            lsl = lrgb_to_srgb(r, g, b)
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        # sRGB to HSX
        v_min = min( r, g, b )
        v_max = max( r, g, b )
        d_max = v_max - v_min
        v = v_max
        if d_max == 0:
            h = angle_live
            s = 0
        else:
            s = d_max / v_max
            d_r = ( ( ( v_max - r ) / 6 ) + ( d_max / 2 ) ) / d_max
            d_g = ( ( ( v_max - g ) / 6 ) + ( d_max / 2 ) ) / d_max
            d_b = ( ( ( v_max - b ) / 6 ) + ( d_max / 2 ) ) / d_max
            if r == v_max :
                h = d_b - d_g
            elif g == v_max :
                h = ( 1 / 3 ) + d_r - d_b
            elif b == v_max :
                h = ( 2 / 3 ) + d_g - d_r
            if h < 0 :
                h += 1
            if h > 1 :
                h -= 1
        return [h, s, v]
    def hsv_to_rgb(h, s, v):
        # HSX to sRGB
        if s == 0:
            r = v
            g = v
            b = v
        else:
            vh = h * 6
            if vh == 6 :
                vh = 0
            vi = int( vh )
            v1 = v * ( 1 - s )
            v2 = v * ( 1 - s * ( vh - vi ) )
            v3 = v * ( 1 - s * ( 1 - ( vh - vi ) ) )
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
        if d_cd != "U8":
            lsl = srgb_to_lrgb(r, g, b)
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        return [r, g, b]
    # HSL
    def rgb_to_hsl(r, g, b):
        # In case Krita is in Linear Format
        if d_cd != "U8":
            lsl = lrgb_to_srgb(r, g, b)
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        # sRGB to HSX
        v_min = min( r, g, b )
        v_max = max( r, g, b )
        d_max = v_max - v_min
        l = ( v_max + v_min )/ 2
        if d_max == 0 :
            h = angle_live
            s = 0
        else:
            if l < 0.5 :
                s = d_max / ( v_max + v_min )
            else:
                s = d_max / ( 2 - v_max - v_min )
            d_r = ( ( ( v_max - r ) / 6 ) + ( d_max / 2 ) ) / d_max
            d_g = ( ( ( v_max - g ) / 6 ) + ( d_max / 2 ) ) / d_max
            d_b = ( ( ( v_max - b ) / 6 ) + ( d_max / 2 ) ) / d_max
            if r == v_max :
                h = d_b - d_g
            elif g == v_max:
                h = ( 1 / 3 ) + d_r - d_b
            elif b == v_max:
                h = ( 2 / 3 ) + d_g - d_r
            if h < 0:
                h += 1
            if h > 1:
                h -= 1
        return [h, s, l]
    def hsl_to_rgb(h, s, l):
        if s == 0 :
            r = l
            g = l
            b = l
        else:
            if l < 0.5:
                v2 = l * ( 1 + s )
            else:
                v2 = ( l + s ) - ( s * l )
            v1 = 2 * l - v2
            r = hsl_chan( v1, v2, h + ( 1 / 3 ) )
            g = hsl_chan( v1, v2, h )
            b = hsl_chan( v1, v2, h - ( 1 / 3 ) )
        # In case Krita is in Linear Format
        if d_cd != "U8":
            lsl = srgb_to_lrgb(r, g, b)
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        return [r, g, b]
    def hsl_chan(v1, v2, vh):
        if vh < 0 :
            vh += 1
        if vh > 1 :
            vh -= 1
        if ( 6 * vh ) < 1 :
            return ( v1 + ( v2 - v1 ) * 6 * vh )
        if ( 2 * vh ) < 1 :
            return ( v2 )
        if ( 3 * vh ) < 2 :
            return ( v1 + ( v2 - v1 ) * ( ( 2 / 3 ) - vh ) * 6 )
        return ( v1 )
    # HSY (Krita version)
    def rgb_to_hsy(r, g, b):
        # In case Krita is NOT in Linear Format
        if d_cd == "U8":
            lsl = srgb_to_lrgb(r, g, b)
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        # sRGB to HSX
        minval = min(r, g, b)
        maxval = max(r, g, b)
        luma= (luma_r*r + luma_g*g + luma_b*b)
        luma_a = luma
        chroma = maxval-minval
        max_sat = 0.5
        if chroma == 0:
            hue = angle_live
            sat = 0
        else:
            if maxval == r:
                if minval == b:
                    hue = (g-b)/chroma
                else:
                    hue = (g-b)/chroma + 6.0
            elif maxval == g:
                hue = (b-r)/chroma + 2.0
            elif maxval == b:
                hue = (r-g)/chroma + 4.0
            hue /=6.0
            # segment = 0.166667
            segment = 1/6
            if (hue > 1.0 or hue < 0.0):
                hue = math.fmod(hue, 1.0)
            if (hue>=0.0 and hue<segment):
                max_sat = luma_r + luma_g*(hue*6)
            elif (hue>=segment and hue<(2.0*segment)):
                max_sat = (luma_g+luma_r) - luma_r*((hue-segment)*6)
            elif (hue>=(2.0*segment) and hue<(3.0*segment)):
                max_sat = luma_g + luma_b*((hue-2.0*segment)*6)
            elif (hue>=(3.0*segment) and hue<(4.0*segment)):
                max_sat = (luma_b+luma_g) - luma_g*((hue-3.0*segment)*6)
            elif (hue>=(4.0*segment) and hue<(5.0*segment)):
                max_sat =  (luma_b) + luma_r*((hue-4.0*segment)*6)
            elif (hue>=(5.0*segment) and hue<=1.0):
                max_sat = (luma_r+luma_b) - luma_b*((hue-5.0*segment)*6)
            else:
                max_sat=0.5

            if(max_sat>1.0 or max_sat<0.0):
                max_sat = math.fmod(max_sat, 1.0)
            if luma <= max_sat:
                luma_a = (luma/max_sat)*0.5
            else:
                luma_a = ((luma-max_sat)/(1-max_sat)*0.5)+0.5

            if (chroma > 0.0):
                sat = ((chroma/(2*luma_a)) if (luma <= max_sat) else (chroma/(2.0-(2*luma_a))))
        if sat<=0.0:
            sat=0.0
        if luma<=0.0:
            luma=0.0
        h=hue
        s=sat
        y=luma**(1/gamma_y)
        return [h, s, y]
    def hsy_to_rgb(h, s, y):
        hue = 0.0
        sat = 0.0
        luma = 0.0
        if ( h > 1.0 or h < 0.0):
            hue = math.fmod(h, 1.0)
        else:
            hue = h
        if s < 0.0:
            sat = 0.0
        else:
            sat = s
        if y < 0.0:
            luma = 0.0
        else:
            luma = y**(gamma_y)
        # segment = 0.166667
        segment = 1/6
        r=0.0
        g=0.0
        b=0.0
        if (hue >= 0.0 and hue < segment):
            max_sat = luma_r + ( luma_g*(hue*6) )
            if luma <= max_sat:
                luma_a = (luma/max_sat)*0.5
                chroma=sat*2*luma_a
            else:
                luma_a = ((luma-max_sat)/(1-max_sat)*0.5)+0.5
                chroma=sat*(2-2*luma_a)

            fract = hue*6.0
            x = (1-abs(math.fmod(fract, 2)-1))*chroma
            r = chroma
            g=x
            b=0
            m = luma-( (luma_r*r)+(luma_b*b)+(luma_g*g) )
            r += m
            g += m
            b += m
        elif (hue >= (segment) and hue < (2.0*segment)):
            max_sat = (luma_g+luma_r) - (luma_r*(hue-segment)*6)

            if luma<max_sat:
                luma_a = (luma/max_sat)*0.5
                chroma = sat*(2*luma_a)
            else:
                luma_a = ((luma-max_sat)/(1-max_sat)*0.5)+0.5
                chroma=sat*(2-2*luma_a)

            fract = hue*6.0
            x = (1-abs(math.fmod(fract, 2)-1) )*chroma
            r = x
            g=chroma
            b=0
            m = luma-( (luma_r*r)+(luma_b*b)+(luma_g*g) )
            r += m
            g += m
            b += m
        elif (hue >= (2.0*segment) and hue < (3.0*segment)):
            max_sat = luma_g + (luma_b*(hue-2.0*segment)*6)
            if luma<max_sat:
                luma_a = (luma/max_sat)*0.5
                chroma=sat*(2*luma_a)
            else:
                luma_a = ((luma-max_sat)/(1-max_sat)*0.5)+0.5
                chroma=sat*(2-2*luma_a)
            fract = hue*6.0
            x = (1-abs(math.fmod(fract,2)-1) )*chroma
            r = 0
            g=chroma
            b=x
            m = luma-( (luma_r*r)+(luma_b*b)+(luma_g*g) )
            r += m
            g += m
            b += m
        elif (hue >= (3.0*segment) and hue < (4.0*segment)):
            max_sat = (luma_g+luma_b) - (luma_g*(hue-3.0*segment)*6)
            if luma<max_sat:
                luma_a = (luma/max_sat)*0.5
                chroma=sat*(2*luma_a)
            else:
                luma_a = ((luma-max_sat)/(1-max_sat)*0.5)+0.5
                chroma=sat*(2-2*luma_a)

            fract = hue*6.0
            x = (1-abs(math.fmod(fract,2)-1) )*chroma
            r = 0
            g=x
            b=chroma
            m = luma-( (luma_r*r)+(luma_b*b)+(luma_g*g) )
            r += m
            g += m
            b += m
        elif (hue >= (4.0*segment) and hue < (5*segment)):
            max_sat = luma_b + (luma_r*((hue-4.0*segment)*6))
            if luma<max_sat:
                luma_a = (luma/max_sat)*0.5
                chroma=sat*(2*luma_a)
            else:
                luma_a = ((luma-max_sat)/(1-max_sat)*0.5)+0.5
                chroma=sat*(2-2*luma_a)

            fract = hue*6.0
            x = (1-abs(math.fmod(fract,2)-1) )*chroma
            r = x
            g=0
            b=chroma
            m = luma-( (luma_r*r)+(luma_b*b)+(luma_g*g) )
            r += m
            g += m
            b += m
        elif (hue >= (5.0*segment) and hue <= 1.0):
            max_sat = (luma_b+luma_r) - (luma_b*(hue-5.0*segment)*6)
            if (luma<max_sat):
                luma_a = (luma/max_sat)*0.5
                chroma=sat*(2*luma_a)
            else:
                luma_a = ((luma-max_sat)/(1-max_sat)*0.5)+0.5
                chroma=sat*(2-2*luma_a)

            fract = hue*6.0
            x = (1-abs(math.fmod(fract,2)-1) )*chroma
            r = chroma
            g=0
            b=x
            m = luma-( (luma_r*r)+(luma_b*b)+(luma_g*g) )
            r += m
            g += m
            b += m
        else:
            r=0.0
            g=0.0
            b=0.0
        if r<0.0:
            r=0.0
        if g<0.0:
            g=0.0
        if b<0.0:
            b=0.0
        # In case Krita is NOT in Linear Format
        if d_cd == "U8":
            lsl = lrgb_to_srgb(r, g, b)
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        return [r, g, b]
    # HCY (My Paint Version)
    def rgb_to_hcy(r, g, b):
        # In case Krita is NOT in Linear Format
        if d_cd != "U8": # == vs !=
            lsl = srgb_to_lrgb(r, g, b)
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        # sRGB to HSX
        y = luma_r*r + luma_g*g + luma_b*b
        p = max(r, g, b)
        n = min(r, g, b)
        d = p - n
        if n == p:
            h = angle_live
        elif p == r:
            h = (g - b)/d
            if h < 0:
                h += 6.0
        elif p == g:
            h = ((b - r)/d) + 2.0
        else:  # p==b
            h = ((r - g)/d) + 4.0
        h /= 6.0
        if (r == g == b or y == 0 or y == 1):
            h = angle_live
            c = 0.0
        else:
            c = max((y-n)/y, (p-y)/(1-y))
        if d_cd != "U8": # == vs !=
            y = y**(1/gamma_y) # Gama compression of the luma value
        return [h, c, y]
    def hcy_to_rgb(h, c, y):
        if d_cd != "U8": # == vs !=
            y = y**(gamma_y) # Gama compression of the luma value
        if c == 0:
            r = y
            g = y
            b = y
        h %= 1.0
        h *= 6.0
        if h < 1:
            th = h
            tm = luma_r + luma_g * th
        elif h < 2:
            th = 2.0 - h
            tm = luma_g + luma_r * th
        elif h < 3:
            th = h - 2.0
            tm = luma_g + luma_b * th
        elif h < 4:
            th = 4.0 - h
            tm = luma_b + luma_g * th
        elif h < 5:
            th = h - 4.0
            tm = luma_b + luma_r * th
        else:
            th = 6.0 - h
            tm = luma_r + luma_b * th
        # Calculate the RGB components in sorted order
        if tm >= y:
            p = y + y*c*(1-tm)/tm
            o = y + y*c*(th-tm)/tm
            n = y - (y*c)
        else:
            p = y + (1-y)*c
            o = y + (1-y)*c*(th-tm)/(1-tm)
            n = y - (1-y)*c*tm/(1-tm)
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
        if d_cd != "U8": # == vs !=
            lsl = lrgb_to_srgb(r, g, b)
            r = lsl[0]
            g = lsl[1]
            b = lsl[2]
        return [r, g, b]

    #//
    #\\ XYZ ####################################################################
    # XYZ (sRGB)
    def rgb_to_xyz(r, g, b):
        lrgb = srgb_to_lrgb(r, g, b)
        x = (lrgb[0] * m_rgb_xyz[0][0]) + (lrgb[1] * m_rgb_xyz[0][1]) + (lrgb[2] * m_rgb_xyz[0][2])
        y = (lrgb[0] * m_rgb_xyz[1][0]) + (lrgb[1] * m_rgb_xyz[1][1]) + (lrgb[2] * m_rgb_xyz[1][2])
        z = (lrgb[0] * m_rgb_xyz[2][0]) + (lrgb[1] * m_rgb_xyz[2][1]) + (lrgb[2] * m_rgb_xyz[2][2])
        return [x, y, z]
    def xyz_to_rgb(x, y, z):
        var_r = (x * m_xyz_rgb[0][0]) + (y * m_xyz_rgb[0][1]) + (z * m_xyz_rgb[0][2])
        var_g = (x * m_xyz_rgb[1][0]) + (y * m_xyz_rgb[1][1]) + (z * m_xyz_rgb[1][2])
        var_b = (x * m_xyz_rgb[2][0]) + (y * m_xyz_rgb[2][1]) + (z * m_xyz_rgb[2][2])
        srgb = lrgb_to_srgb(var_r, var_g, var_b)
        r = Math_1D_Limit(srgb[0])
        g = Math_1D_Limit(srgb[1])
        b = Math_1D_Limit(srgb[2])
        return [r, g, b]
    # XYY
    def xyz_to_xyy(x, y, z):
        if (x == 0 and y == 0 and z == 0):
            x1 = 0.31272660439158345
            y2 = 0.3290231524027522
            y3 = y
        else:
            x1 = x / ( x + y + z )
            y2 = y / ( x + y + z )
            y3 = y
        return [x1, y2, y3]
    def xyy_to_xyz(x1, y2, y3):
        if y2 == 0:
            x = 0
            y = 0
            z = 0
        else:
            x = ( x1 * y3 ) / y2
            y = y3
            z = (( 1 - x1 - y2) * y3) / y2
        return [x, y, z]
    # LUV ??????????????????????????????????????????? REF
    def xyz_to_luv_old(x, y, z):
        try:
            vu = ( 4 * x ) / ( x + ( 15 * y ) + ( 3 * z ) )
            vv = ( 9 * y ) / ( x + ( 15 * y ) + ( 3 * z ) )
            vy = y / 100
            if vy > 0.008856:
                vy = vy ** ( 1/3 )
            else:
                vy = ( 7.787 * vy ) + ( 16 / 116 )
            ru = ( 4 * ref_x ) / ( ref_x + ( 15 * ref_y ) + ( 3 * ref_z ) )
            rv = ( 9 * ref_y ) / ( ref_x + ( 15 * ref_y ) + ( 3 * ref_z ) )
            l = ( 116 * vy ) - 16
            u = 13 * l * ( vu - ru )
            v = 13 * l * ( vv - rv )
        except:
            l = 0
            u = 0
            v = 0
        return [l, u, v]
    def luv_to_xyz_old(l, u, v):
        try:
            vy = ( l + 16 ) /116
            if (vy**3) > 0.008856:
                vy = vy**3
            else:
                vy = ( vy - 16 / 116 ) / 7.787
            ru = ( 4 * ref_x ) / ( ref_x + ( 15 * ref_y ) + ( 3 * ref_z ) )
            rv = ( 9 * ref_y ) / ( ref_x + ( 15 * ref_y ) + ( 3 * ref_z ) )
            vu = u / ( 13 * l ) + ru
            vv = v / ( 13 * l ) + rv
            y = vy * 100
            x =  - ( 9 * y * vu ) / ( ( vu - 4 ) * vv - vu * vv )
            z = ( 9 * y - ( 15 * vv * y ) - ( vv * x ) ) / ( 3 * vv )
        except:
            x = 0
            y = 0
            z = 0
        return [x, y, z]

    def xyz_to_luv(x, y, z):
        k = 903.3
        e = 0.008856

        try:
            yr = y / ref_y

            ud =  (4*x) / ( x + (15*y) + (3*z) )
            vd =  (9*x) / ( x + (15*y) + (3*z) )

            udr = ( 4 * ref_x ) / ( ref_x + ( 15 * ref_y ) + ( 3 * ref_z ) )
            vdr = ( 9 * ref_y ) / ( ref_x + ( 15 * ref_y ) + ( 3 * ref_z ) )

            if yr > e:
                l = 116 * yr**(1/3) - 16
            else:
                l = k * yr
            u = 13 * l * (ud - udr)
            v = 13 * l * (vd - vdr)
        except:
            l = 0
            u = 0
            v = 0

        return [l, u, v]
    def luv_to_xyz(l, u, v):
        k = 903.3
        e = 0.008856

        try:
            if l > (k*e):
                y = (( l + 16 ) / 116 )**3
            else:
                y = l / k

            uo = ( 4 * ref_x ) / ( ref_x + ( 15 * ref_y ) + ( 3 * ref_z ) )
            vo = ( 9 * ref_y ) / ( ref_x + ( 15 * ref_y ) + ( 3 * ref_z ) )

            a = (1/3) * ((( 52 * l )/( u + (13*l*uo) )) - 1 )
            b = -5*y
            c = -(1/3)
            d = y * ( (( 39 * l )/( v + (13*l*vo) )) - 5 )

            x = (d - b) / (a - c)
            z = (x*a) + b
        except:
            x = 0
            y = 0
            z = 0

        return [x, y, z]

    # Hunter LAB ???????????????????????????????????? REF
    def xyz_to_hlab(x, y, z):
        va = ( 175.0 / 198.04 ) * ( ref_y + ref_x )
        vb = (  70.0 / 218.11 ) * ( ref_y + ref_z )
        hl = 100.0 * sqrt( Y / ref_y )
        ha = va * ( ( ( x / ref_x ) - ( y / ref_y ) ) / math.sqrt( y / ref_y ) )
        hb = vb * ( ( ( y / ref_y ) - ( z / ref_z ) ) / math.sqrt( y / ref_y ) )
        return [hl, ha, hb]
    def hlab_to_xyz(hl, ha, hb):
        va = ( 175.0 / 198.04 ) * ( ref_y + ref_x )
        vb = (  70.0 / 218.11 ) * ( ref_y + ref_z )
        y = ( ( hl / ref_y ) ** 2 ) * 100.0
        x =   ( ha / va * math.sqrt( y / ref_y ) + ( y / ref_y ) ) * ref_x
        z = - ( hb / vb * math.sqrt( y / ref_y ) - ( y / ref_y ) ) * ref_z
        return [x, y, z]
    # LAB ??????????????????????????????????????????? REF
    def xyz_to_lab(x, y, z):
        k = 903.3 # Kappa
        e = 0.008856 # Epsilon
        x_r = x / ref_x
        y_r = y / ref_y
        z_r = z / ref_z
        if x_r > e:
            f_x = x_r ** ( 1/3 )
        else:
            f_x = ( k * x_r +  16) / 116
        if y_r > e:
            f_y = y_r ** ( 1/3 )
        else:
            f_y = ( k * y_r + 16 ) / 116
        if z_r > e:
            f_z = z_r ** ( 1/3 )
        else:
            f_z = ( k * z_r + 16 ) / 116
        l = (( 116 * f_y ) - 16)
        a = ( f_x - f_y )  # 500 * ( f_x - f_y )
        b = ( f_y - f_z )  # 200 * ( f_y - f_z )
        l = l / 100
        a = 0.5 + a
        b = 0.5 + b
        return [l, a, b]
    def lab_to_xyz(l, a, b):
        k = 903.3 # Kappa
        e = 0.008856 # Epsilon
        l = l * 100
        a = a - 0.5
        b = b - 0.5
        f_y = ( l + 16 ) / 116
        f_x = a + f_y  # ( a / 500 ) + f_y
        f_z = f_y - b  # f_y - ( b / 200 )
        if (f_x**3) > e:
            x_r = f_x**3
        else:
            x_r = (( 116 * f_x ) - 16 ) / k
        if l > (k*e):
            y_r = (( l + 16 ) / 116 )**3
        else:
            y_r = l / k
        if (f_z**3) > e:
            z_r = f_z**3
        else:
            z_r = ((116 * f_z) - 16 ) / k
        x = x_r * ref_x
        y = y_r * ref_y
        z = z_r * ref_z
        return [x, y, z]
    def rgb_to_lab(r, g, b):
        xyz = rgb_to_xyz(r, g, b)
        lab = xyz_to_lab(xyz[0], xyz[1], xyz[2])
        return [lab[0], lab[1], lab[2]]
    def lab_to_rgb(l, a, b):
        xyz = lab_to_xyz(l, a, b)
        rgb = xyz_to_rgb(xyz[0], xyz[1], xyz[2])
        return [rgb[0], rgb[1], rgb[2]]
    # LCH ???????????????????????????????????????????
    def lab_to_lch(l, a, b):
        vh = math.atan( b, a )
        if vh > 0:
            vh = ( vh / math.pi ) * 180
        else:
            vh = 360 - ( abs( vh ) / math.pi ) * 180
        l = l
        c = math.sqrt( a ** 2 + b ** 2 )
        h = vh
        return [l, c, h]
    def lch_to_lab(l, c, h):
        l = l
        a = math.cos( radians(h) ) * c
        b = math.sin( radians(h) ) * c
        return [l, a, b]
    def xyz_to_lch(x, y, z):
        lab = xyz_to_lab(x, y, z)
        lch = lab_to_lch(lab[0], lab[1], lab[2])
        return [lch[0], lch[1], lch[2]]
    def lch_to_xyz(l, c, h):
        lab = lch_to_lab(x, y, z)
        xyz = lab_to_xyz(lab[0], lab[1], lab[2])
        return [xyz[0], xyz[1], xyz[2]]

    #//

class math():

    def M1D_Limit(var):
        if var <= 0:
            var = 0
        if var >= 1:
            var = 1
        return var
    def M1D_Loop(var):
        if var <= 0:
            var += 1
        if var >= 1:
            var -= 1
        return var
    def M1D_Lerp(v0, v1, t):
        return (v0+t*(v1-v0))
    def M2D_Points_Distance(x1, y1, x2, y2):
        dd = math.sqrt( math.pow((x1-x2),2) + math.pow((y1-y2),2) )
        return dd
    def M2D_Points_Lines_Intersection(x1, y1, x2, y2, x3, y3, x4, y4):
        try:
            xx = ((x2*y1-x1*y2)*(x4-x3)-(x4*y3-x3*y4)*(x2-x1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
            yy = ((x2*y1-x1*y2)*(y4-y3)-(x4*y3-x3*y4)*(y2-y1)) / ((x2-x1)*(y4-y3)-(x4-x3)*(y2-y1))
        except:
            xx = 0
            yy = 0
        return xx, yy
    def M2D_Points_Lines_Angle(x1, y1, x2, y2, x3, y3):
        v1 = (x1-x2, y1-y2)
        v2 = (x3-x2, y3-y2)
        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])
        angle = (v2_theta - v1_theta) * (180.0 / math.pi)
        if angle < 0:
            angle += 360.0
        return angle
    def M2D_Centroid_Triangle(a1, a2, b1, b2, c1, c2):
        cx = (a1+b1+c1)/3
        cy = (a2+b2+c2)/3
        return [cx, cy]
    def M2D_Centroid_Square(a1, a2, b1, b2, c1, c2, d1, d2):
        cx = (a1+b1+c1+d1)/4
        cy = (a2+b2+c2+d2)/4
        return [cx, cy]
    def M3D_Points_Distance(x1, y1, z1, x2, y2, z2):
        d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        return d
