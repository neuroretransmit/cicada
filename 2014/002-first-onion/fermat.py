#!/usr/bin/env python3

def isqrt(n):
	x=n
	y=(x+n//x)//2
	while(y<x):
		x=y
		y=(x+n//x)//2
	return x
def fermat(n):
	t0=isqrt(n)+1
	counter=0
	t=t0+counter
	temp=isqrt((t*t)-n)
	while((temp*temp)!=((t*t)-n)):
		counter+=1
		t=t0+counter
		temp=isqrt((t*t)-n)
	s=temp
	p=t+s
	q=t-s
	return p,q

print("Enter the number to factor of form (p*q):	")
n=int(input())
p,q=fermat(n)
print("Your first number   : ",int(p))
print("Your Second number  : ",int(q))
