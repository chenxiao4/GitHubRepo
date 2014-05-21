""" a spaceship python game """

import simplegui as gui
import math
import random


width = 800
height = 600
score = 0
lives = 3
time = 0.5
started = False


spath = "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/"


#------------------------------------ define some online functions ----------------

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
    mis_speed = 6.
    
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
        
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
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
        global obs
        pos_on_canv = [self.pos[0]+self.forward[0]*0.5*self.image_size[0],self.pos[1]+self.forward[1]*0.5*self.image_size[1]]
        
        vel_of_mis = list_add(self.vel,self.mis_speed,self.forward)
        
        a_missile = Sprite(pos_on_canv,vel_of_mis,self.angle,0,missile_info,missile_sound)
        obs.add_obj("missile",a_missile)
        #missles.add(a_missle)
        
            
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
        
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]], self.image_size,self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)

    def update(self, is_rock):
        
        self.pos = list_add(self.pos,1.,self.vel)
        
        if is_rock:
            self.pos[0] %= width
            self.pos[1] %= height
            
        self.angle += self.angle_vel
        self.age += 1
        return self.age < self.lifespan
        
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
     
    def collide(self, other_object):
        distance = dist(self.pos,other_object.get_position())
        return distance <= (self.radius + other_object.get_radius()) 
        




#---------------------------------- class objects --------------------------------
class Objects:
    
    def __init__(self):
        self.missiles = set([])
        self.rocks = set([])
        self.explosions = set([])
       
    def hash_table(self,obname):
        if obname == "missile":
            return self.missiles
        elif obname == "rock":
            return self.rocks
        else:
            return self.explosions
    
    def process_object(self,obs,canvas):
        remove = set([])
        for ob in obs:
            ob.draw(canvas)
            if obs is self.missiles and (not ob.update(False)):
                remove.add(ob)
            elif obs is self.missiles:
                ob.update(False)
            else:
                ob.update(True)

        obs.difference_update(remove)
        
        
    def process(self,canvas):
        
        self.process_object(self.missiles,canvas)
        self.process_object(self.rocks,canvas)
        self.process_object(self.explosions,canvas)
        
    def add_obj(self, obname,ob):
        self.hash_table(obname).add(ob)
        
    def deal_gcollid(self, oneob):
        remove = set([]) 
        for ob in self.rocks:
            if ob.collide(oneob):
                explosion = Sprite(ob.pos, ob.vel, ob.angle, ob.angle_vel, explosion_info, explosion_sound)
                self.explosions.add(explosion)
                remove.add(ob)
        self.rocks.difference_update(remove)
        
        #return collision numbers
        return len(remove)
    
    def deal_ggcollid(self):
        remove = set([])
        for oneob in self.missiles:
            if self.deal_gcollid(oneob) > 0:
                remove.add(oneob)
        self.missiles.difference_update(remove)
        return len(remove)
    
    
    def clear(self):
        del self.missiles
        del self.rocks
        del explosions
        
        self.missile = set([])
        self.rocks = set([])
        self.explosions = set([])
    
    
#----------------------------------- Objects --------------------------------------    
obs = Objects()
#----------------------------------- draw on canvas -------------------------------

def draw(canvas):
    global time,started,lives,score
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    
    canvas.draw_image(nebula_info.get_image(), nebula_info.get_center(), nebula_info.get_size(), [width / 2, height / 2], [width, height])
    
    canvas.draw_image(debris_info.get_image(), [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], [width / 2 + 1.25 * wtime, height / 2], [width - 2.5 * wtime, height])
    
    canvas.draw_image(debris_info.get_image(), [size[0] - wtime, center[1]], [2 * wtime, size[1]], [1.25 * wtime, height / 2], [2.5 * wtime, height])

    if lives == 0:
        started = False
        #lives = 3
        #score = 0
        obs.clear()
        
    if not started:
        splash.draw(canvas)
        
        
    
    # draw ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    
    obs.process(canvas)
    lives -= obs.deal_gcollid(my_ship)
    score += obs.deal_ggcollid()
    
    
    if lives > 0:
        color = "White"
    else:
        color = "Red"
    canvas.draw_text('lives: %d' % lives, (50, 50), 30, color)
    canvas.draw_text('score: %d' % score, (width-150, 50), 30, "White")

            
        

def rock_spawner():
    
    global started
       
    a_rock = Sprite([random.random() * width, random.random() * height], [random.random(), random.random()], random.random() * 0.1, random.random() * 0.1, asteroid_info)
    if started and not a_rock.collide(my_ship):
        obs.add_obj("rock",a_rock)
    else:
        obs.rocks


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


        
def click(pos):
    global started,lives,score
    
    if pos[0] > (splash.get_position()[0] - 200) and pos[0] < (splash.get_position()[0]+ 200) and pos[1] > (splash.get_position()[1] - 150) and pos[1] < (splash.get_position()[1] + 150):
        started = True
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()
        
        
        
# initialize frame
frame = gui.create_frame("Asteroids", width, height)

# initialize ship and two sprites
my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_info)

splash = Sprite([width / 2, height / 2], [0, 0],0,0,splash_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = gui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
