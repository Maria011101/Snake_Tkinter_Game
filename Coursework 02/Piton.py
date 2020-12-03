from tkinter import *
import tkinter.messagebox as box
import random
import sys

# global variables for customization
global backgroundColour
global snakeHead
global snakeColour
global up
global down
global right
global left
global menu_window
global leaderboard_window
snakeHead = "#60992D"
snakeColour = "#ABC798"
backgroundColour = "#1A1F16"
up = '<Up>'
down = '<Down>'
right = '<Right>'
left = '<Left>'


# This function runs the game
def play_game():
    global score
    global window
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
    global pause
    global pause1
    global resume
    global snakeColour
    pause = False
    pause1 = False
    resume = False
    obstacle = []

    menu_window.destroy()

    def setWindowDimensions(w, h):
        window = Tk()  # create window
        window.title("PITON Game")  # title of window
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
        global pause
        global pause1
        global resume
        pause1 = False
        obstacle = None
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

        # Making each part of the body follow the previous one
        for i in range(1, len(snake)):
            positions.append(canvas.coords(snake[i]))
        for i in range(len(snake)-1):
            canvas.coords(
                snake[i+1],
                positions[i][0],
                positions[i][1],
                positions[i][2],
                positions[i][3])

        # Resets the pausing and resuming booleans
        # so it will be able to continue
        if resume:
            resume = False
            pause = False
            pause1 = False

        # if score > 30:
        #     if len(obstacle) == 0:
        #         xrand = random.randint(0, 1900)
        #         obstacle.append(
        #             canvas.create_rectangle(
        #                 xrand,
        #                 0,
        #                 xrand + 20,
        #                 100,
        #                 fill = "white"))
        #     else:
        #         canvas.move(obstacle[0], 0, 10)

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
                fill=snakeColour))

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
                    fill=snakeColour))

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

    def endScreen():
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
        if pause:
            resume = True
            canvas.delete(pauseText1)
            canvas.delete(pauseText2)
            moveSnake()

    def pause_game(event):
        global pause
        global pause1
        global pauseText1
        global pauseText2

        if not pause:
            pause = True
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
    global backgroundColour
    canvas = Canvas(window, bg=backgroundColour, width=width, height=height)

    # creating the snake
    snake = []
    snakeSize = 20
    snake.append(
        canvas.create_rectangle(
            snakeSize,
            snakeSize,
            snakeSize * 2,
            snakeSize * 2,
            fill=snakeHead))

    score = 0  # the score starts at 0
    txt = "Score:" + str(score)
    # Creating a text widget to show the score
    scoreText = canvas.create_text(
        width/2,
        20,
        fill="white",
        font="Times 20 italic bold",
        text=txt)

    canvas.bind(left, leftKey)
    canvas.bind(right, rightKey)
    canvas.bind(up, upKey)
    canvas.bind(down, downKey)
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


# gets you back from settings to the menu page
def backfsettings():
    global settings_window
    settings_window.destroy()
    menu_page()


# gets you back from leaderboard to the menu page
def backfleaderboard():
    global leaderboard_window
    leaderboard_window.destroy()
    menu_page()

def leaderboard_manage():
    global username
    leaderboard = {}
    leaders = open("leaderboard.txt", 'a')
    if username.get() in leaders:
        if bestScore < end_score:
            bestScore = endscore
    else:
        pass



