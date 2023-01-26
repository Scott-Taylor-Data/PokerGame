import time
import random
deck = [('2', 's'), ('2', 'h'), ('2', 'd'), ('2', 'c'), ('3', 's'), ('3', 'h'), ('3', 'd'), ('3', 'c'), 
         ('4', 's'), ('4', 'h'), ('4', 'd'), ('4', 'c'), ('5', 's'), ('5', 'h'), ('5', 'd'), ('5', 'c'), 
         ('6', 's'), ('6', 'h'), ('6', 'd'), ('6', 'c'), ('7', 's'), ('7', 'h'), ('7', 'd'), ('7', 'c'), 
         ('8', 's'), ('8', 'h'), ('8', 'd'), ('8', 'c'), ('9', 's'), ('9', 'h'), ('9', 'd'), ('9', 'c'), 
         ('10', 's'), ('10', 'h'), ('10', 'd'), ('10', 'c'), ('J', 's'), ('J', 'h'), ('J', 'd'), ('J', 'c'),
         ('Q', 's'), ('Q', 'h'), ('Q', 'd'), ('Q', 'c'), ('K', 's'), ('K', 'h'), ('K', 'd'), ('K', 'c'),
         ('A', 's'), ('A', 'h'), ('A', 'd'), ('A', 'c')]

dic = {'0.1': 0.1,
       '0.25': 0.25,
       '0.5': 0.5,
       '2': 2,
       '3': 3,
       '4': 4,
       '5': 5,
       '6': 6,
       '7': 7,
       '8': 8,
       '9': 9,
       '10': 10,
       'J': 11,
       'Q': 12,
       'K': 13,
       'A': 14}

opposite_dic = {0.25: '0.25',
                0.5: '0.5',
                2: '2',
                3: '3',
                4: '4',
                5: '5',
                6: '6',
                7: '7',
                8: '8',
                9: '9',
                10: '10',
                11: 'J',
                12: 'Q',
                13: 'K',
                14: 'A'}

########## Useful functions ##########
def handgen(deck):
    #Generates a random two card hand
    hand = []
    for i in range(2):
        hand.append(random.choice(deck))
        deck.remove(hand[i])
    return(handsorter(hand))

def handsorter(hand):
    values = convert(hand,[])
    values.reverse()
    return(makehand(values,hand,[]))
        
def boardgen(deck):
    #Generates a random five card board
    board = []
    for i in range(5):
        board.append(random.choice(deck))
        deck.remove(board[i])
    return(board)

def convert(hand,board):
    #Converts the given hand and board into a list containing each cards numerical value
    seven = hand + board
    value = []
    for i in seven:
        value.append(dic[i[0]])
    value.sort()
    return(value)

def converttiebreak(hand,board):
    #Converts the given hand and board into a list containing each cards numerical value
    seven = hand + board
    value = []
    for i in seven:
        value.append(dic[i[0]])
    return(value)

def count(value):
    #Creates a list of the count of each element from the hand and the board 
    count = []
    for i in value:
        count.append(value.count(i))
    return(count)

def makehand(sd,hand,board):
    #Takes a completed list of numbers and converts it back into card form to create the final five card hand
    seven = hand + board
    showdown = []
    sd1= []
    for i in sd:
        sd1.append(opposite_dic[i])
    for i in sd1:
        for j in seven:
            if i == j[0]:
                showdown.append(j)
                seven.remove(j)
                break
    return(showdown)

def erase(sd,value):
    #Removes any values of sd from list value. Used to find which high cards complete the hand.
    for x in sd:
        if x in value:
            value.remove(x)

def fill_out(i,sd,value):
    #input number i is the number of cards required to complete the hand. e.g in one pair hand i = 3, two pair i = 1. Returns complete 5 card hand.
    for j in range(1,i+1):
        sd = [value[-j]] + sd
    return(sd)
        
def countappend(value,i):
    sd = []
    for x in value:
        if value.count(x) == i:
            sd.append(x)
    return(sd)

def countappendflush(value,i):
    sd = []
    for x in value:
        if value.count(x) > i:
            sd.append(x)
    return(sd)

def removemorethan1(value):
    for x in value:
        if value.count(x) > 1:
            value.remove(x)
            
def straightfinder(i,value,f):
    if value[i] - value[i-1] == 1:
        if value[i-1] - value[i-2] == 1:
            if value[i-2] - value[i-3] == 1:
                if value[i-3] - value[i-4] ==f:
                    return(value)
    return('no straight')            

def flushcardselection(suits,hand,board):
    final = hand + board
    for x in suits:
        if suits.count(x) < 5:
            for y in final:
                if x == y[1]:
                    final.remove(y)
    return(final)

########## Hand Rank Functions ##########
def highcard(hand,board):
    value = convert(hand,board)
    value.remove(value[0])
    value.remove(value[0])
    return('High Card', makehand(value,hand,board))
    
def onepair(hand,board):
    value = convert(hand,board)
    sd = countappend(value,2)
    if len(sd) != 2:
        return('Hand is not one pair.')
    erase(sd,value)
    sd = fill_out(3,sd,value)
    return('One Pair',makehand(sd,hand,board))
    
def twopair(hand,board):
    value = convert(hand,board)
    sd = countappend(value,2)
    if len(sd) < 4:
        return('Hand is not two pair.')
    if len(sd) == 6:
        sd.remove(sd[0])
        sd.remove(sd[0])
    erase(sd,value)
    sd = fill_out(1,sd,value)
    return('Two Pair',makehand(sd,hand,board))
   
def trips(hand,board):
    value = convert(hand,board)
    sd = countappend(value,3)
    if len(sd) != 3:
        return('Hand is not three of a kind.')
    erase(sd,value)
    sd = fill_out(2,sd,value)
    return('Trips',makehand(sd,hand,board))

def wheel(hand,board):
    value = convert(hand,board)
    removemorethan1(value)
    if len(value) < 5:
        return('Hand is not a straight.')
    ace = value[-1]
    value.remove(ace)
    value = [ace] + value
    while len(value) > 5:
        value.remove(value[-1])
    if straightfinder(4,value,-12) != 'no straight':
        return('Straight',makehand(value,hand,board))    
    return('Hand is not a straight.')

def straight(hand,board):
    value = convert(hand,board)
    removemorethan1(value)
    for i in [7,6,5]:
        if len(value) == i:
            if straightfinder(i-1,value,1) != 'no straight':
                for j in range(i-5):
                    value.remove(value[0])
                return('Straight',makehand(value,hand,board))
            value.remove(value[-1])
    return('Hand is not a straight.')

def flush(hand,board):
    seven = hand + board
    suits = []
    cards = []
    for x in seven: # makes a list of the suits of the hand
        suits.append(x[1])
    final = flushcardselection(suits,hand,board)
    flush = countappendflush(suits,4)
    if len(flush) < 5:
        return('Hand is not a flush.')
    for x in flush:
        for y in seven:
            if x == y[1]:
                cards.append(y)
                seven.remove(y) # converts list of one suit back into card form
    value = convert(cards,[]) #creates numerical list of cards & sorts
    while len(value) > 5: #removes lowest values if more than 5 cards of same suit
        value.remove(value[0])
    return('Flush',makehand(value,final,[]))

