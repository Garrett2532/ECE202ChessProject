import RPi.GPIO as GPIO
import time

buttons = [22,24,26,32] 


def setup():
       GPIO.setmode(GPIO.BOARD)
       for b in buttons:
           print(b)
           GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
        while True:
            for b in buttons:
              button_state = GPIO.input(b)
              if  button_state == False:
                  print("Button" , buttons.index(b), "pressed")
                  time.sleep(.3)

def endprogram():
         GPIO.cleanup()


if __name__ == '__main__':
          
          setup()
          
          try:
                 loop()
          
          except KeyboardInterrupt:
               #  print( 'keyboard interrupt detected' )
                 endprogram()
