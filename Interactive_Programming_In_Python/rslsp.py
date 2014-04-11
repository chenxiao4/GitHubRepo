# Rock-paper-scissors-lizard-Spock template

import random


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    
    name = name.lower()
    
    if name == "rock":
        return 0
    elif name == "spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        #print "Invalid input!"
        return -1
    


def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif:
        return "scissors"

    
def rpsls(player_choice): 

    player = name_to_number(player_choice)
        
    computer = random.randrange(0,5)
    computer_choice = number_to_name(computer)

    diff = (computer - player) % 5

    if diff == 0:
        msg = "Player and computer ties!"
    elif diff <= 2:
        msg = "Computer wins!"
    else:
        msg = "Player wins!"
        

    print
    print "Player chooses %s" % player_choice
    print "Computer chooses %s" % computer_choice    
    print msg
 
    
# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric

