class Constants():
    """
    Color Space Model Constants
    """
    def Krita(self):
        factorAAA = 255
        factorRGB = 255
        factorHUE = 360
        factorSVL = 255
        factorCMYK = 255
        constant1 = [factorAAA, factorRGB, factorHUE, factorSVL, factorCMYK]
        return constant1

    def HEX(self):
        factorHEXAAA = 100
        factorHEXRGB = 255
        factorHEXHUE = 360
        factorHEXSVL = 100
        factorHEXCMYK = 100
        constant2 = [factorHEXAAA, factorHEXRGB, factorHEXHUE, factorHEXSVL, factorHEXCMYK]
        return constant2

    def LAB(self):
        # D65 - Daylight, sRGB, Adobe-RGB, 2ºC
        factorX=95.047
        factorY=100.000
        factorZ=108.883
        constant3 = [factorX, factorY, factorZ]
        return constant3
