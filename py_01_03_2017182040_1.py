
import turtle

turtle.speed(0)
first_x =-150;
first_y =50;

def moveto(a, b):
	turtle.penup()
	turtle.goto(a,b)
	turtle.pendown()

def jiot(a,b):
	moveto(a, b)
	turtle.setheading(0)
	turtle.forward(70)
	turtle.right(140)
	turtle.forward(90)
	turtle.backward(45)
	turtle.left(100)
	turtle.forward(45)

def ieung(a,b):
	moveto(a, b)
	turtle.setheading(180)
	turtle.circle(32)

def nieun(a,b):
	moveto(a, b)
	turtle.setheading(270)
	turtle.forward(40)
	turtle.left(90)
	turtle.forward(100)

	
def eu(a,b):
	moveto(a, b)
	turtle.setheading(270)
	turtle.forward(100)
	turtle.backward(60)
	turtle.right(90)
	turtle.forward(30)


def yu(a,b):
	moveto(a, b)
	turtle.setheading(0)
	turtle.forward(140)
	turtle.backward(90)
	turtle.right(90)
	turtle.forward(30)
	turtle.backward(30)
	turtle.left(90)
	turtle.forward(40)
	turtle.right(90)
	turtle.forward(30)

def yi(a,b):
	moveto(a, b)
	turtle.setheading(270)
	turtle.forward(150)

	
jiot(first_x-50, first_y + 50)
eu(first_x+70, first_y+60)
ieung(first_x + 30, first_y - 30)
ieung(first_x + 180, first_y + 55)
yu(first_x + 110,first_y - 20)
nieun(first_x+140, first_y - 50)
jiot(first_x+280, first_y + 30)
eu(first_x + 380, first_y + 40)
yi(first_x + 400, first_y + 50)
turtle.exitonclick()