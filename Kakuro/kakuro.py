from csp import *
from utils import *
from search import *

#alias python='/usr/bin/python3.4'

#some boards i found online converted in the format that my program wants them
board_10 = [[-1, -1, -1, [-1, 6], [-1, 3]], [-1, [-1, 4], [3, 3], 0, 0], [[10, -1], 0, 0, 0, 0,], [[3, -1], 0, 0, -1, -1]]
board_9 = [[-1, [-1, 20], [-1, 18], [-1, 10]], [[23, -1], 0, 0, 0], [[19, -1], 0, 0, 0], [[6, -1], 0, 0, 0]]
board_4 = [[-1, [-1, 11], [-1, 3]], [[3, -1], 0, 0], [[11, -1], 0, 0]]

#here specify which board the program will use
board = board_4


class kakuro(CSP):
	def __init__(self):
		#first initialize the variables the CSP will use
		self.create()
		#second call CSP to be initialized
		CSP.__init__(self, self.variables, self.domains, self.neighbors, self.kakuro_constraint)

	def kakuro_constraint(self, A, a, B, b):
		#saving in this variable the assignments that have been made so far
		assignment = self.infer_assignment()

		#if a is equal to any of the values of A's neighbors the constraint cannot be satisfied
		for n in self.neighbors[A]:
			if n in assignment:
				if assignment[n] == a:
					return False

		#also a and b cannot have the same value in order for the Kakuro to be correct
		if (a == b):
			return False

		#if b is equal to any of the values of B's neighbors the constraint cannot be satisfied
		for n in self.neighbors[B]:
			if n in assignment:
				if assignment[n] == b:
					return False

		#at this point i make 3 checks, one to see if the neighbors A and B satisfy their common constraint
		#the second and third are to see if every constraint that A or B have to satisfy don't break with the values a or b 

		for con in self.constr:
			if ((A in con[1]) and (B in con[1])):
				sum_of_neighbors = 0
				assigned_neighbors = 0
				for c in con[1]:
					if n in assignment:
						if (n != A) and (n != B):
							sum_of_neighbors += assignment[n]
							assigned_neighbors += 1
				sum_of_neighbors += a + b
				assigned_neighbors += 2
				if ((len(con[1]) > assigned_neighbors) and (sum_of_neighbors >= con[0])):
					return False
				if ((len(con[1]) == assigned_neighbors) and (sum_of_neighbors != con[0])):
					return False

		#checking if the constraints that only A has to obey are still ok
		for con in self.constr:
			if (A in con[1]) and (B not in con[1]):
				sum_of_neighbors = 0
				assigned_neighbors = 0
				for c in con[1]:
					if n in assignment:
						if n != A:
							sum_of_neighbors += assignment[n]
							assigned_neighbors += 1
				sum_of_neighbors += a
				assigned_neighbors += 1
				if ((len(con[1]) > assigned_neighbors) and (sum_of_neighbors >= con[0])):
					return False
				if ((len(con[1]) == assigned_neighbors) and (sum_of_neighbors != con[0])):
					return False

		#checking if the constraints that only A has to obey are still satisfied
		for con in self.constr:
			if (A not in con[1]) and (B in con[1]):
				sum_of_neighbors = 0
				assigned_neighbors = 0
				for c in con[1]:
					if n in assignment:
						if n != B:
							sum_of_neighbors += assignment[n]
							assigned_neighbors += 1
				sum_of_neighbors += b
				assigned_neighbors += 1
				if ((len(con[1]) > assigned_neighbors) and (sum_of_neighbors >= con[0])):
					return False
				if ((len(con[1]) == assigned_neighbors) and (sum_of_neighbors != con[0])):
					return False

		return True

	def create(self):
		#i traverse the whole board to create the variables the CSP will use
		self.variables = []

		for x in range(len(board)):
			for y in range(len(board[x])):
				row = board[x]
				element = row[y]
				#when element is 0, it represent a white square in the board that needs to be filled
				if element == 0:
					var1 = str(x)
					var2 = str(y)
					#i append all the variables inside the self.variables. Each variable has V in the front to say it is a variable
					#and after that it has 2 numbers that represent the coordinates of the value on the board
					self.variables.append("V"+var1+var2)

		#here i store all the constraints and the variables that have to satisfy the constraint
		self.constr = []

		for x in range(len(board)):
			for y in range(len(board[x])):
				row = board[x]
				element = row[y]
				#again i traverse the board, but when element is something else than, -1 or 0 it means at stores a constraint
				if ((element != -1) and (element != 0)):
					#element[0] is the constraint for the rows
					if (element[0] != -1):
						self.con = []
						for z in range(y+1, len(row)):
							if (row[z] != 0):
								break
							var1 = str(x)
							var2 = str(z)
							self.con.append("V"+var1+var2)
						self.constr.append((element[0], self.con))
					if (element[1] != -1):
						#element[1] is the contraint for the columns
						self.con = []
						for z in range(x+1, len(board)):
							r = board[z]
							if (r[y] != 0):
								break
							var1 = str(z)
							var2 = str(y)
							self.con.append("V"+var1+var2)
						self.constr.append((element[1], self.con))

		#creating the domain of each variable
		self.domains = {}

		for element in self.variables:
			self.domains[element] = []
			for i in range(1, 10):
				self.domains[element].append(i)


		self.neighbors = {}

		for element in self.variables:
			#i traverse the variables to find their neighbors using the constr list i created
			self.neighbors[element] = []
			for i in self.constr:
				#for the neighbors i only care about i[1] where i have stored the variables that have to satisfy the same constraint
				if element in i[1]:
					whole = i[1]
					for y in range(len(i[1])):
						#now i append every variable except for the variable i'm currently checking, aka the element
						if whole[y] != element:
							self.neighbors[element].append(whole[y])

		#print stuff to know they work correctly
		print("\nVariables:", self.variables)
		print("\nDomains:", self.domains)
		print("\nNeighbors:", self.neighbors)
		print("\nConstraints:", self.constr)


def main():
	fin = kakuro()
	magic = backtracking_search(fin, select_unassigned_variable=mrv, inference=forward_checking)
	print("\nSolution:", magic)

	fin2 = kakuro()
	magic2 = backtracking_search(fin2, inference=forward_checking)
	print("\nSolution:", magic2)


if __name__ == "__main__":
	main()