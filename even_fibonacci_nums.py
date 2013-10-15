#!/usr/bin/python
import sys

max_num = 0
try:
	max_num = (int(float(sys.argv[1])))
except ValueError:
	print >>sys.stderr, 'There was a problem parsing the command line arguments.'
	+ ' Remember to enter a number'
	sys.exit(1)

def generate_even_fib(x1, x2, max):
	sum = x1 + x2
	if (sum > max):
		return 0
	if ((sum % 2) == 0):
		return sum + generate_even_fib(x2, sum, max)
	else:
		return 0 + generate_even_fib(x2, sum, max)

#generate even fibs
even_sum = generate_even_fib(1, 1, max_num)
print "The sum of even-valued fibonacci terms not exceeding " + str(max_num) + " is " + str(even_sum)

