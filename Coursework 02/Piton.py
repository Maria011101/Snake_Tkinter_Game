from tkinter import *
import tkinter.messagebox as box
import random


# This function runs the game
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
    global Obstacles
    global pause
    global pause1
    global resume
    pause = False
    pause1 = False
    resume = False

    menu_window.destroy()

    def setWindowDimensions(w, h):
        window = Tk()  # create window
        window.title("Snake Game")  # title of window
        window.geometry("1080x1920")
        return window

    def placeFood():
        global food1
        global food1X
        global food1Y
        global food2
        global food2X
        global food2Y

        food1 = canvas.create_rectangle(
        	0, 0, snakeSize, snakeSize, fill="#FEFFA5")
        food1X = random.randint(0, width-snakeSize)
        food1Y = random.randint(0, height-snakeSize)
        canvas.move(food1, food1X, food1Y)

        food2 = canvas.create_rectangle(
            0, 0, snakeSize, snakeSize, fill="#931F1D")
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

    # Moving the snake
    def moveSnake():
        global portals_placed
        global portals
        global pause
        global pause1
        global resume

        pause1 = False
        canvas.pack()
        positions = []
        positions.append(canvas.coords(snake[0]))
        # Adding the snake's head coords to the list

        # Checking to see if the snake reached the edge and teleporting it
        # to the other side of the canvas
        if positions[0][0] < 0:
            canvas.coords(
                snake[0],
                width,
                positions[0][1],
                width-snakeSize,
                positions[0][3])
        elif positions[0][2] > width:
            canvas.coords(
                snake[0],
                0-snakeSize,
                positions[0][1],
                0,
                positions[0][3])
        elif positions[0][3] > height:
            canvas.coords(
                snake[0],
                positions[0][0],
                0 - snakeSize,
                positions[0][2],
                0)
        elif positions[0][1] < 0:
            canvas.coords(
                snake[0],
                positions[0][0],
                height,
                positions[0][2],
                height-snakeSize)

        # Updating the coordonates of the snake's head
        positions.clear()
        positions.append(canvas.coords(snake[0]))

        # Moving the snake
        if direction == "left":
            canvas.move(snake[0], -snakeSize, 0)
        elif direction == "right":
            canvas.move(snake[0], snakeSize, 0)
        elif direction == "up":
            canvas.move(snake[0], 0, -snakeSize)
        elif direction == "down":
            canvas.move(snake[0], 0, snakeSize)

        sHeadPos = canvas.coords(snake[0])
        # Checking to see if the snake collided with food
        foodPos1 = canvas.coords(food1)
        if overlapping(sHeadPos, foodPos1):
            moveFood()
            growSnake()

        foodPos2 = canvas.coords(food2)
        if overlapping(sHeadPos, foodPos2):
            grow_2blocks = True
            moveFood()
            growSnake(grow_2blocks)

        # Checking to see if the snake collided with itself
        for i in range(1, len(snake)):
            if overlapping(sHeadPos, canvas.coords(snake[i])):
                gameOver = True
                canvas.create_text(
                    width/2,
                    height/2,
                    fill="white",
                    font="Times 20 italic bold",
                    text="Game Over!")

        for i in range(1, len(snake)):
            positions.append(canvas.coords(snake[i]))
        for i in range(len(snake)-1):
            canvas.coords(
                snake[i+1],
                positions[i][0],
                positions[i][1],
                positions[i][2],
                positions[i][3])
        if resume:
            window.after(90, moveSnake)

        # Looping through the function if gameOver is False
        if 'gameOver' not in locals():
            if pause:
                pass
            else:
                window.after(90, moveSnake)
        else:
            endScreen()

    def moveFood():
        global food1, food1X, food1Y, food2, food2X, food2Y

        # randomly moving the food on the canvas
        canvas.move(food1, (food1X*(-1)), (food1Y*(-1)))
        food1X = random.randint(0, width-snakeSize)
        food1Y = random.randint(0, height-snakeSize)
        canvas.move(food1, food1X, food1Y)

        canvas.move(food2, (food2X*(-1)), (food2Y*(-1)))
        food2X = random.randint(0, width-snakeSize)
        food2Y = random.randint(0, height-snakeSize)
        canvas.move(food2, food2X, food2Y)

    def growSnake(grow_2blocks=False):

        # we add a block at the end of the snake, depending on the direction
        lastElement = len(snake)-1
        lastElementPos = canvas.coords(snake[lastElement])
        snake.append(
            canvas.create_rectangle(
                0,
                0,
                snakeSize,
                snakeSize,
                fill="#ABC798"))

        # adding  a block to the right of the last one if the direction is left
        if (direction == "left"):
            canvas.coords(
                snake[lastElement+1],
                lastElementPos[0] + snakeSize,
                lastElementPos[1],
                lastElementPos[2] + snakeSize,
                lastElementPos[3])

        # adding  a block to the left of the last one if the direction is right
        elif (direction == "right"):
            canvas.coords(
                snake[lastElement+1],
                lastElementPos[0] - snakeSize,
                lastElementPos[1],
                lastElementPos[2] - snakeSize,
                lastElementPos[3])

        # adding  a block under the last one if the direction is up
        elif (direction == "up"):
            canvas.coords(
                snake[lastElement+1],
                lastElementPos[0],
                lastElementPos[1] + snakeSize,
                lastElementPos[2],
                lastElementPos[3]+snakeSize)
        # adding  a block above the last one if the direction is down
        else:
            canvas.coords(
                snake[lastElement+1],
                lastElementPos[0],
                lastElementPos[1]-snakeSize,
                lastElementPos[2],
                lastElementPos[3]-snakeSize)
        # We add the second block only if grow_2blocks is True
        # (the snake has eaten the red food)
            lastElement = len(snake)-1
            lastElementPos = canvas.coords(snake[lastElement])
            snake.append(
                canvas.create_rectangle(
                    0,
                    0,
                    snakeSize,
                    snakeSize,
                    fill="#ABC798"))

            if (direction == "left"):
                canvas.coords(
                    snake[lastElement+1],
                    lastElementPos[0]+snakeSize,
                    lastElementPos[1],
                    lastElementPos[2]+snakeSize,
                    lastElementPos[3])

            elif (direction == "right"):
                canvas.coords(
                    snake[lastElement+1],
                    lastElementPos[0] + snakeSize,
                    lastElementPos[1],
                    lastElementPos[2] - snakeSize,
                    lastElementPos[3])

            elif (direction == "up"):
                canvas.coords(
                    snake[lastElement+1],
                    lastElementPos[0],
                    lastElementPos[1]+snakeSize,
                    lastElementPos[2],
                    lastElementPos[3]+snakeSize)

            else:
                canvas.coords(
                    snake[lastElement+1],
                    lastElementPos[0],
                    lastElementPos[1]-snakeSize,
                    lastElementPos[2],
                    lastElementPos[3]-snakeSize)

        global score
        score += 10
        txt = "Score:" + str(score)
        canvas.itemconfigure(scoreText, text=txt)

    def overlapping(a, b):
        if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
            return True
        else:
            return False

    # def createObstacle(x, y):
    # 	global Ob
    # 	Ob = canvas.create_rectangle(x, y, x + 20, y + 100, fill = "white")

    # 	def moveObstacle():
    # 		global Ob
    # 		for i in range(1000):
    # 			canvas.move(Ob, 10, 10)

    # 	canvas.after(1000, moveObstacle)

    def endScreen():
        global end_screen
        global end_score

        end_screen = canvas.create_rectangle(0, 0, 1000, 850, fill="#ABC798")

        game_over = Label(
            window,
            text="GAME OVER!",
            font=("Times 50 italic bold"),
            bg="#ABC798",
            fg="#1A1F16")
        game_over.place(x=200, y=200)

        end_score = Label(
            window,
            text="Your Score: " + str(score),
            font=("Times 30 italic bold"),
            bg="#ABC798",
            fg="#1A1F16")
        end_score.place(x=200, y=300)

        back_to_menu_button = Button(
            text="Back to Menu",
            bg="#5D737E",
            activebackground="#D68C45",
            height=2,
            width=15,
            font=("Arial, 15"),
            command=backToMenu)
        back_to_menu_button.place(x=200, y=400)

    def CheatCode1(event):
        global score
        score += 20
        txt = "Score:" + str(score)
        canvas.itemconfigure(scoreText, text=txt)

    def backToMenu():
        window.destroy()
        menu_page()

    def resume_game(event):
        global pauseText1
        global resume
        global pauseText2

        resume = True
        pause = False
        pause1 = False
        canvas.delete(pauseText1)
        canvas.delete(pauseText2)
        canvas.bind("<Left>", leftKey)
        canvas.bind("<Right>", rightKey)
        canvas.bind("<Up>", upKey)
        canvas.bind("<Down>", downKey)
        canvas.bind("c", CheatCode1)
        canvas.bind("p", pause_game)
        canvas.bind("r", resume_game)
        canvas.focus_set()
        window.after(90, moveSnake)

    def pause_game(event):
        global pause
        global canvas
        global pause1
        global pauseText1
        global pauseText2

        pause = True

        if not pause1:
            pause1 = True
            pauseText1 = canvas.create_text(
                (450, 350),
                text="Game Paused",
                fill="red",
                font="Arial 50")

            pauseText2 = canvas.create_text(
                (450, 400),
                text="Press <r> to resume game",
                fill="red",
                font="Arial 20")

    width = 1000  # width of snake’s world
    height = 850  # height of snake’s world

    # creating the window
    window = setWindowDimensions(width, height)
    canvas = Canvas(window, bg="#1A1F16", width=width, height=height)

    # creating the snake
    snake = []
    snakeSize = 20
    snake.append(
        canvas.create_rectangle(
            snakeSize,
            snakeSize,
            snakeSize * 2,
            snakeSize * 2,
            fill="#60992D"))

    score = 0  # the score starts at 0
    txt = "Score:" + str(score)
    # Creating a text widget to show the score
    scoreText = canvas.create_text(
        width/2,
        20,
        fill="white",
        font="Times 20 italic bold",
        text=txt)

    canvas.bind("<Left>", leftKey)
    canvas.bind("<Right>", rightKey)
    canvas.bind("<Up>", upKey)
    canvas.bind("<Down>", downKey)
    canvas.bind("c", CheatCode1)
    canvas.bind("p", pause_game)
    canvas.bind("r", resume_game)
    canvas.focus_set()
    direction = "right"

    # createObstacle(100,10)

    placeFood()
    moveSnake()
    window.mainloop()