def fullhouse(hand,board):
    value = convert(hand,board)
    trips = countappend(value,3)
    pairs = countappend(value,2)
    if len(trips) == 6:
        trips.remove(trips[-1])
        return('Full House',makehand(pairs + trips,hand,board))
    if len(trips) == 3:
        if len(pairs) == 4:
            pairs.remove(pairs[0])
            pairs.remove(pairs[0])
        if len(pairs) == 2:
            return('Full House',makehand(pairs + trips,hand,board))
    return("Hand is not a full house.")

def quads(hand,board):
    value = convert(hand,board)
    quads = []
    for x in value:
        if value.count(x) == 4:
            quads.append(x)
    if len(quads) < 4:
        return('Hand is not four of a kind.')
    erase(quads,value)
    quads = [value[-1]] + quads
    return('Quads',makehand(quads,hand,board))

def straightwheel(hand,board):
    seven = hand + board
    suits = []
    flush = []
    cards = []
    for x in seven: # makes a list of the suits of the hand
        suits.append(x[1])
    final = flushcardselection(suits,hand,board)
    flush = countappendflush(suits,4)
    for x in flush:
        for y in seven:
            if x == y[1]:
                cards.append(y)
                seven.remove(y) # converts list of one suit back into card form
    value = convert(cards,[]) #creates numerical list of cards & sorts
    if len(value) < 5:
        return('Hand is not a straight flush.')
    ace = value[-1]
    value.remove(ace)
    value = [ace] + value
    for i in [7,6,5]:
        if len(value) == i:
            if straightfinder(i-1,value,-12) != 'no straight':
                for j in range(i-5):
                    value.remove(value[0])
                return('Straight Flush',makehand(value,final,[]))
            value.remove(value[-1])
    return('Hand is not a straight flush.')

def straightflush(hand,board):
    seven = hand + board
    suits = []
    flush = []
    cards = []
    for x in seven: # makes a list of the suits of the hand
        suits.append(x[1])
    final = flushcardselection(suits,hand,board)
    flush = countappendflush(suits,4)
    for x in flush:
        for y in seven:
            if x == y[1]:
                cards.append(y)
                seven.remove(y) # converts list of one suit back into card form
    value = convert(cards,[]) #creates numerical list of cards & sorts
    for i in [7,6,5]:
        if len(value) == i:
            if straightfinder(i-1,value,1) != 'no straight':
                for j in range(i-5):
                    value.remove(value[0])
                return('Straight Flush',makehand(value,final,[]))
            value.remove(value[-1])
    return('Hand is not a straight flush.')

def royalflush(hand,board):
    seven = hand + board
    suits = []
    flush = []
    cards = []
    for x in seven: # makes a list of the suits of the hand
        suits.append(x[1])
    final = flushcardselection(suits,hand,board)
    flush = countappendflush(suits,4)
    for x in flush:
        for y in seven:
            if x == y[1]:
                cards.append(y)
                seven.remove(y) # converts list of one suit back into card form
    value = convert(cards,[]) #creates numerical list of cards & sorts
    for i in [7,6,5]:
        if len(value) == i:
            if straightfinder(i-1,value,1) != 'no straight':
                for j in range(i-5):
                    value.remove(value[0])
                if value[-1] == 14:
                    return('Royal Flush',makehand(value,final,[]))
    return('Hand is not a royal flush.')

########## Hand Idenifying Functions ##########
def whathand(hand,board):
    value = [0]
    dicto = {0: highcard(hand,board),
            1: onepair(hand,board),
           2: twopair(hand,board),
           3: trips(hand,board),
           3.5: wheel(hand,board),
           4: straight(hand,board),
           5: flush(hand,board),
           6: fullhouse(hand,board),
           7: quads(hand,board),
           7.5: straightwheel(hand,board),
           8: straightflush(hand,board),
           9: royalflush(hand,board)
            }
    for i in dicto:
        if dicto[i][0] != 'H':
            value.append(i)
    return(max(value),dicto[max(value)])

def tiebreak(hand1,hand2):
    h1 = converttiebreak(hand1[1],[])
    h2 = converttiebreak(hand2[1],[])
    for i in range(1,6):
        if h1[-i] > h2[-i]:
            return("Player 1 wins",
               "Player 1s hand:",hand1,
               "Player 2s hand:",hand2)
        if h1[-i] < h2[-i]:
            return("Player 2 wins",
               "Player 1s hand:",hand1,
               "Player 2s hand:",hand2)
    return("Hand is a tie. Pot is split between both players.",
               "Player 1s hand:",hand1,
               "Player 2s hand:",hand2)
    
def whowins(h1,h2,board):
    hand1 = whathand(h1,board)
    hand2 = whathand(h2,board)
    if hand1[0] > hand2[0]:
        return("Player 1 wins",
               "Player 1s hand:",hand1[1],
               "Player 2s hand:",hand2[1])
    if hand2[0] > hand1[0]:
        return("Player 2 wins",
               "Player 1s hand:",hand1[1],
               "Player 2s hand:",hand2[1])
    return(tiebreak(hand1[1],hand2[1]))

