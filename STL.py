from decimal import Decimal
from PIL import Image
import sys


class Facet:

	def __init__(self, verteces=[], normal=[0, 0, 0]):
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


class Lithophane(Shape):

	def __init__(self, name, image, width=100, maxHeight=2, maxPixels=50000):
		"""
		Create Lithophane object. All units are millimeters unless specified
		otherwise.
		"""

		Shape.__init__(self, name)
		self.image = Image.open(image).convert('L')
		self.pixels = list(self.image.getdata())
		self.cols = self.image.size[0]
		self.rows = self.image.size[1]
		self.buildLithophane(width, maxHeight, maxPixels)
		# self.maxHeight = maxHeight

		# if len(self.pixels) > maxPixels:
		# 	scale = (maxPixels / len(self.pixels)) ** 0.5
		# 	self.image = self.image.resize((int(self.cols * scale), 
		# 		int(self.rows * scale)))
		# 	self.pixels = list(self.image.getdata())
		# 	self.cols = self.image.size[0]
		# 	self.rows = self.image.size[1]

		# self.width = width
		# self.pixelWidth = self.width / self.cols
		# self.length = self.pixelWidth * self.rows

		# for row in range(self.rows):

		# 	for col in range(self.cols):
		# 		topLeftBase = [(col / self.cols) * self.width, self.length 
		# 			- (self.pixelWidth * row), 0]
		# 		height = self.pixels[(row * self.cols) + col] * (-self.maxHeight
		# 			/ 255) + self.maxHeight + 0.5
		# 		self.addBlock(topLeftBase, height)

	
	def addSurface(self, points, normal=[0, 0, 0]):
		"""
		Add a face to the lithopane based on four points. Points must be given
		in counter-clockwise order w/ respect to the normal vector.
		"""

		self.addFacet(Facet([points[0], points[2], points[3]], normal))
		self.addFacet(Facet([points[1], points[2], points[3]], normal))

	
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

		blankNormal = [0, 0, 0]

		# Create bottom and top surfaces.
		self.addFacet(Facet([points[1], points[2], points[0]]))
		self.addFacet(Facet([points[1], points[3], points[2]]))

		self.addFacet(Facet([points[4], points[6], points[5]]))
		self.addFacet(Facet([points[5], points[6], points[7]]))

		# Create +y surface.
		self.addFacet(Facet([points[1], points[4], points[0]]))
		self.addFacet(Facet([points[1], points[5], points[4]]))
		# Create +x surface.
		self.addFacet(Facet([points[3], points[5], points[1]]))
		self.addFacet(Facet([points[3], points[7], points[5]]))
		# Create -y surface.
		self.addFacet(Facet([points[2], points[6], points[3]]))
		self.addFacet(Facet([points[6], points[7], points[3]]))
		# Create -x surface.
		self.addFacet(Facet([points[0], points[4], points[2]]))
		self.addFacet(Facet([points[4], points[6], points[2]]))
	
	def buildLithophane(self, width, maxHeight, maxPixels=50000):
		"""
		Create an STL lithophane of the given picture based on given
		paramters. Allow for post-initialization modification.
		"""
	
		self.facets_.clear()
		self.maxHeight = maxHeight

		# Scale down image to match or be under maxPixels.
		if len(self.pixels) > maxPixels:
			scale = (maxPixels / len(self.pixels)) ** 0.5
			self.image = self.image.resize((int(self.cols * scale), 
				int(self.rows * scale)))
			self.pixels = list(self.image.getdata())
			self.cols = self.image.size[0]
			self.rows = self.image.size[1]

		self.width = width
		self.pixelWidth = self.width / self.cols
		self.length = self.pixelWidth * self.rows

		for row in range(self.rows):

			for col in range(self.cols):
				topLeftBase = [(col / self.cols) * self.width, self.length 
					- (self.pixelWidth * row), 0]

				height = self.pixels[(row * self.cols) + col] * (-self.maxHeight
					/ 255) + self.maxHeight + 0.5

				self.addBlock(topLeftBase, height)

