##Try excepts, log the error
##Handle the backend
from hardwareControl import Door, Led, Beeper
from databases.database import Database
from threading import Thread
from databases.tableDef import *
import datetime
import sys
import time

def log(user, event, time):
    log = AccessLog(user, event, time)
    userDB.add(log)

def checkCard(card):
    ##Query database
    q = userDB.query(card)
    if len(q) > 0:
        log(q[0].name, "Allowed",datetime.datetime.now())
        return True
    else:
        user = User(id = card)
        log(user.id, "Denied", datetime.datetime.now())
        return False

def main():
    door.unlock()
    while True:
        if door.checkLock():
            led.turnOff(Led.AMBER)
            led.turnOff(Led.GREEN)
            led.turnOn(Led.RED)
            continue
        
        led.turnOn(Led.AMBER)
        led.turnOff(Led.GREEN)
        led.turnOff(Led.RED)
        
        rawCard = input("SwipeCard: ")
        formCard = rawCard[1:8]
        if checkCard(formCard):
            try:
                door.open()
                print("Door open")
                time.sleep(3)
            except:
                print("Door is locked: ")
            
            door.close()
        else:
            #Flash LEDs
            led.flashColor(Led.RED)



if __name__ == "__main__":
        userDB = Database()
        door = Door()
        led = Led()
        beeper = Beeper()
        main()
