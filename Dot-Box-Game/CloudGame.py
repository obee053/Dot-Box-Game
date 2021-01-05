# Imports
from turtle import *
from time import *
from operator import itemgetter
import random

title("Dots-N-Boxes")
screen = getscreen()
screen.listen()
hideturtle() # Hide the turtle icon, cuz it's ugly
tracer(0,0) # Used to remove turtle animation, update() to refresh screen now
screen.setworldcoordinates(0,0,500,500) # Set screen cordinates to quadrant 1 only
penup()

# There are two main variables we use here:
# 1. A seperate variable for each line, which allows easier screen drawing and checking for errors
# 2. A seperate variable for each box some belonging to more than one line, which allows for easier win checking
verticals = [0,0,0,0,0,0,0,0,0,0,0,0] # Read from bottom left to upper right
horizontals = [0,0,0,0,0,0,0,0,0,0,0,0]
boxes = [0,0,0,0,0,0,0,0,0]
turn = 1
grid = 4

def main():
    # Update Score
    printScore()
    goto(100,100)
    for i in range(1,5):
        for i in range(1,5):
            dot(10)
            forward(100)
        goto((xcor() - 400),(ycor() + 100))

    # Get input
    onscreenclick(clickHandler)
    mainloop()

def clickHandler(rawx,rawy):
    x = int(rawx//1) # Round click to a full int
    y = int(rawy//1)
    for xnum in range(1,5):
        tempx = (xnum % 4) + 1
        for ynum in range(1,4):
            tempy = (ynum % 3) + 1
            if ((tempx * 100) + 10) >= x >= ((tempx * 100) - 10) and ((tempy * 100) + 90) >= y >= ((tempy * 100) + 10):
                onscreenclick(None)
                updateVariable(tempx, tempy, True)
    for xnum in range(1,4):
        tempx = (xnum % 3) + 1
        for ynum in range(1,5):
            tempy = (ynum % 4) + 1
            if ((tempx * 100) + 90) >= x >= ((tempx * 100) + 10) and ((tempy * 100) + 10) >= y >= ((tempy * 100) - 10):
                onscreenclick(None)
                updateVariable(tempx, tempy, False)
    goto(250,30)
    write("Click a spot", align="center", font=("Arial", 50))


def updateVariable(x, y, isVertical):
    goAgain = False
    global verticals
    global horizontals
    if isVertical:
        verticals[((y - 1) * 4 + x)-1] = 12
    else:
        horizontals[((y - 1) * 3 + x)-1] = 1

    # Draw lines
    clear()
    for xnum in range(1,5): # 4
        for ynum in range(1,4): # 3
            if verticals[((ynum - 1) * 4 + xnum) - 1] != 0:
                goto((100 * xnum), (100 * ynum))
                pendown()
                goto((100 * xnum), (100 * (ynum + 1)))
                penup()
    for xnum in range(1,4):
        for ynum in range(1,5):
            if horizontals[((ynum - 1) * 3 + xnum) - 1] != 0:
                goto((100 * xnum), (100 * ynum))
                pendown()
                goto((100 * (xnum + 1)), (100 * ynum))
                penup()

    # Check for box filled
    for i in range(0,9):
        yMulti = 0
        if i >= 6:
            yMulti = 2
        elif i >= 3:
            yMulti = 1
        if (0 not in itemgetter(i,(i+3))(horizontals)) and (0 not in itemgetter((i + yMulti),(i+ yMulti + 1))(verticals)):
            if boxes[i] == 0:
                boxes[i] = turn
                goAgain = True


    # Draw boxes
    for xnum in range(1,4):
        for ynum in range(1,4):
            pos = ((ynum-1) * 3) + xnum - 1
            if boxes[pos] != 0:
                goto((100 * xnum + 50), (100 * ynum + 50))
                write(boxes[pos], align="center", font=("Arial", 50))

    # Detect a winner
    if not 0 in boxes:
        clear()
        goto(250,250)
        score = countScore()
        if score[0] > score[1]:
            write("Player 1 wins", align="center", font=("Arial", 50))
        else:
            write("Player 2 wins", align="center", font=("Arial", 50))
        goto(100,100)
        write("Play again", align="center", font=("Arial", 50))
        goto(400,100)
        write("Quit", align="center", font=("Arial", 50))
        onscreenclick(endGame)
        mainloop()

    finishUp(goAgain)
def printScore():
    score = countScore()
    goto(100, 450)
    if turn == 1:
        write("Player 1: " + str(score[0]), align="center", font=("Arial", 50, "bold"))
        goto(400, 450)
        write("Player 2: " + str(score[1]), align="center", font=("Arial", 50))
    if turn == 2:
        write("Player 1: " + str(score[0]), align="center", font=("Arial", 50))
        goto(400, 450)
        write("Player 2: " + str(score[1]), align="center", font=("Arial", 50, "bold"))


def endGame(rawx, rawy):
    global verticals
    global horizontals
    global boxes
    global turn
    x = int(rawx//1) # Round click to a full int
    y = int(rawy//1)
    if 150 >= x >= 50 and 150 >= y >= 50:
        onscreenclick(None)
        verticals = [0,0,0,0,0,0,0,0,0,0,0,0] # Read from bottom left to upper right
        horizontals = [0,0,0,0,0,0,0,0,0,0,0,0]
        boxes = [0,0,0,0,0,0,0,0,0]
        turn = 1
        clear()
        finishUp(True)
    if 450 >= x >= 350 and 150 >= y >= 50:
        raise SystemExit

def countScore():
    player1 = 0
    player2 = 0
    for i in range(0,9):
        if boxes[i] == 1:
            player1 += 1
        elif boxes[i] == 2:
            player2 += 1
    return [player1, player2]


def finishUp(again):
    global turn
    if turn == 1 and not again:
        turn = 2
    elif not again:
        turn = 1
    main()
main()

screen._root.mainloop() # Stops program from quitting while waiting for input