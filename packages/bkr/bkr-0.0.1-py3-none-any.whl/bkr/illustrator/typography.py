import numpy as np

from bkr.essentials.elm import E
from bkr.essentials.vector import V

class Char(E):
	def __init__(self, char="", sp=V(0,0), stroke="none", fill="black", fontsize=4, textAnchor=False):
		if isinstance(char, str):
			super().__init__('text', stroke, fill)
			self.contents.append(char)
			self.attributes['font-size'] = fontsize
			self.attributes['x'] = sp.p[0]
			self.attributes['y'] = sp.p[1]
			self.p = sp
			if textAnchor:
				self.attributes['text-anchor'] = textAnchor
		else:
			print('char needs to be str.')

class Chars:
	def __init__(self, paragraph, sp=V(0,0), stroke="none", fill="black", fontsize=4):
		self.chars = []
		for i, char in enumerate(paragraph):
			newSp = sp.copy()
			newSp.p[0] =  newSp.p[0] + i * fontsize
			self.chars.append(Char(char, newSp, stroke, fill, fontsize))

	def assemble(self):
		result = ""
		for char in self.chars:
			result += char.assemble()
		return result


class Text(E):
	def __init__(self, sp=False, stroke="none", fill="black", fontsize=4, lineHeight=1.4, textAnchor=False):
		super().__init__('text', stroke, fill)
		self.attributes['font-size'] = fontsize
		self.fontSize = fontsize
		self.lineHeight = np.round(lineHeight * fontsize, self.precision)
		self.tspans = []
		if sp:
			if self.isV(sp):
				self.attributes['x'] = sp.p[0]
				self.attributes['y'] = sp.p[1]
		if textAnchor:
			self.attributes['text-anchor'] = textAnchor

	def tspan(self, text, sp=False, f=False, fArgs=False):
		tspan = {}
		numChars = len(text)
		if sp: 
			if self.isV(sp):
				tspan['x'] = sp.p[0]
				tspan['y'] = sp.p[1]
		if f: #return dx, dy
			f(tspan, text, fArgs)
		tspan['text'] = text
		self.tspans.append(tspan)

	def assemble(self):
		for tspan in self.tspans:
			assembled = '<tspan '
			if "x" in tspan:
				assembled += f'x="{tspan["x"]}" '
				assembled += f'y="{tspan["y"]}" '
			if "dx" in tspan:
				dx = ', '.join(map(str, tspan["dx"]))
				assembled += f'dx="{dx}" '
			if "dy" in tspan:
				dy = ', '.join(map(str, tspan["dy"]))
				assembled += f'dy="{dy}" '
			if "letter-spacing" in tspan:
				val = tspan["letter-spacing"]
				assembled += f'letter-spacing="{val}" '
			assembled = assembled[:-1]
			assembled += f'>{tspan["text"]}</tspan>'
			self.contents.append(assembled)
		return super().assemble(self)

	#FUNCTIONS FOR tspan
	def randomXY(self, tspan, text, args):
		amp = args['amp'] if 'amp' in args else 1
		x = args['x'] if 'x' in args else True
		y = args['y'] if 'y' in args else True
		if x:
			tspan['dx'] = np.round(np.random.random(len(text)) * amp, self.precision)
		if y:
			tspan['dy'] = np.round(np.random.random(len(text)) * amp, self.precision)
			for i, dy in enumerate(tspan['dy']):
				if i != len(tspan['dy']) - 1:
					tspan['dy'][i] = np.round(dy - tspan['dy'][i+1], self.precision)
		print(tspan['dy'])

	def addTracking(self, tspan, text, val):
		tspan['letter-spacing'] = val



