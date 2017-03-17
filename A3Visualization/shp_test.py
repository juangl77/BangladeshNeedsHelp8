import shapefile as shp
import matplotlib.pyplot as plt

sf = shp.Reader("BGD_adm0.shp")

plt.figure()
for shape in sf.iterShapes():
	last_part = 0
	for part in shape.parts[1:]:
		x = [i[0] for i in shape.points[last_part:part]]
		y = [i[1] for i in shape.points[last_part:part]]
		plt.plot(x,y)
		last_part = part
plt.show()