# gets you back to the menu from the rules page
def backfrules():
    global rule_window
    rule_window.destroy()
    menu_page()


# This displays the menu page
def menu_page():
    global menu_window
    global username_window

    # destroying the enter username window
    try:
        username_window.destroy()
    except:
        pass

    menu_window = Tk()
    menu_window.title("P I T O N")
    menu_window.geometry("1080x1920")
    menu_window.configure(bg="#ABC798")

    # Title
    menuTitle = Label(
        menu_window,
        text="MENU",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 50"))
    menuTitle.place(x=450, y=100)

    # Menu Buttons

    playButton = Button(
        menu_window,
        text="Start",
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=15,
        font=("Arial, 15"),
        command=play_game)
    playButton.place(x=200, y=300)

    rulesButton = Button(
        menu_window,
        text="Rules",
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=15,
        font=("Arial, 15"),
        command=rules_page)
    rulesButton.place(x=200, y=400)

    leaderboardButton = Button(
        menu_window,
        text="Leaderboard",
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=15,
        font=("Arial, 15"))
    leaderboardButton.place(x=200, y=500)

    settingsButton = Button(
        menu_window,
        text="Settings",
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=15,
        font=("Arial, 15"))
    settingsButton.place(x=200, y=600)

    exitButton = Button(
        menu_window,
        text="Exit",
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=15,
        font=("Arial, 15"),
        command=menu_window.destroy)
    exitButton.place(x=200, y=700)

    # Menu picture of snake
    pythonImage = PhotoImage(file="snake.png")
    python = Label(image=pythonImage, bg="#ABC798")
    python.place(x=500, y=400)

enter_username_page()
