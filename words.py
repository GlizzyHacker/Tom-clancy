import random
import csv

init = False

words = []
finishers = []
asked_responses = []
not_asked_responses = []

def init_words():
    global init

    random.seed()
    with open('words.csv', newline='',encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if init:
                words.append(row[0])
                if row[1]:
                    finishers.append(row[1])
                if row[5]:
                    asked_responses.append(row[5])
                if row[6]:
                    not_asked_responses.append(row[6])
            init = True
    print("insults: " + " ".join(words))
    print("finishers: ", "".join(finishers))
    print("asked: " + " ".join(asked_responses))
    print("not_asked: " + " ".join(not_asked_responses))

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
        init_words()
    length = max(1,min(length,len(words)))
    result = set()
    if sucki:
        if random.random() < 0.05:
            result.add("sucki")
    while len(result) < length:
        result.add(words[random.randrange(0, len(words))])

    return " ".join(result) + " " + finishers[random.randrange(0, len(finishers))]

def generate_response(asked: bool):
    if not init:
        init_words()
    if asked:
        return random.choice(asked_responses)
    else:
        return random.choice(not_asked_responses)

if __name__ == "__main__" or __name__ == "words":
    init_words()