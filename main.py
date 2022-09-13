# This program is a solution for
# Project Euler Problem 54
# https://projecteuler.net/problem=54

# The file, p054_poker.txt, contains one-thousand random hands dealt to two players.
# Each line of the file contains ten cards (separated by a single space):
# the first five are Player 1's cards and the last five are Player 2's cards.

# Program shows how many hands players have won


def sortHand(hand):
    # Sorts hand's values from lowest to highest for ease of operation
    handValues = [i[0] for i in hand]
    digitValues = []
    alphaValues = []
    for i in handValues:
        if i.isdigit():
            digitValues.append(i)
        else:
            alphaValues.append(i)
    digitValues.sort()
    newAlphaValues = []
    for i in ['T', 'J', 'Q', 'K', 'A']:  # Sorts by poker values
        if i in alphaValues:
            for j in range(alphaValues.count(i)):
                newAlphaValues.append(i)
    newHand = digitValues + newAlphaValues
    # Returns in string form
    return "".join(newHand)


def separateHands(hand):
    # Separates player1's hand and players2's hand
    hand1 = hand[:14]
    hand2 = hand[15:]
    hand1 = hand1.split()
    hand2 = hand2.split()
    return hand1, hand2


def tieTime(hand1, hand2):
    # If there is a tie, this part is trying to find out in which hand is the highest card
    hand1 = list(hand1)
    hand2 = list(hand2)
    consecutive = "123456789TJQKA"
    for i in range(len(hand1) - 1, -1, -1):  # goes from end to beginning to find out the highest card
        if consecutive.index(hand1[i]) == consecutive.index(hand2[i]):
            hand1.pop()
            hand2.pop()
            if hand1 == [] and hand2 == []:  # if hands are empty, it means a tie
                return "tie"
            return tieTime(hand1, hand2)
        if consecutive.index(hand1[i]) > consecutive.index(hand2[i]):
            return "player1"
        if consecutive.index(hand1[i]) < consecutive.index(hand2[i]):
            return "player2"


def flush(handSuits):
    # looks for if all suits are same
    for i in range(0, len(handSuits) - 1):
        if handSuits[i] != handSuits[i + 1]:
            return False
    return True


def straight(handValues):
    # looks for if values are consecutive
    consecutive = "123456789TJQKA"
    if handValues in consecutive:
        return True
    return False


def straightFlush(handValues, handSuits):
    # looks for if values are consecutive and if all suits are same
    if straight(handValues) and flush(handSuits):
        return True
    return False


def fourOfAKind(handValues):
    # looks for four cards of the same value
    for i in handValues:
        if handValues.count(i) == 4:
            return True
    return False


def fullHouse(handValues):
    # looks for three of a kind and a pair
    if threeOfAKind(handValues) and onePair(handValues):
        return True
    return False


def threeOfAKind(handValues):
    # looks for three cards of the same value
    for i in handValues:
        if handValues.count(i) == 3:
            return True
    return False


def twoPairs(handValues):
    # looks for two different pairs
    for i in range(5):
        currentValue = handValues[i]
        if handValues.count(currentValue) == 2:
            for j in range(i + 2, 5):
                currentValue = handValues[j]
                if handValues.count(currentValue) == 2:
                    return True
            return False
    return False


def onePair(handValues):
    # looks for two cards of the same value
    for i in range(5):
        currentValue = handValues[i]
        if handValues.count(currentValue) == 2:
            return True
    return False


