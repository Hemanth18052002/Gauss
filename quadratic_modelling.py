import numpy as np

n = int(input("Enter number of inputs: "))   # 5
x = np.array(list(map(float,input("Enter x values: ").split())))  # 0.69 1.92 3.46 5.72 6.31
y = np.array(list(map(float,input("Enter y values: ").split())))  # 6.01 8.32 10.43 15.61 21.23

A = []

for i in range(len(x)):
    l = []
    for j in range(len(x)):
        l.append(x[i]**j)
    l.append(y[i])
    A.append(l)

for i in range(n):
    for j in range(i+1,n):
        ratio = A[j][i]/A[i][i]
        for k in range(n+1):
            A[j][k] = A[j][k] - ratio * A[i][k]

coeff = np.zeros(len(x))
coeff[n-1] = A[n-1][n]/A[n-1][n-1]

for i in range(n-2,-1,-1):
    coeff[i] = A[i][n]
    for j in range(i+1,n):
        coeff[i] = coeff[i] - A[i][j]*coeff[j]
    coeff[i]=coeff[i]/A[i][i]

for i in range(n):
    print('a%d = %f'%(i,coeff[i]))

s = float(input("Enter the value of x for y : "))
res = 0
for i in range(n):
    res = res + coeff[i]*(s**i)
    
print("Respective y value: ",round(res,5))