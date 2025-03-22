import random
import csv

init = False

words = [
    # "dummy",
    # "fucker",
    # "cunt",
    # "cuntfucker",
    # "asshole",
    # "sniveling",
    # "sniveling pussy",
    # "eueueue",
    # "dumbfuck",
    # "twat",
    # "bitch",
    # "fuck",
    # "pussy",
    # "thrower",
    # "ewwwww",
    # "gecii",
    # "kurva szádat",
    # "fhuu",
    # "gechi",
    # "szopo",
    # "fasz",
    # "asked",
    # "ass",
]

finishers = []

def initInsult():
    global init

    random.seed()
    with open('words.csv', newline='',encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if (init):
                words.append(row[0])
                if (row[1]):
                    finishers.append(row[1])   
            init = True
    print((", ").join(words))
    print((", ").join(finishers))

def generateInsult(length):
    global init
    global words
    global finishers
    
    if (not init):
        initInsult()
    length = max(1,min(length,len(words)))
    result = set()
    while len(result) < length:
        result.add(words[random.randrange(0, len(words))])

    return " ".join(result) + " " + finishers[random.randrange(0, len(finishers))]


if __name__ == "__main__":
    initInsult()