import math

def median(x): 
	sorted_x = sorted(x)
	if (len(sorted_x)%2 == 1):
		return sorted_x[((len(sorted_x)+1)/2)-1]
	elif (len(sorted_x) == 2):
		return (float(sorted_x[0]+sorted_x[1])/2)
	else: 
		a1 = sorted_x[len(sorted_x)/2 +1]
		a2 = sorted_x[len(sorted_x)/2 -1]
		return (float((a1+a2)/2))
def mean(x):
	return (float(sum(x)/float(len(x))))

def skewness(x):
	cube_x = []
	a = len(x)
	m = mean(x)
	sd = s_dev(x)
	if (sd == 0):
		return "?"
	else:
		for i in range(0,a):
			cube_x.append(((x[i]-m)/float(sd))*((x[i]-m)/float(sd))*((x[i]-m)/float(sd)))
		return (float(sum(cube_x)/float(a)))
	
def s_dev(x):
	square_x = []
	a = len(x)
	if (a == 1):
		return 0 
	else: 
		m = mean(x)
		for i in range(0,a):
			square_x.append((x[i]-m)*(x[i]-m))
		variance = float(sum(square_x)/float(a))
		return (math.sqrt(variance))
	

def kurtosis(x):
	quad_x = []
	a = len(x)
	m = mean(x)
	sd = s_dev(x)
	if (sd == 0):
		return "?"
	else:
		for i in range(0,a):
			quad_x.append((x[i]-m)*(x[i]-m)*(x[i]-m)*(x[i]-m))
		k = float(sum(quad_x)/float(a))
		return (k/(sd*sd*sd*sd))

def proto(protocol,dest_port): 
	if (protocol == 6):
		if (dest_port == 80):
			return 1
		elif (dest_port == 8080):
			return 1
		elif (dest_port == 443):
			return 2 
		else:
			return 3 
	elif (protocol == 17):
		return 4 
