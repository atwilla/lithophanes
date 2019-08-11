import sys
import STL

args = sys.argv
options = {"-o":'litho-output.stl', '-w':'100', '-p':'100000', '-h':'2'}

if len(args) == 1:
	print("Usage: lithotest.py input")
	print("Options: ")
	print("\t-o output\n\t-w width(mm)\n\t-p max pixels\n\t-h max height")

else:

	for flag in options:
		if flag in args:
			options[flag] = args[args.index(flag) + 1]


	litho = STL.Lithophane(str(options['-o']), args[1], 
		width=int(options['-w']), maxHeight=int(options['-h']), 
			maxPixels=int(options['-p']))

	litho.print(options['-o'])
