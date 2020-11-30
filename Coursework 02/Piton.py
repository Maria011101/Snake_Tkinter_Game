from tkinter import *
import tkinter.messagebox as box
import random

#This function runs the game
def play_game():
    global score
    global window
    global canvas
    global direction
    global menu_window
    global food1
    global food1X
    global food1Y
    global food2
    global food2X
    global food2Y
    global width
    global height
    global portals_placed
    global portals


    menu_window.destroy()

    def setWindowDimensions(w,h):
        window = Tk() #create window
        window.title("Snake Game") #title of window
        # ws = window.winfo_screenwidth() # computers screen size
        # hs = window.winfo_screenheight()
        # x = (ws/2) - (w/2) # calculate center
        # y = (hs/2) - (h/2)
        # window.geometry('%dx%d+%d+%d' % (w, h, x, y)) # window size
        window.geometry("1080x1920")
        return window

    def placeFood():
        global food1
        global food1X
        global food1Y
        global food2
        global food2X
        global food2Y

        food1 = canvas.create_rectangle( 0, 0, snakeSize, snakeSize, fill = "steel blue" )
        food1X = random.randint(0, width-snakeSize)
        food1Y = random.randint(0, height-snakeSize)
        canvas.move(food1, food1X, food1Y)

        food2 = canvas.create_rectangle( 0, 0, snakeSize, snakeSize, fill = "#824670" )
        food2X = random.randint(0, width-snakeSize)
        food2Y = random.randint(0, height-snakeSize)
        canvas.move(food2, food2X, food2Y)

    def leftKey(event):
        global direction
        direction = "left"

    def rightKey(event):
        global direction
        direction = "right"

    def upKey(event):
        global direction
        direction = "up"

    def downKey(event):
        global direction
        direction = "down"

    #Moving the snake
    def moveSnake():
        global portals_placed
        global portals
        canvas.pack()
        positions = []
        positions.append(canvas.coords(snake[0])) #Adding the snake's head coords to the list

        #Checking to see if the snake reached the edge and teleporting it to the other side of the canvas
        if positions[0][0] < 0:
            canvas.coords( snake[0], width, positions[0][1], width-snakeSize, positions[0][3] )
        elif positions[0][2] > width:
            canvas.coords(snake[0], 0-snakeSize, positions[0][1], 0, positions[0][3])
        elif positions[0][3] > height:
            canvas.coords(snake[0], positions[0][0], 0 - snakeSize, positions[0][2], 0)
        elif positions[0][1] < 0:
            canvas.coords(snake[0], positions[0][0],height, positions[0][2], height-snakeSize)

    #Updating the coordonates of the snake's head
        positions.clear()
        positions.append(canvas.coords(snake[0]))

    #Moving the snake
        if direction == "left":
            canvas.move(snake[0], -snakeSize,0)
        elif direction == "right":
            canvas.move(snake[0], snakeSize,0)
        elif direction == "up":
            canvas.move(snake[0], 0,-snakeSize)
        elif direction == "down":
            canvas.move(snake[0], 0, snakeSize)

        sHeadPos = canvas.coords(snake[0])
        #Checking to see if the snake collided with food
        foodPos1 = canvas.coords(food1)
        if overlapping(sHeadPos, foodPos1):
            moveFood()
            growSnake()

        foodPos2 = canvas.coords(food2)
        if overlapping(sHeadPos,foodPos2):
            grow_2blocks = True
            moveFood()
            growSnake(grow_2blocks)

        for i in range(1,len(snake)):
            if overlapping(sHeadPos, canvas.coords(snake[i])):
                gameOver = True
                canvas.create_text(width/2, height/2, fill="white", font="Times 20 italic bold", text="Game Over!")

        for i in range(1,len(snake)):
            positions.append(canvas.coords(snake[i]))
        for i in range(len(snake)-1):
            canvas.coords(snake[i+1], positions[i][0], positions[i][1], positions[i][2], positions[i][3])

    #Looping through the function if gameOver is False
        if 'gameOver' not in locals():
            window.after(90, moveSnake)
        else:
            endScreen()

    def moveFood():
        global food1, food1X, food1Y, food2, food2X, food2Y
        canvas.move(food1, (food1X*(-1)), (food1Y*(-1)))
        food1X = random.randint(0,width-snakeSize)
        food1Y = random.randint(0,height-snakeSize)
        canvas.move(food1, food1X, food1Y)

        canvas.move(food2, (food2X*(-1)), (food2Y*(-1)))
        food2X = random.randint(0,width-snakeSize)
        food2Y = random.randint(0,height-snakeSize)
        canvas.move(food2, food2X, food2Y)

    def growSnake(grow_2blocks = False):
    #we add a block at the end of the snake, depending on the direction
        lastElement = len(snake)-1
        lastElementPos = canvas.coords(snake[lastElement])
        snake.append(canvas.create_rectangle(0, 0, snakeSize, snakeSize, fill="#FDF3F3"))

#adding  a block to the right of the last one if the direction is left
        if (direction == "left"):
            canvas.coords(snake[lastElement+1], lastElementPos[0] + snakeSize, lastElementPos[1], lastElementPos[2] + snakeSize, lastElementPos[3])

#adding  a block to the left of the last one if the direction is right
        elif (direction == "right"):
            canvas.coords(snake[lastElement+1], lastElementPos[0] - snakeSize, lastElementPos[1], lastElementPos[2] - snakeSize, lastElementPos[3])

