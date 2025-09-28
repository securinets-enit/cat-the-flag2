from Crypto.Util.number import bytes_to_long, getPrime
from json import dump
from secret import flag

p, q = getPrime(512), getPrime(512)
n = p * q
e = 65537
d = pow(e, -1, (p - 1) * (q - 1))
h = (p >> 128) << 128
m = bytes_to_long(flag.encode())
c = pow(m, e, n)
with open("output.json", "w") as f:
    dump({"n": n, "e": e, "c": c, "h": h}, f)