############################## A Game Of Poker ##############################
#Bot hand values
pocket_pairs = {('A'):10, ('K'):10,('Q'):10,('J'):9,('10'):9,('9'):9,('8'):7,('7'):7,('6'):7,('5'):7,('4'):5,('3'):5,('2'):5}
suited = {('10', '2'): 0,('10', '3'): 0,('10', '4'): 0,('10', '5'): 0,('10', '6'): 0,('10', '7'): 5,('10', '8'): 5,('10', '9'): 7,('3', '2'): 0,('4', '2'): 0,('4', '3'): 0, ('5', '2'): 0,('5', '3'): 0,('5', '4'): 0,('6', '2'): 0,('6', '3'): 0,('6', '4'): 0,('6', '5'): 5,('7', '2'): 0,('7', '3'): 0,('7', '4'): 0,('7', '5'): 0,('7', '6'): 5,('8', '2'): 0,('8', '3'): 0, ('8', '4'): 0, ('8', '5'): 0,('8', '6'): 5,('8', '7'): 5,('9', '2'): 0,('9', '3'): 0,('9', '4'): 0,('9', '5'): 0,('9', '6'): 0,('9', '7'): 5,('9', '8'): 5,('A', '10'): 10,('A', '2'): 8,('A', '3'): 8,('A', '4'): 8,('A', '5'): 8,('A', '6'): 8,('A', '7'): 8,('A', '8'): 8,('A', '9'): 9,('A', 'J'): 10,('A', 'K'): 10,('A', 'Q'): 10,('J', '10'): 10,('J', '2'): 0,('J', '3'): 0,('J', '4'): 0,('J', '5'): 0,('J', '6'): 0,('J', '7'): 0,('J', '8'): 5,('J', '9'): 5,('K', '10'): 8,('K', '2'): 5,('K', '3'): 5,('K', '4'): 5,('K', '5'): 5,('K', '6'): 5,('K', '7'): 5,('K', '8'): 5,('K', '9'): 7,('K', 'J'): 10,('K', 'Q'): 10,('Q', '10'): 9,('Q', '2'): 5,('Q', '3'): 5,('Q', '4'): 5,('Q', '5'): 5,('Q', '6'): 5,('Q', '7'): 5,('Q', '8'): 5,('Q', '9'): 8,('Q', 'J'): 9}
non_suited = {('10', '2'): 0,('10', '3'): 0,('10', '4'): 0,('10', '5'): 0,('10', '6'): 0,('10', '7'): 5,('10', '8'): 5,('10', '9'): 7,('3', '2'): 0,('4', '2'): 0,('4', '3'): 0, ('5', '2'): 0,('5', '3'): 0,('5', '4'): 0,('6', '2'): 0,('6', '3'): 0,('6', '4'): 0,('6', '5'): 5,('7', '2'): 0,('7', '3'): 0,('7', '4'): 0,('7', '5'): 0,('7', '6'): 5,('8', '2'): 0,('8', '3'): 0, ('8', '4'): 0, ('8', '5'): 0,('8', '6'): 5,('8', '7'): 5,('9', '2'): 0,('9', '3'): 0,('9', '4'): 0,('9', '5'): 0,('9', '6'): 0,('9', '7'): 5,('9', '8'): 5,('A', '10'): 10,('A', '2'): 8,('A', '3'): 8,('A', '4'): 8,('A', '5'): 8,('A', '6'): 8,('A', '7'): 8,('A', '8'): 8,('A', '9'): 9,('A', 'J'): 10,('A', 'K'): 10,('A', 'Q'): 10,('J', '10'): 10,('J', '2'): 0,('J', '3'): 0,('J', '4'): 0,('J', '5'): 0,('J', '6'): 0,('J', '7'): 0,('J', '8'): 5,('J', '9'): 5,('K', '10'): 8,('K', '2'): 5,('K', '3'): 5,('K', '4'): 5,('K', '5'): 5,('K', '6'): 5,('K', '7'): 5,('K', '8'): 5,('K', '9'): 7,('K', 'J'): 10,('K', 'Q'): 10,('Q', '10'): 9,('Q', '2'): 5,('Q', '3'): 5,('Q', '4'): 5,('Q', '5'): 5,('Q', '6'): 5,('Q', '7'): 5,('Q', '8'): 5,('Q', '9'): 8,('Q', 'J'): 9}

#When one variable changes in poker, almost all other variables are changed. All are connected. There must be a way to define them so that they are connected.
#The action of making a bet changes the current bet, the betters stack size and the pot size. A call changes the pot size and the stack size and the bet size 
########## DATA MODIFYING FUNCTIONS ##########
def dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount):
    info = { 'playerstack' : playerstack,
        'botstack' : botstack,
        'pot' : pot,
        'playerbet' : playerbet,
        'botbet' : botbet,
        'raise_amount': raise_amount
        }
    return(info)

########## PLAYER FUNCTIONS ##########
#pot surrender could be its own function that gets called on with entry'bot' or'player'depending on which person wins the pot.
def playerfolds(bothand,info):
    gloat = random.choice(list(range(20)))
    if gloat in list(range(10)):
        print('Good fold. I had you crushed.',bothand)
    if gloat in list(range(10,15)):
        print("I'll show you one",bothand[0])
    if gloat in list(range(15,20)):
        print('Terrible. Do you play any hands?!?')
    return(botwinspot(info))

def playerbets(info):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    playerbet = int(input('How much would you like to bet?'))
    if playerbet >= playerstack:
        print('Player has moved all in.')
        playerbet = playerstack
        playerstack = 0
        pot += playerbet
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)
    if playerbet >= botstack:
        print('Player has put bot all in.')
        playerbet = botstack
        pot += playerbet
        playerstack -= playerbet
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)
    if playerbet < playerstack:
        raise_amount = playerbet
        playerstack, pot = playerstack - playerbet, pot + playerbet
        print('Player has bet',playerbet,'.')
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)

def playercalls(info):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    amount_to_call = botbet - playerbet
    if amount_to_call >= playerstack:
        print('Player has called all in.')
        playerbet += playerstack
        pot += playerstack
        change_in_bot_bet = botbet - playerbet
        pot -= change_in_bot_bet
        botstack += change_in_bot_bet
        botbet = playerbet
        playerstack = 0
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)
    if amount_to_call < playerstack: 
        playerbet = botbet
        pot += amount_to_call
        playerstack -= amount_to_call
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        print('Player has called for',playerbet,'chips.')
        return(info)

def playerraises(info):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    new_bet = int(input('How much would you like to raise to?'))
    if playerstack + playerbet <= new_bet:
        print("Player has raised all in.")
        new_bet = playerstack + playerbet
        change_in_bet = new_bet - playerbet
        playerstack = 0
        pot += change_in_bet
        playerbet = new_bet
        raise_amount = playerbet - botbet
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)
    if new_bet >= botbet + botstack:
        print("Player has raised bot all in.")
        new_bet = botbet + botstack
        change_in_bet = new_bet - playerbet
        pot += change_in_bet
        playerbet = new_bet
        raise_amount = playerbet - botbet
        playerstack -= change_in_bet
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)
    if playerstack + playerbet > new_bet:
        if raise_amount == 0:
            while new_bet < 2 * botbet:
                print('Raise too small. Your raise must be at least twice the bet so the minimum raise is',2*botbet)
                new_bet = int(input('How much would you like to raise to?'))
        if raise_amount > 0:
            while new_bet < botbet + raise_amount:
                print('Raise too small. You must re-raise the bet by at least as much as the previous raise which was',raise_amount,'so the minimum re-raise is', raise_amount + botbet)
                new_bet = int(input('How much would you like to raise to?'))
        change_in_bet = new_bet - playerbet
        pot += change_in_bet
        playerstack -= change_in_bet
        playerbet = new_bet
        raise_amount = playerbet - botbet
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        print('Player has raised to',playerbet,'.')
        return(info)

def playerwinspot(info):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    print('Player wins the',pot,'chip pot.')
    playerstack += pot
    pot, playerbet, botbet, raise_amount = 0,0,0,0
    info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
    return(info)

########## BOT FUNCTIONS FOR ACTIONS NOT FOR MAKING DECISIONS ###########
def botchecks(info):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    print('Bot checks.')
    info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
    return(info)

def botfolds(info):
    print('Bot folded.')
    return(False,playerwinspot(info))
    
def botcalls(info):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    print('Bot called.')
    amount_to_call = playerbet - botbet
    if amount_to_call >= botstack:
        botbet += botstack
        pot += botstack
        change_in_player_bet = playerbet - botbet
        pot -= change_in_player_bet
        playerstack += change_in_player_bet
        playerbet = botbet
        botstack = 0    
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)
    if amount_to_call < botstack:
        pot += amount_to_call
        botbet += amount_to_call
        botstack -= amount_to_call    
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)

