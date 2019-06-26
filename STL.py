import sys


class STLFacet:

	def __init(self, verteces=[], normal=[]):
		self.verteces = verteces
		self.normal = normal


class STLShape:

	def __init__(self, name):
		self.name = name
		self.facets_ = []

	def addFacet(self, facet):
		self.facets_.append(facet)

	def export(self, outputFile=""):
		"""Print the contents of the shape to the given file in STL ASCII format."""
		pass
