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

		facetStr = "\tfacet normal " + "%e %e %e\n\t\touter loop\n" % (self.normal[0], self.normal[1], self.normal[2])
		
		for vertex in self.verteces:
			facetStr += "\t\t\tvertex %e %e %e\n" % (vertex[0], vertex[1], vertex[2])

		facetStr += "\t\tendloop\n\tend facet\n"

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
		self.height = self.pixelWidth * self.rows

		for row in range(self.rows):

			for col in range(self.cols):
				currLeftCorner = [(col / self.cols) * self.width, self.height - (self.pixelWidth * row), maxHeight]
				self.addBlock(currLeftCorner, 0)

	def addBlock(self, topLeft, height):
		# Create block base
		topRight = [topLeft[0] + self.pixelWidth, topLeft[1], 0]
		bottomRight = [topRight[0], topRight[1] - self.pixelWidth, 0]
		bottomLeft = [topLeft[0], topLeft[1] - self.pixelWidth, 0]
		baseNormal = [0, 0, -1]

		self.addFacet(Facet([topLeft, topRight, bottomLeft], baseNormal))
		self.addFacet(Facet([topRight, bottomRight, bottomLeft], baseNormal))

	def getData(self):
		print("Lithopane Dimensions: ")
		return (self.width, self.height)
		

# facet = Facet(verteces=[[0, 0, 0], [0, 1, 0], [0, 0, 1]], normal=[0, 0, 1])
# print(facet.toStr())
# shape = Shape("testSolid")
# shape.addFacet(facet)
# shape.print("test-output.stl")
litho = Lithopane("test-litho", "test-picture-2.png")
print(litho.getData())
litho.print("test-litho.stl")