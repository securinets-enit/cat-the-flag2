from Crypto.Util.number import bytes_to_long, getPrime
from json import dump
from secret import flag

p, q = getPrime(128), getPrime(128)
n = p * q
e = 65537
d = pow(e, -1, (p - 1) * (q - 1))
m = bytes_to_long(flag.encode())
c = pow(m, e, n)
with open("output.json", "w") as f:
    dump({"n": n, "e": e, "c": c}, f)
