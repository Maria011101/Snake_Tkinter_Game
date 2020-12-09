from tkinter import *
import tkinter.messagebox as box
import random
import json
import webbrowser as web
import os

# global variables for customization
global backgroundColour
global snakeHead
global snakeColour
global up
global down
global right
global left
# other globals
global name
global bestScore
global leaderboard

name = None
snakeHead = "#157F1F"
snakeColour = "#4CB963"
backgroundColour = "#48233C"
up = '<Up>'
down = '<Down>'
right = '<Right>'
left = '<Left>'

# Loads a saved game
def load_game():
    global name
    # The game creates a text file with a save with each username
    # So each user can have their on saved game
    try:
        with open(name + ".txt") as saved:
                saved_game = json.load(saved)
                saved.close()
                play_game(
                    saved_game["score"],
                    saved_game['snake'],
                    saved_game['positions'],
                    saved_game["food1"],
                    saved_game["food2"],
                    saved_game["direction"])
    except FileNotFoundError:
        # In case there is no load present for the user, this error message appears
        box.showwarning("ERROR", "No game saved! Please start a new game!")

# This function creates a new text file for each user that wants to create a save
def save_game(save_data):
    global name
    try:
        with open(name + ".txt", 'w') as saved:
                json.dump(save_data, saved)
    except FileNotFoundError:
        saved = open(name + ".txt", 'x')
        json.dump(save_data, saved)
    saved.close()

