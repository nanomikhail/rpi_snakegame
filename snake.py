import time
import random
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

###################################
GPIO.setup(21, GPIO.OUT)####-string
GPIO.setup(10, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)###--------
###################################
GPIO.setup(12, GPIO.OUT)###-column-
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(8,  GPIO.OUT)###---------
####################################

GPIO.setup(15,  GPIO.IN, pull_up_down = GPIO.PUD_DOWN)#up
GPIO.setup(13,  GPIO.IN, pull_up_down = GPIO.PUD_DOWN)#down
GPIO.setup(11,  GPIO.IN, pull_up_down = GPIO.PUD_DOWN)#left
GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)#right

def string(n, number):
	if n==number:
		return 0
	else:
		return 1

snake = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

snakelook = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],]

eatvar = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0],[2,1],[2,2],[2,3],[2,4],[3,0],[3,1],[3,2],[3,3],[3,4],[4,0],[4,1],[4,2],[4,3],[4,4],]
eat = [0,0,0]

upend =     [[0,0],[0,1],[0,2],[0,3],[0,4]]
bottomend = [[4,0],[4,1],[4,2],[4,3],[4,4]]
leftend =   [[0,0],[1,0],[2,0],[3,0],[4,0]]
rightend =  [[0,4],[1,4],[2,4],[3,4],[4,4]]

snakelenth = 1

br=0

def clear():
	arr_cl = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
	GPIO.output(21, 1)
	GPIO.output(10, 1)
	GPIO.output(24, 1)
	GPIO.output(23, 1)
	GPIO.output(26, 1)
	GPIO.output(8,  0)
	GPIO.output(22, 0)
	GPIO.output(18, 0)
	GPIO.output(16, 0)
	GPIO.output(12, 0)

def display(array):
	i=0
	t=0
	t2=1000
	while t<t2:
		GPIO.output(21, string(i, 0))
		GPIO.output(10, string(i, 1))
		GPIO.output(24, string(i, 2))
		GPIO.output(23, string(i, 3))
		GPIO.output(26, string(i, 4))
		GPIO.output(8,  array[i][0])
		GPIO.output(22, array[i][1])
		GPIO.output(18, array[i][2])
		GPIO.output(16, array[i][3])
		GPIO.output(12, array[i][4])
		clear()
		t=t+1
		i=i+1
		if i==5: i=0
		time.sleep(0.001)

def gameover():
	pic = [
[0,1,1,1,0],
[1,1,0,1,1],
[1,0,1,0,1],
[0,1,0,1,0],
[0,1,1,1,0]]
	display(pic)

#--------------------------------------##spawn-begin------#
spawn = random.randrange(0, 4, 1)
spawnarr = [[4,2],[0,2],[2,4],[2,0]]
if spawn == 0:
	direction = 0 #up↑
elif spawn == 1:
	direction = 1 #down↓
elif spawn == 2:
	direction = 2 #left←
elif spawn == 3:
	direction = 3 #right→
snake[spawnarr[spawn][0]][spawnarr[spawn][1]] = 1
snakelook[0][0] = spawnarr[spawn][0]
snakelook[0][1] = spawnarr[spawn][1]
snakelook[0][2] = 1
#--------------------------------------##spawn-end--------#

for j in range(0, 24):
	if snakelook[j][2] != 0:
		snake[snakelook[j][0]][snakelook[j][1]] = 1
		
