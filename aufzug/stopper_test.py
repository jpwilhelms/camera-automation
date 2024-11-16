import time
from hardware import Hardware

hw = Hardware()

while True:
    if hw.stopperTop.isTriggered():
        print( "stopper top")
    
    if hw.stopperDown1.isTriggered():
        print( "stopper down 1")

    if hw.stopperDown2.isTriggered():
        print( "stopper down 2")

    time.sleep(0.5)