# This function runs the game
def play_game(saved_score=None, saved_snake=None,
 saved_positions=None, saved_food1=None, saved_food2=None, saved_direction=None):
    global leaderboard
    global name
    global direction
    global food1
    global food1X
    global food1Y
    global food2
    global food2X
    global food2Y
    global pause
    global pause1
    global resume
    global snakeColour
    global created
    global obstacle1
    global obstacle2
    global upOb
    global downOb
    global positions
    global frame
    # Initialising some of the global variables
    upOb = 1
    downOb = 2
    created = False
    pause = False
    pause1 = False
    resume = False
    obstacle1 = None
    obstacle2 = None
    frame = 90
    food1X = None
    food1Y = None
    food2X = None
    food2Y = None

    menu_window.destroy()

    def setWindowDimensions():
        window = Tk()  # create window
        window.title("PITON Game")  # title of window
        window.geometry("1100x1920")
        window.configure(bg="black")
        return window


    # places food randomly on the canvas
    def placeFood():
        global food1
        global food1X
        global food1Y
        global food2
        global food2X
        global food2Y

        # Creates the food rectangle and if the game is not
        # a loaded save then it randomly generates the first position,
        # otherwise it loads the previous position
        food1 = canvas.create_rectangle(
        	0, 0, snakeSize, snakeSize, fill="#FEFFA5")
        if saved_food1 == None:
            food1X = random.randint(0, width-snakeSize)
            food1Y = random.randint(0, height-snakeSize)
        else:
            food1X = saved_food1[0]
            food1Y = saved_food1[1]

        canvas.move(food1, food1X, food1Y)

        # Creates the food rectangle and if the game is not
        # a loaded save then it randomly generates the first position,
        # otherwise it loads the previous position
        food2 = canvas.create_rectangle(
            0, 0, snakeSize, snakeSize, fill="#931F1D")
        if saved_food2 == None:
            food2X = random.randint(0, width-snakeSize)
            food2Y = random.randint(0, height-snakeSize)
        else:
            food2X = saved_food2[0]
            food2Y = saved_food2[1]

        canvas.move(food2, food2X, food2Y)

    # direction of the snake functions
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
        global created
        global frame
        global positions
        pause1 = False
        canvas.pack()

        if saved_positions != None:
            positions = saved_positions
        else:
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
            frame -= 1
            moveFood()
            growSnake()

        foodPos2 = canvas.coords(food2)
        if overlapping(sHeadPos, foodPos2):
            frame -= 1
            grow_2blocks = True
            moveFood()
            growSnake(grow_2blocks)

        # Checking to see if the snake collided with itself
        for i in range(1, len(snake)):
            if overlapping(sHeadPos, canvas.coords(snake[i])):
                gameOver = True
                print("overlapped with itself " + str(i))
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

        game = obstacles(score, snake)

        # Resets the pausing and resuming booleans
        # so it will be able to continue
        if resume:
            resume = False
            pause = False
            pause1 = False

        # Looping through the function if gameOver is False
        if 'gameOver' not in locals() and not game:
            if pause:
                pass
            else:
                window.after(frame, moveSnake)
        else:
            endScreen()


    # moves the food
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


    # adds a new block at the end of the snake
    # if grow_2blocks is false and two blocks
    # if grow_2blocks is true
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

        # Updating the score
        global score
        score += 10
        txt = "Score:" + str(score)
        canvas.itemconfigure(scoreText, text=txt)


    # checks to see if a and be are overlapping
    def overlapping(a, b):
        if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
            return True
        else:
            return False


    # creates the endscreen
    def endScreen():
        global name
        global leaderboard
        # this creates a rectangle on top of the game that will be the end screen
        end_screen = canvas.create_rectangle(0, 0, 900, 850, fill="#ABC798")
        saveButton.destroy()
        # the game over text
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

        # The game deletes the previous save if there is one
        # at the end of the game
        if os.path.exists(name + ".txt"):
            os.remove(name + ".txt")


        # opening the leaderboard file or
        # create a new one 
        try:
            with open('leaderboard.txt') as leaders:
                try:
                    leaderboard = json.load(leaders)
                    leaders.close()
                except:
                    leaderboard = {}
        except FileNotFoundError:
            leaders = open("leaderboard.txt", 'x')
            leaderboard = {}
            leaders.close()

        # updating the leaderboard file
        try:
            if score > leaderboard[name]:
                    leaderboard[name] = score
        except KeyError:
            leaderboard[name] = score

        with open('leaderboard.txt', 'w') as leaders:
            leaderboard = dict(sorted(
            leaderboard.items(),
            key=lambda x: x[1],
            reverse=True))
            json.dump(leaderboard, leaders)
            leaders.close()


    # creates obstacles the first time is called
    # and moves them every other time
    def obstacles(score, snake):
        global created
        global upOb
        global downOb
        global obstacle1
        global obstacle2
        aux = None

        if score >= 50:
                if not created:
                    # created is a variable that becomes true once
                    # the first obstacles have been created 
                    created = True
                    x1rand = random.randint(0,800)
                    x2rand = random.randint(0,800)
                    obstacle1 = canvas.create_rectangle(
                        x1rand,
                        0,
                        x1rand + 20,
                        100,
                        fill = "white")
                    obstacle2 = canvas.create_rectangle(
                        x2rand,
                        800,
                        x2rand + 20,
                        900,
                        fill = "white")
                else:
                    # coordinates of the obstacles
                    x1 = canvas.coords(obstacle1)[2]
                    y1 = canvas.coords(obstacle1)[3]
                    y2 = canvas.coords(obstacle2)[3]
                    x2 = canvas.coords(obstacle2)[2]

                    # If the obstacles reach the edge then they change direction
                    if y1 == 1000 or y2 == 0 or y1 == 0 or y2 == 1000:
                        aux = upOb
                        upOb = downOb
                        downOb = aux

                    # UpOb and downOb determine which obstacle goes which way
                    # For example if upOb is 1 then obstacle 1 is going up
                    if upOb == 1 and downOb == 2:
                        canvas.move(obstacle1, 0, 10)
                        y1 += 10
                        canvas.move(obstacle2, 0, -10)
                        y2 -= 10
                    elif upOb == 2 and downOb == 1:
                        canvas.move(obstacle2, 0, 10)
                        y2 += 10
                        canvas.move(obstacle1, 0, -10)
                        y1 -= 10

                    #checking to see if the obstacles overlap with the snake
                    #returning true if the condition is met
                    for i in range(1,len(snake)):
                        if overlapping(canvas.coords(snake[i]), canvas.coords(obstacle1)):
                            return True
                        if overlapping(canvas.coords(snake[i]), canvas.coords(obstacle2)):
                            return True
                    if overlapping(canvas.coords(snake[0]), canvas.coords(obstacle1)):
                        return True
                    if overlapping(canvas.coords(snake[0]), canvas.coords(obstacle2)):
                        return True
        return False


    # cheat code 1
    def CheatCode1(event):
        global score
        score += 20
        txt = "Score:" + str(score)
        canvas.itemconfigure(scoreText, text=txt)

    # cheat code 2
    def CheatCode2(event):
        global snake
        if len(snake) >= 2:
            canvas.delete(snake[len(snake)-1])
            snake.remove(snake[len(snake)-1])
        else:
            pass



    # bossKey activation
    def bossKey(event):
        pause_game(event)
        web.open("https://finance.yahoo.com/topic/stock-market-news/")

    # Back to menu function for when the game is finished
    # (associated with the back to menu button)
    def backToMenu():
        window.destroy()
        menu_page()

    # Resume game after pause
    def resume_game(event):
        global pauseText1
        global resume
        global pauseText2
        if pause:
            resume = True
            canvas.delete(pauseText1)
            canvas.delete(pauseText2)
            moveSnake()

    # Pauses the game
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
                fill="#06BEE1",
                font="Times 50")

            pauseText2 = canvas.create_text(
                (450, 400),
                text="Press <r> to resume game",
                fill="#06BEE1",
                font="Arial 20")

    # when the save button is pressed this function creates
    # a dictionary with data needed to be uploaded to the file
    def save_dict():
        global score
        global snake
        global positions
        global food1
        global food2
        global direction

        game = {}
        game["score"] = score
        game["snake"] = snake
        game["direction"] = direction
        game["positions"] = positions
        game["food1"] = canvas.coords(food1)
        game["food2"] = canvas.coords(food2)
        save_game(game)
        backToMenu()

    width = 850  # width of snake’s world
    height = 850  # height of snake’s world

    # creating the window
    window = setWindowDimensions()
    global backgroundColour
    canvas = Canvas(window, bg=backgroundColour, width=width, height=height)

    # the Save and exit button
    saveButton = Button(
        window,
        text="Save and Exit",
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=10,
        font=("Arial, 15"),
        command=save_dict)
    saveButton.place(x=10, y=10)

    # creating the snake
    global snake
    snakeSize = 20
    snake = []

    # Creating the snake head
    snake.append(
        canvas.create_rectangle(
            snakeSize,
            snakeSize,
            snakeSize * 2,
            snakeSize * 2,
            fill=snakeHead))
    # If a saved game is loaded, the game moves the snake to its previous position
    if saved_positions != None:
        canvas.move(snake[0], saved_positions[0][0], saved_positions[0][1])

    # If there is a saved game loaded then we create the snake
    # so it has the same length
    if saved_snake != None:
        for i in range(1, len(saved_snake)):
            snake.append(
                canvas.create_rectangle(
                    0,
                    0,
                    snakeSize,
                    snakeSize,
                    fill=snakeColour))
            canvas.move(snake[i], saved_positions[i][0], saved_positions[i][1])

    if saved_score != None:
        score = saved_score
    else:
        score = 0  # the score starts at 0 if there
        # was no previous save

    txt = "Score:" + str(score)
    # Creating a text widget to show the score
    scoreText = canvas.create_text(
        width/2,
        20,
        fill="white",
        font="Times 20 italic bold",
        text=txt)

    if up == 'w':
        # binding capital keys as well
        canvas.bind('A', leftKey)
        canvas.bind('D', rightKey)
        canvas.bind('W', upKey)
        canvas.bind('S', downKey)

    canvas.bind(left, leftKey)
    canvas.bind(right, rightKey)
    canvas.bind(up, upKey)
    canvas.bind(down, downKey)
    canvas.bind("c", CheatCode1)
    canvas.bind("m", CheatCode2)
    canvas.bind("p", pause_game)
    canvas.bind("r", resume_game)
    canvas.bind("b", bossKey)
    # binding capital keys as well
    canvas.bind("C", CheatCode1)
    canvas.bind("M", CheatCode2)
    canvas.bind("P", pause_game)
    canvas.bind("R", resume_game)
    canvas.bind("B", bossKey)
    canvas.focus_set()
    if saved_direction != None:
        direction = saved_direction
    else:
        direction = "right"

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


