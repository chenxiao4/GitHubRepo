import simplegui as gui
import random
import math

#initialize globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PA_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

peddle  = dict()

BALL_POS = [0,0]
BALL_VEL = [0,0]

SCORE = dict()
SERVE = "left"
ACC = 0

def init_ball():

    global ACC
    
    BALL_POS[0] = WIDTH / 2
    BALL_POS[1] = HEIGHT / 2

    if SERVE == "left":
        for i in range(0,2):
            BALL_VEL[i] = random.randrange(1,5)
    if SERVE == "right":
        for i in range(0,2):
            BALL_VEL[i] = -random.randrange(1,5)    
    ACC = 1
            
def init_other():
    
    peddle1 = {"pos":HEIGHT/2,"vel":0}
    peddle2 = {"pos":HEIGHT/2,"vel":0}
    peddle["left"] = peddle1       
    peddle["right"] = peddle2

    SCORE["left"] = 0
    SCORE["right"] = 0        



def init_all():
    init_ball()
    init_other()



def peddle_ulti():

    for key in peddle:
        
        if peddle[key]["pos"] <= HALF_PAD_HEIGHT:
            peddle[key]["pos"] += 1
        elif peddle[key]["pos"] >= HEIGHT - HALF_PAD_HEIGHT:
            peddle[key]["pos"] -= 1
        else:
            peddle[key]["pos"] -= peddle[key]["vel"]




def ball_ulti():
    
    global ACC
    
    for i in range(0,2):
        BALL_POS[i] += BALL_VEL[i]
            
    if (BALL_POS[1] <= BALL_RADIUS) or (BALL_POS[1] >= HEIGHT - BALL_RADIUS - 1):
        BALL_VEL[1] = -BALL_VEL[1]

        
    if (BALL_POS[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS-1): 
        if math.fabs(BALL_POS[1]-peddle["right"]["pos"]) <= HALF_PAD_HEIGHT + 1:
            BALL_VEL[0] += ACC
            BALL_VEL[0] = -BALL_VEL[0]
        else:
            SCORE["left"] += 1
            SERVE = "right"
            init_ball()
            
    if (BALL_POS[0] <= PAD_WIDTH + BALL_RADIUS):
        if math.fabs(BALL_POS[1]-peddle["left"]["pos"]) <= HALF_PAD_HEIGHT + 1:
            BALL_VEL[0] -= ACC
            BALL_VEL[0] = -BALL_VEL[0]
        else:
            SCORE["right"] += 1
            SERVE = "left"
            init_ball()
                    

       
    
def draw(canvas):
    
    canvas.draw_line([WIDTH/2,0],[WIDTH/2,HEIGHT],1,'White')
    canvas.draw_line([PAD_WIDTH,0],[PAD_WIDTH,HEIGHT],1,'White')
    canvas.draw_line([WIDTH-PAD_WIDTH,0],[WIDTH-PAD_WIDTH,HEIGHT],1,'White')
    canvas.draw_text(str(SCORE["left"]),[0.35 * WIDTH,1./4 * HEIGHT],40,'White')
    canvas.draw_text(str(SCORE["right"]),[0.6 * WIDTH,1./4 * HEIGHT],40,'White')

    
    peddle_ulti()
    ball_ulti()

        
    canvas.draw_circle(BALL_POS,BALL_RADIUS,1,'White','White')

    
    canvas.draw_polygon([[0,peddle["left"]["pos"]-HALF_PAD_HEIGHT],\
                         [PAD_WIDTH,peddle["left"]["pos"]-HALF_PAD_HEIGHT],\
                         [PAD_WIDTH,peddle["left"]["pos"] + HALF_PAD_HEIGHT],\
                         [0,peddle["left"]["pos"] + HALF_PAD_HEIGHT]],1,\
                         'White','White')
    

    canvas.draw_polygon([[WIDTH-PAD_WIDTH,peddle["right"]["pos"]-HALF_PAD_HEIGHT],\
                         [WIDTH,peddle["right"]["pos"]-HALF_PAD_HEIGHT],\
                         [WIDTH,peddle["right"]["pos"]+HALF_PAD_HEIGHT],\
                         [WIDTH-PAD_WIDTH,peddle["right"]["pos"]+HALF_PAD_HEIGHT]],\
                         1,'White','White')
    



def keyup(key):

    val = 10
    act = "vel"
    
    if key == gui.KEY_MAP["up"]:
        peddle["right"][act] -= val
            
    if key == gui.KEY_MAP["w"]:
        peddle["left"][act] -= val         
        
    if key == gui.KEY_MAP["down"]:
        peddle["right"][act] += val
        
    if key == gui.KEY_MAP["s"]:
        peddle["left"][act] += val
        


                         


def keydown(key):

    val = 10
    act = "vel"
    
    if key == gui.KEY_MAP["up"]:
        peddle["right"][act] += val
            
    if key == gui.KEY_MAP["w"]:
        peddle["left"][act] += val         
        
    if key == gui.KEY_MAP["down"]:
        peddle["right"][act] -= val
        
    if key == gui.KEY_MAP["s"]:
        peddle["left"][act] -= val
        




        

frame = gui.create_frame("Ping-Pong Gamre",WIDTH,HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart",init_all,100)

init_all()

frame.start()