def leaderboard_page():
    global leaderboard_window
    global menu_window
    menu_window.destroy()
    leaderboard_window = Tk()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("1080x1920")
    leaderboard_window.configure(bg="#ABC798")

    backButton = Button(
        leaderboard_window,
        text="Back",
        bg="#5D737E",
        activebackground="#D68C45",
        height=1,
        width=5,
        font=("Arial, 15"),
        command=backfleaderboard)
    backButton.place(x=50, y=10)

    # scroll = Scrollbar(leaderboard_window, bg="#D68C45", orient=VERTICAL)
    # scroll.pack()

    Label(
        rule_window,
        text="Leaderboard",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 50")).place(x=300, y=50)

    leaderboard_window.mainloop()


# displays the rules and information page
def rules_page():
    global rule_window
    global menu_window

    menu_window.destroy()

    rule_window = Tk()
    rule_window.title("Rules")
    rule_window.geometry("1080x1920")
    rule_window.configure(bg="#ABC798")

    Label(
        rule_window,
        text="Game Rules",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 50")).place(x=300, y=50)

    yellowfoodButton = Button(
        rule_window,
        bg="#FEFFA5",
        activebackground="#FEFFA5",
        height=1,
        width=1)
    yellowfoodButton.place(x=100, y=200)

    Label(
        rule_window,
        text="-This food adds one block at the tail of the snake,"
        " \nwhile adding 10 points to the score.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=150, y=200)

    redfoodButton = Button(
        rule_window,
        bg="#931F1D",
        activebackground="#931F1D",
        height=1,
        width=1)
    redfoodButton.place(x=100, y=300)

    Label(
        rule_window,
        text="-This food adds two blocks at the tail of the snake,"
        " \nwhile adding 10 points to the score.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=150, y=300)

    Label(
        rule_window,
        text="< Cheat Code > - Press 'c' to add 20 points to your score.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=400)

    Label(
        rule_window,
        text="- Press 'p' to add pause the game.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=450)

    Label(
        rule_window,
        text="- Press 'r' to resume the game.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=500)

    backButton = Button(
        rule_window,
        text="Back",
        bg="#5D737E",
        activebackground="#D68C45",
        height=1,
        width=5,
        font=("Arial, 15"),
        command=backfrules)
    backButton.place(x=50, y=10)

    rule_window.mainloop()


# function to change background colour to green
def changeToGreen():
    global backgroundColour
    backgroundColour = "#1A1F16"
    box.showinfo("Done!", "Selected dark green!")


# function to change background colour to blue
def changeToBlue():
    global backgroundColour
    backgroundColour = "#05204A"
    box.showinfo("Done!", "Selected blue!")


# function to change background colour to beige
def changeToBeige():
    global backgroundColour
    backgroundColour = "#EFF0D1"
    box.showinfo("Done!", "Selected beige!")


# function to change background colour to pink
def changeToPurple():
    global backgroundColour
    backgroundColour = "#511730"
    box.showinfo("Done!", "Selected purple!")


# function to change snake colour to green
def snakeGreen():
    global snakeHead
    global snakeColour
    snakeHead = "#60992D"
    snakeColour = "#ABC798"
    box.showinfo("Done!", "Selected green!")


# function to change snake colour to pink
def snakePink():
    global snakeHead
    global snakeColour
    snakeHead = "#8E3B46"
    snakeColour = "#FE938C"
    box.showinfo("Done!", "Selected pink!")


# function to change the controls to the letters
def letterControl():
    global up
    global down
    global right
    global left

    box.showinfo("Done!", "Selected the letters as controls!")
    up = 'w'
    down = 's'
    right = 'd'
    left = 'a'


# function to change the controls to the arrows
def arrowsControl():
    global up
    global down
    global right
    global left

    box.showinfo("Done!", "Selected the arrows as controls!")
    up = "<Up>"
    down = "<Down>"
    right = "<Right>"
    left = "<Left>"


# Settings and customization page
def settings_page():
    global settings_window
    global menu_window
    global backgroundColour
    menu_window.destroy()

    settings_window = Tk()
    settings_window.title("Settings")
    settings_window.geometry("1080x1920")
    settings_window.configure(bg="#ABC798")

    backButton = Button(
        settings_window,
        text="Back",
        bg="#5D737E",
        activebackground="#D68C45",
        height=1,
        width=5,
        font=("Arial, 15"),
        command=backfsettings)
    backButton.place(x=50, y=10)

    Label(
        settings_window,
        text="Settings",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 50")).place(x=350, y=50)

    Label(
        settings_window,
        text="Background colour:",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=200)

    colourButton1 = Button(
        settings_window,
        bg="#1A1F16",
        height=5,
        width=10,
        command=changeToGreen)
    colourButton1.place(x=100, y=250)

    colourButton2 = Button(
        settings_window,
        bg="#05204A",
        height=5,
        width=10,
        command=changeToBlue)
    colourButton2.place(x=300, y=250)

    colourButton3 = Button(
        settings_window,
        bg="#EFF0D1",
        height=5,
        width=10,
        command=changeToBeige)
    colourButton3.place(x=500, y=250)

    colourButton4 = Button(
        settings_window,
        bg="#511730",
        height=5,
        width=10,
        command=changeToPurple)
    colourButton4.place(x=700, y=250)

    Label(
        settings_window,
        text="Snake colour:",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=400)

    colourButton5 = Button(
        settings_window,
        bg="#60992D",
        height=5,
        width=10,
        command=snakeGreen)
    colourButton5.place(x=100, y=450)

    colourButton6 = Button(
        settings_window,
        bg="#8E3B46",
        height=5,
        width=10,
        command=snakePink)
    colourButton6.place(x=300, y=450)

    Label(
        settings_window,
        text="Controls:",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=600)

    wasdcontrol = Button(
        settings_window,
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=2,
        command=letterControl)
    wasdcontrol.place(x=100, y=650)

    Label(
        settings_window,
        text="Press this button to change the controls into\n "
        "'w'-up, 'a'-right, 's'-down, 'd'-left",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 15")).place(x=200, y=650)

    arrowscontrol = Button(
        settings_window,
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=2,
        command=arrowsControl)
    arrowscontrol.place(x=100, y=750)

    Label(
        settings_window,
        text="Press this button to change the controls into\n "
        "'<Up>'-up, '<Right>'-right, '<Down>'-down, '<Left>'-left",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 15")).place(x=150, y=750)

    settings_window.mainloop()


# This displays the menu page
def menu_page():
    global username_window
    global menu_window

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
        text="P I T O N",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Helvetica, 50"))
    menuTitle.place(x=350, y=100)

    menuTitleSmall = Label(
        menu_window,
        text=" M E N U",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Helvetica, 35"))
    menuTitleSmall.place(x=200, y=240)
    
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
        font=("Arial, 15"),
        command=leaderboard_page)
    leaderboardButton.place(x=200, y=500)

    settingsButton = Button(
        menu_window,
        text="Settings",
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=15,
        font=("Arial, 15"),
        command=settings_page)
    settingsButton.place(x=200, y=600)

    exitButton = Button(
        menu_window,
        text="Exit",
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=15,
        font=("Arial, 15"),
        command=sys.exit)
    exitButton.place(x=200, y=700)

    # Menu picture of snake
    snakeImage = PhotoImage(file="converted.gif")
    snake = Label(menu_window, image=snakeImage, bg="#ABC798")
    snake.place(x=450, y=400)

    menu_window.mainloop()


# A page where we get the username
def enter_username_page():
    global username_window
    global username

    # This displays a warning if the username is empty
    def validate_user_input():
        for character in username.get():
            if character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ1234567890":
                box.showwarning(
                    "Warning",
                    "Usernames can only contain letters and numbers.")
                break
            else:
                menu_page()

    # Creating the page and configuring it
    username_window = Tk()
    username_window.title("Welcome to PITON!")
    username_window.geometry("350x250")
    username_window.configure(bg="#AEC5EB")
    Label(
        text="Enter username:",
        bg="#AEC5EB",
        font="Arial",
        fg="#3A405A",
        pady=20).pack()

    # Creating the entry
    username = Entry(username_window, width=30, borderwidth=2, bg="#F9DEC9")
    username.pack()

    ok_button = Button(
        username_window,
        text="Let's play!",
        bg="#E9AFA3",
        padx=10,
        pady=10,
        command=validate_user_input)
    ok_button.place(x=125, y=100)

    exit_button = Button(
        username_window,
        text="Exit",
        bg="#E9AFA3",
        padx=10,
        pady=10,
        command=username_window.destroy)
    exit_button.place(x=150, y=150)

    username_window.mainloop()


enter_username_page()
