def genererTab(mapString):
	lines = mapString.split('|')
	matrix = []
	for line in lines:
		matrix.append(line.split(':'))
	count = 0
	for i in range(10):
		for j in range(10):
			if int(matrix[i][j]) < 32: count+=1
	print(count) 
	for i in range(10):
		for j in range(10):
			matrix[i][j] = '{0:06b}'.format(int(matrix[i][j]))
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
	if dir_x == 1 : return matrix[cell_x][cell_y][3] == '0' #bas
	if dir_x == -1 : return matrix[cell_x][cell_y][5] == '0' #haut
	if dir_y == 1 : return matrix[cell_x][cell_y][2] == '0' #droite
	if dir_y == -1 : return matrix[cell_x][cell_y][4] == '0' #gauche

def isUnplayable(matrix, cell) : 
	return int(matrix[cell[0]][cell[1]][:2]) != 0
	
	
#print(main(genererTab('3:9:71:69:65:65:65:65:65:73|2:8:3:9:70:68:64:64:64:72|6:12:2:8:3:9:70:68:64:72|11:11:6:12:6:12:3:9:70:76|10:10:11:11:67:73:6:12:3:9|14:14:10:10:70:76:7:13:6:12|3:9:14:14:11:7:13:3:9:75|2:8:7:13:14:3:9:6:12:78|6:12:3:1:9:6:12:35:33:41|71:77:6:4:12:39:37:36:36:44|')))
print(main(genererTab))
