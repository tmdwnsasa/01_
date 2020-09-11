import turtle as t

t.speed(0)

size = 100
cell = 5
first_x = -250
first_y = 300
line_len = 500
col_dir = 270
row_dir = 0



def moveto(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

def gocolumn(i):
    t.setheading(col_dir)
    moveto(size * i + first_x, first_y)
    t.forward(line_len)

def gorow(i):
    t.setheading(row_dir)
    moveto(first_x , first_y - size * i)
    t.forward(line_len)

    
for i in range(cell + 1):
    gocolumn(i)
    gorow(i)
t.exitonclick()