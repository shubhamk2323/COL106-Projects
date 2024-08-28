import random
import math

def modpower(a, b, q): #Helper function
	#helps in calculating a**b mod q in O(b) time and log2(q) bits
	if b == 0:
		return 1
	else:
		result = a%q
		for i in range(b-1): #runs in O(b) time, each comparison takes O(log(q)) time
			result = (result*(a%q))%q #because (xy)modq = ((x mod q)(y mod q))mod q
			#as mod is being taken at every iteration, it is ensured that space complexity bounds are met
		return result
	#O(blog(q)) time and O(log(q)) space
		
def randPrime(N): #pre implemented
	primes = []
	for q in range(2,N+1):
		if(isPrime(q)):
			primes.append(q)
	return primes[random.randint(0,len(primes)-1)]

def isPrime(q): #pre implemented
	if(q > 1):
		for i in range(2, int(math.sqrt(q)) + 1):
			if (q % i == 0):
				return False
		return True
	else:
		return False

def randPatternMatch(eps,p,x): #pre implemented
	N = findN(eps,len(p))
	q = randPrime(N) #q is O(N) space
	#from our choice of N, N is O(log(m/eps)) space
	
	return modPatternMatch(q,p,x)
	#modPatternMatch runs in O((n+m)logq) time
	#and q is O(log(m/eps))
	#hence randPatternMatch runs in O((n+m)log(m/eps)) time
	#similarly as space taken by modPatternMatch is O(k+logq+logn)
	#due to q being O(log(m/eps)), we get overall space complexity of randPatternMatch as O(k+logn+log(m/eps))

def randPatternMatchWildcard(eps,p,x): #pre implemented
	N = findN(eps,len(p))
	q = randPrime(N) #q is O(N) space
	#from our choice of N, N is O(log(m/eps)) space
	return modPatternMatchWildcard(q,p,x)
	#modPatternMatchWildcard runs in O((n+m)logq) time
	#and q is O(log(m/eps))
	#hence randPatternMatchWildcard runs in O((n+m)log(m/eps)) time
	#similarly as space taken by modPatternMatchWildcard is O(k+logq+logn)
	#due to q being O(log(m/eps)), we get overall space complexity of randPatternMatchWildcard as O(k+logn+log(m/eps))
	
def findN(eps,m): 
	N = int((4*(m/eps)*math.log(26,2))*math.log(4*(m/eps)*math.log(26,2), 2)) + 1
	return N
	
	#EXPLANATION FOR FINDN
	#We have been given a probability bound eps
	#First we need to figure out when does a collision occur
	#a hash collision or a false positive occurs when the hash function of the substring is equal to f(p) mod q but 
	#the value of that substring is not equal to f(p)
	#This occurs when q (our chosen prime) divides abs(f(p) - value of the substring), this is by the definition of mod
	#hence what the problem reduces to is choosing one of such primes out of all primes less than equal to N
	#we can use the statements provided in the assignment
	#firstly the number of primes of a number d is less than log(d)
	#we want log(d)/pi(N) to be less than eps which means pi(N) should be greater than log(d)/eps
	#d is the difference a~b which is less than 26^m
	#hence we want pi(N) greater than mlog(26)/eps, lets call this c
	#using the statement given that pi(N) is greater than N/2log(N)
	#we can write pi(klogk) > klog(k)/2log(klogk) = klogk/2(log(k) + loglog(k)) > klogk/2(2log(k)) = k/4
	#hence I can use my N to be 4clog(4c) as I proved it is greater than c
	#so N = 4c(2+log(c))

