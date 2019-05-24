def main(matrix) :
	parcels = []

	notYet = set()
	for i in range(len(matrix))
		for j in range(len(matrix[0]))
			notYet.add((i, j))

	while notYet :
		cell = notYet.pop()

		if (isUnplayable(matrix, cell)) :
			parcel.add('blocked')

		parcel = set().add(cell)
		second(matrix, notYet, cell, parcel)
		parcels.append(parcel)

	return parcels

def second(matrix, notYet, cell, parcel) :
	for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)) :
		if canMove(cell, matrix, direction) :
			moveOn = (cell[0]+direction[0], cell[1]+direction[1])
			parcel.add(moveOn)
			notYet.remove(moveOn)
			second(matrix, notYet, moveOn, parcel)

def canMove(cell, matrix, direction) :
	pass

def isUnplayable(matrix, cell) : 
	pass
