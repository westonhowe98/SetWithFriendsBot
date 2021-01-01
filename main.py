import keyboard

from SetCard import *
from SetCardSettings import *
from CardImageCapture import *
from EnterSet import *


def main():
    cardImages = loadCards()

    while True:
        if keyboard.is_pressed('q'):
            quit()

        try:
            clickMatches(cardImages)
        except TypeError:
            print("Handling Error")

        # Amount of time to wait for animations to pass (s)
        time.sleep(0.75)


main()