def modPatternMatch(q,p,x):
	m = len(p) #to avoid using len() again and again
	t = len(x) #to avoid using len() again and again
	result = [] #final list to be returned
		
	fp = 0 #f(p)%q that we will calculate is stored in this variable
	value = 0 #the hash function for the first m values of the text calculated as f(x[i..m]) mod q
	space = modpower(26, m-1, q) #using the modpower function that we defined to calculate (26**(m-1)) mod q
	#this takes O(logq) bits and runs in O(mlogq) time hence is much better in terms of space than directly calculating 26**(m-1)
	
	prev = 1 #helper variable for calculating the value and fp 
	
	for i in range(m-1, -1, -1): #for calculation of fp and value 
		fp = (fp + (((ord(p[i])-65)%q)*(prev%q))%q)%q 
		value = (value + (((ord(x[i])-65)%q)*(prev%q))%q)%q
		prev = (prev*(26%q))%q #the helper variable, made such that space constraints are met as always log(q) bits are being stored
		#and helps calculate (26**(m-i-1)) mod q without using any extra space or extra time
	
	if value == fp: #checking whether the first m sized substring has same hash value as f(p) mod q
		result += [0] 
	
	for i in range(m, t): #checking for the other substrings one by one
		value = ((((value - (((ord(x[i-m])-65)%q)*space)%q)%q)*(26%q))%q + (ord(x[i]) - 65)%q)%q
		#from moving from one substring to the next, we subtract the value of the first letter (taking into account its significance in powers of 26) of that substring mod q
		#then we add the immediate next letter and the middle letters are multiplied with 26 (taking into account mod q everywhere for space complexity bounds)
		
		if value == fp: #if hash equals fp mod q then add to the result list
			result += [i-m+1] 
			
		#this runs in O(nlog2q) time
		#loop runs in O(n) time
		#each iteration of the loop compares O(log2q) bits
		
	#hence overall time complexity of modPatternMatch is O((m+n)log(q) time
	
	#Space taken at every step is ensured to be O(logq) bits as we keep taking mod q at every step,
	#even for calculations we have ensured taking mod q after every multiplication
	#O(logn) is the value of the index i while iterating to check the various substrings
	#O(k) space is for the final list that is being returned
	#Hence overall space omplexity comes out to be O(k + logn + logq)
			
	return result

def modPatternMatchWildcard(q,p,x):
	m = len(p) #to avoid using len() again and again
	t = len(x) #to avoid using len() again and again
	result = [] #final list to be returned
	
	if m > len(x):
		return []
	else:
		wildcard = 0 #index of the wildcard
		for i in range(m): #loop to find the index of the wildcard 
			if p[i] == '?':
				wildcard = i
				break
		fp = 0 #f(p)%q that we will calculate is stored in this variable
		value = 0 #the hash function for the first m values of the text calculated as f(x[i..m]) mod q
		space = modpower(26, m-1, q) #using the modpower function that we defined to calculate (26**(m-1)) mod q
		#this takes O(logq) bits and runs in O(mlogq) time hence is much better in terms of space than directly calculating 26**(m-1)
		smallspace = modpower(26, m-wildcard-1, q) #similarly calculating (26**(m-1-wildcard))
		prev = 1
		
		for i in range(m-1, wildcard, -1):
			fp =(fp + (((ord(p[i])-65)%q)*((prev%q))%q))%q
			value = (value + (((ord(x[i])-65)%q)*(prev%q))%q)%q
			prev = (prev*(26%q))%q
			
		prev = (prev*(26%q))%q
		for i in range(wildcard-1, -1, -1):
			fp =(fp + (((ord(p[i])-65)%q)*((prev%q))%q))%q
			value = (value + (((ord(x[i])-65)%q)*(prev%q))%q)%q
			prev = (prev*(26%q))%q
		
		#The above two loops are the same as ModPatternMatch except that we do not add the value at the index in the substring corresponding to the wildcard position in the pattern
		#hence that index is not added or treated as an A which has value 0
		#in our pattern also we are treating the ? as an A so that we have a match at that corresponding index
			
		if value == fp: #checking whether the first m sized substring has same hash value as f(p) mod q
			result += [0]

		for i in range(m, t):#checking for the other substrings one by one
			value = ((((value + (((ord(x[i - m + wildcard])-65)%q)*smallspace)%q - (((ord(x[i-m])-65)%q)*space)%q)%q)*(26%q))%q + ((ord(x[i]) - 65))%q - (((ord(x[i-m + wildcard+1])-65)%q)*smallspace)%q)%q
			#from moving from one substring to the next, we subtract the value of the first letter (taking into account its significance in powers of 26) of that substring mod q
			#we also have to add back the value at the previous wildcard and subtract the value at the position of the wildcard in the next substring
			#this is done because for our wildcard we treat both the ? and the corresponding index in the substring as A so that they match at that position always
			#then we add the immediate next letter and the middle letters are multiplied with 26 (taking into account mod q everywhere for space complexity bounds)
			
			if value == fp: #if hash equals fp mod q then add to the result list
				result += [i-m+1]			
		return result
		#this runs in O(nlog2q) time
		#loop runs in O(n) time
		#each iteration of the loop compares O(log2q) bits
		
		
	#hence overall time complexity of modPatternMatch is O((m+n)log(q) time

		
	#Space taken at every step is ensured to be O(logq) bits as we keep taking mod q at every step,
	#even for calculations we have ensured taking mod q after every multiplication
	#O(logn) is the value of the index i while iterating to check the various substrings
	#O(k) space is for the final list that is being returned
	#Hence overall space omplexity comes out to be O(k + logn + logq)
		
	


