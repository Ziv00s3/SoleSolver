#!/usr/bin/python
# -*- coding: utf-8 -*-
import applied
import wolframalpha
import os
import sys
import argparse
import sys

LOGO = """ ____  ____  _     _____   ____  ____  _     _     _____ ____ 
/ ___\/  _ \/ \   /  __/  / ___\/  _ \/ \   / \ |\/  __//  __\\
|    \| / \|| |   |  \    |    \| / \|| |   | | //|  \  |  \/|
\___ || \_/|| |_/\|  /_   \___ || \_/|| |_/\| \// |  /_ |    /
\____/\____/\____/\____\  \____/\____/\____/\__/  \____\\\\_/\_\\
Version 1.0.0a (release)
by Roman Lebed

Moscow State University
Faculty of Computational Mathematics & Cyberntetics

2014
"""

GLOBAL_CONFIG = {"Method":"GAUSS_M", "WAlpha":False, "Output":"output.sole", "WAlphaKey":None, "Clear":"False", "Eps":0.0001, "Omega":1.0}
TASKS = []

def setter(param):
	global GLOBAL_CONFIG
	s = raw_input("Set"+param+": ")
	if len(s) > 0:
		GLOBAL_CONFIG[param] = s


def config():
	global GLOBAL_CONFIG
	print "Press Enter to avoid input current parameter"

	for i in GLOBAL_CONFIG.keys():
		setter(i)
	print "Done!"

def load_matrix(filename = "input.soles", format="directInput"):
	global TASKS 
	TASKS = []
	if format == "soles":
		f = open(filename, "r")
		lines = f.readlines()
		T = []
		for line in lines:
			if "###" in line:
				TASKS.append(T)
				T = []
			else:
				row = [float(x) for x in line.split()]
				T.append(row)

	elif format == "directInput":
		S = int(raw_input("Enter number of matrices to compute:"))
		print "Input format: a1i a2i ... ani bi"
		for s in range(S):
			print "Input matrix " + str(s+1) + ":"
			T = []
			N = int(raw_input("Enter N: "))
			for i in range(N):
					r = raw_input("Enter row " + str(i+1) + ": ")
					row = r.split()
					for k in range(len(row)):
						row[k] = float(row[k])
					T.append(row)
			TASKS.append(T)
			
def validate(matrix):
	n = len(matrix)
	for row in matrix:
		if len(row) != (n+1):
			print "Wrong input"
			return False
	return True


def procces(interactive = False):
	global GLOBAL_CONFIG
	ofile = open(GLOBAL_CONFIG["Output"], "w")
	wfile = None
	if GLOBAL_CONFIG["WAlpha"]:
		wfile = open(GLOBAL_CONFIG["Output"] + "w", "w")
	n = 0
	outputw =""
	for matrix in TASKS:
		n += 1
		print "Computing:" , n, "/", len(TASKS)
		ofile.write("#MATRIX: "+ str(n) + "\n")
		outputw += "#MATRIX: "+ str(n) + "\n"
		if validate(matrix):
			if GLOBAL_CONFIG["Method"] == "GAUSS_M":
				A, D = applied.gauss(matrix, True, True, True)
				I = applied.inverse_matrix(A, gaussed = True)
				S ="["
				for i in range(len(matrix)):
					S += str(A[i][len(matrix)])+" "
				S += "]"
				ofile.write("#SOLUTION: "+ S + "\n")
				ofile.write("#DETERMINANT: "+ str(D) + "\n")
				ofile.write("#INVERSED MATRIX: "+ "\n")
				outputw+= "#SOLUTION: "+ S + "\n" + "#DETERMINANT: "+ str(D) + "\n" + "#INVERSED MATRIX: "+ "\n"
				for i in range(len(I)):
					r = str(I[i]).replace("[","").replace(",","").replace("]","")
					ofile.write(r + "\n")
					outputw += r + "\n"
				ofile.write("###\n")
				outputw += "###\n"
			elif GLOBAL_CONFIG["Method"] == "GAUSS":
				A, D = applied.gauss(matrix, False, True, True)
				I = applied.inverse_matrix(A, gaussed = True)
				S ="["
				for i in range(len(matrix)):
					S += str(A[i][len(matrix)])+" "
				S += "]"
				ofile.write("#SOLUTION: "+ S + "\n")
				ofile.write("#DETERMINANT: "+ str(D) + "\n")
				ofile.write("#INVERSED MATRIX: "+ "\n")
				outputw+= "#SOLUTION: "+ S + "\n" + "#DETERMINANT: "+ str(D) + "\n" + "#INVERSED MATRIX: "+ "\n"
				for i in range(len(I)):
					r = str(I[i]).replace("[","").replace(",","").replace("]","")
					ofile.write(r + "\n")
					outputw += r + "\n"
				ofile.write("###\n")
				outputw += "###\n"
				pass
			elif GLOBAL_CONFIG["Method"] == "SOR":
				if GLOBAL_CONFIG["Omega"] == None:
					omega = 1.0
				else:
					omega = float(GLOBAL_CONFIG["Omega"])
				if GLOBAL_CONFIG["Eps"] == None:
					eps = 0.000001
				else:
					eps = float(GLOBAL_CONFIG["Eps"])
				A = []
				b = []
				for i in matrix:
					A.append(i[:-1])
					b.append(i[-1])
				solution, counter = applied.SOR(A, b, eps, omega)
				ofile.write("#SOLUTION: [")
				outputw += "#SOLUTION: ["
				#normalize:
				for i in solution:
					ofile.write(str(i)+' ')
					outputw += str(i) + ' '
				ofile.write("]\n")
				outputw += "]\n"
				ofile.write("#NUMBER_OF_STEPS: "+str(counter)+"\n")
				outputw  += "#NUMBER_OF_STEPS: "+str(counter)+"\n"
			if GLOBAL_CONFIG["WAlpha"]:
				var ="["
				for i in range(len(matrix)):
					var += ",x"+str(i+1)+" "
				var += "]"
				var = var.replace("[,x","[x")
				wmatrix = []
				b = []
				for i in matrix:
					wmatrix.append(i[:-1])
					b.append(i[-1])

				q = "solve" + str(wmatrix) + "*" + var + "=" + str(b) 
				print q
				client = wolframalpha.Client(GLOBAL_CONFIG["WAlphaKey"])
				res = client.query(q)
				wfile.write("#TASK: " + str(n)+"\n")
				for pod in res.pods:
					wfile.write(pod.text + "\n")
	if interactive:
		print outputw
	
	if wfile:
		wfile.close()
	ofile.close()


