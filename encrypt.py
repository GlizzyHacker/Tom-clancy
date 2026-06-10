
import os

from dotenv import load_dotenv


load_dotenv()

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

encrypt_hash = int(ENCRYPTION_KEY)

#Implements a very simple caesar cipher that depends on the length of the word
def encrypt(word: str):
    cipher = ""
    for char in word:
        cipher += chr(((ord(char) + encrypt_hash * len(word) - 33) % 96) + 33)
    return cipher

def decrypt(cipher: str):
    word = ""
    for char in cipher:
        word += chr(((ord(char) - encrypt_hash * len(cipher) - 33) % 96) + 33)
    return word

if __name__ == "__main__":
    while True:
        word = input()
        print(encrypt(word))
        print(decrypt(encrypt(word)))