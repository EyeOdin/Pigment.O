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

    def SVG_LMB(self, color1):
        color1 = str(color1)
        string_lmb = str(
        "<svg \n"+
        "   width=\"72pt\" \n"+
        "   height=\"72pt\" \n"+
        "   viewBox=\"0 0 72 72\" \n"+
        "   version=\"1.1\" \n"+
        "   id=\"svg54\"> \n"+
        "  <defs \n"+
        "     id=\"defs46\" /> \n"+
        "  <path \n"+
        "     style=\"fill:"+color1+";fill-rule:evenodd;stroke:none;stroke-width:0;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:0;fill-opacity:1\" \n"+
        "     d=\"M 48 0 C 21.408 0 0 21.408 0 48 C 0 54.863148 1.4347208 61.375921 4.0078125 67.269531 C 6.5788315 65.888574 9.5224519 65.103516 12.65625 65.103516 C 13.168364 65.103516 13.670683 65.138701 14.171875 65.179688 C 11.560014 60.026336 10.080078 54.193868 10.080078 48 C 10.080078 26.992316 26.992316 10.080078 48 10.080078 C 69.007684 10.080078 85.919922 26.992316 85.919922 48 C 85.919922 69.007684 69.007684 85.919922 48 85.919922 C 41.806132 85.919922 35.973664 84.439986 30.820312 81.828125 C 30.861299 82.329317 30.896484 82.831636 30.896484 83.34375 C 30.896484 86.477548 30.111426 89.421169 28.730469 91.992188 C 34.624079 94.565279 41.136852 96 48 96 C 74.592 96 96 74.592 96 48 C 96 21.408 74.592 0 48 0 z \" \n"+
        "     id=\"shape0\" \n"+
        "     transform=\"scale(0.75)\" \n"+
        "     inkscape:label=\"circle\" /> \n"+
        "  <rect \n"+
        "     id=\"shape02\" \n"+
        "     width=\"18.984152\" \n"+
        "     height=\"18.984152\" \n"+
        "     rx=\"9.4920759\" \n"+
        "     ry=\"9.4920759\" \n"+
        "     x=\"0\" \n"+
        "     y=\"53.01585\" \n"+
        "     style=\"fill:"+color1+";fill-rule:evenodd;stroke:none;stroke-width:0;stroke-linecap:square;stroke-linejoin:bevel;stroke-opacity:0;fill-opacity:1\" \n"+
        "     inkscape:label=\"dot\" /> \n"+
        "</svg> "
        )
        array_lmb = bytearray(string_lmb, encoding='utf-8')
        return array_lmb

    def SVG_Select(self, color2):
        color2 = str(color2)
        string_select = str(
        "<svg width=\"72pt\" height=\"72pt\" viewBox=\"0 0 72 72\" version=\"1.1\" id=\"svg54\"> \n"+
        "  <defs id=\"defs46\" /> \n"+
        "  <circle style=\"fill:"+color2+";fill-opacity:1;stroke:none;stroke-width:0.0\" id=\"path4518\" cx=\"36\" cy=\"36\" inkscape:label=\"select\" r=\"20.209631\" /> \n"+
        "</svg> "
        )
        array_select = bytearray(string_select, encoding='utf-8')
        return array_select

    def Alpha(self):
        alpha = str("background-color: rgba(0,0,0,0);")
        return alpha
