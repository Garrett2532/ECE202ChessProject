import chess
import RPi.GPIO as GPIO
import time
import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017

GPIO.setmode(GPIO.BCM)

def lightBoard(animation,speed):                      #funtion to light the proper LED lights 
    sleepTime = .001
    
    GPIO.setmode(GPIO.BCM)

    for cathode in cathodes:
     GPIO.setup(cathode, GPIO.OUT)
     GPIO.output(cathode, 0)
    for anode in anodes:
         GPIO.setup(anode, GPIO.OUT)
         GPIO.output(anode, 0)
   # while(True): taking out inf loop until we get buttons working with code
    for frame in range(len(animation)):                                     #3d loop containng frames in the animation and lines in the frams
                for pause in range (speed):
                    for i in range(8):
                          GPIO.output(cathodes[0],animation[frame][i][0])   #setting the cathode to value in the frame
                          GPIO.output(cathodes[1],animation[frame][i][1])
                          GPIO.output(cathodes[2],animation[frame][i][2])
                          GPIO.output(cathodes[3],animation[frame][i][3])
                          GPIO.output(cathodes[4],animation[frame][i][4])
                          GPIO.output(cathodes[5],animation[frame][i][5])    
                          GPIO.output(cathodes[6],animation[frame][i][6])                    
                          GPIO.output(cathodes[7],animation[frame][i][7])

                          GPIO.output(anodes[i],1)                          #set anode of that node to 1
                          time.sleep(sleepTime)                             # wait to keep lit for a while
                          GPIO.output(anodes[i],0)

def getLegalMoves(chessboard,s):


    cfile = s[0]                           #file is the A in A1 (0-7) to be done with buttons later 
    rank = s[1]                                       #rank is the 1 in A1 (0-7)

    spot  = chess.square(cfile, rank)
    legalMoves = (list(chessboard.generate_legal_moves(from_mask=chess.BB_SQUARES[spot])))
    legalIndex = []
    for M in legalMoves:
        t = chessboard.san(M)
        if(len(t) > 2):
            if(t[-1] == '+' or t[-1] == '#'):
                t = t[:-1]
        while(len(t) > 2):                          #get rid of any symbols and like R for rook or + for check or x for taking a peice
         t= t[1:]
        legalIndex.append(chess.parse_square(t))


    boardlight  =  [[1,1,1,1,1,1,1,1],              #get inital board state for LEDs
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1]]

    for i in legalIndex:
         r = int(i/8)
         index = i%8                                 #get rank and file for each peice in legal index and convert to a numerical index and change index of led baord to be lit on those spots
         boardlight[r][index] = 0

    return boardlight





def getSquare(chessboard,toFrom,ani):
    #code for the buttons will go here
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    i2c = busio.I2C(board.SCL, board.SDA)

# Create an instance of either the MCP23008 or MCP23017 class depending on
# which chip you're using:
#mcp = MCP23008(i2c)  # MCP23008
    mcp = MCP23017(i2c)  # MCP23017
    GPIO.setmode(GPIO.BCM)
    rank = []
    for pin in range(0,8):
        rank.append(mcp.get_pin(pin))
    File = []
    for pin in range(8,16):
        File.append(mcp.get_pin(pin))

    for pin in rank:
        pin.direction = Direction.INPUT
        pin.pull = Pull.UP
    
    for pin in File:
        pin.direction = Direction.INPUT
        pin.pull = Pull.UP
    rankb = False
    fileb = False
    rankval = -1
    fileval = -1
    while(True):
        if rankb == True:
            break
        for num, button in enumerate(rank):
            if(toFrom):
                lightBoard(ani,1)
            if not button.value:
                print("Button ", num , "pressed")
                rankval = num
                rankb = True
                break
            else:
                state = GPIO.input(21);
                if(state==False):
                   startTime = time.time()
                   while(GPIO.input(21) == False):
                       if(time.time()-startTime > 3):
                       #restart the game
                           print("restarting game...")
                           print("")
                           chessboard.reset()
                           chessboard.clear_stack()
                           lightBoard([reset],100)
                           print(chessboard)
                           return(-2)
                   if(toFrom):
                       return(-1)
    
    while(True):
        if fileb ==  True:
            break
        for num,button in enumerate(File):
            if(toFrom):
                lightBoard(ani,1)
            if not button.value :
                print( "Button ", num ," pressed")
                print("")
                fileval = num
                fileb = True
                break
    
    return[rankval,fileval]                 #first posit is the file, A in A1 will be numbered 0-7
                                #second position is the rank, 1 in A1 and will be numberered 0-7




