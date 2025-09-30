from __future__ import annotations
import hashlib
import hmac
import time
import random
from typing import List
from secret import flag

LIE_BASE = 0.58
MAX_ATTEMPTS = len(flag) * 100
HINT_FREQ = 0.003
SUSPICION_PENALTY = 0.25
LENGTH_BIAS_SCALE = 0.5
TIME_NOISE_MAX = 0.002


class Challenge:
    def __init__(self, flag: str) -> None:
        self.flag = flag
        self.attempts = MAX_ATTEMPTS

        seed_material = hashlib.sha256(
            flag.encode("utf-8") + b"::dishonest_oracle::"
        ).digest()
        self.rng = random.Random()
        self.hmac_key = hashlib.sha256(seed_material + b"::hmac_key::").digest()
        self.history: List[str] = []
        self.prefix_counts = {}
        self.truth_window_ticks = 0

    def _update_history(self, guess: str) -> None:
        self.history.append(guess)
        if len(self.history) > 5000:
            self.history.pop(0)

        for l in range(1, min(len(guess), len(self.flag)) + 1):
            p = guess[:l]
            self.prefix_counts[p] = self.prefix_counts.get(p, 0) + 1

    def _suspicion_score(self, guess: str) -> float:
        base = 0.0
        same_guess_count = sum(1 for g in self.history[-200:] if g == guess)
        if same_guess_count > 3:
            base += min(0.6, 0.12 * (same_guess_count - 2))

        pref_count = 0
        for l in range(1, min(len(guess), len(self.flag)) + 1):
            p = guess[:l]
            pref_count = max(pref_count, self.prefix_counts.get(p, 0))
        if pref_count > 10:
            base += 0.15

        length_ratio = len(guess) / max(1, len(self.flag))
        if length_ratio < 0.25:
            base += 0.2 * (0.25 - length_ratio) / 0.25

        return max(0.0, min(1.0, base))

    def _length_bias(self, guess: str) -> float:
        r = len(guess) / max(1, len(self.flag))
        return (r - 0.5) * LENGTH_BIAS_SCALE

    def _should_lie(self, guess: str) -> bool:
        lie_p = LIE_BASE
        lie_p += -self._length_bias(guess)
        suspicion = self._suspicion_score(guess)
        lie_p += suspicion * SUSPICION_PENALTY

        lie_p += (self.rng.random() - 0.5) * 0.12

        if lie_p < 0.02:
            lie_p = 0.02
        if lie_p > 0.98:
            lie_p = 0.98

        if self.truth_window_ticks > 0:
            self.truth_window_ticks -= 1
            return False

        if self.rng.random() < 0.3 and len(guess) > 0.4 * len(self.flag):
            self.truth_window_ticks = self.rng.randint(6, 7)
            return False

        return self.rng.random() < lie_p

    def _maybe_emit_hint(self, guess: str) -> None:
        if self.rng.random() < HINT_FREQ:
            mac = hmac.new(
                self.hmac_key, guess.encode("utf-8"), hashlib.sha256
            ).hexdigest()
            hint = mac[:10]
            print(f"oracle hums: {hint}")

    def check(self, guess: str) -> bool:
        self._update_history(guess)

        # no timing attack over here :^)
        time.sleep(self.rng.random() * TIME_NOISE_MAX)
        honest = self.flag.startswith(guess)
        should_lie = self._should_lie(guess)
        self._maybe_emit_hint(guess)
        if should_lie:
            return not honest
        return honest


def main():
    challenge = Challenge(flag)
    print("Dishonest Oracle online. Ask nicely — but don't trust everything you hear.")
    print(
        "Tip: the oracle is stateful and adaptive. Repeating the same probe will often backfire!"
    )
    print(f"You have {MAX_ATTEMPTS} attempts. Use them wisely.")

    while True:
        challenge.attempts -= 1
        if challenge.attempts <= 0:
            print("Don't overstay your welcome!")
            break

        try:
            guess = input("> ").strip()
        except EOFError:
            print()
            break

        if len(guess) == 0:
            print("The oracle does not accept empty supplications.")
            continue

        result = challenge.check(guess)
        if result:
            print("Maybe you're onto something...")
        else:
            print("Nope, that's not it.")


if __name__ == "__main__":
    main()
