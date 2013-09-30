import itertools as its
import string

def alphabetCycle(alphabetCase,countNumber):

    if alphabetCase == 'lower':
        alphabetList = list(string.ascii_lowercase)
    else:
        alphabetList = list(string.ascii_uppercase)

    returnList = []
    alphabetIts = its.cycle(alphabetList)

    for y,x in enumerate(alphabetIts):
        returnList.append(x)
        if y == countNumber:
            break

    return returnList

print alphabetCycle('lower',35)