def botbets(info):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    x = random.choice([0.4,0.45,0.5,0.55,0.6,0.7,0.75])
    botbet = int(x * pot)
    if botbet >= botstack:
        print('Bot has moved all in.')
        botbet = botstack
        botstack = 0
        pot += botbet
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)
    if botbet >= playerstack:
        botbet = playerstack
        botstack -= botbet
        pot += botbet
        print('Bot has put player all in.')
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)
    if botbet < botstack:
        raise_amount = botbet
        botstack, pot = botstack - botbet, pot + botbet
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        print('Bot has bet',botbet,'.')
        return(info)
    
def botraises(info):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    y = random.choice([2,2.5,3,3.5,4])
    new_bet = int(playerbet * y)
    if new_bet >= botstack + botbet:
        print('Bot has raised all in.')
        new_bet = botstack + botbet
        change_in_bet = new_bet - botbet
        botstack = 0
        botbet = new_bet
        pot += change_in_bet
        raise_amount = botbet - playerbet
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)
    if new_bet >= playerstack + playerbet:
        print('Bot has raised player all in.')
        new_bet = playerstack + playerbet
        change_in_bet = new_bet - botbet
        botstack -= change_in_bet
        pot += change_in_bet
        botbet = new_bet
        raise_amount = botbet - playerbet
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)
    if new_bet < botstack + botbet:
        change_in_bet = new_bet - botbet
        botbet = new_bet
        botstack -= change_in_bet
        pot += change_in_bet
        raise_amount = botbet - playerbet
        print('Bot has raised to',botbet,'.')
        info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
        return(info)

def botwinspot(info):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    print('Bot wins the',pot,'chip pot.')
    botstack += pot
    pot, playerbet, botbet, raise_amount = 0,0,0,0
    info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
    return(info)

def splitpot(info):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    print('Hand is a tie. The ', pot,' chip pot is split between both players.')
    playerstack += int(pot/2)
    botstack += int(pot/2)
    pot, playerbet, botbet, raise_amount = 0,0,0,0
    info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
    return(info)

########## Functions For The Bot To Use Whenever It Likes ##########
def classify_bot_hand(hand):
    if hand[0][1] == hand[1][1]:
        return('Hand is suited')
    if hand [0][0] == hand[1][0]:
        return('Hand is pocket pair')
    else:
        return('Hand is not suited')
    
def hand_value(hand):
    if classify_bot_hand(hand) == 'Hand is pocket pair':
        return(pocket_pairs[hand[0][0]])
    else:
        return(suited[(hand[0][0],hand[1][0])])

def potoddscalc(botbet,playerbet,pot):
    to_call = playerbet - botbet
    pot_odds = to_call/(pot + to_call)
    return(pot_odds)

########## Preflop Bot Must Make Decisions! ##########
def preflopbotplayercalled(bothand,info):
    botstack = info['botstack']
    if botstack == 0:
        return(info)
    if hand_value(bothand) <= 6:
        return(botchecks(info))
    if hand_value(bothand) > 6:
        return(botraises(info))

def preflopbotplayerraised(bothand,info):
    pot,playerbet,botbet = info['pot'], info['playerbet'], info['botbet']
    x = potoddscalc(botbet,playerbet,pot)
    y = hand_value(bothand)
    if y < 5:
        return(botfolds(info))
    if y in [5,6]:
        if x < 0.4:
            return(botcalls(info))
        else:
            return(botfolds(info))
    if y in [7,8]:
        if x < 0.4:
            return(botraises(info))
        else:
            return(botcalls(info))
    if y in [9,10]:
        return(botraises(info))

def preflopbotplayerraisedallin(bothand,info):
    pot,playerbet,botbet = info['pot'], info['playerbet'], info['botbet']
    x = potoddscalc(botbet,playerbet,pot)
    y = hand_value(bothand)
    if y < 5:
        return(botfolds(info))
    if y in [5,6]:
        if x < 0.4:
            return(botcalls(info))
        else:
            return(botfolds(info))
    if y > 6:
            return(botcalls(info))
    
########## POST FLOP BOT MUST MAKE DECISIONS ##########
def flopbotplayerchecked(info):
     y = random.choice(list(range(10)))
     if y < 5:
         return(botbets(info))
     return(botchecks(info))
 
def flopbotplayerbet(bothand,board,info):
    x = whathand(bothand,board)[0]
    if x == 0:
        y = random.choice(list(range(100)))
        if y < 90:
            return(botfolds(info))
        if y < 95:
            return(botraises(info))
        return(botcalls(info))
    z = random.choice(list(range(100)))
    if z < 50:
        return(botcalls(info))
    return(botraises(info))

def flopbotplayerraisedallin(bothand,board,info):
    x = whathand(bothand,board)[0]
    if x > 1:
        return(botcalls(info))
    else:
        return(botfolds(info))
    
def flopbotplayerraised(bothand,board,info):
    x = whathand(bothand,board)[0]
    z = random.choice(list(range(100)))
    if x == 0:
        return(botfolds(info))
    if x in [1,2,3]:
        if z < 50:
            return(botcalls(info))
        return(botraises(info))
    if x > 3:
        return(botraises(info))

########## TURN BOT MUST MAKE DECISIONS #########
def turnbotplayerchecked(bothand,board,info):
    x = whathand(bothand,board)[0]
    y = random.choice(list(range(100)))
    if x == 0:
        return(botchecks(info))
    if x == 1:
        if y < 50:
            return(botchecks(info))
        else:
            return(botbets(info))
    if x == 2:
        return(botbets(info))
    if x > 2:
        #This clause makes it so that the bot doesn't always bet its strong hands on the turn. This reflects either slow playing or just a bad play on the bots part.
        if y < 90:
            return(botbets(info))
        else:
            return(botchecks(info))

def turnbotplayerbet(bothand,board,info):
    playerbet, botbet, pot = info['playerbet'], info['botbet'], info['pot']
    x = whathand(bothand,board)[0]
    y  = random.choice(list(range(100)))
    z = potoddscalc(botbet,playerbet,pot)
    if x == 0:
        return(botfolds(info))
    if x == 1:
        if z < 0.45:
            return(botcalls(info))
        return(botfolds(info))
    if x > 1:
        if y < 25:
            return(botcalls(info))
        return(botraises(info))

def turnbotplayerraised(bothand,board,info):
    playerbet, botbet, pot = info['playerbet'], info['botbet'], info['pot']
    x = whathand(bothand,board)[0]
    z = potoddscalc(botbet,playerbet,pot)
    if x == 0:
        return(botfolds(info))
    if x == 1:
        if z < 0.35:
            return(botcalls(info))
        return(botfolds(info))
    if x == 2:
        if z < 0.6:
            return(botcalls(info))
        return(botfolds(info))
    return(botraises(info))

def turnbotplayerraisedallin(bothand,board,info):
    playerbet, botbet, pot = info['playerbet'], info['botbet'], info['pot']
    x = whathand(bothand,board)[0]
    z = potoddscalc(botbet,playerbet,pot)
    if x == 0 or x == 1:
        return(botfolds(info))
    if x == 2:
        if z < 0.5:
            return(botcalls(info))
        return(botfolds(info))
    return(botcalls(info))

