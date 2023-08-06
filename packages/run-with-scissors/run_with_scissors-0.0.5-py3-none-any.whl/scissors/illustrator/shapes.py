from essentials.elm import E
from essentials.vector import V

class Rect(E):
	def __init__(self, sp=V(0,0), w=10, h=10, stroke="black", fill="none", center=True):
		if self.isV(sp):
			super().__init__('rect', stroke, fill)
			if center:
				self.attributes['x'] = sp.p[0] - w / 2
				self.attributes['y'] = sp.p[1] - h / 2
				self.center = sp.copy()
			else:
				self.attributes['x'] = sp.p[0]
				self.attributes['y'] = sp.p[1]
				self.center = sp.copy()
				self.center.add(V(w/2, h/2))
			self.attributes['width'] = w
			self.attributes['height'] = h

class Circle(E):
	def __init__(self, center, r, stroke="black", fill="none"):
		if self.isV(center):
			super().__init__('circle', stroke, fill)
			self.center = center
			self.attributes['cx'] = center.p[0]
			self.attributes['cy'] = center.p[1]
			self.attributes['r'] = r


class Ellipse(E):
	def __init__(self, center, rx, ry, stroke="black", fill="none"):
		if self.isV(center):
			super().__init__('ellipse', stroke, fill)
			self.center = center
			self.attributes['cx'] = center.p[0]
			self.attributes['cy'] = center.p[1]
			self.attributes['rx'] =	rx
			self.attributes['ry'] = ry

class Line(E):
	def __init__(self, sp, end, stroke="black", fill="none"):
		if self.isVlist([sp, end]):
			super().__init__('line', stroke, fill)
			self.attributes['x1'] = sp.p[0]
			self.attributes['y1'] = sp.p[1]
			self.attributes['x2'] = end.p[0]
			self.attributes['y2'] = end.p[1]

class Polygon(E):
	def __init__(self, points, stroke="black", fill="none"):
		if self.isVlist(points):
			super().__init__('polygon', stroke, fill)
			self.attributes['points'] = ""
			for point in points:
				self.attributes['points'] += point.format()

class Polyline(E):
	def __init__(self, points, stroke="black", fill="none"):
		if self.isVlist(points):
			super().__init__('polyline', stroke, fill)
			self.attributes['points'] = ""
			for point in points:
				self.attributes['points'] += point.format()