def gameOver(baord):
    if(baord.is_checkmate()):
            return True         #returns true if in a checkmate state need to be updated to check for stalemate or good peices 
    else:
            return False
def getAni(i):
    lity =    [[1,1,1,1,1,1,1,1],              #get inital board state for LEDs
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1]]
      
    r = int(i/8)
    index = i%8
    lity[r][index] = 0

    return lity

    


#program starts here
reset =         [[0,0,0,0,0,0,0,0],              #get inital board state for LEDs
                [0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0],              #get inital board state for LEDs
                [0,0,0,0,0,0,0,0]]

dim =          [[1,1,1,1,1,1,1,1],              #get inital board state for LEDs
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1]]

badmove =      [[0,1,0,1,0,1,0,1],              #get inital board state for LEDs
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,1,0,1,0]]
mintime = 5#5
shortTime =50 #50
midTime = 75#75
longTime = 100#100
longestTime =200 #200

cathodes = [4,17,27,22,10,9,11,0]               #need to change this 
anodes = [14,15,18,23,24,25,8,7]
chessboard = chess.Board()



print(chessboard)
print("")
lightBoard([reset],longTime)
while(True):
    if(gameOver(chessboard)):                        #breaks the inf loop when checkmate is detected 
        #do Stuff before game is over?
        winner = "White"
        if(chessboard.turn):
            winner = "Black"
        print("Game over ", winner, "won!")
        break
    
    isIlegal = True                             # assumes the move is illegal until proven legal
    while(isIlegal):                            #inf loop until legal move is given
         fromsq = getSquare(chessboard,False,[dim])
         legalMoves = []
         if(fromsq != -2):
             fsquare = chess.square(fromsq[0],fromsq[1])
             legalMoves = (list(chessboard.generate_legal_moves(from_mask=chess.BB_SQUARES[fsquare])))
         if(len(legalMoves) == 0):              #if no legal moves with that peice a differeent peice must be used
             if(fromsq == -2):
                 continue
             else:
                 lightBoard([badmove],midTime)
                 print("Illegal move that piece cannot move!") #inf loop if illegal due to no buttons right now 
                 print("")
             #other things to handle illegal moves here blink board?check if pinned?

         else:
            t =  getLegalMoves(chessboard,fromsq) #add things like blinking spot for a king in check here       
            ani = [t]                           #if that square has moves then light up the board
            lightBoard(ani,midTime)
            
            tosq = getSquare(chessboard,True,ani)             #gets square fromm buttons txt imput right now
            if(tosq != -1 and tosq != -2):
                tsquare = chess.square(tosq[0],tosq[1])
            legalIndex = []
            for M in legalMoves:
                 t = chessboard.san(M)
                 if(t[-1] == '+' or t[-1] == '#'):
                     t = t[:-1]
                 while(len(t) > 2):                          #get rid of any symbols and like R for rook or + for check or x for taking a peice
                     t= t[1:]
                 legalIndex.append(chess.parse_square(t))   #change the a2 to a numerical value repreenting a legal move and add it to the array
            if(tosq != -1 and tosq != -2):
                for i in legalIndex:
                    if(i == tsquare):                           #if the peice selected matches the index of one of the legal moves make the move legal and convert from numbers to spaces 1 to a2
                        isIlegal = False
                        s = ""
                        s = s + chess.square_name(fsquare)
                        s = s + chess.square_name(tsquare)
                        chessboard.push(chess.Move.from_uci(s))      #code that makes the move
                        ani = [getAni(i)]
                        for  i in range (2):
                            lightBoard([dim],midTime)
                            lightBoard(ani, midTime)
                        print(chessboard)
                        print("")
                        if(gameOver(chessboard)):                        #breaks the inf loop when checkmate is detected 
        #do Stuff before game is over?
                            winner = "White"
                            if(chessboard.turn):
                                winner = "Black"
                            print("Game over ", winner, "won!")
                        break
            if(tosq == -1):
                ani = [getAni(fsquare)]
                lightBoard(ani, longestTime)
                print("Restting move")
                print("")
            elif(tosq == -2 or fromsq == -2):
                continue
            elif(isIlegal == True):                           #if no match for index then the space given was illegal
                lightBoard([badmove],midTime)
                print("Illegal move that piece cannot move there")
                print("")






























