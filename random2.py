class Heap:
	def __init__(self, n, source, maxcap):
		self.maxcapacity = [-1 for i in range(n)] 
		#ith index stores the maxcapacity of the ith numbered node
		#self.maxcapacity = mylist
		self.maxcapacity[source] = maxcap
		self.struct = [i for i in range(n)] #actual structure of the heap
		self.positions = [i for i in range(n)] #ith index represents the position of the ith node in the heap structure
		self.size = n
		self.heap_up(self.positions[source])
		#O(n)
	def parent(self, i): #calculates the position of the parent for the given index
		return max(0, (i-1)//2)
		#O(1)
	def left(self, i): #calculates the position of the left child for the given 
		if 2*i + 1 > self.size - 1:
			return i
		return 2*i+1
		#O(1)
	def right(self, i): #calculates the position of the right child for the given index
		if 2*i + 2 > self.size - 1:
			return i
		return 2*i+2
		#O(1)
	def heap_up(self, k): #This is the standard heap up operation
		p = self.parent(k) #parent index of the kth index
		p_node = self.struct[p]
		k_node = self.struct[k]
		if self.maxcapacity[p_node] < self.maxcapacity[k_node] :
			self.positions[k_node], self.positions[p_node] = p, k
			self.struct[k], self.struct[p] = p_node, k_node
			self.heap_up(p) #recurse on the parent
		#O(logn)
	def heap_down(self, k):#This is the standard heap down operation
		#print("k is ", k)
		l = self.left(k) #left child index of the kth index
		r = self.right(k) #right child indez of the kth index
		k_node = self.struct[k]
		l_node = self.struct[l]
		r_node = self.struct[r]
		max_cap_lr = l
		if self.maxcapacity[r_node] > self.maxcapacity[l_node]:
			max_cap_lr = r
		max_cap_node = self.struct[max_cap_lr]	
		if self.maxcapacity[max_cap_node] > self.maxcapacity[k_node]:
			self.positions[k_node], self.positions[max_cap_node] = max_cap_lr, k
			self.struct[k], self.struct[max_cap_lr] = max_cap_node, k_node
			self.heap_down(max_cap_lr)
		#O(logn)
	def build(self): #this is the standard linear time build heap operation
		for i in range(self.size-1,-1,-1): #heap down from the last element
			#print("I is ", i)
			self.heap_down(i) 
		#O(n)
	def extract_max(self): #Standard extract max operation
		top = self.struct[0]
		bottom = self.struct[self.size-1]
		self.positions[top], self.positions[bottom] = self.size - 1, 0
		self.struct[0], self.struct[self.size-1] = bottom, top 
		self.size -= 1
		if self.size > 0:
			self.heap_down(0)
		return top
"""def make_adjlist(n, links):
	adjlist = [[] for i in range(n)]
	for i in links:
		adjlist[i[0]].append((i[1], i[2]))
		adjlist[i[1]].append((i[0], i[2]))
	return adjlist"""
def findMaxCapacity(n, links, s, t):
	maxcap = max(i for i in [links[j][2] for j in range(len(links))])
	adjlist = [[[],0, -1] for i in range(n)]
	for i in links:
		adjlist[i[0]][0].append((i[1], i[2])) #2nd element of the tuple is the link capacity
		adjlist[i[1]][0].append((i[0], i[2]))
	print("adjlist is ", adjlist)
	capacities = Heap(n, s, maxcap +1)
	#print(capacities.struct)
	#print(capacities.maxcapacity)
	while capacities.size > 0:
		#print("hey")
		max_node = capacities.extract_max()
		#print("max_node is ", max_node)
		adjlist[max_node][1] = 1
		for j in adjlist[max_node][0]:
			#print("j is ", j)
			if adjlist[j[0]][1] == 0:
				replace_by = min(j[1], capacities.maxcapacity[max_node])
				replace_this = capacities.maxcapacity[j[0]]
				if replace_by > replace_this:
					adjlist[j[0]][2] = max_node
					capacities.maxcapacity[j[0]] = replace_by
					capacities.heap_up(capacities.positions[j[0]])
		#print("yo")
		#print(max_node, capacities.maxcapacity)
		#print(capacities.struct)
	prev = t
	result = []
	while prev != -1:
		result.append(prev)
		prev = adjlist[prev][2]
	#result.append(s)
	return (capacities.maxcapacity[t], result[::-1])
print(findMaxCapacity(8, [(0,1,5), (1,2,8), (2,3,6), (3,4,1), (4,5,15), (5,6,2), (6,7,3), (7,0,12), (1,5,7), (1,6,3), (2,5,9), (2,7,11), (3,7,14), (0,4,3), (0,5,4)], 0, 0))
'''
class Heap:
    def __init__(self, n, source, maxcap):
        # Initialize the maximum capacity for each node as -1
        self.maxcapacity = [-1] * n
        self.maxcapacity[source] = maxcap  # Set the capacity of the source node

        # Create the heap structure with node indices
        self.struct = [i for i in range(n)]

        # Position of each node in the heap
        self.positions = [i for i in range(n)]
        self.size = n

        # Adjust the heap for the source node
        self.heap_up(self.positions[source])

    def parent(self, i):
        return max(0, (i - 1) // 2)

    def left(self, i):
        return 2 * i + 1 if 2 * i + 1 < self.size else i

    def right(self, i):
        return 2 * i + 2 if 2 * i + 2 < self.size else i

    def heap_up(self, k):
        p = self.parent(k)
        p_node = self.struct[p]
        k_node = self.struct[k]

        if self.maxcapacity[p_node] < self.maxcapacity[k_node]:
            # Swap the nodes in heap and positions
            self.positions[k_node], self.positions[p_node] = p, k
            self.struct[k], self.struct[p] = p_node, k_node
            # Continue heap-up with the parent node
            self.heap_up(p)

    def heap_down(self, k):
        l = self.left(k)
        r = self.right(k)

        k_node = self.struct[k]
        l_node = self.struct[l]
        r_node = self.struct[r]

        larger_child = l
        if self.maxcapacity[r_node] > self.maxcapacity[l_node]:
            larger_child = r

        larger_child_node = self.struct[larger_child]

        # If the larger child has a greater capacity, swap and recurse
        if self.maxcapacity[larger_child_node] > self.maxcapacity[k_node]:
            self.positions[k_node], self.positions[larger_child_node] = larger_child, k
            self.struct[k], self.struct[larger_child] = larger_child_node, k_node
            self.heap_down(larger_child)

    def extract_max(self):
        top_node = self.struct[0]
        last_node = self.struct[self.size - 1]

        # Swap the top of the heap with the last element
        self.positions[top_node], self.positions[last_node] = self.size - 1, 0
        self.struct[0], self.struct[self.size - 1] = last_node, top_node

        # Reduce the size of the heap and heap-down to restore the heap property
        self.size -= 1
        if self.size > 0:
            self.heap_down(0)

        return top_node


def findMaxCapacity(n, links, s, t):
    # Step 1: Find the maximum capacity of any link
    maxcap = -1
    for link in links:
        capacity = link[2]
        if capacity > maxcap:
            maxcap = capacity

    # Step 2: Create an adjacency list to represent the network
    adjlist = []
    for i in range(n):
        adjlist.append([[], 0, -1])  # [Neighbors, Visited (0/1), Parent]

    for u, v, capacity in links:
        adjlist[u][0].append((v, capacity))
        adjlist[v][0].append((u, capacity))

    # Step 3: Initialize the heap
    heap = Heap(n, s, maxcap + 1)

    # Step 4: Process the nodes using a Dijkstra-like approach
    while heap.size > 0:
        current_node = heap.extract_max()
        adjlist[current_node][1] = 1  # Mark the current node as visited
        for neighbor, capacity in adjlist[current_node][0]:
            if adjlist[neighbor][1] == 0:  # If the neighbor is not visited
                possible_capacity = min(capacity, heap.maxcapacity[current_node])
                if possible_capacity > heap.maxcapacity[neighbor]:
                    adjlist[neighbor][2] = current_node  # Set the parent of the neighbor
                    heap.maxcapacity[neighbor] = possible_capacity
                    heap.heap_up(heap.positions[neighbor])

    # Step 5: Reconstruct the path from the target to the source
    path = []
    current_node = t
    while current_node != -1:
        path.append(current_node)
        current_node = adjlist[current_node][2]

    path.reverse()  # Reverse the path to get it from source to target

    return heap.maxcapacity[t], path


# Example Test Case
print(findMaxCapacity(8, [
    (0, 1, 5), (1, 2, 8), (2, 3, 6), (3, 4, 1), (4, 5, 15),
    (5, 6, 2), (6, 7, 3), (7, 0, 12), (1, 5, 7), (1, 6, 3),
    (2, 5, 9), (2, 7, 11), (3, 7, 14), (0, 4, 3), (0, 5, 4)
], 0, 0))
'''