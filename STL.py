from decimal import Decimal
from PIL import Image
import sys


class Facet:

	def __init__(self, verteces=[], normal=[]):
		self.verteces = verteces
		self.normal = normal

	def print(self, outputFile=""):

		if outputFile == "":
			file = sys.stdout
		else:
			file = open(outputFile, "a")

		print(self.toStr(), end="", file=file)
		file.close()

	def toStr(self):
		"""Construct a string that represents the STL facet."""

		facetStr = "\tfacet normal " + "%e %e %e\n\t\touter loop\n" % (self.normal[0], 
			self.normal[1], self.normal[2])
		
		for vertex in self.verteces:
			facetStr += "\t\t\tvertex %e %e %e\n" % (vertex[0], vertex[1], vertex[2])

		facetStr += "\t\tendloop\n\tendfacet\n"

		return facetStr


class Shape:

	def __init__(self, name):
		self.name = name
		self.facets_ = []

	def addFacet(self, facet):
		self.facets_.append(facet)

	def print(self, outputFile):
		"""Print the contents of the shape to the given file in STL ASCII format."""
	
		with open(outputFile, 'w') as file:
			print("solid " +  self.name, file=file)
			print("name written")

			for facet in self.facets_:
				print(facet.toStr(), end="", file=file)

			print("endsolid " + self.name, file=file)
			print("end written")


class Lithopane(Shape):

	def __init__(self, name, image, desiredWidth=40, maxHeight=2):
		"""
		Create Lithopane object. All units are millimeters unless specified
		otherwise.
		"""

		Shape.__init__(self, name)
		self.image = Image.open(image).convert('L')
		self.pixels = list(self.image.getdata())
		self.cols = self.image.size[0]
		self.rows = self.image.size[1]
		self.width = desiredWidth
		self.pixelWidth = self.width / self.cols
		self.length = self.pixelWidth * self.rows
		self.maxHeight = maxHeight

		for row in range(self.rows):

			for col in range(self.cols):
				topLeftBase = [(col / self.cols) * self.width, self.length 
					- (self.pixelWidth * row), 0]
				height = self.pixels[(row * self.cols) + col] * (-self.maxHeight
					/ 255) + self.maxHeight + 1
				self.addBlock(topLeftBase, height)

	
	def addSurface(self, points, normal):
		"""
		Add a face to the lithopane based on four points.
		"""
		self.addFacet(Facet(points[0:-1], normal))
		self.addFacet(Facet(points[1:], normal))

	
	def addBlock(self, topLeftBase, height):

		# print(topLeftBase)

		# Determine block points.
		points = [topLeftBase]
		# topRightBase point
		points.append([topLeftBase[0] + self.pixelWidth, topLeftBase[1], 0])

		# bottom left and right base points
		for i in range(2):
			newPoint = [points[-2][0], points[-2][1] - self.pixelWidth, points[-2][2]]
			points.append(newPoint)
			# print(points)

		# Add points for top of block
		for i in range(4):
			newPoint = [points[i][0], points[i][1], points[i][2] + height]
			points.append(newPoint)

		# for point in points:
			# print(point)

		# Create bottom and top surfaces.
		self.addSurface(points[:4], [0, 0, 1])
		self.addSurface(points[4:], [0, 0, -1])

		# Create +y surface.
		self.addSurface(points[:2] + points[4:6], [0, 1, 0])
		# Create +x surface.
		self.addSurface([points[1], points[3], points[5], points[7]], 
			[1, 0, 0])
		# Create -y surface.
		self.addSurface(points[2:4] + points[6:], [0, -1, 0])
		# Create -x surface.
		self.addSurface([points[0], points[4], points[2], points[6]],
			[-1, 0, 0])

		## bottomLeftBase point
		#points.append(topLeftBase)
		#points[-1][1] -= self.pixelWidth
		## bottomRightBase point

		#botLeftBase = topLeftBase
		#botLeftBase[1] -= self.pixelWidth
		#botRightBase = topRightBase
		#botRightBase[1] -= self.pixelWidth

		#topLeftTop = topLeftBase
		#topLeftTop[2] += height
		#topRightTop = topRightBase
		#topRightTop[2] += height
		#botLeftTop = botLeftBase
		#botLeftTop[2] += height
		#botRightTop = botRightBase
		#botRightTop[2] += height

	
	def buildLithopane(self, resolution):
		"""
		Create an STL lithopane of the given picture based on given
		paramters.
		"""
	

	def getData(self):
		print("Lithopane Dimensions: ")
		return (self.width, self.height)
		
