from .pigment_o_constants import Constants

# Color Space Factors
constant3 = Constants().LAB()
factorX = constant3[0]
factorY = constant3[1]
factorZ = constant3[2]

# Some floating point constants
ONE_THIRD = 1.0/3.0
ONE_SIXTH = 1.0/6.0
TWO_THIRD = 2.0/3.0

class Convert():
    """
    Input range 0-1
    Output range 0-1
    """

    # HSV
    def rgb_to_hsv(self, r, g, b):
        maxc = max(r, g, b)
        minc = min(r, g, b)
        v = maxc
        if minc == maxc:
            return 0.0, 0.0, v
        s = (maxc-minc) / maxc
        rc = (maxc-r) / (maxc-minc)
        gc = (maxc-g) / (maxc-minc)
        bc = (maxc-b) / (maxc-minc)
        if r == maxc:
            h = bc-gc
        elif g == maxc:
            h = 2.0+rc-bc
        else:
            h = 4.0+gc-rc
        h = (h/6.0) % 1.0
        return h, s, v
    def hsv_to_rgb(self, h, s, v):
        if s == 0.0:
            return v, v, v
        i = int(h*6.0) # XXX assume int() truncates!
        f = (h*6.0) - i
        p = v*(1.0 - s)
        q = v*(1.0 - s*f)
        t = v*(1.0 - s*(1.0-f))
        i = i%6
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q

    # HSL
    def rgb_to_hsl(self, r, g, b):
        maxc = max(r, g, b)
        minc = min(r, g, b)
        # XXX Can optimize (maxc+minc) and (maxc-minc)
        l = (minc+maxc)/2.0
        if minc == maxc:
            return 0.0, l, 0.0
        if l <= 0.5:
            s = (maxc-minc) / (maxc+minc)
        else:
            s = (maxc-minc) / (2.0-maxc-minc)
        rc = (maxc-r) / (maxc-minc)
        gc = (maxc-g) / (maxc-minc)
        bc = (maxc-b) / (maxc-minc)
        if r == maxc:
            h = bc-gc
        elif g == maxc:
            h = 2.0+rc-bc
        else:
            h = 4.0+gc-rc
        h = (h/6.0) % 1.0
        return h, s, l
    def hsl_to_rgb(self, h, s, l):
        if s == 0.0:
            return l, l, l
        if l <= 0.5:
            m2 = l * (1.0+s)
        else:
            m2 = l+s-(l*s)
        m1 = 2.0*l - m2
        return (self._v(m1, m2, h+ONE_THIRD), self._v(m1, m2, h), self._v(m1, m2, h-ONE_THIRD))
    def _v(self, m1, m2, hue):
        hue = hue % 1.0
        if hue < ONE_SIXTH:
            return m1 + (m2-m1)*hue*6.0
        if hue < 0.5:
            return m2
        if hue < TWO_THIRD:
            return m1 + (m2-m1)*(TWO_THIRD-hue)*6.0
        return m1

    # CMYK
    def rgb_to_cmyk(self, r, g, b):
        q = max(r, g, b)
        if q == 0:
            c = 0
            m = 0
            y = 0
            k = 1
        else:
            k = 1-max(r, g, b)
            c = (1-r-k) / (1-k)
            m = (1-g-k) / (1-k)
            y = (1-b-k) / (1-k)
        return c, m, y, k
    def cmyk_to_rgb(self, c, m, y, k):
        r = (1-c) * (1-k)
        g = (1-m) * (1-k)
        b = (1-y) * (1-k)
        return r, g, b

    # XYZ
    def rgb_to_xyz(self, r, g, b):
        if r > 0.04045:
            r = ( ( r + 0.055 ) / 1.055 ) ** 2.4
        else:
            r = r / 12.92
        if g > 0.04045:
            g = ( ( g + 0.055 ) / 1.055 ) ** 2.4
        else:
            g = g / 12.92
        if b > 0.04045:
            b = ( ( b + 0.055 ) / 1.055 ) ** 2.4
        else:
            b = b / 12.92
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        return x, y, z
    def xyz_to_rgb(self, x, y, z):
        r = x *  3.2406 + y * -1.5372 + z * -0.4986
        g = x * -0.9689 + y *  1.8758 + z *  0.0415
        b = x *  0.0557 + y * -0.2040 + z *  1.0570
        if r > 0.0031308:
            r = 1.055 * ( r ** ( 1 / 2.4 ) ) - 0.055
        else:
            r = 12.92 * r
        if g > 0.0031308:
            g = 1.055 * ( g ** ( 1 / 2.4 ) ) - 0.055
        else:
            g = 12.92 * g
        if b > 0.0031308:
            b = 1.055 * ( b ** ( 1 / 2.4 ) ) - 0.055
        else:
            b = 12.92 * b
        return r, g, b

    # LAB
    def xyz_to_lab(self, x, y, z):
        if x > 0.008856:
            x = x ** ( 1/3 )
        else:
            x = ( 7.787 * x ) + ( 16 / 116 )
        if y > 0.008856:
            y = y ** ( 1/3 )
        else:
            y = ( 7.787 * y ) + ( 16 / 116 )
        if z > 0.008856:
            z = z ** ( 1/3 )
        else:
            z = ( 7.787 * z ) + ( 16 / 116 )
        l = ( 116 * y ) - 16
        a = 500 * ( x - y )
        b = 200 * ( y - z )
        l = l / factorX
        a = a / factorY
        b = b / factorZ
        return l, a, b
    def lab_to_xyz(self, l, a, b):
        y = ( l + 16 ) / 116
        x = a / 500 + y
        z = y - b / 200
        if (y**3)  > 0.008856:
            y = y**3
        else:
            y = ( y - 16 / 116 ) / 7.787
        if (x**3)  > 0.008856:
            x = x**3
        else:
            x = ( x - 16 / 116 ) / 7.787
        if (z**3)  > 0.008856:
            z = z**3
        else:
            z = ( z - 16 / 116 ) / 7.787
        return x, y, z

    # YIQ
    def rgb_to_yiq(self, r, g, b):
        y = 0.30*r + 0.59*g + 0.11*b
        i = 0.74*(r-y) - 0.27*(b-y)
        q = 0.48*(r-y) + 0.41*(b-y)
        return y, i, q
    def yiq_to_rgb(self, y, i, q):
        # r = y + (0.27*q + 0.41*i) / (0.74*0.41 + 0.27*0.48)
        # b = y + (0.74*q - 0.48*i) / (0.74*0.41 + 0.27*0.48)
        # g = y - (0.30*(r-y) + 0.11*(b-y)) / 0.59

        r = y + 0.9468822170900693*i + 0.6235565819861433*q
        g = y - 0.27478764629897834*i - 0.6356910791873801*q
        b = y - 1.1085450346420322*i + 1.7090069284064666*q

        if r < 0.0:
            r = 0.0
        if g < 0.0:
            g = 0.0
        if b < 0.0:
            b = 0.0
        if r > 1.0:
            r = 1.0
        if g > 1.0:
            g = 1.0
        if b > 1.0:
            b = 1.0
        return r, g, b