def print_config():
	global GLOBAL_CONFIG
	for i in GLOBAL_CONFIG.keys():
		print i, "-", GLOBAL_CONFIG[i]
def wolframconsole():
	global GLOBAL_CONFIG
	while True:
		q = raw_input("Query(! to exit):")
		if q == "!":
			return
		client = wolframalpha.Client(GLOBAL_CONFIG["WAlphaKey"])
		res = client.query(q)
		print "="*79
		for pod in res.pods:
			print pod.text
		print "="*79

def menu():
	global GLOBAL_CONFIG
	print "Interactive mode"
	while True:
		try:
			if GLOBAL_CONFIG["Clear"] == "True":
				print chr(27) + "[2J"
			m = int(raw_input("""
================================
| Exit - 0 or unlisted number  |
| 1 - Config                   |
| 2 - Print current config     |
| 3 - Input and Solve          |
| 4 - WolfraAlpha Console      |
================================
> """))
			if m == 1:
				config()
			elif m == 2:
				print_config()
			elif m == 3:
				load_matrix(format = "directInput")
				procces(interactive = True)
			elif m == 4:
				wolframconsole()
			else:
				os._exit(0)
			raw_input("Press Enter to continue")
		except:
			print "!!!!!!!!!!!!!!!!!!!!!!!!!!"
			print "!!! Something is wrong !!!"
			print "!!!!!!!!!!!!!!!!!!!!!!!!!!"
			pass


def main(argv):
	print LOGO
	global GLOBAL_CONFIG
	parser = argparse.ArgumentParser(description='Short usage guide:\n')
	parser.add_argument("-i", "--input", action="store", help="path to input file in SOLE format")
	parser.add_argument("-m", "--method", action="store", help="method of SOLE solution (GAUSS|GAUSS_M|MUR), default - GAUSS_M")
	parser.add_argument("-o", "--interactive", action="store_true", help="manual matrix input in interactive mode")
	parser.add_argument("-w", "--wolfram", action="store_true", help="use Wolfra,Alpha for checking (requries API key)")
	parser.add_argument("-k", "--wolframkey", action="store", help="Developer's appliaction key for WA")
	parser.add_argument("-e", "--eps", action="store", help="Epsilon for SOR method")
	parser.add_argument("-q", "--omega", action="store", help="Omega for SOR method")
	args = parser.parse_args()
	if args.method:
		GLOBAL_CONFIG["Method"] = args.method
	if args.wolfram and args.wolframkey:
		GLOBAL_CONFIG["WAlpha"] = True
		GLOBAL_CONFIG["WAlphaKey"] = args.wolframkey
	if args.eps and float(args.eps) > 0:
		GLOBAL_CONFIG["Eps"] = float(args.eps)
	if args.omega and float(args.omega) < 2 and float(args.omega) > 0:
		GLOBAL_CONFIG["Omega"] = float(args.omega)
	if args.interactive:
		menu()
	else:
		if args.input != None:
			load_matrix(format ="soles", filename = args.input)
			procces()
	exit()
if __name__ == "__main__":
    main(sys.argv[1:])
