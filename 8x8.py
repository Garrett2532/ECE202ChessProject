import RPi.GPIO as GPIO
import time






def getImput():
            toPrint = []
            for b in testpins:
                button_state = GPIO.input(b)
                toPrint.append(button_state)
            print(toPrint)
            print(testpins)




GPIO.setmode(GPIO.BOARD)
testpins = [36,32,31,33,35,37,38,40]
pins = [8,10,12,16,18,22,24,26]
aclock = 3
cclock = 5



sleepTime =.001

lit = [[0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0]]


dim  = [[1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1]]

lity = [[1,0,0,0,0,0,0,0],
       [0,1,0,0,0,1,0,0],
       [0,0,1,0,0,0,0,0],
       [0,0,0,1,0,0,0,0],
       [0,0,0,0,1,0,0,0],
       [0,0,0,0,0,1,0,0],
       [0,0,0,0,0,0,1,0],
       [0,0,0,0,0,0,0,1]]

a = [[0,0,0,1,1,1,0,0],
      [0,0,1,1,0,1,1,0],
      [0,1,1,0,0,1,1,0],
      [0,1,1,0,0,1,1,0],
      [0,1,1,1,1,1,1,0],
      [0,1,1,0,0,1,1,0],
      [0,1,1,0,0,1,1,0],
      [1,1,0,0,0,0,1,1]]





ani = [lity, dim, lit]

speed =300

for b in testpins:
    print(b)
    GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#print("pins")
for p in pins:
 #   print(cathode)
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, 0)

GPIO.setup(aclock, GPIO.OUT)
GPIO.output(aclock, 0)

GPIO.setup(cclock, GPIO.OUT)
GPIO.output(cclock, 0)
#print("pins")
try: 
    while(True):
        for frame in range(len(ani)):
            for pause in range (speed):
                for i in range(8):
  #                  print( "pins", pins,"ani",  ani,"frame", frame)
                    GPIO.output(pins[0],ani[frame][i][0])
                   
                    GPIO.output(pins[1],ani[frame][i][1])
                  
                    GPIO.output(pins[2],ani[frame][i][2])
                    
                    GPIO.output(pins[3],ani[frame][i][3])
                    
                    GPIO.output(pins[4],ani[frame][i][4])
                    #sets each pin in the row to the number in the frame of the animation
                    GPIO.output(pins[5],ani[frame][i][5])
                    
                    GPIO.output(pins[6],ani[frame][i][6])
                    
                    GPIO.output(pins[7],ani[frame][i][7])
                    

                    getImput()


                    GPIO.output(cclock, 0)
                    getImput()#sets the cathode clock to 1 to save the cathodes in the state 
                    GPIO.output(cclock, 1)
                    getImput()#sets back to 
                    
                    
                    for pin in pins:
                        GPIO.output(pin, 0)
                    getImput()

                    GPIO.output(pins[i],1)                          #sets the anode high to light up the leds in the row
                    getImput()
                    GPIO.output(aclock, 1)                          #sets the anode clock to high to save this
                    GPIO.output(aclock, 0)                          #sets the anode pin back to 0

                    


                    time.sleep(sleepTime)                           #sleeps for sleeptime amount of time to keep the board lit 
                    
                    GPIO.output(pins[i],0)                          #sets the anode pin to low to make all LEDs in the row dim
                    getImput()
                    GPIO.output(aclock, 1)                          #set output to 1 to save the row being off
                    GPIO.output(aclock, 0)                          #sets back to 0

except KeyboardInterrupt:
    GPIO.cleanup()


