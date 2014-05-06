import simplegui as gui
import random


NumberofCards = 16

#dict to store card information
card = dict(zip(("W","H","N","S"),(50,100,NumberofCards,[])))

#store exposing status of cards
expos = []

#postion of cards
pos = [card["W"]//2]
state = 0

# Queue to store cards which are clicked 
record = []
turns = 0

DEBUG = "off"


def clear_all():
    del expos[:]
    del record[:]
    pos[1:] = []

    
def new_game():

    global state,turns
    
    clear_all()
    num = [i % card["N"]//2 for i in range(0,card["N"])]
    random.shuffle(num)
    card["S"] = list(num)

    expos.append(False)
    
    for i in range(1,card["N"]):
        pos.append(card["W"] * i + card["W"] // 2 + i)
        expos.append(False)    

    state = 0
    turns = 0
    l.set_text("Turns = %d" % turns)
        
def mouseclick(pos):
    global state,turns

    ind = pos[0] // card["W"]
    
    #ignores clicks on exposed cards
    if expos[ind]:
        return
    
    if ind < card["N"]:
        expos[ind] = True
        record.append(ind)
    
    #update state
    if state == 0 or state == 1:
        state += 1
    else:
        state = 1
                
    if state == 1 and len(record) == 3:
        if card["S"][record[0]] != card["S"][record[1]]:
            for i in range(0,2):
                expos[record.pop(0)] = False
        else:
            for i in range(0,2):
                record.pop(0)    


    if state == 2:
        turns += 1
        l.set_text("Turns = %d" % turns)
    
    if DEBUG is "on":     
        print state,"   ",record
        print expos
               

def draw(canvas):

    for i in range(0,card["N"]):
        if expos[i]:
            canvas.draw_text(str(card["S"][i]),[pos[i]-card["W"]/4.,card["H"]*0.6],30,"White")
        else:
            canvas.draw_line([pos[i],0],[pos[i],card["H"]],card["W"],"Green")


    
    
frame = gui.create_frame("Memory", card["W"]*card["N"] + card["N"]-1, card["H"])
frame.add_button("Restart",new_game,60)
l = frame.add_label("Turns = %d" % turns)

frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)


new_game()

frame.start()

