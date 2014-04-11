import simplegui as gui



# global variables about frame and text
button_size = 100
canvas_size = [300,200]
watch_pos = [80,120]
watch_font_size = 50 
watch_color = 'White'

score_pos = [250,30]
score_font_size = 20
score_color = 'Red'

#global variables that can change when running
interval = 100
start_tick = 0
total_trys = 0
goodjob = 0


#helper functions

def format(t):
    minutes = t / 600
    secs = (t % 600) / 10
    sec_in_tens = (t % 600) % 10
    return "%02d:%02d.%d" % (minutes,secs,sec_in_tens)



def score():
    return "%d/%d" % (goodjob,total_trys)


def timer_handler():
    global start_tick
    start_tick = start_tick + 1


def start_handler():
    timer.start()

    

def stop_handler():
    global total_trys,goodjob
    total_trys = total_trys + 1
    if start_tick % 10 == 0:
        goodjob = goodjob + 1
    timer.stop()
    
    

def reset_handler():
    global start_tick,total_trys,goodjob
    start_tick = 0
    total_trys = 0
    goodjob = 0


def draw(canvas):
    canvas.draw_text(format(start_tick),watch_pos,watch_font_size,watch_color)
    canvas.draw_text(score(),score_pos,score_font_size,score_color)


frame = gui.create_frame("Stopwatch",canvas_size[0],canvas_size[1])

frame.add_button("Start",start_handler,button_size)
frame.add_button("Stop",stop_handler,button_size)
frame.add_button("Reset",reset_handler,button_size)

frame.set_draw_handler(draw)

timer = gui.create_timer(interval,timer_handler)


frame.start()