########## Functions that structure the game ##########
def blinds(hand_number,small_blind,big_blind):
    if hand_number == 0:
        small_blind = 25
        big_blind = 50
    x = [0,10,20,30,40,50,60,70,80,90,100]
    for i in range(1,11):
        if hand_number == x[i]:
            small_blind *= 2
            big_blind *= 2
    return(small_blind,big_blind)

def postblinds(small_blind,big_blind,info,position):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
    if position == 'Dealer':
        if botstack < big_blind:
            big_blind = botstack
        if playerstack < small_blind:
            small_blind = playerstack
            big_blind = small_blind
        playerstack -= small_blind
        playerbet = small_blind
        botstack -= big_blind
        botbet = big_blind
        pot = small_blind + big_blind
    if position == 'Big Blind':
        if playerstack < big_blind:
            big_blind = playerstack
        if botstack < small_blind:
            small_blind = botstack
            big_blind = small_blind
        playerstack -= big_blind
        playerbet = big_blind
        botstack -= small_blind
        botbet = small_blind
        pot = small_blind + big_blind
    info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
    return(info)

def preflop(small_blind,big_blind,position,playerhand,bothand,info):
    aux_ticker = 0
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'],info['raise_amount']
    info = postblinds(small_blind,big_blind,info,position)
    playerstack,botstack,pot,playerbet,botbet= info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet']
    update = [['Player Stack:',playerstack],['Bot Stack:',botstack],['Your bet:',playerbet],['Bot bet:',botbet],['Pot:',pot]]
    
    if position == 'Dealer':
        print('Player is dealer and small blind. Blinds are ',small_blind,'and ', big_blind,'.', 'It is your turn.',"\n","\n",
              'Game info',update,"\n","\n",
              'Your hand:',playerhand, "\n","\n")
        
        while info['playerbet'] != info['botbet']:
            #Player bet has forced bot all in to call
            if info['playerbet'] == info['botbet'] + info['botstack'] or info['playerstack'] == 0:
                info = preflopbotplayerraisedallin(bothand,info)
                if len(info) == 2:
                    #These clauses trigger if the bot folds to a raise to end the hand.
                    info = info[1]
                    return(False,info)
                break
            
            if info['botstack'] == 0:
                #BOT IS ALL IN
                entry = input("Would you like to fold or call?")
                if entry == 'fold':
                    info = playerfolds(bothand,info)
                    return(False,info)
                if entry == 'call':
                    info = playercalls(info)
                    break
                    
            entry = input("Would you like to fold, call or raise?")
            if entry == 'fold':
                info = playerfolds(bothand,info)
                return(False,info)
            
            if entry == 'call':
                info = playercalls(info)
                if aux_ticker > 0:
                    break
                info = preflopbotplayercalled(bothand,info)
                aux_ticker += 1

            if entry == 'raise':
                info = playerraises(info)
                
                if info['playerstack'] == 0:
                    #player is all in 
                    info = preflopbotplayerraisedallin(bothand,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                    break
                
                if info['playerbet'] == info['botbet'] + info['botstack']:
                    #bot is all in to call
                    info = preflopbotplayerraisedallin(bothand,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                    break
                
                info = preflopbotplayerraised(bothand,info)
                if len(info) == 2:
                    info = info[1] 
                    return(False,info)
                aux_ticker += 1
            if entry == 'end game':
                info['playerstack'] = 0
                break             
    if position == 'Big Blind':
        print("Player is big blind. Blinds are ",small_blind,'and ', big_blind,'.'," It is Bot's turn.","\n","\n",
              'Game info',update,"\n","\n",
              'Your hand:',playerhand, "\n","\n")
        info = preflopbotplayerraised(bothand,info)
        if len(info) == 2:
            info = info[1] 
            return(False,info)

        
        while info['playerbet'] == info['botbet']:
            if aux_ticker > 0:
                break
            entry = input("What would you like to do, check or raise?")
            
            if entry == 'check':
                print('Player has checked.')
                break
            
            if entry == 'raise':
                info = playerraises(info)
                if info['playerstack'] == 0:
                    #player is all in 
                    info = preflopbotplayerraisedallin(bothand,info)
                    if len(info) == 2:
                        info = info[1] 
                        return(False,info)
                    break
                    
                if info['playerbet'] == info['botbet'] + info['botstack']:
                    #bot is all in to call
                    info = preflopbotplayerraisedallin(bothand,info)
                    if len(info) == 2:
                        info = info[1] 
                        return(False,info)
                    break
                    
                info = preflopbotplayerraised(bothand,info)
                if len(info) == 2:
                    info = info[1] 
                    return(False,info)
                aux_ticker += 1
            
            if entry == 'end game':
                info['playerstack'] = 0
                break
            
        while info['playerbet'] != info['botbet']:
            if info['playerbet'] == info['botbet'] + info['botstack'] or info['playerstack'] == 0:
                #player has raised bot all in to call
                info = preflopbotplayerraisedallin(bothand,info)
                if len(info) == 2:
                    info = info[1] 
                    return(False,info)
                break
                
            if info['botstack'] == 0:
                #BOT IS ALL IN
                entry = input("Would you like to fold or call?")
                if entry == 'fold':
                    info = playerfolds(bothand,info)
                    return(False,info)
                if entry == 'call':
                    info = playercalls(info)
                    break
                if entry == 'end game':
                    info['playerstack'] = 0
                    break
                
            entry = input("Would you like to fold, call or raise?")
            if entry == 'fold':
                info = playerfolds(bothand,info)
                return(False,info)
    
            if entry == 'call':
                info = playercalls(info)
                break
            
            if entry == 'raise':
                info = playerraises(info)
                if info['playerstack'] == 0:
                    #player is all in 
                    info = preflopbotplayerraisedallin(bothand,info)
                    if len(info) == 2:
                        info = info[1] 
                        return(False,info)
                    break
                    
                if info['playerbet'] == info['botbet'] + info['botstack']:
                    #bot is all in to call
                    info = preflopbotplayerraisedallin(bothand,info)
                    if len(info) == 2:
                        info = info[1] 
                        return(False,info)
                    break
                info = preflopbotplayerraised(bothand,info)
                aux_ticker += 1
                if len(info) == 2:
                    info = info[1] 
                    return(False,info)
                
            if entry == 'end game':
                info['playerstack'] = 0
                break
    return(info)

def playpoker():
    input("Hi there! I'm the bot and we're about to play poker. Are you ready?")
    print("Great!. Please type in lower case throughout. You can end the game by typing end game between hands.",
          "\n", "What would you like your starting stack to be? I recommend 5000.","\n")
    a  = int(input())
    print("What would you like my starting stack to be?","\n")
    b = int(input())
    small_blind = 0
    big_blind = 0
    info = dictionarythat(a,b,0,0,0,0)
    for n in range(100):
        if info['botstack'] == 0 or info['playerstack'] == 0:
            break
        endgame = input("Press enter to start the next hand or type end game to quit.")
        if endgame == 'end game':
            break
        print ("\n","PREHAND:", "Player's stack:", info['playerstack'], "Bot's stack:", info['botstack'])
        deck = [('2', 's'), ('2', 'h'), ('2', 'd'), ('2', 'c'), ('3', 's'), ('3', 'h'), ('3', 'd'), ('3', 'c'), 
         ('4', 's'), ('4', 'h'), ('4', 'd'), ('4', 'c'), ('5', 's'), ('5', 'h'), ('5', 'd'), ('5', 'c'), 
         ('6', 's'), ('6', 'h'), ('6', 'd'), ('6', 'c'), ('7', 's'), ('7', 'h'), ('7', 'd'), ('7', 'c'), 
         ('8', 's'), ('8', 'h'), ('8', 'd'), ('8', 'c'), ('9', 's'), ('9', 'h'), ('9', 'd'), ('9', 'c'), 
         ('10', 's'), ('10', 'h'), ('10', 'd'), ('10', 'c'), ('J', 's'), ('J', 'h'), ('J', 'd'), ('J', 'c'),
         ('Q', 's'), ('Q', 'h'), ('Q', 'd'), ('Q', 'c'), ('K', 's'), ('K', 'h'), ('K', 'd'), ('K', 'c'),
         ('A', 's'), ('A', 'h'), ('A', 'd'), ('A', 'c')]
        playerhand = handgen(deck)
        bothand = handgen(deck)
        board = boardgen(deck)
        board_flop = board[:3]
        board_turn = board[:4]
        small_blind,big_blind = blinds(n,small_blind,big_blind)[0],blinds(n,small_blind,big_blind)[1]
        print("\n")
        if (-1) ** n > 0:
            #PREFLOP            
            info = preflop(small_blind,big_blind,'Dealer',playerhand,bothand,info)
            if len(info) == 2:
                info = info[1]
                continue
            #FLOP
            info = flop(playerhand,bothand,board_flop,info,'Dealer')
            if len(info) == 2:
                info = info[1]
                continue
            #TURN
            info = turn(playerhand,bothand,board_turn,info,'Dealer')
            if len(info) == 2:
                info = info[1]
                continue
            #RIVER
            info = river(playerhand,bothand,board,info,'Dealer')
            if len(info) == 2:
                info = info[1]
                continue
            #SHOWDOWN
            info = showdown(playerhand,bothand,board,info)
        if (-1) ** n < 0:
            #PREFLOP
            info = preflop(small_blind,big_blind,'Big Blind',playerhand,bothand,info)
            if len(info) == 2:
                info = info[1]
                continue
            #FLOP
            info = flop(playerhand,bothand,board_flop,info,'Big Blind')
            if len(info) == 2:
                info = info[1]
                continue
            #TURN
            info = turn(playerhand,bothand,board_turn,info,'Big Blind')
            if len(info) == 2:
                info = info[1]
                continue
            #RIVER
            info = river(playerhand,bothand,board,info,'Big Blind')
            if len(info) == 2:
                info = info[1]
                continue
            #SHOWDOWN
            info = showdown(playerhand,bothand,board,info)
    print('Game is over')
    
def flop(playerhand,bothand,board_flop,info,position):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'],info['raise_amount']
    playerbet,botbet,raise_amount = 0,0,0
    info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
    update = [['Player Stack:',playerstack],['Bot Stack:',botstack],['Your bet:',playerbet],['Bot bet:',botbet],['Pot:',pot]]
    print('Lets see the flop!',"\n","\n",
          'Your hand:',playerhand,"\n","\n",
          'FLOP',board_flop,"\n","\n")
    board_flop.append(['0.5','f'])
    board_flop.append(['0.25','z'])
    print("\n","Game info:",update,"\n")   
    print("Player has:",whathand(playerhand,board_flop)[1])
    if info['playerstack'] == 0 or info['botstack'] == 0:
        return(info)
    if position == 'Big Blind':
        print("It is your turn to act.")
        entry = input("What would you like to do? Check or bet?")
        if entry == "end game":
            info['playerstack'] = 0
            return(info)
       
        if entry == 'check':
            print ('Player checks.')
            info = flopbotplayerchecked(info)
            
        if entry == 'bet':
            info = playerbets(info)
            if info['playerstack'] == 0 or info['playerbet'] == info['botstack']:
                #player is all in
                info = flopbotplayerraisedallin(bothand,board_flop,info)
                if len(info) == 2:
                    info = info[1]
                    return(False,info)
            else:
                info = flopbotplayerbet(bothand,board_flop,info)
                if len(info) == 2:
                    info = info[1] 
                    return(False,info)
                     
        #This clause activates if its the players turn i.e if it went check bet or bet raise.
        while info['playerbet'] != info['botbet']:
            if info['botbet']  == info['playerstack'] + info['playerbet']:
                #bot has forced player all in.
                entry = input("What would you like to do? Fold or call?")
                if entry == "fold":
                    info = playerfolds(bothand,info)
                    return(False,info)
                
                if entry == "call":
                    info = playercalls(info)
                    break
                
            entry = input("What would you like to do? Fold, call or raise?")
            if entry == "fold":
                info = playerfolds(bothand,info)
                return(False,info)
                    
            if entry == "call":
                info = playercalls(info)
                break
                    
            if entry == "raise":
                info = playerraises(info)
                
                if  info['playerstack'] == 0:
                    #player has raised all in so bot can only fold or call
                    info = flopbotplayerraisedallin(bothand,board_flop,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                    
                if info['playerbet'] == info['botbet'] + info['botstack']:
                    #player has raised the bot all in so bot can only fold or call
                    info = flopbotplayerraisedallin(bothand,board_flop,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
               
                else:
                    info = flopbotplayerraised(bothand,board_flop,info)
                    if len(info) == 2:
                        info = info[1] 
                        return(False,info)
            
    if position == 'Dealer':
        print("It is Bot's turn to act")
        info = flopbotplayerchecked(info)
        if info['botbet'] == 0:
            entry = input("What would you like to do? Check or bet?")
            if entry == "check":
                print("Player has checked")
            if entry == "bet":
                info = playerbets(info)
                if info['playerstack'] == 0:
                    info = flopbotplayerraisedallin(bothand,board_flop,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                info = flopbotplayerbet(bothand,board_flop,info)
                if len(info) == 2:
                    info = info[1]
                    return(False,info)
        
        while info['playerbet'] != info['botbet']:
            #This clause will only activate if the bot bets
            if info['botbet'] == info['playerstack'] or info['botstack'] == 0:
                #Bot has bet player all in or bot has moved all in 
                entry = input("What would you like to do? Fold or call?")
                if entry == "fold":
                    info = playerfolds(bothand,info)
                    return(False,info)
                if entry  == "call":
                    info  = playercalls(info)
                    break
                
            entry = input("What would you like to do? Fold, call or raise?")
            
            if entry == "fold":
                info = playerfolds(bothand,info)
                return(False,info)
            
            if entry == "call":
                info = playercalls(info)
                break
            
            if entry == "raise":
                info = playerraises(info)
                if  info['playerstack'] == 0:
                    #player has raised all in so bot can only fold or call
                    info = flopbotplayerraisedallin(bothand,board_flop,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                    
                if info['playerbet'] == info['botbet'] + info['botstack']:
                    #player has raised the bot all in so bot can only fold or call
                    info = flopbotplayerraisedallin(bothand,board_flop,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                    
                else:
                    info = flopbotplayerraised(bothand,board_flop,info)
                    if len(info) == 2:
                        info = info[1] 
                        return(False,info)      
    return(info)

def turn(playerhand,bothand,board_turn,info,position):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'],info['raise_amount']
    playerbet,botbet,raise_amount = 0,0,0
    info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
    update = [['Player Stack:',playerstack],['Bot Stack:',botstack],['Your bet:',playerbet],['Bot bet:',botbet],['Pot:',pot]]
    print('Lets see the turn!',"\n","\n",
          'Your hand:',playerhand,"\n","\n",
          'TURN',board_turn,"\n","\n")
    board_turn.append(('0.1','p'))
    print("\n","Game info:",update,"\n")
    print("Player has:",whathand(playerhand,board_turn)[1])
    
    if info['playerstack'] == 0 or info['botstack'] == 0:
        return(info)
    
    if position == 'Big Blind':
        
        print("It is your turn to act.")
        entry = input("What would you like to do? Check or bet?")
        
        if entry == "end game":
            info['playerstack'] = 0
            return(info)
       
        if entry == 'check':
            print ('Player checks.')
            info = turnbotplayerchecked(bothand,board_turn,info)
            
        if entry == 'bet':
            info = playerbets(info)
            if info['playerstack'] == 0 or info['playerbet'] == info['botstack']:
                #player is all in
                info = turnbotplayerraisedallin(bothand,board_turn,info)
                if len(info) == 2:
                    info = info[1]
                    return(False,info)
            else:
                info = turnbotplayerbet(bothand,board_turn,info)
                if len(info) == 2:
                    info = info[1] 
                    return(False,info)
                     
        #This clause activates if its the players turn i.e if it went check bet or bet raise.
        while info['playerbet'] != info['botbet']:
            if info['botbet']  == info['playerstack'] + info['playerbet']:
                #bot has forced player all in.
                entry = input("What would you like to do? Fold or call?")
                if entry == "fold":
                    info = playerfolds(bothand,info)
                    return(False,info)
                
                if entry == "call":
                    info = playercalls(info)
                    break
                
            entry = input("What would you like to do? Fold, call or raise?")
            if entry == "fold":
                info = playerfolds(bothand,info)
                return(False,info)
                    
            if entry == "call":
                info = playercalls(info)
                break
                    
            if entry == "raise":
                info = playerraises(info)
                
                if  info['playerstack'] == 0:
                    #player has raised all in so bot can only fold or call
                    info = turnbotplayerraisedallin(bothand,board_turn,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                    
                if info['playerbet'] == info['botbet'] + info['botstack']:
                    #player has raised the bot all in so bot can only fold or call
                    info = turnbotplayerraisedallin(bothand,board_turn,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
               
                else:
                    info = turnbotplayerraised(bothand,board_turn,info)
                    if len(info) == 2:
                        info = info[1] 
                        return(False,info)
            
    if position == 'Dealer':
        print("It is Bot's turn to act")
        info = turnbotplayerchecked(bothand,board_turn,info)
        if info['botbet'] == 0:
            entry = input("What would you like to do? Check or bet?")
            if entry == "check":
                print("Player has checked")
            if entry == "bet":
                info = playerbets(info)
                if info['playerstack'] == 0 or info['playerbet'] == info['botstack']:
                    info = turnbotplayerraisedallin(bothand,board_turn,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                info = turnbotplayerbet(bothand,board_turn,info)
                if len(info) == 2:
                    info = info[1]
                    return(False,info)
        
        while info['playerbet'] != info['botbet']:
            #This clause will only activate if the bot bets
            if info['botbet'] == info['playerstack'] or info['botstack'] == 0:
                #Bot has bet player all in or bot has moved all in
                entry = input("What would you like to do? Fold or call?")
                if entry == "fold":
                    info = playerfolds(bothand,info)
                    return(False,info)
                if entry  == "call":
                    info  = playercalls(info)
                    break
            entry = input("What would you like to do? Fold, call or raise?")
            
            if entry == "fold":
                info = playerfolds(bothand,info)
                return(False,info)
            
            if entry == "call":
                info = playercalls(info)
                break
            
            if entry == "raise":
                info = playerraises(info)
                if  info['playerstack'] == 0:
                    #player has raised all in so bot can only fold or call
                    info = turnbotplayerraisedallin(bothand,board_turn,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                    
                if info['playerbet'] == info['botbet'] + info['botstack']:
                    #player has raised the bot all in so bot can only fold or call
                    info = turnbotplayerraisedallin(bothand,board_turn,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                
                else:
                    info = turnbotplayerraised(bothand,board_turn,info)
                    if len(info) == 2:
                        info = info[1] 
                        return(False,info)
    return(info)

def river(playerhand,bothand,board,info,position):
    playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'],info['raise_amount']
    playerbet,botbet,raise_amount = 0,0,0
    info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)
    update = [['Player Stack:',playerstack],['Bot Stack:',botstack],['Your bet:',playerbet],['Bot bet:',botbet],['Pot:',pot]]
    print('Lets see the river!',"\n","\n",
          'Your hand:',playerhand,"\n","\n",
          'RIVER',board,"\n","\n")
    print("\n","Game info:",update,"\n")
    print("Player has:",whathand(playerhand,board)[1])
    
    if info['playerstack'] == 0 or info['botstack'] == 0:
        print("Bot's Hand:",bothand)
        return(info)
    if position == 'Big Blind':
        
        print("It is your turn to act.")
        entry = input("What would you like to do? Check or bet?")
        

        if entry == "end game":
            info['playerstack'] = 0
            return(info)
       
        if entry == 'check':
            print ('Player checks.')
            info = turnbotplayerchecked(bothand,board,info)
            
        if entry == 'bet':
            info = playerbets(info)
            if info['playerstack'] == 0 or info['playerbet'] == info['botstack']:
                #player is all in
                info = turnbotplayerraisedallin(bothand,board,info)
                if len(info) ==2 :
                    info = info[1]
                    return(False,info)
            else:
                info = turnbotplayerbet(bothand,board,info)
                if len(info) == 2:
                    info = info[1] 
                    return(False,info)
                     
        #This clause activates if its the players turn i.e if it went check bet or bet raise.
        while info['playerbet'] != info['botbet']:
            if info['botbet']  == info['playerstack'] + info['playerbet']:
                #bot has forced player all in.
                entry = input("What would you like to do? Fold or call?")
                if entry == "fold":
                    info = playerfolds(bothand,info)
                    return(False,info)
                
                if entry == "call":
                    info = playercalls(info)
                    break
                
            entry = input("What would you like to do? Fold, call or raise?")
            if entry == "fold":
                info = playerfolds(bothand,info)
                return(False,info)
            if entry == "call":
                info = playercalls(info)
                break
                    
            if entry == "raise":
                info = playerraises(info)
                
                if  info['playerstack'] == 0:
                    #player has raised all in so bot can only fold or call
                    info = turnbotplayerraisedallin(bothand,board,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                    
                if info['playerbet'] == info['botbet'] + info['botstack']:
                    #player has raised the bot all in so bot can only fold or call
                    info = turnbotplayerraisedallin(bothand,board,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
               
                else:
                    info = turnbotplayerraised(bothand,board,info)
                    if len(info) == 2:
                        info = info[1] 
                        return(False,info)
            
    if position == 'Dealer':
        print("It is Bot's turn to act")
        info = turnbotplayerchecked(bothand,board,info)
        if info['botbet'] == 0:
            entry = input("What would you like to do? Check or bet?")
            if entry == "check":
                print("Player has checked")
            if entry == "bet":
                info = playerbets(info)
                if info['playerstack'] == 0 or info['playerbet'] == info['botstack']:
                    info = turnbotplayerraisedallin(bothand,board,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                info = turnbotplayerbet(bothand,board,info)
                if len(info) == 2:
                    info = info[1]
                    return(False,info)
        
        while info['playerbet'] != info['botbet']:
            #This clause will only activate if the bot bets
            if info['botbet'] == info['playerstack'] or info['botbet'] == 0:
                #Bot has bet player all in or bot has moved all in
                entry = input("What would you like to do? Fold or call?")
                if entry == "fold":
                    info = playerfolds(bothand,info)
                    return(False,info)
                if entry  == "call":
                    info  = playercalls(info)
                    break
            entry = input("What would you like to do? Fold, call or raise?")
            
            if entry == "fold":
                info = playerfolds(bothand,info)
                return(False,info)
            
            if entry == "call":
                info = playercalls(info)
                break
            
            if entry == "raise":
                info = playerraises(info)
                if  info['playerstack'] == 0:
                    #player has raised all in so bot can only fold or call
                    info = turnbotplayerraisedallin(bothand,board,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                    
                if info['playerbet'] == info['botbet'] + info['botstack']:
                    #player has raised the bot all in so bot can only fold or call
                    info = turnbotplayerraisedallin(bothand,board,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
                
                else:
                    info = turnbotplayerraised(bothand,board,info)
                    if len(info) == 2:
                        info = info[1]
                        return(False,info)
    return(info)

def showdown(playerhand,bothand,board,info):
    print("\n","Lets go to showdown!","\n","Bot shows:",bothand)
    x = whowins(playerhand,bothand,board)
    if x[0] == "Player 1 wins":
        print("Player wins!","\n",
              "Player's hand:", x[2],"\n"
              "Bot's hand:", x[4])
        info = playerwinspot(info)
    if x[0] == "Player 2 wins":
        print("Bot wins!","\n",
              "Player's hand:", x[2],"\n"
              "Bot's hand:", x[4])
        info = botwinspot(info)
    if x[0] == "hand is a tie. Pot is split between both players.":
        info = splitpot(info)
    return(info)

########## Tests ##########
'''
#Manual Test of the player action functions
botstack = 4950
playerstack = 4975
botbet = 50
playerbet = 25
pot = 75
raise_amount = 0

info = dictionarythat(playerstack,botstack,pot,playerbet,botbet,raise_amount)

print('info',"\n",info,"\n")
#preflop sim
info = playerraises(playerstack,botstack,pot,playerbet,botbet,raise_amount)
playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
print('player calls BB',info,"\n")

info = botraises(playerstack,botstack,pot,playerbet,botbet,raise_amount)
playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
print('bot raise',info,"\n")

info = playerraises(playerstack,botstack,pot,playerbet,botbet,raise_amount)
playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
print('player re-raises', info,"\n")

info = botraises(playerstack,botstack,pot,playerbet,botbet,raise_amount)
playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
print('bot raise',info,"\n")

info = playercalls(playerstack,botstack,pot,playerbet,botbet,raise_amount)
playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
print('player re-raises', info,"\n")

info = botcalls(playerstack,botstack,pot,playerbet,botbet,raise_amount)
playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
print('bot calls',info,"\n")

info = playerwinspot(playerstack,botstack,pot,playerbet,botbet,raise_amount)
playerstack,botstack,pot,playerbet,botbet,raise_amount = info['playerstack'], info['botstack'], info['pot'], info['playerbet'], info['botbet'], info['raise_amount']
print('after hand',"\n",info)

#TESTS THE ACCURACY OF THE HAND RANK FUNCTIONS
p = 1
q = 1000000
for w in range(p):
    time1 = time.clock()
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0 
    h = 0
    i = 0
    j = 0
    s = 0
    tally = {'High Card': a,
         'One Pair': b,
         'Two Pair': c,
         'Trips': d,
         'Straight': e,
         'Flush': f,
         'Full House': g,
         'Quads': h,
         'Straight Wheel': s,
         'Straight Flush': i,
         'Royal Flush': j
        }
    for z in range(q):
        deck = [('2', 's'), ('2', 'h'), ('2', 'd'), ('2', 'c'), ('3', 's'), ('3', 'h'), ('3', 'd'), ('3', 'c'), 
         ('4', 's'), ('4', 'h'), ('4', 'd'), ('4', 'c'), ('5', 's'), ('5', 'h'), ('5', 'd'), ('5', 'c'), 
         ('6', 's'), ('6', 'h'), ('6', 'd'), ('6', 'c'), ('7', 's'), ('7', 'h'), ('7', 'd'), ('7', 'c'), 
         ('8', 's'), ('8', 'h'), ('8', 'd'), ('8', 'c'), ('9', 's'), ('9', 'h'), ('9', 'd'), ('9', 'c'), 
         ('10', 's'), ('10', 'h'), ('10', 'd'), ('10', 'c'), ('J', 's'), ('J', 'h'), ('J', 'd'), ('J', 'c'),
         ('Q', 's'), ('Q', 'h'), ('Q', 'd'), ('Q', 'c'), ('K', 's'), ('K', 'h'), ('K', 'd'), ('K', 'c'),
         ('A', 's'), ('A', 'h'), ('A', 'd'), ('A', 'c')]
        x = handgen(deck)
        y = boardgen(deck)
        tally[whathand(x,y)[1][0]] += 1
        if whathand(x,y)[0] == 7.5:
            print(x,"\n",y,"\n",whathand(x,y),"\n")
    print('Tally',"\n")
    print(tally)
    print("\n")
    total = 0
    for i in tally:
        tally[i] = (tally[i]/(q)) * 100
        total += tally[i]
    print('Percentage',"\n")
    print(tally)
    print("\n")
    print('total',total)
    time2 = time.clock()
    print('duration:',time2-time1)
    print("\n")
    print("\n")
    print("--------------------------------------------------------")

'''
#SPLIT POTS CAN STILL BE FUCKY APPARENTL