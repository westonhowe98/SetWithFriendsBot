import pyautogui
import cv2
import numpy as np
import time

from SetCardSettings import *
from SetCard import *

from os import listdir
from os.path import isfile, join
from PIL import Image


# Card location index will start at 0 and increase left to right and top to bottom


def getCardRegion(locationIndex):
    leftO, topO = TL_ORIGIN

    horizontalSpacing = (CARD_WIDTH + CARD_H_SPACING) * (locationIndex % SET_SIZE)
    verticalSpacing = (CARD_HEIGHT + CARD_v_SPACING) * (locationIndex // SET_SIZE)

    left = horizontalSpacing + leftO
    top = verticalSpacing + topO

    region = (left, top, CARD_WIDTH, CARD_HEIGHT)

    return region


def getLocationCenter(locationIndex):
    left, top, w, h = getCardRegion(locationIndex)

    x = left + (w / 2)
    y = top + (h / 2)

    return x, y


def screenshotCard(locationIndex, name):
    pyautogui.screenshot(name, region=getCardRegion(locationIndex))


def screenshotLocation(locationIndex):
    return pyautogui.screenshot(region=getCardRegion(locationIndex))


def getMissingCards():
    allCards = []

    cards = getCards()
    for card in cards:
        allCards.append(str(card))

    missingCards = []
    capturedCards = getCapturedCards()
    for card in allCards:
        if card not in capturedCards:
            missingCards.append(card)

    missingCards.sort()

    return missingCards


def getCapturedCards():
    rawCards = [f for f in listdir(CARD_IMG_DIR) if isfile(join(CARD_IMG_DIR, f))]

    cards = []
    for card in rawCards:
        cards.append(card[:len(card) - len(IMG_TYPE)])

    return cards


def loadCards():
    capturedCards = getCapturedCards()

    cardImages = {}
    for card in capturedCards:
        image = cv2.imread(CARD_IMG_DIR + card + IMG_TYPE)
        image = np.array(image)

        cardImages[card] = image

    return cardImages


def captureAllLocations():
    images = []
    for i in range(SET_SIZE * 4):
        images.append(screenshotLocation(i))

    return images


def hasBeenCaptured(image, capturedImages):
    imageArray = np.array(image)
    imageArray = cv2.cvtColor(imageArray, cv2.COLOR_RGB2BGR)

    for capturedImage in capturedImages:
        capturedImageArray = np.array(capturedImage)
        if (imageArray == capturedImageArray).all():
            return True

    return False


def findUnknownCard():
    capturedImages = list(loadCards().values())
    locationImages = captureAllLocations()

    for i in range(len(locationImages)):
        locationImage = locationImages[i]
        if not hasBeenCaptured(locationImage, capturedImages):
            return i

    return None


def cardCaptureLoop():
    print(getMissingCards())
    print()

    while True:
        # locationIndex = int(input("Input Location Index:"))
        unknownCard = findUnknownCard()

        if unknownCard is not None:
            cardName = str(input("Input card for location %i:" % (unknownCard + 1)))
            cardName = cardName.upper()

            if isValidCard(cardName):
                filename = CARD_IMG_DIR + cardName + IMG_TYPE
                screenshotCard(unknownCard, filename)
            else:
                print("Invalid card entered")

        else:
            print("No unknown cards, halting!")
            quit()

        time.sleep(0.5)


def identifyLocation(locationIndex, cardImages):
    locationImage = np.array(screenshotLocation(locationIndex))
    locationImage = cv2.cvtColor(locationImage, cv2.COLOR_RGB2BGR)

    for cardName, cardImage in cardImages.items():
        res = cv2.matchTemplate(locationImage, cardImage, cv2.TM_CCOEFF_NORMED)

        if res > 0.98:
            return cardName

    return None


def cropImages():
    capturedCards = getCapturedCards()

    cardImages = {}
    for card in capturedCards:
        filename = CARD_IMG_DIR + card + IMG_TYPE
        image = Image.open(filename)
        image = image.crop((1, 1, CARD_WIDTH + 1, CARD_HEIGHT + 1))
        image.save(filename)