while True:

	for q in range(0,1):
		display(snake)
		if GPIO.input(15) == True:
			direction = 0
			br=0
		elif GPIO.input(13) == True:
			direction = 1
			br=0
		elif GPIO.input(11) == True:
			direction = 2
			br=0
		elif GPIO.input(19) == True:
			direction = 3
			br=0

	if br == 1:
		gameover()
		break

	while eat[2] != 1:
	 	eatpos = random.randrange(0, 25, 1)
	 	eat[0] = eatvar[eatpos][0]
	 	eat[1] = eatvar[eatpos][1]
	 	eat[2] = 1
	 	for y in range(0,24):
	 		if snakelook[y][0] == eat[0] and snakelook[y][1] == eat[1] and snakelook[y][2] != 0:
	 			eat[2] = 0

	if snakelenth != 1:
		for x in range(0, snakelenth-1):
			snakelook[x][0] = snakelook[x+1][0]
			snakelook[x][1] = snakelook[x+1][1]

	if direction == 0:
		snakelook[snakelenth-1][0] = snakelook[snakelenth-1][0]-1
		for v in range(0,5):
			if snakelook[snakelenth-1][0] == upend[v][0] and snakelook[snakelenth-1][1] == upend[v][1]:
				br = 1
		for z in range(0, snakelenth-1):
			if snakelook[snakelenth-1][0]-1 == snakelook[z][0] and snakelook[snakelenth-1][1] == snakelook[z][1]:
				br = 1
			if snakelook[snakelenth-1][0] == snakelook[z][0] and snakelook[snakelenth-1][1] == snakelook[z][1]:
				br = 1
		if snakelook[snakelenth-1][0]-1 == eat[0] and snakelook[snakelenth-1][1] == eat[1]:
			snakelenth = snakelenth+1
			snakelook[snakelenth-1][0] = eat[0]
			snakelook[snakelenth-1][1] = eat[1]
			snakelook[snakelenth-1][2] = 1
			eat[2] = 0
	if direction == 1:
		snakelook[snakelenth-1][0] = snakelook[snakelenth-1][0]+1
		for v in range(0,5):
			if snakelook[snakelenth-1][0] == bottomend[v][0] and snakelook[snakelenth-1][1] == bottomend[v][1]:
				br = 1
		for z in range(0, snakelenth-1):
			if snakelook[snakelenth-1][0]+1 == snakelook[z][0] and snakelook[snakelenth-1][1] == snakelook[z][1]:
				br = 1
			if snakelook[snakelenth-1][0] == snakelook[z][0] and snakelook[snakelenth-1][1] == snakelook[z][1]:
				br = 1
		if snakelook[snakelenth-1][0]+1 == eat[0] and snakelook[snakelenth-1][1] == eat[1]:
			snakelenth = snakelenth+1
			snakelook[snakelenth-1][0] = eat[0]
			snakelook[snakelenth-1][1] = eat[1]
			snakelook[snakelenth-1][2] = 1
			eat[2] = 0
	if direction == 2:
		snakelook[snakelenth-1][1] = snakelook[snakelenth-1][1]-1
		for v in range(0,5):
			if snakelook[snakelenth-1][0] == leftend[v][0] and snakelook[snakelenth-1][1] == leftend[v][1]:
				br = 1
		for z in range(0, snakelenth-1):
			if snakelook[snakelenth-1][0] == snakelook[z][0] and snakelook[snakelenth-1][1]-1 == snakelook[z][1]:
				br = 1
			if snakelook[snakelenth-1][0] == snakelook[z][0] and snakelook[snakelenth-1][1] == snakelook[z][1]:
				br = 1
		if snakelook[snakelenth-1][0] == eat[0] and snakelook[snakelenth-1][1]-1 == eat[1]:
			snakelenth = snakelenth+1
			snakelook[snakelenth-1][0] = eat[0]
			snakelook[snakelenth-1][1] = eat[1]
			snakelook[snakelenth-1][2] = 1
			eat[2] = 0
	if direction == 3:
		snakelook[snakelenth-1][1] = snakelook[snakelenth-1][1]+1
		for v in range(0,5):
			if snakelook[snakelenth-1][0] == rightend[v][0] and snakelook[snakelenth-1][1] == rightend[v][1]:
				br = 1
		for z in range(0, snakelenth-1):
			if snakelook[snakelenth-1][0] == snakelook[z][0] and snakelook[snakelenth-1][1]+1 == snakelook[z][1]:
				br = 1
			if snakelook[snakelenth-1][0] == snakelook[z][0] and snakelook[snakelenth-1][1] == snakelook[z][1]:
				br = 1
		if snakelook[snakelenth-1][0] == eat[0] and snakelook[snakelenth-1][1]+1 == eat[1]:
			snakelenth = snakelenth+1
			snakelook[snakelenth-1][0] = eat[0]
			snakelook[snakelenth-1][1] = eat[1]
			snakelook[snakelenth-1][2] = 1
			eat[2] = 0

	snake = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

	for j in range(0, 24):
		if snakelook[j][2] != 0:
			snake[snakelook[j][0]][snakelook[j][1]] = 1

	snake[eat[0]][eat[1]] = 1

	time.sleep(0.01)