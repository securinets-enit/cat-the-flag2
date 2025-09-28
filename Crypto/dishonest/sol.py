from pwn import process
from typing import List
import hashlib
import hmac
from time import sleep
from string import printable
from collections import Counter
io = process(["python3", "chall.py"])
lenflag = int(io.recvline_contains(b"You have ").strip().split(b" ")[2])//100
print(f"{lenflag}")
io.close()
LIE_BASE = 0.58       
MAX_ATTEMPTS = lenflag * 100  
HINT_FREQ = 0.003    
SUSPICION_PENALTY = 0.25
LENGTH_BIAS_SCALE = 0.5  
TIME_NOISE_MAX = 0.002 
truth_window = False
class Challenge:
    def __init__(self) -> None:
        self.history: List[str] = []
        self.prefix_counts = {}
        self.truth_window_ticks = 0

    def _update_history(self, guess: str) -> None:
        self.history.append(guess)
        if len(self.history) > 5000:
            self.history.pop(0)

        for l in range(1, min(len(guess), lenflag) + 1):
            p = guess[:l]
            self.prefix_counts[p] = self.prefix_counts.get(p, 0) + 1

    def _suspicion_score(self, guess: str) -> float:
        base = 0.0
        same_guess_count = sum(1 for g in self.history[-200:] if g == guess)
        if same_guess_count > 3:
            base += min(0.6, 0.12 * (same_guess_count - 2))

        pref_count = 0
        for l in range(1, min(len(guess), lenflag) + 1):
            p = guess[:l]
            pref_count = max(pref_count, self.prefix_counts.get(p, 0))
        if pref_count > 10:
            base += 0.15

        length_ratio = len(guess) / max(1, lenflag)
        if length_ratio < 0.25:
            base += 0.2 * (0.25 - length_ratio) / 0.25

        return max(0.0, min(1.0, base))

    def _length_bias(self, guess: str) -> float:
        r = len(guess) / max(1, lenflag)
        return (r - 0.5) * LENGTH_BIAS_SCALE

    def _should_lie(self, guess: str) -> float:
        global truth_window
        lie_p = LIE_BASE
        lie_p += -self._length_bias(guess)
        suspicion = self._suspicion_score(guess)
        lie_p += suspicion * SUSPICION_PENALTY

        lie_p += 0

        if lie_p < 0.02:
            lie_p = 0.02
        if lie_p > 0.98:
            lie_p = 0.98

        if len(guess) > 0.4 * lenflag:
            truth_window = True
        
        # lie_p += 0.06
        return lie_p

    def check(self, guess: str) -> float:
        self._update_history(guess)
        return self._should_lie(guess)



def calc_optimal_count(lie_p:float)-> tuple[int,bool]:
    inverted = None
    exp = 1
    if lie_p >= 0.5:
        prob = (1-lie_p)
        inverted = True
    else:
        prob = lie_p
        inverted = False
    while prob >= 0.01:
        exp += 1 
        prob *= prob
    return (exp,inverted)

def is_positive(resp: list) -> bool:
    return "Maybe you're onto something..." in resp

sixtru = [True]*6
sixfals = [False]*6
chall = Challenge()
found = "3vEn_a_Ly1ng_cL0cK_1s"
while True:
    io = process(["python3", "chall.py"])
    if not chall:
        chall = Challenge()
    try:
        for p in printable:
            guess = found+p
            responses = []
            lie_p = chall.check(guess)
            count, inv = calc_optimal_count(lie_p)
            print(f"{count=} | {inv=} | {lie_p} ", end="")
            for i in range(40):
                io.sendline(guess.encode())
                resp = io.recvuntil(b"> ").decode().split("\n")[:-1]
                responses.append(is_positive(resp))
            c = Counter(responses)
            if sixtru in responses:
                print("ACCEPTED BY 6 TRUES")
            if sixfals in responses:
                print("REJECTED BY 6 FALSES")
            conclusion = c.most_common()[0][0]
            print(c.most_common())
            if truth_window:
                truth_window = False
                if conclusion:
                    found += p 
                    print(found)
                    sleep(0.5)
                    break
                else:
                    continue
            if inv ^ conclusion:
                found += p 
                print(found)
                sleep(0.5)
                break
        else:
            print("No valid character found")
            exit(1)
    except EOFError:
        io.close()
        print("Restarting...")
        sleep(1)
        chall = None
        continue

        