# Leaderboard page
def leaderboard_page():
    global leaderboard_window
    global menu_window
    menu_window.destroy()
    leaderboard_window = Tk()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("1080x1920")
    leaderboard_window.configure(bg="#ABC798")

    try:
        with open('leaderboard.txt') as leaders:
            try:
                leaderboard = json.load(leaders)
            except:
                leaderboard = {}
    except FileNotFoundError:
        leaders = open("leaderboard.txt", 'x')
        leaderboard = {}

    if name not in leaderboard:
        leaderboard[name] = 0

    leaderboard_canvas = Canvas(leaderboard_window, bg="#ABC798", width=900, height=900)
    place = 1
    y = 200

    for x in leaderboard:
        player = str(place) + ". " + str(x) + " :  " + str(leaderboard[x])
        leaderboard_canvas.create_text(
            200, y, fill="#1A1F16", font="Times 20", text=str(player)
        )
        y += 50
        place += 1
    leaderboard_canvas.pack()

    pythonImage = PhotoImage(file="snake4.png")
    snake = Label(leaderboard_window, image=pythonImage, bg="#ABC798")
    snake.place(x=500, y=300)

    backButton = Button(
        leaderboard_window,
        text="Back",
        bg="#5D737E",
        activebackground="#D68C45",
        height=1,
        width=5,
        font=("Times, 15"),
        command=backfleaderboard)
    backButton.place(x=50, y=10)

    Label(
        leaderboard_window,
        text="If you are a new player, "
        "you will appear with a score of 0 but"
        " you will only be saved\n to the leaderboard after your first game.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 15")).place(x=100, y=700)

    Label(
        leaderboard_window,
        text="Leaderboard",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Times, 50")).place(x=300, y=50)

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

    Label(
        rule_window,
        text="Default Controls:",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 25")).place(x=100, y=150)

    Label(
        rule_window,
        text="'<Up>'-up, '<Right>'-right, '<Down>'-down, '<Left>'-left",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=200)

    yellowfoodButton = Button(
        rule_window,
        bg="#FEFFA5",
        activebackground="#FEFFA5",
        height=1,
        width=1)
    yellowfoodButton.place(x=100, y=250)

    Label(
        rule_window,
        text="-This food adds one block at the tail of the snake,"
        " \nwhile adding 10 points to the score.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=150, y=250)

    redfoodButton = Button(
        rule_window,
        bg="#931F1D",
        activebackground="#931F1D",
        height=1,
        width=1)
    redfoodButton.place(x=100, y=350)

    Label(
        rule_window,
        text="-This food adds two blocks at the tail of the snake,"
        " \nwhile adding 10 points to the score.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=150, y=350)

    obstacleButton = Button(
        rule_window,
        bg="white",
        activebackground="white",
        height=6,
        width=1)
    obstacleButton.place(x=100, y=450)

    Label(
        rule_window,
        text="- These obstacles appear after you reach the score of 50."
        " If the\n snake touches them either with the head or the tail it dies\n and"
        " the game ends.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=150, y=450)

    Label(
        rule_window,
        text="< Cheat Code > - Press 'c' to add 20 points to your score.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=600)

    Label(
        rule_window,
        text="< Cheat Code > - Press 'm' to delete a block off the tail of the snake.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=650)

    Label(
        rule_window,
        text="- Press 'p' to pause the game.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=700)

    Label(
        rule_window,
        text="- Press 'r' to resume the game.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=750)
    Label(
        rule_window,
        text="- Press 'b' to activate the boss key.",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Arial, 20")).place(x=100, y=800)

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
def changeToOrange():
    global backgroundColour
    backgroundColour = "#FCD29F"
    box.showinfo("Done!", "Selected Orange!")


# function to change background colour to blue
def changeToBlue():
    global backgroundColour
    backgroundColour = "#05204A"
    box.showinfo("Done!", "Selected blue!")


# function to change background colour to beige
def changeToLightBlue():
    global backgroundColour
    backgroundColour = "#028090"
    box.showinfo("Done!", "Selected Metallic Seaweed!")


# function to change background colour to pink
def changeToPurple():
    global backgroundColour
    backgroundColour = "#48233C"
    box.showinfo("Done!", "Selected purple!")


# function to change snake colour to green
def snakeGreen():
    global snakeHead
    global snakeColour
    snakeHead = "#157F1F"
    snakeColour = "#4CB963"
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
        bg="#FCD29F",
        height=5,
        width=10,
        command=changeToOrange)
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
        bg="#028090",
        height=5,
        width=10,
        command=changeToLightBlue)
    colourButton3.place(x=500, y=250)

    colourButton4 = Button(
        settings_window,
        bg="#48233C",
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
    global username

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
    menuTitle.place(x=400, y=50)

    menuTitleSmall = Label(
        menu_window,
        text=" M E N U",
        bg="#ABC798",
        fg="#1A1F16",
        font=("Helvetica, 35"))
    menuTitleSmall.place(x=200, y=140)
    
    # Menu Buttons

    playButton = Button(
        menu_window,
        text="New Game",
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=15,
        font=("Arial, 15"),
        command=play_game)
    playButton.place(x=200, y=200)

    loadButton = Button(
        menu_window,
        text="Load A Saved Game",
        bg="#5D737E",
        activebackground="#D68C45",
        height=2,
        width=15,
        font=("Arial, 15"),
        command=load_game)
    loadButton.place(x=200, y=300)

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
        command=menu_window.destroy)
    exitButton.place(x=200, y=700)

    # Menu picture of snake
    snakeImage = PhotoImage(file="converted.gif")
    snake = Label(menu_window, image=snakeImage, bg="#ABC798")
    snake.place(x=450, y=400)

    menu_window.mainloop()


# This displays a warning if the username is empty
def validate_user_input():
    global username
    global name
    ok = False
    name = username.get()
    if name != "":
        for character in name:
            if character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ1234567890":
                box.showwarning(
                    "Warning",
                    "Usernames can only contain letters and numbers.")
                ok = True
                break
        if not ok:
            menu_page()
    else:
        box.showwarning(
                    "Warning",
                    "Usernames cannot be null")


# A page where we get the username
def enter_username_page():
    global username_window
    global username

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
    user_var = StringVar()
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
