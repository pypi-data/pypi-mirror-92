from essentials import V
class C:
	def __init__(self, width="210", height="297"):
		self.opening = f'<svg width="{width}" height="{height}" viewbox="0, 0, {width}, {height}" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg">'
		self.closing = '</svg>'
		self.content = ''
		self.w = float(width)
		self.h = float(height)
		self.center = V(self.w/2, self.h/2)

	
	def add(self, elm):
		if isinstance(elm, list):
			for e in elm:
				self.content += e.assemble()
		else:
			self.content += elm.assemble()

	def assemble(self):
		return self.opening + self.content + self.closing