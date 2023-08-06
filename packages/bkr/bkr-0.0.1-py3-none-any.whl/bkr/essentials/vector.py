import numpy as np
import copy
class V:
	"""3d nparray"""
	def __init__(self, x=0.00, y=0.00, z=0.00, precision=3):
		self.precision = precision
		x = round(x, precision)
		y = round(y, precision)
		z = round(z, precision)
		self.p = np.array([round(x, self.precision), y, z])
	def format(self):
		return f'{round(self.p[0], 3)},{round(self.p[1], 3)} '
	def copy(self):
		return copy.deepcopy(self)
	
	#ARITHMATICS
	def add(self, vector, out=False):
		if isinstance(vector, V):
			if out:
				result = self.copy()
				result.add(vector)
				return result
			else:
				self.p += vector.p
		else:
			self.message()

	def sub(self, vector, out=False):
		if isinstance(vector, V):
			if out:
				result = self.copy()
				result.sub(vector)
				return result
			else:
				self.p -= vector.p
		else:
			self.message()

	def mul(self, vector):
		if isinstance(vector, V):
			self.p *= vector.p
		else:
			self.message()

	def div(self, vector):
		if isinstance(vector, V):
			self.p = self.p / vector.p
			self.p[np.isnan(self.p)] = 0
		else:
			self.message()

	#VECTOR UTILITY
	def length(self):
		return np.linalg.norm(self.p)
		
	def angle2d(self):
		addition = 0
		if self.p[1] < 0:
			if self.p[0] < 0:
				addition = np.pi
			else:
				addition = np.pi * 2
		else:
			if self.p[0] < 0:
				addition = np.pi
		return np.arctan(self.p[1] / self.p[0]) + addition

	#COMMON
	def message(self):
		print('argument must be a V')
		return