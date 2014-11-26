import applied
import math
def pm(A):
	for i in range(len(A)):
		print A[i]

def m1(i,j,n, m):
	if i ==j:
		return n + m*m + float(j)/m + float(i)/n
	if i != j:
		return float((i+j))/(n+m)

def B(p,m, i, n):
	if p == 1:
		return n*i +m
	if p == 2:
		return 200 + 50*i
	if p == 3:
		return i*i - 100
	if p == 4:
		return m*n - i**3
	if p == 5:
		return m*i + n
	if p == 6:
		return i*i - n
	print "Alert", p, m ,i , n
	exit()
def B2(p,x, i, n):
	x = float(x)
	if p == 1:
		return n*(math.e)**(x/i) + math.cos(x)
	if p == 2:
		return abs(x - n/10) * i * math.sin(x)
	if p == 3:
		return x*(math.e**(x/i)) * math.cos(x/i)
	if p == 4:
		return n*(math.e**(x/i)) * math.cos(x/i)
	if p == 5:
		return abs(x - n/10) * i * math.sin(x)
	if p == 6:
		return x*(math.e**(x/i)) * math.cos(x/i)
	print "Alert", p, m ,i , n
	exit()

def q(m):
	return 1.001 -2*m*0.001

def m2(i,j, m):
	if i == j:
		return (q(m) - 1)**(i+j)
	else:
		return q(m) ** (i+j) + 0.1*(j-i)


M = [10, 8 , 9, 15, 20, 10]
N = [40, 20, 30, 50, 30, 25]

outfile = open("ex2.1.sole", "w")
for p in range(6):
	for i in range(N[p]):
		s= ""
		for j in range((N[p])):
			s+= str(m1(i, j, N[p], M[p])) +" "
		s+= str(B(p+1, M[p], i, N[p])) +"\n"
		outfile.write(s)
	outfile.write("### "+str(p+1) + "\n")

wutfile = open("ex2.1.math", "w")
for p in range(6):
	wutfile.write("LinearSolve[{")
	for i in range(N[p]):
		w ="{"
		for j in range((N[p])):
			w+= str(m1(i, j, N[p], M[p])) +", "
		w= w[:-2]
		w+="},"
		wutfile.write(w)
	if i == N[p] - 1 :
			w = w[:-1]
	w = "},{"
	for i in range(N[p]):
		w+= str(B(p+1, M[p], i, N[p])) +", "
	w =w[:-2]
	w+= "}"
	wutfile.write(w +"]\n")
	wutfile.write("### "+str(p+1) + "\n")


M = [1, 2 , 3, 4, 5, 6]
N = [20, 20, 20, 20, 20, 20]


outfile = open("ex2.2.sole", "w")
for p in range(6):
	for i in range(N[p]):
		s= ""
		for j in range((N[p])):
			s+= str(m2(i+1, j+1, M[p])) +" "
		s+= str(B2(p+1, M[p], i+1, N[p])) + "\n"
		outfile.write(s)
	outfile.write("### "+str(p+1) + "\n")

wutfile = open("ex2.2.math", "w")
for p in range(6):
	wutfile.write("LinearSolve[{")
	for i in range(N[p]):
		w ="{"
		for j in range((N[p])):
			w+= str(m2(i+1, j+1, M[p])) +", "
		w= w[:-2]
		w+="},"
		if i == N[p] - 1 :
			w = w[:-1]
		wutfile.write(w)

	w = "},{"
	for i in range(N[p]):
		w+= str(B2(p+1, M[p], i+1, N[p])) +", "
	w =w[:-2]
	w+= "}"
	wutfile.write(w +"]\n")
	wutfile.write("### "+str(p+1) + "\n")

