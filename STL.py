from decimal import Decimal
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

		print("facet normal %e %e %e" % (self.normal[0], self.normal[1], self.normal[2]), file=file)
		print("\touter loop", file=file)

		for vertex in self.verteces:
			print("\t\tvertex %e %e %e" % (vertex[0], vertex[1], vertex[2]))

		print("\tendloop", file=file)
		print("end facet", file=file)

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

	def export(self, outputFile=""):
		"""Print the contents of the shape to the given file in STL ASCII format."""
		pass

facet = Facet(verteces=[[0, 0, 0], [0, 1, 0], [0, 0, 1]], normal=[0, 0, 1])
facet.print()
