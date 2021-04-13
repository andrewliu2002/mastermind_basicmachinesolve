import random;
global_numberlist = [1,2,3,4,5,6]

def listCreator():
    finishList = []
    while len(finishList)<4:
        digit = random.choice(range(1,6))
        if digit not in finishList:
            finishList.append(digit)
    return finishList

def firstListChecker(finalCode, guessCode):
    breaktemp = []
    for i in range(4):
        if( finalCode[i] == guessCode[i]):
            breaktemp.append(guessCode[i])
            global_numberlist.remove(guessCode[i])         #removes numbers from global number list b/c it is correct
        elif guessCode[i] in finalCode and guessCode[i]:
            breaktemp.append("B")
        elif guessCode[i] not in finalCode:
            breaktemp.append("C")                       #removes numbers from global number list b/c it is completely wrong
            global_numberlist.remove(guessCode[i])
    return breaktemp     

def secondListChecker(finalCode, guessCode):
    breaktemp = []
    for i in range(4):
        if( finalCode[i] == guessCode[i]):
            breaktemp.append(guessCode[i])              #removes numbers from global number list b/c it is correct
        elif(guessCode[i] == "C"):
            breaktemp.append(guessCode[i])
        elif((guessCode[i] not in finalCode) and (guessCode[i] != "B")):
            breaktemp.append("C")                       #removes numbers from global number list b/c it is completely wrong
            global_numberlist.remove(guessCode[i])
        else:
            breaktemp.append("B")
    print("Here is the the response: " + str(breaktemp))
    return breaktemp     

def newReplaceBreaker(masterCode):
    for i in range(4):
        if(masterCode[i] == "B" or masterCode[i] == "C"):
            masterCode[i] = random.choice(global_numberlist)
            break
    print("Here is the updated machine guess: " + str(masterCode))
    return masterCode


def main():
    finalCode = listCreator()
    machineGuess = listCreator()        # creates two random lists
    guess_count = 0
    print("Here is the code that the machine needs to find: " + str(finalCode))
    print("Here is the code that the machine initially guessed: " + str(machineGuess))
    print("")
    print("And now here is the process !")
    print("")
    if(machineGuess == finalCode):
        print("Machine got it on first try! ")
        print("Here is the guess count: 0")
        exit()
    masterCode = firstListChecker(finalCode,machineGuess)
    guess_count = guess_count + 1
    while(masterCode != finalCode):
        masterCode = secondListChecker(finalCode,masterCode)
        masterCode = newReplaceBreaker(masterCode)
        guess_count = guess_count + 1
        print("")
    print("Here is the final code: " + str(masterCode))
    print("Congrats, if you made it here, the computer just solved it for you! ")
    print("Here is the guess count: " + str(guess_count))
                
main()