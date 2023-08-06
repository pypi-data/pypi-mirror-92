from PIL import Image
from bkr.cnvs import C
from bkr.essentials.vector import V
from bkr.essentials.utils import map_range
from bkr.essentials.color import RGB

class Img:
	def __init__(self, svg, imgPath):
		if isinstance(svg, C):
			self.img = Image.open(str(imgPath))
			self.center = V(self.img.size[0] / 2, self.img.size[1] / 2)
			self.isWide = True if self.img.size[0] > self.img.size[1] else False
			self.px = self.img.load()
			self.svgW = svg.w
			self.svgH = svg.h
			if self.isWide:
				th = self.img.size[1]
				tw = th * svg.h / svg.w 
			else:
				tw = self.img.size[0]
				th = tw * svg.h / svg.w  
			self.cnvsStart = self.center.add(V(-tw/2, -th/2), True)
			self.cnvsEnd = self.center.add(V(tw/2, th/2), True)
		else:
			print('svg must be instance of C.')
	def spoit(self, point, greyScale=False):
		if isinstance(point, V):
			#adust point to Img canvas
			x = map_range(point.p[0], 0, self.svgW, self.cnvsStart.p[0], self.cnvsEnd.p[0])
			y = map_range(point.p[1], 0, self.svgH, self.cnvsStart.p[1], self.cnvsEnd.p[1])

			if greyScale:
				return round(sum(list(self.px[x, y])) / 3, 2)
			else:	
				r, g, b = self.px[x, y]
				color = RGB(r, g, b)
				return color.out()
		else:
			print('point must be instance of V.')

	#https://pillow.readthedocs.io/en/3.0.x/reference/PixelAccess.html
