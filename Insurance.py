import math
import random

# inverse transform method
def itm(pmf):
	cumul = 0.0
	x = random.random()
	for i in range(len(pmf)):
		cumul += pmf[i]
		if x < cumul:
			return i

# claim random variable with distribution F
# number of policy holders
def claimRV(n):
	# rate of a new policy holder
	v = 0
	# rate of a lost policy holder
	u = 0
	# rate of a claim
	lda = 10
	# RV where 1 = v, 2 = u, 3 = c
	j = 0
	denom = v + n*u + n*lda
	pmf = []
	pmf.append(v/denom)
	pmf.append((n*u)/denom)
	pmf.append((n*lda)/denom)
	j = itm(pmf) + 1
	return j

# claim random variable with distribution F
# number of policy holders
def nextEvent(n):
	v = 0
	u = 0
	lda = 10
	rate = v + n*u + n*lda
	U = random.random()
	eventTime = -(1/rate)*math.log(U)
	return eventTime

def sizeClaim():
	U = random.random()
	value = -1000 * math.log(U)
	return value

# An Insurance Risk Model
# @param a0 : initial capital
# @param n0 : initial policy holders
def insurance(a0,n0,T0):
	# binary variable: 1 if firm's capital is nonnegative from [0, t], 0 o.w.
	I = -1
	# constant revenue per unit time
	c = 11000
	# time variable
	t = 0
	T = T0
	# number of policy holders
	n = n0
	# firm's current capital
	a = a0
	# System State Variable
	SS = [n,a]
	# event list
	EL = nextEvent(SS[0])
	while t < T:
		# next arrival time
		t_E = t + nextEvent(SS[0])
		# check to see if next event occurs before deadline	
		if t_E > T:
			t = T
			I = 1
		else:
			# add income over period of time leading up event
			SS[1] = SS[1] + n*c*(t_E-t)
			t = t_E
			# determine which event occurred
			j = claimRV(SS[0])
			# new policyholder found
			if j == 1:
				SS[0] += 1
			# lost a policyholder
			elif j == 2:
				SS[0] -= 1
			# a claim was filed
			elif j == 3:
				# generate size of the claim
				Y = sizeClaim()
				# claim sending balance negative
				if Y > SS[1]:
					I = 0
					SS[1] = SS[1] - Y
					T = t
				else:
					SS[1] = SS[1] - Y
	
	SS.append(I)
	SS.append(t)
	return SS