#adding  a block under the last one if the direction is up
        elif (direction == "up"):
            canvas.coords(snake[lastElement+1], lastElementPos[0], lastElementPos[1] + snakeSize, lastElementPos[2], lastElementPos[3]+snakeSize)

#adding  a block above the last one if the direction is down
        else:
            canvas.coords(snake[lastElement+1], lastElementPos[0], lastElementPos[1]-snakeSize, lastElementPos[2], lastElementPos[3]-snakeSize)

    #We add the second block only if grow_2blocks is True (the snake has eaten the red food)
        if grow_2blocks == True:
            lastElement = len(snake)-1
            lastElementPos = canvas.coords(snake[lastElement])
            snake.append(canvas.create_rectangle(0, 0, snakeSize, snakeSize, fill="#FDF3F3"))

            if (direction == "left"):
                canvas.coords(snake[lastElement+1], lastElementPos[0]+snakeSize, lastElementPos[1], lastElementPos[2]+snakeSize, lastElementPos[3])

            elif (direction == "right"):
                canvas.coords(snake[lastElement+1], lastElementPos[0] + snakeSize, lastElementPos[1], lastElementPos[2] -snakeSize, lastElementPos[3])

            elif (direction == "up"):
                canvas.coords(snake[lastElement+1], lastElementPos[0], lastElementPos[1]+snakeSize, lastElementPos[2], lastElementPos[3]+snakeSize)

            else:
                canvas.coords(snake[lastElement+1], lastElementPos[0], lastElementPos[1]-snakeSize, lastElementPos[2], lastElementPos[3]-snakeSize)


        global score
        score += 10
        txt = "Score:" + str(score)
        canvas.itemconfigure(scoreText, text=txt)

    def overlapping(a,b):
        if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
            return True
        else:
            return False



     def endScreen():
        global end_screen
        global end_score

        end_screen = canvas.create_rectangle(0, 0 , 800, 800)
        end_screen.pack()

        end_score = Label(window, text = "Your Score:" + str(score), font = ("Times 20 italic bold"))


    width = 1000 # width of snake’s world
    height = 850 # height of snake’s world

    #creating the window
    window = setWindowDimensions(width, height)
    canvas = Canvas(window, bg="black", width=width, height=height)

    #Creating the snake
    snake = []
    snakeSize = 20
    snake.append(canvas.create_rectangle(snakeSize, snakeSize, snakeSize * 2, snakeSize * 2, fill = "white" ))

    score = 0 #the score starts at 0
    txt = "Score:" + str(score)
    #Creating a text widget to show the score
    scoreText = canvas.create_text( width/2 , 20 , fill="white", font = "Times 20 italic bold", text = txt)

    canvas.bind("<Left>", leftKey)
    canvas.bind("<Right>", rightKey)
    canvas.bind("<Up>", upKey)
    canvas.bind("<Down>", downKey)
    canvas.focus_set()
    direction = "right"


    placeFood()
    moveSnake()
    window.mainloop()

#This displays the menu page
def menu_page():
    global menu_window
    global username_window

    #destroying the enter username window
    username_window.destroy()

    menu_window = Tk()
    menu_window.title("P I T O N")
    menu_window.geometry("1080x1920")
    menu_window.configure( bg = "#ABC798")

    #Title
    menuTitle = Label(menu_window, text = "MENU", bg = "#ABC798", fg = "#1A1F16", font = ("Arial, 50"))
    menuTitle.place( x = 450, y = 100)

    #Menu Buttons

    playButton = Button(text = "Start", bg = "#5D737E", activebackground = "#D68C45", height = 2 ,width = 15, font = ("Arial, 15"), command = play_game)
    playButton.place( x = 200, y = 300)

    rulesButton = Button(text = "Rules", bg = "#5D737E", activebackground = "#D68C45", height = 2 ,width = 15, font = ("Arial, 15"))
    rulesButton.place( x = 200, y = 400)

    settingsButton = Button(text = "Settings", bg = "#5D737E", activebackground = "#D68C45", height = 2 ,width = 15, font = ("Arial, 15"))
    settingsButton.place( x = 200, y = 500)

    exitButton = Button(text = "Exit", bg = "#5D737E", activebackground = "#D68C45", height = 2 ,width = 15, font = ("Arial, 15"), command = menu_window.destroy)
    exitButton.place( x = 200, y = 600)

    #Menu picture of snake
    pythonImage = PhotoImage(file = "snake.png")
    python = Label(image = pythonImage , bg = "#ABC798")
    python.place( x = 500, y = 400)



    menu_window.mainloop()

#A page where we get the username
def enter_username_page():
    global username_window
    global username

    #This displays a warning if the username is empty
    def validate_user_input():
        if username.get() == '':
            box.showwarning("Warning", "Please enter a valid name")
        else:
            menu_page()

#Creating the page and configuring it
    username_window = Tk()
    username_window.title("Welcome to PITON!")
    username_window.geometry("350x250")
    username_window.configure(bg = "#AEC5EB")
    Label(text = "Enter username:", bg = "#AEC5EB", font = "Arial", fg = "#3A405A", pady =20).pack()

#Creating the entry
    username = Entry(username_window, width = 30, borderwidth = 2, bg = "#F9DEC9")
    username.pack()


    ok_button = Button(username_window, text = "Let's play!", bg ="#E9AFA3", padx = 10, pady = 10, command = validate_user_input)
    ok_button.pack()

    exit_button = Button(username_window, text = "Exit", bg ="#E9AFA3", padx = 10, pady = 10, command = username_window.destroy)
    exit_button.pack()



    username_window.mainloop()




enter_username_page()
