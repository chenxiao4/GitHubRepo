""" a spaceship python game """

import simplegui as gui
import math
import random


width = 800
height = 600
score = 0
lives = 3
time = 0.5

spath = "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/"


#------------------------------------ define some Inline functions ----------------

fullpath = lambda depath, fname: "%s%s" % (depath,fname)
sound_load = lambda fname: gui.load_sound(fullpath(spath,fname))
unit_vector = lambda ang: [math.cos(ang),math.sin(ang)]
dist = lambda p,q: math.sqrt(sum([(x-y)**2 for x,y in zip(p,q)]))
list_add = lambda ll,fac,lr: [x+fac*y for x,y in zip(ll,lr)]
list_minus = lambda ll,fac,lr: [x-fac*y for x,y in zip(ll,lr)]
list_mult = lambda l,fac:[x*fac for x in l]

#--------------------------------------  Image class -----------------------------
class ImageInfo:

    depath = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/"
    
    def __init__(self, fname, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
        #print fullpath(self.depath,fname)
        self.image = gui.load_image(fullpath(self.depath,fname))
        
        
            
    def get_image(self):
        return self.image
        
    def get_center(self):
        return self.center
        
    def get_size(self):
        return self.size
    
    def get_radius(self):
        return self.radius
    
    def get_lifespan(self):
        return self.lifespan
    
    def get_animated(self):
        return self.animated
            
    

#----------------------------------  create objects -------------------------------

debris_info = ImageInfo("debris2_blue.png",[320, 240], [640, 480])
nebula_info = ImageInfo("nebula_blue.png",[400, 300], [800, 600])
splash_info = ImageInfo("splash.png",[200, 150], [400, 300])
ship_info = ImageInfo("double_ship.png",[45, 45], [90, 90], 35)
missile_info = ImageInfo("shot2.png",[5,5], [10, 10], 3, 50)
asteroid_info = ImageInfo("asteroid_blue.png",[45, 45], [90, 90], 40)
explosion_info = ImageInfo("explosion_alpha.png",[64, 64], [128, 128], 17, 24, True)



#----------------------------------- load sound -----------------------------------

soundtrack = sound_load("soundtrack.mp3")
missile_sound = sound_load("missile.mp3") 
missile_sound.set_volume(.5)
ship_thrust_sound = sound_load("thrust.mp3")       
explosion_sound = sound_load("explosion.mp3")


#------------------------------------ ship class ----------------------------------
class Ship:

    C = 0.02
    mis_speed = 10.
    
    def __init__(self, pos, vel, angle, info):
        self.pos = pos
        self.vel = vel
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = info.get_image()
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = None
        
    def draw(self,canvas):
        self.image_center[0] = self.thrust and 135 or 45
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)


    def update(self):
        self.vel = list_mult(self.vel, (1. - self.C))
        self.pos = list_add(self.pos,1.,self.vel)
        self.pos[0] %= width
        self.pos[1] %= height
        self.angle += self.angle_vel
        self.forward = unit_vector(self.angle)
        
        if self.thrust:
            ship_thrust_sound.play()
            self.vel = list_add(self.vel,0.2,self.forward)
        else:
            ship_thrust_sound.rewind()


    def fire(self):
        global a_missile
        pos_on_canv = [self.pos[0]+self.forward[0]*0.5*self.image_size[0],self.pos[1]+self.forward[1]*0.5*self.image_size[1]]
        
        vel_of_mis = list_add(self.vel,self.mis_speed,self.forward)
        
        a_missile = Sprite(pos_on_canv,vel_of_mis,self.angle,0,missile_info,missile_sound)

#---------------------------------- Sprite class ----------------------------------
class Sprite:

    def __init__(self, pos, vel, ang, ang_vel, info, sound = None):
        self.pos = pos
        self.vel = vel
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = info.get_image()
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0

        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)

    def update(self):
        self.pos = list_add(self.pos,1.,self.vel)
        self.angle += self.angle_vel



#----------------------------------- draw on canvas -------------------------------

def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % width
    center = debris_info.get_center()
    size = debris_info.get_size()
      
    canvas.draw_image(nebula_info.get_image(), nebula_info.get_center(), nebula_info.get_size(), [width / 2, height / 2], [width, height])
    canvas.draw_image(debris_info.get_image(), center, size, (wtime - width / 2, height / 2), (width, height))
    canvas.draw_image(debris_info.get_image(), center, size, (wtime + width / 2, height / 2), (width, height))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    canvas.draw_text('lives: %d' % lives, (50, 50), 24, "White")
    canvas.draw_text('score: %d' % score, (width-150, 50), 24, "White")

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
            


def rock_spawner():
    global a_rock
    a_rock = Sprite([random.random() * width, random.random() * height], [random.random(), random.random()], random.random() * 0.1, random.random() * 0.1, asteroid_info)



def keydown(key):
    
    if key == gui.KEY_MAP['left']:
        my_ship.angle_vel=-0.1
    elif key == gui.KEY_MAP['right']:
        my_ship.angle_vel=0.1
    elif key == gui.KEY_MAP['up']:
        my_ship.thrust=True
    elif key == gui.KEY_MAP['space']:
        my_ship.fire()

        
def keyup(key):
    
    if key == gui.KEY_MAP['left']:
        my_ship.angle_vel=0
    elif key == gui.KEY_MAP['right']:
        my_ship.angle_vel=0
    elif key == gui.KEY_MAP['up']:
        my_ship.thrust=False


# initialize frame
frame = gui.create_frame("Asteroids", width, height)

# initialize ship and two sprites
my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_info)

a_rock = Sprite([random.random() * width, random.random() * height], [random.random(), random.random()], random.random() * 0.1, random.random() * 0.1, asteroid_info)
 
a_missile = Sprite([2 * width / 3, 2 * height / 3], [-1,1], 0, 0, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = gui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
