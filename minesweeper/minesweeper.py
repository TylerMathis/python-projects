import random
import pygame

pygame.init()

# define colors
GRAY = (200, 200, 200)
DARKGRAY = (180, 180, 180)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

FONT = pygame.font.Font("DS-DIGI.TTF", 50)
FLAG = pygame.image.load("flag.png")
BOMB = pygame.image.load("bomb.png")

def main():

	# make screen
	displayInfo = pygame.display.Info()
	width = int(displayInfo.current_w / 1.3)
	height = int(displayInfo.current_h / 1.3)
	size = (width, height)
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("MediiSweeper")

	# init clock
	clock = pygame.time.Clock()

	# important values related to board sizes
	cellSize = int(width / 40)
	cellsX = int(width / cellSize)
	cellsY = int(height / cellSize)
	cellsInfo = {"size": cellSize, "numX": cellsX, "numY": cellsY}

	# scale FLAG image
	global FLAG, BOMB
	FLAG = pygame.transform.scale(FLAG, (int(cellSize - (cellSize / 2)), int(cellSize - (cellSize / 8))))
	BOMB = pygame.transform.scale(BOMB, (int(cellSize - (cellSize / 10)), int(cellSize - (cellSize / 10))))

	# setup board
	cells = setupBoard(cellsX, cellsY)
	drawBoard(screen, cells, cellsInfo)

	mainLoop(screen, clock, cells, cellsInfo)

def mainLoop(screen, clock, cells, cellsInfo):

	running = True

	while running:

		# get events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				cells = updateBoard(screen, cells, cellsInfo, pos[0], pos[1], event.button)
				drawBoard(screen, cells, cellsInfo)

		pygame.display.flip()

		clock.tick(20)

	# end program
	pygame.quit()

def setupBoard(cellsX, cellsY):
	# main 2D array that holds data about the game
	# (bomb/notBomb, bombsNearby, revealed, flag)
		# draw 100xn grid of squares
	cells = [[{"bomb": True if not random.randint(0, 5) else False, "neighbors": 0, "revealed": False, "flag": False} for j in range(cellsY)] for i in range(cellsX)]

	for i in range(0, cellsX):
		for j in range(0, cellsY):
			calcNeighbors(cells, cellsX, cellsY, i, j)

	return cells

def calcNeighbors(cells, cellsX, cellsY, xLoc, yLoc):

	for i in range(-1, 2):
		for j in range(-1, 2):
			newX = xLoc + i;
			newY = yLoc + j;

			# they are not the og square
			if not (newX == xLoc and newY == yLoc):
				if newX >= 0 and newX < cellsX:
					if newY >= 0 and newY < cellsY:
						if cells[newX][newY]["bomb"]:
							cells[xLoc][yLoc]["neighbors"] += 1

# click type (1 - left, 3 - right)
def updateBoard(screen, cells, cellsInfo, x, y, clickType):

	cellSize = cellsInfo["size"]

	xLoc = int(x / cellSize)
	yLoc = int(y / cellSize)

	if clickType == 1:
		if cells[xLoc][yLoc]["bomb"]:
			revealAll(screen, cells, cellsInfo)
		# TODO: UPDATE FOR FULL FUNCTIONALITY
		recursiveReveal(cells, cellsInfo, xLoc, yLoc)
	else:
		cells[xLoc][yLoc]["flag"] = not cells[xLoc][yLoc]["flag"]

	return cells

def recursiveReveal(cells, cellsInfo, xLoc, yLoc):

	# unpack cellsInfo
	cellsX = cellsInfo["numX"]
	cellsY = cellsInfo["numY"]

	cells[xLoc][yLoc]["revealed"] = True

	if cells[xLoc][yLoc]["neighbors"] == 0:
		for i in range(-1, 2):
			for j in range(-1, 2):
				newX = xLoc + i;
				newY = yLoc + j;

				# they are not the og square
				if not (newX == xLoc and newY == yLoc):
					if newX >= 0 and newX < cellsX:
						if newY >= 0 and newY < cellsY:
							if not cells[newX][newY]["revealed"]:
								recursiveReveal(cells, cellsInfo, newX, newY)

def drawBoard(screen, cells, cellsInfo):

	# unpack cellsInfo
	cellSize = cellsInfo["size"]
	cellsX = cellsInfo["numX"]
	cellsY = cellsInfo["numY"]

	# fill background
	screen.fill(DARKGRAY)

	for i in range(0, cellsX):
		for j in range(0, cellsY):
			if cells[i][j]["revealed"] == True:
				pygame.draw.rect(screen, GRAY, [i * cellSize + 1, j * cellSize + 1, cellSize - 2, cellSize - 2], 0)
				if cells[i][j]["bomb"]:
					screen.blit(BOMB, (int(i * cellSize + (cellSize / 20)), int(j * cellSize + (cellSize / 20))))
				else:
					neighbors = cells[i][j]["neighbors"]
					if neighbors == 1:
						color = (2, 0, 251)
					elif neighbors == 2:
						color = (5, 125, 5)
					elif neighbors == 3:
						color = (250, 2, 1)
					elif neighbors == 4:
						color = (2, 0, 126)
					elif neighbors == 5:
						color = (129, 1, 1)
					elif neighbors == 6:
						color = (0, 128, 128)
					elif neighbors == 7:
						color = (0, 0, 0)
					else:
						color = (128, 128, 128)

					if neighbors != 0:
						textToScreen(screen, neighbors, (i * cellSize + (cellSize / 4)), (j * cellSize + (cellSize / 25)), color)

			elif cells[i][j]["flag"] == True:
				pygame.draw.rect(screen, WHITE, [i * cellSize + 1, j * cellSize + 1, cellSize - 2, cellSize - 2], 0)
				screen.blit(FLAG, (int(i * cellSize + (cellSize / 4)), int(j * cellSize + (cellSize / 16))))
			else:
				pygame.draw.rect(screen, WHITE, [i * cellSize + 1, j * cellSize + 1, cellSize - 2, cellSize - 2], 0)

def revealAll(screen, cells, cellsInfo):

	# unpack cellsInfo
	cellSize = cellsInfo["size"]
	cellsX = cellsInfo["numX"]
	cellsY = cellsInfo["numY"]

	for i in range(0, cellsX):
		for j in range(0, cellsY):
			cells[i][j]["revealed"] = True

	drawBoard(screen, cells, cellsInfo)



def textToScreen(screen, text, x, y, color):

	text = str(text)
	text = FONT.render(text, True, color)
	screen.blit(text, (int(x), int(y)))

if __name__ == '__main__':
	main()