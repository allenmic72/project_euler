#!/usr/bin/python
import sys

max_num = 0
try:
	max_num = (int(float(sys.argv[1])))
except ValueError:
	print >>sys.stderr, 'There was a problem parsing the command line arguments.'
		+ ' Remember to enter a number'
	sys.exit(1)

#since we are looking for multiples below the input, not inclusive
max_num = max_num - 1

sum_divis = 0
divis_3 = max_num - (max_num % 3) 
while(divis_3 > 0):
	if ((divis_3 % 5) != 0):
		sum_divis = sum_divis + divis_3
	divis_3 = divis_3 - 3

divis_5 = max_num - (max_num % 5)
while(divis_5 > 0):
	sum_divis = sum_divis + divis_5
	divis_5 = divis_5 - 5

print "sum of multiples of 3 and 5 less than " + str(max_num) + " is " + str(sum_divis)
sys.exit(0)