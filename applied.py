# -*- coding: utf-8 -*-
import math
import decimal
decimal.getcontext().prec = 100
def matrixcp(A):
	B = []
	for i in A:
		r = []
		for j in i:
			r.append(j)
		B.append(r)
	return B

def Igen(i,j):
	if i == j:
		return 1.0
	return 0.0

	
def generate_matrix(M, N, generator = None):
	matrix = []
	if generator == None:
		generator = Igen
	for i in range(M):
		row = []
		for j in range(N):
			row.append( float(generator(i,j)) )
		matrix.append(row)
	return matrix

def multiply(A,B):
	#no cmp
	C = []
	for i in range(len(A)):
		row = []
		for j in range(len(B[0])):
			s = 0.0
			for x in range(len(A)):
				s+= A[i][x] * B[x][j]
			row.append(s)
		C.append(row)
	return C

def abs_determinant(A, triangle=False):
	det = 1.0
#only for square matrix
	if not triangle:
		B, det = gauss(A, det = True)
		return det
	for j in range(len(A)):
		det *= A[j][j]
	return det

def choose_of_element(A,z,main = True):
	M = len(A)
	m = 0.0
	mindex = 0
	#find max(abs())

	if main:
		for i in range(z, M):
			if abs(A[i][z]) > m:
				m = abs(A[i][z])
				mindex = i
	else:
		for i in range(z, M):
			if abs(A[i][z]) != 0:
				mindex = i
				break
	return mindex

# N*(N+1)
# [A|b]
# 0   1  2    .... N N+1
# ========================
#   z|  |            | b1
#    |z |            | b2
#    |  |z           | b3
#
# 
def gauss(matrix, melement = True, compute_inverse = False, det = False):
	multiplier = 1.0
	A = matrixcp(matrix)
	M = len(A)

	N = N0 =  len(A[0])
	order = [i for i in range(M)]
	for row in range(M):
		A[row] = map(float, A[row])
#by columns:
	I = [None]

	if compute_inverse:
		#appending I
		#[  A  |b|  I  ]
		#{  N0   }{ M  }
		#{       N     }
		I = generate_matrix(min(M,N), min(M,N))
		for row in range(M):
			A[row] = A[row] + I[row]
		N += min(M,N)

	
	# choose column
	for z in range(M):
		#swap colums
		#print str(A).replace("],","]\n")
		if melement:
			c = A[z][z]
			cindex = z
			for x in range(z+1, M):
				if c < A[z][x]:
					cindex = x
					c = A[z][x]
			multiplier *= (-1)**(cindex-z)
			order[z], order[cindex] = order[cindex], order[z]
			
			for x in range(M):
				A[x][cindex], A[x][z] = A[x][z], A[x][cindex]
				if compute_inverse:
					A[x][M + 1 + cindex], A[x][M + 1 +z] \
					= A[x][M + 1 +z], A[x][M + 1 +cindex]
			


		mindex = choose_of_element(A, z, melement)
		#swap rows
		tmprow = A[mindex]
		A[mindex] = A[z]
		A[z] = tmprow
		multiplier *= (-1)**(mindex - z)
		#making a step
		for x in range(z+1,M):
			a = -A[x][z]/A[z][z]
			for i in range(z, N):
				A[x][i] += a*A[z][i]
	multiplier *= abs_determinant(A, triangle = True)

	#reverse steps
	for z in range(M-1,0,-1):
		a = A[z][z]
		for x in range(z, N):
			A[z][x] /= a
		
		for x in range(z-1,-1, -1):
			a = A[x][z]
			A[x][z] -= a*A[z][z]
			A[x][M] -= a*A[z][M]
			for i in range(M+1, N):
				A[x][i] -= a*A[z][i]
	a = A[0][0]
	for x in range(N):
		A[0][x] /= a

	if not compute_inverse:
		for row in range(M):
			A[row] = A[row][:N0-1]
	#reverse variables order
	if melement:
		for i in range(M):
			c = order.index(i)
			for x in range(M):
				A[x][c], A[x][i] = A[x][i], A[x][c]
				if compute_inverse:
					A[x][M + 1 + c], A[x][M + 1 +i] \
					= A[x][M + 1 +i], A[x][M + 1 +c]

			order[c] ,order[i] = order[i], order[c]

			#diagonalize
		for i in range(M):
			for j in range(M):
				if A[j][i] == 1.0 and i != j:
					A[i], A[j] = A[j], A[i]
					break

	#print str(A).replace("],", "]\n")
	return A, multiplier


def matrixEuclidNorm(A):
	M = len(A)
	N = len(A[0])
	s = 0.0
	for j in range(N):
		for i in range(M):
			s+=A[i][j]
	return math.sqrt(s)

def inverse_matrix(A, gaussed = False):
	M = len(A)
	B = matrixcp(A)
	if not gaussed:
		B = gauss(A, True, True)
	for i in range(M):
		B[i] = B[i][-M:]
	return B

def transposition(A):
	C = []
	M = len(A)
	N = len(A[0])
	for j in range(N):
		row = []
		for i in range(M):
			row.append(A[i][j])
		C.append(row)
	return C
#Ai - inversed matrix A
def condByEuclidNorm(A, Ai = None):
	if Ai == None:
		return matrixEuclidNorm(A) * matrixEuclidNorm(inverse_matrix(A))
	else:
		return matrixEuclidNorm(A) * matrixEuclidNorm(Ai)

def seidel(m, b, eps):
    n = len(m)
    r = range(n)
    x = [0.0] * len(m)
    conv = False
    while not conv:
        p = x[:]
        for i in r:
            var = sum(m[i][j] * x[j] for j in range(i))
            var += sum(m[i][j] * p[j] for j in r)
            x[i] = (b[i] - var) / m[i][i]
 
        conv = (sum((x[i]-p[i])**2 for i in r))**(0.5) < eps 
    return x

def SOR(A,b, eps = 0.0001, omega = 1.5):
	n = len(A)
	x = [decimal.Decimal(0.0)] * n
	xn = x[:]
	conv = False
	counter = 0
	omega = decimal.Decimal(omega)

	#magick (At)*Ax = (At)*b
	blank = []
	blank.append(b)
	b = transposition(multiply(transposition(A), transposition(blank)))[0]

	A = multiply( transposition(A), A)
	AD = []
	for i in A:
		row = []
		for j in i:
			row.append(decimal.Decimal(j))
		AD.append(row)

	while not conv:
		conv = True
		counter += 1
		#print counter
		for i in range(n):
			xn[i] = x[i]+ omega * (decimal.Decimal(b[i]) - \
				sum([AD[i][j] * xn[j] for j in range(i)]) - \
				sum([AD[i][j] *  x[j] for j in range(i, n)]) ) / \
				AD[i][i]

		for i in range(n):
			conv = conv and (abs(decimal.Decimal(b[i]) - sum(AD[i][j] * xn[j] for j in range(n))) < eps)
			#print abs(decimal.Decimal(b[i]) - sum(AD[i][j] * xn[j] for j in range(n))), eps
		x = xn[:]
		
	return x, counter