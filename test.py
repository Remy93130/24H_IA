def genererTab(mapString):
	lines = mapString.split('|')
	matrix = []
	for line in lines:
		matrix.append(line.split(':'))
	for i in range(10):
		for j in range(10):
			matrix[i][j] = '{0:07b}'.format(int(matrix[i][j]))
	return matrix

def main(matrix) :
	parcels = []

	notYet = set()
	for i in range(10):
		for j in range(10):
			notYet.add((i, j))

	while notYet :
		cell = notYet.pop()

		parcel = set()

		if (isUnplayable(matrix, cell)) :
			parcel.add('blocked')
			
		parcel.add(cell)
		
		second(matrix, notYet, cell, parcel)
		parcels.append(parcel)

	return parcels

def second(matrix, notYet, cell, parcel) :
	for direction in ((1, 0), (0, 1), (-1, 0), (0, -1)) :
		moveOn = (cell[0]+direction[0], cell[1]+direction[1])
		if moveOn in notYet :
			if canMove(cell, matrix, direction) :
				parcel.add(moveOn)
				notYet.remove(moveOn)
				second(matrix, notYet, moveOn, parcel)

def canMove(cell, matrix, direction) :
	cell_x = cell[0]
	cell_y = cell[1]
	dir_x = direction[0]
	dir_y = direction[1]
	if dir_x == 1 : return cell_x < 9 and matrix[cell_x][cell_y][4] == '0'#bas
	if dir_x == -1 : return cell_x > 0 and matrix[cell_x][cell_y][6] == '0' #haut
	if dir_y == 1 : return cell_y < 9 and matrix[cell_x][cell_y][3] == '0' #droite
	if dir_y == -1 : return cell_y > 0 and matrix[cell_x][cell_y][5] == '0' #gauche

def isUnplayable(matrix, cell) : 
	return int(matrix[cell[0]][cell[1]][:2]) != 0
	
