#Graphics used from www.kenney.nl

from tkinter import *
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
        self.y = 0
        if(self.rand == 0):
            self.health = 3
            self.bigMeteorImage = None
            self.meteor = None
            self.y = 0
        else:
            self.health = 1
            self.smallMeteorImage = None
            self.meteor = None
            self.y = 0

    def place(self):
        if(self.rand == 0):
            self.bigMeteorImage = PhotoImage(file = "meteorBig.png")
            self.meteor = canvas1.create_image(self.x, self.y, image = self.bigMeteorImage)
            self.meteor_move()
        else:
            self.smallMeteorImage = PhotoImage(file = "meteorSmall.png")
            self.meteor = canvas1.create_image(self.x, self.y, image = self.smallMeteorImage)
            self.meteor_move()


    def meteor_move(self):
        if(self.y <1200):
            canvas1.move(self.meteor, 0, 5)
            self.y += 5
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

#
def shoot():
#Global and local  variables
    global player_x
    global player_y
    global shot_in_action
    beam_speed = -5
    global my_meteor1

    shot_in_action =  True
    shooting_beam = canvas1.create_image(player_x, player_y-50, image = beam)
    beam_y = player_y - 50

#Loop for moving the beam
    for i in range(2000):
        canvas1.move(shooting_beam, 0, beam_speed)
        overlap_condition = overlapping(shooting_beam, my_meteor1)
        if( overlap_condition != 0 ):
            meteor_hit()
        time.sleep(0.001)
        #window.after(5)
        #time.sleep(0.02)
        beam_y -= 5
        canvas1.update()
        if(beam_y <= -20):
            shot_in_action = False
            canvas1.delete(shooting_beam)
            break

#Checks to see if another beam is currently shooting, calls the shoot() function if there is not
def is_shot(event):
    global shot_in_action
#Checking to see if there is another beam currently being shot
    if(shot_in_action):
            pass
    else:
        canvas1.update()
        shoot()

#Checks to see if item1 and item2 are overlapping
def overlapping(item1, item2):
    overlap=canvas1.find_overlapping(canvas1.bbox(item1)[0], canvas1.bbox(item1)[1], canvas1.bbox(item1)[2], canvas1.bbox(item1)[3])
    try:
        return overlap[1]
    except:
        return 0

def meteor_hit():

    global my_meteor1
    #explosion_image = PhotoImage(file = "laserGreenShot.png")

    #explosion = canvas1.create_image(my_meteor1.x, my_meteor1.y, image = explosion_image)
    canvas1.delete(my_meteor1)
    #canvas1.after(100, canvas1.delete(explosion))

window = Tk()

configure_window()

#Declaring global variables used in the functions
player_x = 250
player_y = 500
shot_in_action = False

#Creating a canvas for the backround of the game
canvas1 = Canvas(window, background = "#161756", height = 1920, width = 1080)
canvas1.pack(padx = 10, pady = 10)

#Adding the player's rocket to the screen
player = PhotoImage(file = "player.png")
player_image = canvas1.create_image(player_x, player_y, image = player)

#Loading the images
beam = PhotoImage(file = "laserGreen.png")



#Binding the arrow keys to movement and the space key to shooting a laser beam
window.bind("<Left>", left)
window.bind("<Right>",right)
window.bind("<Up>", up)
window.bind("<Down>", down)
window.bind("<space>", is_shot)

#Generates meteors
for y in range(500):
    my_meteor1 = Meteor()
    canvas1.after(random.randint(5000,100000), my_meteor1.place)


    # my_meteor2 = Meteor()
    # canvas1.after(random.randint(10000,50000), my_meteor2.meteor_move)




window.mainloop()
