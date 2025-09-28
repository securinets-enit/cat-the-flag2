from secret import flag
from random import random

class Challenge:
    def __init__(self, flag: str) -> None:
        self.flag = flag
        self.attempts = 15_000


    def check(self, guess: str) -> bool:
        return self.flag.startswith(guess) or random() < 0.5
    

def main():
    challenge = Challenge(flag)
    print("Honesty is the best policy!")
    print("I'll help you if you ask nicely.")
    while True:
        challenge.attempts -= 1
        if challenge.attempts <= 0:
            print("Don't overstay your welcome!")
            break
        guess = input("> ").strip()
        if challenge.check(guess):
            print("Maybe you're onto something...")
        else:
            print("Nope, that's not it.")

if __name__ == "__main__":
    main()