import krita

pigmento_pyid = "pykrita_pigment_o"
dockers = Krita.instance().dockers()
for i in range(0, len(dockers)):
    if dockers[i].objectName() == pigmento_pyid:
        pigment_o = dockers[i]

space = ["ARD"]
geo = ["4", "A", "D"]
directory = "C:\\Users\\EyeOd\\Desktop\\pigmento\\Directory"
render = "C:\\Users\\EyeOd\\Desktop\\pigmento\\Render"
for g in range(0, len(geo)):
    for s in range(0, len(space)):
        pigment_o.Script_Printer( space[s], geo[g], directory, render, None, None )