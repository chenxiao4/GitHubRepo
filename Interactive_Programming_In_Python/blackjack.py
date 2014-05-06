import simplegui as gui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = gui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = gui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


STAND = False
WHO_WIN = ""
SCORE = 0
IN_ROUND = False

class Card:
    
    def __init__(self,suit,rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ",suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos,side = "front"):
        if side == "front":
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

        if side == "back":
            card_location = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])  
            canvas.draw_image(card_back, card_location, CARD_BACK_SIZE,
                              [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

        




class Hand:
    
    def __init__(self):
        
        self.hand = []
        self.pos = []
        self.cards = 0

        
    def __str__(self):
        s = ""
        for i in range(0,self.cards):
            s += self.hand[i].get_suit() + self.hand[i].get_rank()+" "
        return s

    def add_card(self,card):

        self.cards += 1
        self.hand.append(card)
        self.pos.append(self.cards*100)


    def get_value(self):
        value = 0
        if self.cards > 0:
            for i in range(0,self.cards):
                if (self.hand[i].get_rank() == 'A') and (value <=10):
                    value += 11
                else:
                    value += VALUES[self.hand[i].get_rank()]
        return value

    def busted(self):
        if self.get_value() > 21:
            return True
        else:
            return False


    def clear(self):
        
        if self.cards > 0:
            del self.hand[:]
            del self.pos[:]
            self.cards = 0


        
    def draw(self,canvas,pos,side = "front"):
        if self.cards > 0:
            self.hand[0].draw(canvas,pos,side)

            for i in range(1,self.cards):
                self.hand[i].draw(canvas,[pos[0]+self.pos[i-1],pos[1]])

    
    

class Deck:

    def __init__(self):
        self.deck = []

    def shuffle(self):
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i,j))
        random.shuffle(self.deck)


    def deal_card(self):
        return self.deck.pop()


    def clear(self):
        if len(self.deck) > 0:
            del self.deck[:]





player = Hand()
dealer = Hand()
deck = Deck()

  

def deal():
    global STAND,WHO_WIN,SCORE,IN_ROUND
    
    if IN_ROUND:
        SCORE -= 1
    
    IN_ROUND = True
    
    player.clear()
    dealer.clear()
    deck.clear()
    deck.shuffle()

    STAND = False
    WHO_WIN = ""
    
    for i in range(0,2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    
    



def hit():
    global WHO_WIN,STAND,SCORE,IN_ROUND
    
    if not player.busted() and not STAND:
        player.add_card(deck.deal_card())


    if player.busted():
        if len(WHO_WIN) == 0:
            SCORE -= 1
        WHO_WIN = "dealer"
        STAND = True
        IN_ROUND = False


        
def stand():
    global STAND,WHO_WIN,SCORE,IN_ROUND
    IN_ROUND = False
    
    if len(WHO_WIN) == 0:
        STAND = True
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())

        if dealer.busted():
            WHO_WIN = "player"
            SCORE += 1
        else:
            if dealer.get_value() >= player.get_value():
                WHO_WIN = "dealer"
                SCORE -= 1
            else:
                WHO_WIN = "player"
                SCORE += 1



                
def draw(canvas):
    global STAND,WHO_WIN,SCORE
    
    if not STAND:
        dealer.draw(canvas,[150,170],"back")
    else:
        dealer.draw(canvas,[150,170])
        canvas.draw_text("Dealer\'s Hands: %d" % dealer.get_value(),[0,530],20,"White")
        
    player.draw(canvas,[150,350])
    canvas.draw_text("BlackJack",[300,60],40,"White")
    canvas.draw_text("Dealer",[0,160],40,"White")
    canvas.draw_text("Player",[0,340],40,"Blue")
    canvas.draw_text("Player\'s Hands: %d" % player.get_value(),[0,500],20,"Blue")

    if len(WHO_WIN) != 0:
        canvas.draw_text("New Deal?",[200,340],40,"Blue")
    else:
        canvas.draw_text("Hit or Stand?",[200,340],40,"Blue")
       
    if WHO_WIN == "player":
        canvas.draw_text("You WIN!",[200,160],40,"White")
    elif WHO_WIN == "dealer":
        if player.busted():
            canvas.draw_text("You get busted and LOSE!",[200,160],40,"White")
        else:
            canvas.draw_text("You LOSE!",[200,160],40,"White")
 

    if SCORE < 0:
       color = "Red"
    else:
        color = "White" 
        
    canvas.draw_text("Score: %d" % SCORE,[520,100],40,color)

        
deal()

    
frame = gui.create_frame("Blackjack", 700, 600)
frame.set_canvas_background("Green")

frame.add_button("Deal",deal,200)
frame.add_button("Hit",hit,200)
frame.add_button("Stand",stand,200)

frame.set_draw_handler(draw)
frame.start()
