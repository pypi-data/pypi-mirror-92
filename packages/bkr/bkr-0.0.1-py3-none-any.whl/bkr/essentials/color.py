from bkr.essentials.elm import E
import numpy as np
class RGB:
	def __init__(self, r=0, g=0, b=0, monotonous=False):
		self.monotonous = monotonous
		self.r = round(r, 2) if r <= 255 else 255
		self.g = round(g, 2) if g <= 255 else 255
		self.b = round(b, 2) if b <= 255 else 255
	def out(self):
		if self.monotonous:
			return f'rgb({self.r}, {self.r}, {self.r})'
		else:
			return f'rgb({self.r}, {self.g}, {self.b})'
	
class LinearGradient(E):
	def __init__(self, angle=0, stroke="black", fill="none"):
		super().__init__('linearGradient', stroke, fill)
		del self.attributes['stroke']
		del self.attributes['fill']
		x = np.cos(angle)
		y = np.sin(angle)
		self.attributes['x1'] = 0
		self.attributes['y1'] = 0
		self.attributes['x2'] = abs(x)
		self.attributes['y2'] = abs(y)
		self.stops = []
	
	def addStop(self, offset, color):
		self.contents.append(f'<stop offset="{round(offset, self.precision)}" stop-color="{color}" />')
	def assemble(self):
		return super().assemble(True)
	def out(self):
		return f'url(#{self.id})'