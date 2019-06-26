import sys


class STLFacet:

	def __init__(self, verteces=[], normal=[]):
		self.verteces = verteces
		self.normal = normal

	def print(self, outputFile=""):

		if outputFile == "":
			file = sys.stdout
		else:
			file = open(outputFile, "a")

		print("facet normal %f %f %f" % (self.normal[0], self.normal[1], self.normal[2]), file=file)
		print("\touter loop", file=file)

		for vertex in self.verteces:
			print("\t\tvertex %f %f %f" % (vertex[0], vertex[1], vertex[2]))

		print("\tendloop", file=file)
		print("end facet", file=file)

		file.close()


class STLShape:

	def __init__(self, name):
		self.name = name
		self.facets_ = []

	def addFacet(self, facet):
		self.facets_.append(facet)

	def export(self, outputFile=""):
		"""Print the contents of the shape to the given file in STL ASCII format."""
		pass

facet = STLFacet(verteces=[[0, 0, 0], [0, 1, 0], [0, 0, 1]], normal=[0, 0, 1])
facet.print()