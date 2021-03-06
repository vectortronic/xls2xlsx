#!/usr/bin/python

"""
# XLS2XLSX.PY
#
#   Iyad Obeid, 8/7/2014, v1.0.1
#
#   Converts xls to xlsx
#   Run with -h or -help flag for more information on how to run
#
#   Code is based on xlrd which is downloaded from here:
#       https://pypi.python.org/pypi/xlrd
#   and openpyxl which is downloaded from here:
#       https://pythonhosted.org/openpyxl/
#
#   Installation requires
#     download and follow install instructions: https://pypi.python.org/packages/source/x/xlrd/xlrd-0.9.3.tar.gz#md5=6f3325132f246594988171bc72e1a385
#     pip install openpyxl
"""
import xlrd
import sys
import os
from openpyxl.workbook import Workbook


def main():
	# main function

	# parse the command line, check for errors
	flag, fileNameInput, fileNameOutput = init_vars()

	# print the help screen if requested
	if flag['help'] is True:
		print_help_screen()
		exit()

	# print the verbose screen if requested
	if flag['verbose'] is True:
		print_verbose_screen(fileNameInput, fileNameOutput)

	# run the actual code
	book_out = open_xls_as_xlsx(fileNameInput)
	book_out.save(fileNameOutput)


def open_xls_as_xlsx(filename):
	# first open using xlrd
	book_input  = xlrd.open_workbook(filename)
	book_output = Workbook()

	book_output.remove_sheet(book_output.active)

	for sheet_in in book_input.sheets():
		nrows = sheet_in.nrows
		ncols = sheet_in.ncols
		name  = sheet_in.name

		sheet_out = book_output.create_sheet()
		sheet_out.title = name
		for row in xrange(0, nrows):
			for col in xrange(0, ncols):
				colLetter = chr(ord('A')+col)
				currCell = colLetter + repr(row+1)
				sheet_out[currCell] = sheet_in.cell_value(row, col)

	return book_output


def init_vars():

	flag = dict(verbose=False, help=False, sameOutFile=False)

	input_args = sys.argv[1:]

	# check all the input switches in order to set up process flow properly
	for arg in sys.argv[1:]:

		if arg.lower() == '-verbose' or \
			arg.lower() == '-v':
			flag['verbose'] = True
			input_args.pop(0)

		elif arg.lower() == '-help' or \
			arg.lower() == '-h':
			flag['help'] = True
			input_args.pop(0)

		# unknown switch
		elif arg[0] == '-':
			print ' '
			print 'ERROR: switch ' + arg + ' not found'
			print '         Try ./' , __file__ , '-help for more options'
			print ' '
			exit()

	nArguments = len(input_args)

	# Check to see if the minimum number of arguments (2) has been
	# supplied. Note that you don't need two arguments if the help
	# flag has been thrown
	if flag['help'] is False:
		if nArguments == 0:
			print('ERROR: no filenames provided')
			exit()
		else:
			fileNameInput = input_args[0]
			if nArguments == 1:
				fileNameOutput = fileNameInput[0:-3]+'xlsx'
			elif nArguments == 2:
				fileNameOutput = input_args[1]
			else:
				print('ERROR: too many input arguments specified')
				exit()

	# check to see if the specified input file exists
	if os.path.isfile(fileNameInput) is False:
		print (' ')
		print ('ERROR: input file ' + fileNameInput + ' not found')
		print (' ')
		exit()

	return flag, fileNameInput, fileNameOutput


def print_help_screen():
	print(' ')
	print('XLS2XLSX.py : coverts an xls file to an xlsx file')
	print('    ./xls2xlsx.py inputfile.xls outputfile.xlsx')
	print('    optional switches: -verbose (-v), -help')
	print(' ')


def print_verbose_screen(fileNameInput, fileNameOutput):
		print 'xls2xlsx:'
		print '  Input file:  ', fileNameInput
		print '  Output file: ', fileNameOutput


if __name__ == '__main__':
	main()
