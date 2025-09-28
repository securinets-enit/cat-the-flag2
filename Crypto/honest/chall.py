from secret import flag

class Challenge:
    def __init__(self, flag: str) -> None:
        self.flag = flag

    def check(self, guess: str) -> bool:
        return self.flag.startswith(guess)
    

def main():
    challenge = Challenge(flag)
    print("Honesty is the best policy!")
    print("I'll help you if you ask nicely.")
    while True:
        guess = input("> ").strip()
        if challenge.check(guess):
            print("Maybe you're onto something...")
        else:
            print("Nope, that's not it.")

if __name__ == "__main__":
    main()