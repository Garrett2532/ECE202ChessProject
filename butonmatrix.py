import time
import RPi.GPIO as GPIO
import board
import busio
from digitalio import Direction, Pull
import RPi.GPIO as GPIO

#from adafruit_mcp230xx.mcp23008 import MCP23008
from adafruit_mcp230xx.mcp23017 import MCP23017


# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)

# Create an instance of either the MCP23008 or MCP23017 class depending on
# which chip you're using:
#mcp = MCP23008(i2c)  # MCP23008
mcp = MCP23017(i2c)  # MCP23017
test = [6,5,19,26]
GPIO.setmode(GPIO.BCM)
for pin in test:
    GPIO.setup(pin, GPIO.IN,pull_up_down = GPIO.PUD_UP)

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

while(True):
        if rankb == True:
            break
        for num, button in enumerate(rank):
            if not button.value:
                print("Rank ", num , "pressed")
                rankb = True
                break 
    
while(True):
        if fileb ==  True:
            break
        for num,button in enumerate(File):
            if not button.value :
                print( "File ", num ," pressed")
                fileb = True
                break
        for i in test:
            if(GPIO.input(i) == False):
                print("Button",i,"Pressed")
                break
