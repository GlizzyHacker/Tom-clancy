import random
import csv

init = False

words = []

finishers = []

def init_insult():
    global init

    random.seed()
    with open('words.csv', newline='',encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if init:
                words.append(row[0])
                if row[1]:
                    finishers.append(row[1])   
            init = True
    print(", ".join(words))
    print(", ".join(finishers))

def generate_insult(length, sucki:bool=False):
    """
    Generates a gaydacsi-style insult with given length.
    :param length: length of insult
    :param sucki: True if target is gaydacsi, False otherwise
    """
    global init
    global words
    global finishers
    
    if not init:
        init_insult()
    length = max(1,min(length,len(words)))
    result = set()
    if sucki:
        if random.random() < 0.05:
            result.add("sucki")
    while len(result) < length:
        result.add(words[random.randrange(0, len(words))])

    return " ".join(result) + " " + finishers[random.randrange(0, len(finishers))]


if __name__ == "__main__":
    init_insult()