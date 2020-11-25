#Graphics used from www.kenney.nl

from tkinter import Tk, PhotoImage, Label, Canvas
import random, time


#Configuring the window
def configure_window():
    window.geometry("1920x1080")
    window.title("SPACE INVADERS")

    
#   Meteor Class
class Meteor:

    def __init__(self):
        self.rand =random.randint(0,3)
        self.x = random.randint(0,1080)
        self.meteor_y = 50
        if(self.rand == 0):
            self.health = 3
            self.bigMeteorImage = None
            self.meteor = None
            self.meteor_y = 50
        else:
            self.health = 1
            self.smallMeteorImage = None
            self.meteor = None
            self.meteor_y = 50

    def place(self):
        if(self.rand == 0):
            self.bigMeteorImage = PhotoImage(file = "meteorBig.png")
            self.meteor = canvas1.create_image(self.x, 50, image = self.bigMeteorImage)
            self.meteor_move()
        else:
            self.smallMeteorImage = PhotoImage(file = "meteorSmall.png")
            self.meteor = canvas1.create_image(self.x, 50, image = self.smallMeteorImage)
            self.meteor_move()


    def meteor_move(self):
        if(self.meteor_y <1200):
            canvas1.move(self.meteor, 0, 5)
            self.meteor_y += 5
            canvas1.after(10, self.meteor_move)



def left(event):
    global player_x
    x=-10
    y=0
    player_x -= 10
    canvas1.move(player_image, x, y)

def right(event):
    global player_x
    x=10
    y=0
    player_x += 10
    canvas1.move(player_image, x, y)

def up(event):
    global player_y
    x=0
    y=-10
    player_y -= 10
    canvas1.move(player_image, x, y)

def down(event):
    global player_y
    x=0
    y=10
    player_y += 10
    canvas1.move(player_image, x, y)

def shoot():
#Global and local  variables
    global player_x
    global player_y
    global shot_in_action
    beam_speed = -5


    shot_in_action =  True
    shooting_beam = canvas1.create_image(player_x, player_y-50, image = beam)
    beam_y = player_y - 50

#Loop for moving the beam
    for i in range(2000):
        canvas1.move(shooting_beam, 0, beam_speed)
        time.sleep(0.001)
        #window.after(5)
        #time.sleep(0.02)
        beam_y -= 5
        canvas1.update()
        if(beam_y <= -20):
            shot_in_action = False
            shooting_beam.delete()
            break

def is_shot(event):
    global shot_in_action
#Checking to see if there is another beam currently being shot
    if(shot_in_action):
            pass
    else:
        canvas1.update()
        shoot()
def is_pressed():
    return True



window = Tk()

configure_window()

#Declaring global variables used in the functions
player_x = 250
player_y = 500
shot_in_action = False
meteor_in_action = False
#Creating a canvas for the backround of the game
canvas1 = Canvas(window, background = "#161756", height = 1920, width = 1080)
canvas1.pack(padx = 10, pady = 10)

#Adding the player's rocket to the screen
player = PhotoImage(file = "player.png")
player_image = canvas1.create_image(player_x, player_y, image = player)

#Loading the beam image
beam = PhotoImage(file = "laserGreen.png")



#Binding the arrow keys to movement
window.bind("<Left>", left)
window.bind("<Right>",right)
window.bind("<Up>", up)
window.bind("<Down>", down)
window.bind("<space>", is_shot)
window.bind("q", is_pressed)

for y in range(10):

    my_meteor1 = Meteor()
    canvas1.after(random.randint(1000,10000), my_meteor1.place)


    # my_meteor2 = Meteor()
    # canvas1.after(random.randint(10000,50000), my_meteor2.meteor_move)




window.mainloop()
