""" If you have any questions or suggestions please let me know
my email address: junior.chen007@gmail.com
"""
import simplegui as gui
import random
import math
import re

#global paratemer, can be changed
num_range = 100
steps_left = 0
value = -1
guess = -1


#error hanlder, codeskulptor does not support try
#def safe_int(text):
#    """ convert the input string to integer safely """
                    
#    global guess,num_range
    
#    try:
#        ret = int(text)
#    except (ValueError,TypeError),e:
#        print "Could not convert non-number to int: ",e
#        ret = False

#    if (ret < 0 or ret >= num_range):
#        print "Guess: %d is out of bound, Guess number must be in [0,%s)" % (guess,num_range)
#        ret = False
        
#    return ret


#error handler version 2
def safe_int(text):
    """ this version is based on pattern mathch
        everytime, we check the input string only contains 
        digit numbers """
    
    global guess,num_range
    
    numbers = '\d+'
    m = re.match(numbers,text)
    if m is None:
        print "Could not convert non-number to int!"
        return False
    else:
        string = m.group()
        if len(string) == len(text):
          return int(text)
        else:
          print "Input number should be a interger!"
          return False
                                                                            

#helper function
def max_num_guess(range):
    """calculate the maximum guesses one can take based on binary search"""
    
    return int(round(math.log(range,2)))


def new_game():
    """ initialize the new game """ 
    global num_range,steps_left,value

    value = random.randrange(0,num_range)
    steps_left = max_num_guess(num_range)
    
    print
    print "New game. Range is from 0 to %d" % num_range
    print "Number of remaining guesses is %d" % steps_left
    print

    
def indicate(guess,value):
    """ give the usr an indication """
    
    if guess < value:
        print "Higher!"
    elif guess == value:
        print "Correct!"
        new_game()
    else:
        print "Lower!"
    print

    
def range100():
    """ initialize all global variables """
    
    global value,num_range,steps_left
    num_range = 100
    
    # start the new game
    new_game()
    
    
def range1000():
    """ initialize all global variables """
    
    global value,num_range,steps_left
    num_range = 1000
    
    #start the new game
    new_game()

    
def get_input(text):
    """ deal with the input string from gui """
    
    global guess,steps_left
    
    # check if we can convert the text string 
    guess = safe_int(text)
    
    #reset the input box
    inp.set_text("")
    
    if (guess is not False):
        # guess number is ok
        steps_left = steps_left - 1
        print "Guess was %d" % guess
        print "Number of remaining guesses is %d" % steps_left
        if steps_left == 0 and guess != value:
            print "You ran out of guesses. The number was %d" % value
            new_game()
        else:
            indicate(guess,value)

    else:
        #input is not ok, print the error msg
        print "PLEASE re-input the guess number!!"
        print




frame = gui.create_frame("Guess the number",200,200)

frame.add_button("Range is [0,100)",range100,200)
frame.add_button("Range is [0,1000)",range1000,200)
inp = frame.add_input("Enter a guess",get_input,200)


new_game()


frame.start()
