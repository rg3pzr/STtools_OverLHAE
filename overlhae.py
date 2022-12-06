import numpy
import json
from PIL import Image, ImageDraw, ImageColor
import copy
from shapely.geometry import Point, Polygon

def rgb_to_hex(rgb):
    return '#' + ('%02x%02x%02x' % rgb)

f = open("annotated_he_stain.json")

data = json.load(f)

annotations = data["annotations"]
polygons = []
for i in annotations:
    coords = i['segmentation'][0]
    points = []
    for j in range(0, len(coords) - 1, 2):
        a = coords[j]
        b = coords[j+1]
        if j == 0:
            startx = a
            starty = b
        points.append((a,b))
    points.append((startx, starty))

    polygons.append(points)

he = Image.open("HE_Test.png")
st = Image.open("ST_Test.png")

draw = ImageDraw.Draw(he)
draw2 = ImageDraw.Draw(st)

polygons2 = copy.deepcopy(polygons)
st_resized = st.resize(he.size)

pixels_st = st.load()
pixels_he = he.load()

for x in range(0, len(polygons2)):
    for y in range(0, len(polygons2[x])):
        ta, tb = polygons2[x][y]
        ta = ta + 20
        tb = tb - 10
        polygons2[x][y] = (ta, tb)

    draw.line(polygons[x], joint = "curve", width = 2, fill = "red")
    draw2.line(polygons2[x], joint = "curve", width = 2, fill = "red")

#he.show()
#st.show()
#Green, Orange, Light blue, Purple, dark blue, Red
st_colors = ["#7da43a", "#d59a5b", "#8ab8ac", "#a992bf", "#7795bb", "#aa363b"]

#find where in st image where specified hex value is, and if it is in one of the annotations,
#color that part of HE and also output to dataframe showing certain transcript is expressed there



st_width, st_height = st.size

for x in range(st_width):
    for y in range(st_height):
        (r, g, b, a) = pixels_st[x, y]
        hex_val = rgb_to_hex((r, g, b))
        if hex_val in st_colors:
            inBox = False
            for w in range(len(polygons)):
                p1 = Point(x, y)
                coords = polygons[w]
                poly = Polygon(coords)
                if p1.within(poly):
                    inBox = True
            if inBox:
                draw.point((x, y), fill = hex_val)
              
he.show()
