class Heap:
	#I will be using the min-heap to store values from 1 to n-1 where n is the number of objects
	#The heap invariant is maintained using the time of collisions between the i and i+1th object

	def __init__(self, n, M, x, v, T):#intializing the min-heap object
		self.struct = [i for i in range(n-1)] #array representation of the heap
		self.times = [0 for i in range(n-1)] #array containing times corresponding to collisions of the ith and i+1th collision
		for i in range(n-1):
			self.times[i] = collision_time(0,i,M,x,v,T) #
		self.positions = [i for i in range(n-1)] #index of the ith block in the heap structure
		self.size = n-1 #size of our heap
		#O(n)

	def parent(self, i): #calculates the position of the parent for the given index
		return max(0, (i-1)//2)
		#O(1)

	def left(self, i): #calculates the position of the left child for the given index
		return min(2*i+1, self.size-1)
		#O(1)

	def right(self, i): #calculates the position of the right child for the given index
		return min(2*i+2, self.size-1)
		#O(1)

	def heap_up(self, k): #This is the standard heap up operation
		p = self.parent(k) #parent index of the kth index
		pp = self.struct[p]
		kk = self.struct[k]

		#condition for swapping the element with its parent, when time of parent is less or the number of the parent block is greater with the same time
		if (self.times[pp] == self.times[kk] and kk < pp) or (self.times[pp] > self.times[kk]):
			self.positions[kk], self.positions[pp] = p, k
			self.struct[k], self.struct[p] = pp, kk
			self.heap_up(p) #recurse on the parent
		#O(logn)

	def heap_down(self, k):#This is the standard heap down operation
		l = self.left(k) #left child index of the kth index
		r = self.right(k) #right child indez of the kth index

		kk = self.struct[k]

		mini = r
		if self.times[self.struct[l]] == self.times[self.struct[r]]:
			mini = self.positions[min(self.struct[l],self.struct[r])]
		elif self.times[self.struct[l]] < self.times[self.struct[r]]:
			mini = l
		#mini is the child with the smaller collision time
		minimini = self.struct[mini]

		#condition for swapping the element with its smaller time child, when smaller time of children is less or the number of the smaller time child block is lesser with the same time
		if (self.times[minimini] == self.times[kk] and minimini < kk) or (self.times[minimini] < self.times[kk]):
			self.positions[kk], self.positions[minimini] = mini, k
			self.struct[k], self.struct[mini] = minimini, kk
			self.heap_down(mini) #recurse on the child with the smaller time
		#O(logn)

	def build(self): #this is the standard linear time build heap operation
		for i in range(self.size-1,-1,-1): #heap down from the last element
			self.heap_down(i) 
		#O(n)

	def view_min_time(self): #returns the number of the block at the top of the heap
		return self.times[self.struct[0]]
		#O(1)

	def view_min_i(self): #returns the time corresponding to the block at the top of the heap
		return self.struct[0]
		#O(1)

	def extract_min(self): #Slightly different extract_min
		#When this function is called, the ith and i+1th objects have collided
		#so their velocitie have changed, and hence the time of their next collisions as well
		#this function is more of a repairing operation to satisfy the min-heap property again

		top = self.struct[0]
		self.heap_down(0)

		mini = top - 1
		maxi = top + 1

		#The root object has collided hence the time of next collision changed
		#Heap down to get it to a new position that satisfies the min-heap property

		#Since the time of collisions for the i-1 and i+1th object changed
		#we heap_up both of them to bring them to their correct locations

		if mini > 0 and maxi <= self.size - 1:
			if self.times[top-1] > self.times[top+1]:
				mini = top+1
				maxi = top-1

		#mini is the i-1th object
		#maxi is the i+1th object

		if mini >= 0:
			self.heap_up(self.positions[mini]) #bring mini to its correct position in the heap
		if maxi <= self.size-1:
			self.heap_up(self.positions[maxi]) #bring maxi to its correct position in the heap

		#O(logn)

	def update(self,t, k, M, x, v, T): #updates the collision times of the k-1, k, k+1th object with the next objects after the kth block has collided
		self.times[k] = collision_time(t,k, M, x, v, T)
		if k != 0:
			self.times[k-1] = collision_time(t,k-1, M,x,v,T)
		if k != self.size-1:
			self.times[k+1] = collision_time(t,k+1, M,x,v,T)
		#O(1)

def collision_time(t, k, M, x, v, T): #calculates the collision time between the k and k+1th object
	if v[k] <= v[k+1]:
		return T + 1 #when collision is not possible, set the time as T
	else:
		time = t + (x[k+1]+v[k+1]*t-x[k]-v[k]*t)/(v[k]-v[k+1])
		if time > T:
			time = T+1 #if time exceeds the maximum time T, set it as T+1
		return time
	#O(1)

def velocities(m,v,x,i): #calculates the velocity after elastic collision of the i and i+1th objects
	return (((m[i] - m[i+1])/(m[i+1] + m[i]))*v[i] + ((2*m[i+1])/(m[i+1] + m[i]))*(v[i+1]),((m[i] - m[i+1])/(m[i+1] + m[i]))*(-v[i+1]) + ((2*m[i])/(m[i+1] + m[i]))*v[i])
	#O(1)

def listCollisions(M,x,v,m,T):
	if len(M) <= 1: #case of no collisions
		return []

	minheap = Heap(len(M), M,x,v,T) #Our heap is called minheap
	minheap.build() #build the heap
	current_time = 0
	number = 0 #number of collisions
	result = []

	while True:
		mintime = minheap.view_min_time() #mintime is the the minimum time of collision in the heap
		if mintime <= T and number < m: #runs provided the number of collisions is less than m and time hasn't exceeded T
			least_time = minheap.view_min_i() #number of block at the top of the heap
			current_time = mintime #minimum time of collision in the heap
			point_of_collision = x[least_time] + v[least_time]*current_time #calculates the coordinate of collision
			vel = velocities(M,v,x,least_time) #calculating velocities after collision
			x[least_time] = x[least_time] + current_time*(v[least_time]-vel[0]) #updating coordinate of the collided object
			x[least_time+1] = x[least_time+1] + current_time*(v[least_time+1]-vel[1]) #updating coordinate of the collided object
			#This is the most important step which reduces the time complexity of the algorithm from O(n+mnlogn) to O(m+nlogn)
			#We DO NOT update the location of every block after each collision
			#instead we calculate an equivalent distance for the blocks that have collided
			#this is not their actual position but a substitute that will give us the correct position of the block when needed
			#we only need the position of the block when comparing times of collisions
			#we calculate position by the initial position plus velocity*time elapsed
			#but since we update velocities it is not possible to apply the above formula directly
			#so instead we calculate the substitute position for which this formula can directly be applied

			v[least_time], v[least_time + 1] = vel[0], vel[1] #updating velocities in the list of velocities
			minheap.update(current_time, least_time, M,x,v,T) #updating the times in the heap
			minheap.extract_min() #maintaining the min-heap property after updating the coordinates, velocities and times
			result += [(round(current_time, 4), round(least_time, 4), round(point_of_collision,4))] #push to the result list which has to be returned
			number += 1
		else:
			break #come out of the loop when time exceeds T or number of collisions reaches m
	return result
	#Overall complexity O(n+mlogn)