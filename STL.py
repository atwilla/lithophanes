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

		print("\tfacet normal %e %e %e" % (self.normal[0], self.normal[1], self.normal[2]), file=file)
		print("\t\touter loop", file=file)

		for vertex in self.verteces:
			print("\t\t\tvertex %e %e %e" % (vertex[0], vertex[1], vertex[2]), file=file)

		print("\t\tendloop", file=file)
		print("\tend facet", file=file)

		file.close()

	def toString(self):
		"""Construct a string that represents the STL facet."""

		facetStr = "facet normal"


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
			facet.print(outputFile)

		with open(outputFile, 'a') as file:
			print("endsolid " + self.name, file=file)
			print("end written")


class Lithopane(Shape):

	def __init__(self, image, desiredWidth):
		self.image = Image.open(image)
		self.width = desiredWidth
		

facet = Facet(verteces=[[0, 0, 0], [0, 1, 0], [0, 0, 1]], normal=[0, 0, 1])
shape = Shape("testSolid")
shape.addFacet(facet)
shape.print("test-output.stl")
