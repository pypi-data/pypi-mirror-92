import numpy as np
import string
import random
from .vector import V
import copy

class E:
	def __init__(self, elm, stroke, fill, precision=3):
		self.tag = elm
		self.hasContent = True if elm in ('g', 'text', 'clipPath', 'linearGradient') else False
		self.precision = precision
		self.id = ''.join(random.choices(string.ascii_letters, k=3))
		self.transform = {}
		self.attributes = {
			'stroke': stroke,
			'fill': fill,
		}
		if self.hasContent:
			self.contents = []

	def setStroke(self, color=False, opacity=False, width=False):
		if opacity:
			if float(opacity) > 1:
				opacity = 1
			else:
				opacity = round(opacity, self.precision)
			self.attributes['opacity'] = opacity
		if color:
			self.attributes['stroke'] = color
		if width:
			self.attributes['stroke-width'] = round(width, 2)

	def setFill(self, color, opacity=1):
		if opacity:
			if float(opacity) > 1:
				opacity = 1
			else:
				opacity = round(opacity, self.precision)
			self.attributes['opacity'] = opacity
		self.attributes['fill'] = color

	def rotate(self, angle=0, center=False):
		angle = round(float(angle), self.precision)
		if center:
			if self.isV(center):
				self.transform['rotate'] = f'{angle}, {center.p[0]}, {center.p[1]}'
		else:
			self.transform['rotate'] = f'{angle}'
	def translate(self, to):
		if self.isV(to):
			self.transform['translate'] = f'{to.p[0]}, {to.p[1]}'
	def scale(self, xr, yr=False):
		xr = str(round(float(xr), self.precision))
		if yr:
			yr = str(round(float(yr), self.precision))
		val = f'{xr}, {yr}' if yr else str(xr)
		self.transform['scale'] = val

	def skewX(self, angle):
		self.transform['skewX'] = str(round(float(angle), self.precision))

	def skewY(self, angle):
		self.transform['skewY'] = str(round(float(angle), self.precision))

	def copy(self):
		return copy.deepcopy(self)
	def assemble(self, id=False):
		output = f'<{self.tag} '
		if self.transform:
			output += 'transform="'
			for key, val in self.transform.items():
				if isinstance(val, (float, int)):
					val = round(float(val), self.precision)
				output += f'{key}({val})'
			output += '" '
		if id:
			output += f'id="{self.id}" '
		for attr, val in self.attributes.items():
			output += f'{attr}="{val}" '
		output = output[:-1]
		if self.hasContent:
			output += f'>'
			if self.contents:
				for content in self.contents:
					output += content
			output += f'</{self.tag}>'
		else:
			output += '/>'
		return output

	def isV(self, coordinate):
		if isinstance(coordinate, V):
			return True
		else:
			print('values must be instances of V')
			return False
	def isVlist(self, coordinates):
		if isinstance(coordinates, list):
			for coordinate in coordinates:
				if not isinstance(coordinate, V):
					print('value must be instance of V')
					return False
				else:
					pass
			return True
		else:
			print('values must be list of V')
