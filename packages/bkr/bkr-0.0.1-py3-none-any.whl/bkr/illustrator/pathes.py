import numpy as np
import re

from bkr.essentials.elm import E

class Group(E):
	def __init__(self):
		super().__init__('g', 'none', 'none')
		del self.attributes['stroke']
		del self.attributes['fill']
	def add(self, elms):
		if self.areE(elms):
			for elm in elms:
				self.contents.append(elm.assemble())

	def areE(self, elms):
		result = True
		for elm in elms:
			if not issubclass(type(elm), E):
				result = False
				break
		return result

class Path(E):
	def __init__(self, stroke="black", fill="none"):
		super().__init__('path', stroke, fill)
		self.commands = []

	def m(self, v, absolute=False):
		if self.isV(v):
			m = 'M' if absolute else 'm'
			self.commands.append(f'{m}{v.format()}')
	
	def c(self, bz1, bz2, endpoint, absolute=False):
		if self.isVlist([bz1, bz2, endpoint]):
			c = 'C' if absolute else 'c'
			self.commands.append(f'{c}{bz1.format()}{bz2.format()}{endpoint.format()}')

	def s(self, bz, endpoint, absolute=False):
		if self.isVlist([bz, endpoint]):
			s = 'S' if absolute else 's'
			self.commands.append(f'{s}{bz.format()},{endpoint.format()}')
	def q(self, bz, endpoint, absolute=False):
		if self.isVlist([bz, endpoint]):
			q = 'Q' if absolute else 'q'
			self.commands.append(f'{q}{bz.format()},{endpoint.format()}')
	def t(self, endpoint, absolute=False):
		if self.isV(endpoint):
			t = 'T' if absolute else 't'
			self.commands.append(f'{t}{endpoint.format()}')
	def l(self, endpoint, absolute=False):
		if self.isV(endpoint):
			l = 'L' if absolute else 'l'
			self.commands.append(f'{l}{endpoint.format()}')
	def h(self, x, absolute=False):
		if self.isIntOrFloat(x):
			h = 'H' if absolute else 'h'
			self.commands.append(f'{h}{x} ')
	def v(self, y, absolute=False):
		if self.isIntOrFloat(y):
			cmd = 'V' if absolute else 'v'
			self.commands.append(f'{cmd}{y} ')

	def assemble(self, id=False):
		self.attributes['d'] = ""
		for cmd in self.commands:
			self.attributes['d'] += cmd
		return super().assemble(id)

class ClipPath:
	def __init__(self, subject, clipper):

		if self.areE([subject, clipper]):
			self.subject = subject
			self.clipper = clipper
		else:
			print('arguments must be subclass of E.')

	def assemble(self):
		output = f'<defs><clipPath id="{self.clipper.id}">{self.clipper.assemble()}</clipPath></defs>'
		self.subject.attributes['clip-path'] = f'url(#{self.clipper.id})'
		output += self.subject.assemble()
		return output

	def areE(self, elms):
		result = True
		for elm in elms:
			if not issubclass(type(elm), E):
				result = False
				break
		return result
