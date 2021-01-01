import pyautogui
import time

from SetCardSettings import *
from SetCard import *
from CardImageCapture import *


def getMatchIndexes(cardImages):
    hand = []
    for i in range(12):
        card = identifyLocation(i, cardImages)
        if card is not None:
            hand.append(card)

    matches = findSetStr(hand)

    if matches is None:
        for i in range(3):
            card = identifyLocation(12 + i, cardImages)
            if card is not None:
                hand.append(card)

    matches = findSetStr(hand)

    if matches is None:
        return None

    matchIndexes = []
    for match in matches:
        matchIndexes.append(hand.index(match))

    return matchIndexes


def clickLocation(locationIndex):
    x, y = getLocationCenter(locationIndex)

    pyautogui.moveTo(x, y)
    pyautogui.click()


def clickMatches(cardImages):
    matchIndexes = getMatchIndexes(cardImages)
    print(matchIndexes)

    for index in matchIndexes:
        clickLocation(index)

    pyautogui.moveTo(100, 300)
    pyautogui.click()
