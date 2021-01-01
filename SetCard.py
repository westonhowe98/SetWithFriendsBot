import itertools
from random import shuffle
from SetCardSettings import *


class Card:
    # Single, Double, Triple
    Count = ['S', 'D', 'T']

    # Green, Orange, Pink
    Color = ['G', 'O', 'P']

    # Diamond, Squiggly, Oval
    Shape = ['D', 'S', 'O']

    # Empty, Shaded, Full
    Shade = ['E', 'S', 'F']

    @staticmethod
    def getCard(traitStr):
        traits = {
            "count": traitStr[0],
            "color": traitStr[1],
            "shape": traitStr[2],
            "shade": traitStr[3]
        }

        return Card(traits)

    @staticmethod
    def isSet(cards):
        if len(cards) != SET_SIZE:
            return False

        characteristics = {
            "count": [],
            "color": [],
            "shape": [],
            "shade": []
        }

        # Remap values into dict struct for later comparison
        for card in cards:
            characteristics["count"].append(card.count)
            characteristics["color"].append(card.color)
            characteristics["shape"].append(card.shape)
            characteristics["shade"].append(card.shade)

        # Remove duplicate values and store in separate dictionary
        uniqueness = {}
        for key, value in characteristics.items():
            uniqueness[key] = list(set(value))

        # Check if cards make a valid set
        for key, value in uniqueness.items():
            # A valid set of cards would have either 1 unique value for a trait across all of them,
            # meaning they all share the trait, or SET_SIZE unique values for a trait, meaning they all have
            # different values for the trait.

            uniqueCount = len(uniqueness[key])

            # Should not be possible
            if uniqueCount == 0:
                return False

            # Would indicate 2 cards sharing a trait without a third
            if uniqueCount == 2:
                return False

            # Also should not be possible
            if uniqueCount > SET_SIZE:
                return False

        return True

    def __init__(self, traits):
        self.count = traits["count"]
        self.color = traits["color"]
        self.shape = traits["shape"]
        self.shade = traits["shade"]

    def __str__(self):
        return self.count + self.color + self.shape + self.shade


def getCards():
    cards = []

    for count in Card.Count:
        traits = {"count": count}
        for color in Card.Color:
            traits["color"] = color
            for shape in Card.Shape:
                traits["shape"] = shape
                for shade in Card.Shade:
                    traits["shade"] = shade
                    cards.append(Card(traits))

    shuffle(cards)
    return cards


def findSet(hand):
    sets = list(itertools.combinations(hand, SET_SIZE))

    for candidateSet in sets:
        if Card.isSet(candidateSet):
            return candidateSet

    return None


def findSetStr(hand):
    newHand = []

    for card in hand:
        newHand.append(Card.getCard(card))

    match = findSet(newHand)

    if match is None:
        return None

    matchStr = []
    for card in match:
        matchStr.append(str(card))

    return matchStr


def hasSet(hand):
    return findSet(hand) is not None


def getHand(cards):
    hand = []

    while len(cards) > 0 and (len(hand) < 12 or not hasSet(hand)):
        for j in range(SET_SIZE):
            hand.append(cards.pop())

    return hand


def isValidCard(cardStr):
    cards = getCards()

    for card in cards:
        if str(card) == cardStr:
            return True

    return False
