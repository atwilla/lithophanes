# Lithopanes
This program converts a given picture into an STL lithopane.
## The Facet Class
This class represents an STL facet. The three points of the facet must be 
declared according to the right hand rule with respect to the given normal 
vector. self.toStr() converts the facet information into a valid string 
representation and returns it, and self.print() prints this string to the 
given output file. The script uses this pattern because it makes printing an 
entire STL solid much faster; instead of having to call the print function 
repeatedly, the Shape class can simply get the string representation and print 
the facet with the Shape's own print function, saving a considerable amount of 
time.
## The Shape Class
This class is used to represent an STL solid. self.facets_ is a list that holds 
all facets used to build said solid, and self.addFacet() adds a given facet to 
this list. The print function writes the solid to an STL file.
## The Lithopane Class
This class inherits from the Shape class and adds several new attributes and 
methods:
	1. self.image
		An image object of the given image made with Pillow. This image is 
		converted to black and white.
	1. self.pixels
		A list containing the pixel values for every pixel in the image
	1. self.cols and self.rows
		The number of pixels along the width and height respectively.
	1. self.addBlock(self, topLeftBase, height)
		Adds a block of a given height with the top left corner of the base 
		at the given point.
	1. self.buildLithopane(self, width, maxHeight, maxPixels)
		Resizes image if base pixel count is above maxPixels, calculates the 
		width of each pixel in mm, calculates the height of each pixel based 
		on maxHeight, and places each block.