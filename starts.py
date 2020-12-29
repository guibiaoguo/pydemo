from turtle import *

def drawStar(x, y):
    pu()
    goto(x, y)
    pd()
    # set heading: 0
    seth(0)
    for i in range(14):
        fd(40)
        rt(144)

for x in range(-350, 350, 50):
    drawStar(x, 0)

done()