#!/usr/bin/python
import sys

max_iterations = 100000
try:
	start_num = int(sys.argv[1])
except ValueError:
	print >>sys.stderr, 'There was a problem parsing the command line arguments.'
	+ ' Remember to enter a number'
	sys.exit(1)

iterations = 0
consecutive = 0
last_even = 0
current_even = 0
max_consecutive = 0
max_consecutive_even = 0
while (start_num != 1):
	if (iterations >= max_iterations):
		print "Quit with " + str(start_num) + " after " + str(iterations) + " loop iterations."
		sys.exit(0)
	# even number
	if (start_num % 2 == 0):
		start_num = start_num / 2
		current_even = 1
	# odd number
	else:
		start_num = (start_num * 3) + 1
		current_even = 0
	if (current_even == last_even):
		consecutive += 1
	else:
		if (last_even == 1):
			string = "even"
		else:
			string = "odd"
		print "Encountered " + str(consecutive) + " consecutive " + string + " numbers"
		if (consecutive > max_consecutive):
			max_consecutive = consecutive
			max_consecutive_even = current_even
		consecutive = 0
	last_even = current_even
	iterations += 1

if (max_consecutive_even == 1):
	max_consecutive_even_string = "even"
else:
	max_consecutive_even_string = "odd"
print "It took " + str(iterations) + " loop iterations to reach 1. Max consecutive even/odd number streak was " + str(max_consecutive) + " " + str(max_consecutive_even_string) + " numbers"

