import colorsys

factor_hsv1 = 360
factor_hsv23 = 100

class Style():
    """Style sheet for the pigment_o plugin menus."""

    def Slider(self, mode, ch, rgb1, rgb2, rgb3, hsv1, hsv2, hsv3):
        if mode == "RGB":
            # Gradient on each end
            gradients = [
            [   0*255, rgb2*255, rgb3*255,    1*255, rgb2*255, rgb3*255],
            [rgb1*255,    0*255, rgb3*255, rgb1*255,    1*255, rgb3*255],
            [rgb1*255, rgb2*255,    0*255, rgb1*255, rgb2*255,    1*255]]
            slider_gradient = str(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(%s, %s, %s, 255), stop:1 rgba(%s, %s, %s, 255)); \n" % (gradients[ch][0], gradients[ch][1], gradients[ch][2], gradients[ch][3], gradients[ch][4], gradients[ch][5]) +
            "border: 1px solid rgba(56, 56, 56, 255);")
        if mode == "HSV":
            # RGB points of representation for the Slider
            rgb_000 = colorsys.hsv_to_rgb(  0/360, hsv2, hsv3)
            rgb_060 = colorsys.hsv_to_rgb( 60/360, hsv2, hsv3)
            rgb_120 = colorsys.hsv_to_rgb(120/360, hsv2, hsv3)
            rgb_180 = colorsys.hsv_to_rgb(180/360, hsv2, hsv3)
            rgb_240 = colorsys.hsv_to_rgb(240/360, hsv2, hsv3)
            rgb_300 = colorsys.hsv_to_rgb(300/360, hsv2, hsv3)
            rgb_360 = colorsys.hsv_to_rgb(360/360, hsv2, hsv3)
            rgb_h0v = colorsys.hsv_to_rgb(hsv1, 0, hsv3)
            rgb_h1v = colorsys.hsv_to_rgb(hsv1, 1, hsv3)
            rgb_hs0 = colorsys.hsv_to_rgb(hsv1, hsv2, 0)
            rgb_hs1 = colorsys.hsv_to_rgb(hsv1, hsv2, 1)
            # Style Sheet for the Sliders in HSV
            if ch == 0:
                slider_gradient = str(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n " +
                "stop:0.000 rgba(%s, %s, %s, 255), \n " % (rgb_000[0]*255, rgb_000[1]*255, rgb_000[2]*255) +
                "stop:0.166 rgba(%s, %s, %s, 255), \n " % (rgb_060[0]*255, rgb_060[1]*255, rgb_060[2]*255) +
                "stop:0.333 rgba(%s, %s, %s, 255), \n " % (rgb_120[0]*255, rgb_120[1]*255, rgb_120[2]*255) +
                "stop:0.500 rgba(%s, %s, %s, 255), \n " % (rgb_180[0]*255, rgb_180[1]*255, rgb_180[2]*255) +
                "stop:0.666 rgba(%s, %s, %s, 255), \n " % (rgb_240[0]*255, rgb_240[1]*255, rgb_240[2]*255) +
                "stop:0.833 rgba(%s, %s, %s, 255), \n " % (rgb_300[0]*255, rgb_300[1]*255, rgb_300[2]*255) +
                "stop:1.000 rgba(%s, %s, %s, 255));\n " % (rgb_360[0]*255, rgb_360[1]*255, rgb_360[2]*255) +
                "border: 1px solid rgba(56, 56, 56, 255);")
            elif ch == 1:
                slider_gradient = str(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(%s, %s, %s, 255), stop:1 rgba(%s, %s, %s, 255)); \n" % (rgb_h0v[0]*255, rgb_h0v[1]*255, rgb_h0v[2]*255, rgb_h1v[0]*255, rgb_h1v[1]*255, rgb_h1v[2]*255) +
                "border: 1px solid rgba(56, 56, 56, 255);")
            elif ch == 2:
                slider_gradient = str(
                "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(%s, %s, %s, 255), stop:1 rgba(%s, %s, %s, 255)); \n" % (rgb_hs0[0]*255, rgb_hs0[1]*255, rgb_hs0[2]*255, rgb_hs1[0]*255, rgb_hs1[1]*255, rgb_hs1[2]*255) +
                "border: 1px solid rgba(56, 56, 56, 255);")
        return slider_gradient

    def Percentage(self, count):
        self.count = count
        if self.count == "4":
            percentage_style_sheet = str(
            "background-color: qlineargradient(spread:pad, \n"+
            "x1:0, y1:0, \n"+
            "x2:1, y2:0, \n"+
            "stop:0.000 rgba(255, 255, 255, 255), \n"+
            "stop:0.003 rgba(255, 255, 255, 255), \n"+
            "stop:0.004 rgba(0, 0, 0, 0), \n"+
            "stop:0.248 rgba(0, 0, 0, 0), \n"+
            "stop:0.249 rgba(255, 255, 255, 255), \n"+
            "stop:0.251 rgba(255, 255, 255, 255), \n"+
            "stop:0.252 rgba(0, 0, 0, 0), \n"+
            "stop:0.498 rgba(0, 0, 0, 0), \n"+
            "stop:0.499 rgba(255, 255, 255, 255), \n"+
            "stop:0.501 rgba(255, 255, 255, 255), \n"+
            "stop:0.502 rgba(0, 0, 0, 0), \n"+
            "stop:0.748 rgba(0, 0, 0, 0), \n"+
            "stop:0.749 rgba(255, 255, 255, 255), \n"+
            "stop:0.751 rgba(255, 255, 255, 255), \n"+
            "stop:0.752 rgba(0, 0, 0, 0), \n"+
            "stop:0.997 rgba(0, 0, 0, 0), \n"+
            "stop:0.998 rgba(255, 255, 255, 255), \n"+
            "stop:1.000 rgba(255, 255, 255, 255));"
            )
        elif self.count == "6":
            percentage_style_sheet = str(
            "background-color: qlineargradient(spread:pad, \n"+
            "x1:0, y1:0, \n"+
            "x2:1, y2:0, \n"+
            "stop:0.000 rgba(255, 255, 255, 255), \n"+
            "stop:0.003 rgba(255, 255, 255, 255), \n"+
            "stop:0.004 rgba(0, 0, 0, 0), \n"+
            "stop:0.164 rgba(0, 0, 0, 0), \n"+
            "stop:0.165 rgba(255, 255, 255, 255), \n"+
            "stop:0.167 rgba(255, 255, 255, 255), \n"+
            "stop:0.168 rgba(0, 0, 0, 0), \n"+
            "stop:0.331 rgba(0, 0, 0, 0), \n"+
            "stop:0.332 rgba(255, 255, 255, 255), \n"+
            "stop:0.334 rgba(255, 255, 255, 255), \n"+
            "stop:0.335 rgba(0, 0, 0, 0), \n"+
            "stop:0.498 rgba(0, 0, 0, 0), \n"+
            "stop:0.499 rgba(255, 255, 255, 255), \n"+
            "stop:0.501 rgba(255, 255, 255, 255), \n"+
            "stop:0.502 rgba(0, 0, 0, 0), \n"+
            "stop:0.664 rgba(0, 0, 0, 0), \n"+
            "stop:0.665 rgba(255, 255, 255, 255), \n"+
            "stop:0.667 rgba(255, 255, 255, 255), \n"+
            "stop:0.668 rgba(0, 0, 0, 0), \n"+
            "stop:0.831 rgba(0, 0, 0, 0), \n"+
            "stop:0.832 rgba(255, 255, 255, 255), \n"+
            "stop:0.834 rgba(255, 255, 255, 255), \n"+
            "stop:0.835 rgba(0, 0, 0, 0), \n"+
            "stop:0.997 rgba(0, 0, 0, 0), \n"+
            "stop:0.998 rgba(255, 255, 255, 255), \n"+
            "stop:1.000 rgba(255, 255, 255, 255));"
            )
        elif self.count == "10":
            percentage_style_sheet = str(
            "background-color: qlineargradient(spread:pad, \n"+
            "x1:0, y1:0, \n"+
            "x2:1, y2:0, \n"+
            "stop:0.000 rgba(0, 0, 0, 0), \n"+
            "stop:0.098 rgba(0, 0, 0, 0), \n"+
            "stop:0.099 rgba(0, 0, 0, 255), \n"+
            "stop:0.101 rgba(0, 0, 0, 255), \n"+
            "stop:0.102 rgba(0, 0, 0, 0), \n"+
            "stop:0.198 rgba(0, 0, 0, 0), \n"+
            "stop:0.199 rgba(0, 0, 0, 255), \n"+
            "stop:0.201 rgba(0, 0, 0, 255), \n"+
            "stop:0.202 rgba(0, 0, 0, 0), \n"+
            "stop:0.298 rgba(0, 0, 0, 0), \n"+
            "stop:0.299 rgba(0, 0, 0, 255), \n"+
            "stop:0.301 rgba(0, 0, 0, 255), \n"+
            "stop:0.302 rgba(0, 0, 0, 0), \n"+
            "stop:0.398 rgba(0, 0, 0, 0), \n"+
            "stop:0.399 rgba(0, 0, 0, 255), \n"+
            "stop:0.401 rgba(0, 0, 0, 255), \n"+
            "stop:0.402 rgba(0, 0, 0, 0), \n"+
            "stop:0.498 rgba(0, 0, 0, 0), \n"+
            "stop:0.499 rgba(0, 0, 0, 255), \n"+
            "stop:0.501 rgba(0, 0, 0, 255), \n"+
            "stop:0.502 rgba(0, 0, 0, 0), \n"+
            "stop:0.598 rgba(0, 0, 0, 0), \n"+
            "stop:0.599 rgba(0, 0, 0, 255), \n"+
            "stop:0.601 rgba(0, 0, 0, 255), \n"+
            "stop:0.602 rgba(0, 0, 0, 0), \n"+
            "stop:0.698 rgba(0, 0, 0, 0), \n"+
            "stop:0.699 rgba(0, 0, 0, 255), \n"+
            "stop:0.701 rgba(0, 0, 0, 255), \n"+
            "stop:0.702 rgba(0, 0, 0, 0), \n"+
            "stop:0.798 rgba(0, 0, 0, 0), \n"+
            "stop:0.799 rgba(0, 0, 0, 255), \n"+
            "stop:0.801 rgba(0, 0, 0, 255), \n"+
            "stop:0.802 rgba(0, 0, 0, 0), \n"+
            "stop:0.898 rgba(0, 0, 0, 0), \n"+
            "stop:0.899 rgba(0, 0, 0, 255), \n"+
            "stop:0.901 rgba(0, 0, 0, 255), \n"+
            "stop:0.902 rgba(0, 0, 0, 0), \n"+
            "stop:1.000 rgba(0, 0, 0, 0));"
            )
        elif self.count == "TEN":
            percentage_style_sheet = str(
            "background-color: qlineargradient(spread:pad, \n"+
            "x1:0, y1:0, \n"+
            "x2:1, y2:0, \n"+
            "stop:0.000 rgba(0, 0, 0, 50), \n"+
            "stop:0.099 rgba(0, 0, 0, 50), \n"+
            "stop:0.100 rgba(0, 0, 0, 0), \n"+
            "stop:0.199 rgba(0, 0, 0, 0), \n"+
            "stop:0.200 rgba(0, 0, 0, 50), \n"+
            "stop:0.299 rgba(0, 0, 0, 50), \n"+
            "stop:0.300 rgba(0, 0, 0, 0), \n"+
            "stop:0.399 rgba(0, 0, 0, 0), \n"+
            "stop:0.400 rgba(0, 0, 0, 50), \n"+
            "stop:0.499 rgba(0, 0, 0, 50), \n"+
            "stop:0.500 rgba(0, 0, 0, 0), \n"+
            "stop:0.599 rgba(0, 0, 0, 0), \n"+
            "stop:0.600 rgba(0, 0, 0, 50), \n"+
            "stop:0.699 rgba(0, 0, 0, 50), \n"+
            "stop:0.700 rgba(0, 0, 0, 0), \n"+
            "stop:0.799 rgba(0, 0, 0, 0), \n"+
            "stop:0.800 rgba(0, 0, 0, 50), \n"+
            "stop:0.899 rgba(0, 0, 0, 50), \n"+
            "stop:0.900 rgba(0, 0, 0, 0), \n"+
            "stop:0.999 rgba(0, 0, 0, 0), \n"+
            "stop:1.000 rgba(0, 0, 0, 50));"
            )
        return percentage_style_sheet

    def Alpha(self):
        alpha = str("background-color: rgba(0,0,0,0);")
        return alpha

    def SVG_Cursor_LMB(self):
        string_cursor_lmb = str(
        "<svg width=\"100\" height=\"100\" viewBox=\"0 0 75.000003 75.000003\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#000000;fill-opacity:1;stroke:none;stroke-width:1.47647631\" \n" +
        "     d=\"M 50,0 A 49.999998,49.999998 0 0 0 0,50 49.999998,49.999998 0 0 0 50,100 49.999998,49.999998 0 0 0 100,50 49.999998,49.999998 0 0 0 50,0 Z m 0,6 A 43.999998,43.999998 0 0 1 94,50 43.999998,43.999998 0 0 1 50,94 43.999998,43.999998 0 0 1 6,50 43.999998,43.999998 0 0 1 50,6 Z\" \n" +
        "     id=\"circle824\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     inkscape:label=\"Black\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#ffffff;fill-opacity:1;stroke:none;stroke-width:1.29929912\" \n" +
        "     d=\"M 50,6 A 43.999998,43.999998 0 0 0 6,50 43.999998,43.999998 0 0 0 50,94 43.999998,43.999998 0 0 0 94,50 43.999998,43.999998 0 0 0 50,6 Z m 0,6.5 A 37.500001,37.500001 0 0 1 87.5,50 37.500001,37.500001 0 0 1 50,87.5 37.500001,37.500001 0 0 1 12.5,50 37.500001,37.500001 0 0 1 50,12.5 Z\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     id=\"circle821\" \n" +
        "     inkscape:label=\"White\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "</svg> "
        )
        array_cursor_lmb = bytearray(string_cursor_lmb, encoding='utf-8')
        return array_cursor_lmb

    def SVG_Cursor_RMB(self, color):
        color = str(color)
        string_cursor_rmb = str(
        "<svg width=\"100\" height=\"100\" viewBox=\"0 0 75.000003 75.000003\" version=\"1.1\" id=\"svg54\"> \n" +
        "  <defs id=\"defs46\" /> \n" +
        "  <path \n" +
        "     style=\"display:inline;fill:\#000000;fill-opacity:1;stroke:none;stroke-width:1.47647631\" \n" +
        "     d=\"M 50,0 A 49.999998,49.999998 0 0 0 0,50 49.999998,49.999998 0 0 0 50,100 49.999998,49.999998 0 0 0 100,50 49.999998,49.999998 0 0 0 50,0 Z m 0,6 A 43.999998,43.999998 0 0 1 94,50 43.999998,43.999998 0 0 1 50,94 43.999998,43.999998 0 0 1 6,50 43.999998,43.999998 0 0 1 50,6 Z\" \n" +
        "     id=\"circle824\" \n" +
        "     transform=\"scale(0.75000003)\" \n" +
        "     inkscape:label=\"Black\" \n" +
        "     inkscape:connector-curvature=\"0\" /> \n" +
        "  <circle \n" +
        "     style=\"display:inline;fill:"+color+";fill-opacity:1;stroke:none;stroke-width:0.97447437\" \n" +
        "     id=\"circle816\" \n" +
        "     cx=\"37.5\" \n" +
        "     cy=\"37.500004\" \n" +
        "     inkscape:label=\"Color\" \n" +
        "     r=\"33\" /> \n" +
        "</svg> "
        )
        array_cursor_rmb = bytearray(string_cursor_rmb, encoding='utf-8')
        return array_cursor_rmb

    def HSV_Gradient(self, width, color_left, color_right):
        # Colors
        left = [color_left[3], color_left[4], color_left[5]]
        right = [color_right[3], color_right[4], color_right[5]]
        # Conditions
        cond1 = right[0] - left[0]
        cond2 = (left[0] + 360) - right[0]
        cond3 = right[2] - left[1]
        cond4 = right[2] - left[2]
        # Style String
        slider_gradient = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, \n "
        "stop:%s rgb(%s, %s, %s), " % (0.000, color_left[0], color_left[1], color_left[2])
        unit = 1 / width
        for i in range(width):
            # Stop
            stop = round((i * unit), 3)
            # HSV Calculation
            if cond1 <= cond2:
                hue = left[0] + (stop * cond1)
            else:
                hue = left[0] - (stop * cond2)
                if hue <= 0:
                    hue = hue + 360
                else:
                    pass
            hue = hue / 360
            sat = (left[1] + (stop * cond3)) / 100
            val = (left[2] + (stop * cond4)) / 100

            # HSV to RGB Conversion
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            red = round(rgb[0]*255,3)
            green = round(rgb[1]*255,3)
            blue = round(rgb[2]*255,3)
            # String
            slider_gradient += "stop:%s rgb(%s, %s, %s), \n " % (stop, red, green, blue)
        slider_gradient += "stop:%s rgb(%s, %s, %s) ) " % (1.000, color_right[0], color_right[1], color_right[2])
        # Return StyleSheet String
        return slider_gradient