def whoWins(hand):
    hand1, hand2 = separateHands(hand)
    # separates each hand into values and suits
    hand1Values = sortHand(hand1)
    hand2Values = sortHand(hand2)
    hand1Suits = [i[1] for i in hand1]
    hand2Suits = [i[1] for i in hand2]

    # Royal Flush
    if "TJQKA" == hand1Values and "TJQKA" == hand2Values:
        return "tie"
    if "TJQKA" == hand1Values:
        return "player1"
    if "TJQKA" == hand2Values:
        return "player2"

    # Straight Flush
    if straightFlush(hand1Values, hand1Suits) and straightFlush(hand2Values, hand2Suits):
        return tieTime(hand1Values, hand2Values)
    if straightFlush(hand1Values, hand1Suits):
        return "player1"
    if straightFlush(hand2Values, hand2Suits):
        return "player2"

    # Four of a Kind
    if fourOfAKind(hand1Values) and fourOfAKind(hand2Values):
        # if both hands have "four of a kind", it looks to their  value's rank
        # looks at index 2 because:
        # it must be ____ _ or _ ____
        # second index is common
        interimValue = tieTime(hand1Values[2], hand2Values[2])
        if interimValue != "tie":
            return interimValue
        return tieTime(hand1Values, hand2Values)
    if fourOfAKind(hand1Values):
        return "player1"
    if fourOfAKind(hand2Values):
        return "player2"

    # Full House
    if fullHouse(hand1Values) and fullHouse(hand2Values):
        return tieTime(hand1Values, hand2Values)
    if fullHouse(hand1Values):
        return "player1"
    if fullHouse(hand2Values):
        return "player2"

    # Flush
    if flush(hand1Suits) and flush(hand2Suits):
        return tieTime(hand1Values, hand2Values)
    if flush(hand1Suits):
        return "player1"
    if flush(hand2Suits):
        return "player2"

    # Straight
    if straight(hand1Values) and straight(hand2Values):
        return tieTime(hand1Values, hand2Values)
    if straight(hand1Values):
        return "player1"
    if straight(hand2Values):
        return "player2"

    # Three of a Kind
    if threeOfAKind(hand1Values) and threeOfAKind(hand2Values):
        # if both hands have "three of a kind", it looks to their  value's rank
        # looks at index 2 because:
        # it must be ___ _ _ or _ ____ _ or _ _ ___
        # second index is common
        interimValue = tieTime(hand1Values[2], hand2Values[2])
        if interimValue != "tie":
            return interimValue
        return tieTime(hand1Values, hand2Values)
    if threeOfAKind(hand1Values):
        return "player1"
    if threeOfAKind(hand2Values):
        return "player2"

    # Two Pairs
    if twoPairs(hand1Values) and twoPairs(hand2Values):
        # if both hands have "two pairs", it looks to their  value's rank
        # looks at index 3 and 1 because:
        # it must be __ __ _ or _ __ __ or __ _ __
        # third index is common and highest, if third indexes are same it looks to first index
        interimValue = tieTime(hand1Values[3], hand2Values[3])
        if interimValue != "tie":
            return interimValue
        interimValue = tieTime(hand1Values[1], hand2Values[1])
        if interimValue != "tie":
            return interimValue
        return tieTime(hand1Values, hand2Values)
    if twoPairs(hand1Values):
        return "player1"
    if twoPairs(hand2Values):
        return "player2"

    # One Pair
    if onePair(hand1Values) and onePair(hand2Values):
        # if both hands have "one pair", it looks to their  value's rank
        # looks at index 3 and 1 because:
        # it must be __ _ _ _ or _ __ _ _ or _ _ __ _ or _ _ _ __
        # one of the pairs must be in third or first index
        # checks where one of the pairs is
        if hand1Values.count(hand1Values[1]) == 2:
            pair1is = 1
        else:
            pair1is = 3
        if hand2Values.count(hand2Values[1]) == 2:
            pair2is = 1
        else:
            pair2is = 3
        interimValue = tieTime(hand1Values[pair1is], hand2Values[pair2is])
        if interimValue != "tie":
            return interimValue
        return tieTime(hand1Values, hand2Values)
    if onePair(hand1Values):
        return "player1"
    if onePair(hand2Values):
        return "player2"

    # High Card
    return tieTime(hand1Values, hand2Values)


player1 = 0
player2 = 0
tie = 0
file = open("p054_poker.txt", "r")
pokerHands = file.read()
file.close()
pokerHands = pokerHands.split("\n")
for i in pokerHands:
    winner = whoWins(i)
    if winner == "player1":
        player1 += 1
    elif winner == "player2":
        player2 += 1
    elif winner == "tie":
        tie += 1

print("player1: {}, player2: {}, tie: {}".format(player1, player2, tie))
