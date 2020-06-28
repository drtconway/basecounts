import sys
import json

def parse_pileup_string(x):
    n = len(x)
    i = 0
    X = {}
    while i < n:
        c = x[i]
        if c in "AaCcGgTt*":
            X[c] = 1 + X.get(c, 0)
            i += 1
            continue

        if c == "^":
            # The character following the caret encodes the mapping quality
            i += 2
            continue

        if c == "$":
            i += 1
            continue

        if c == "+":
            # insertion - scan the digits, store the sequence
            i += 1
            j = 0
            while '0' <= x[i] and x[i] <= '9':
                d = ord(x[i]) - ord('0')
                j = (10 * j) + d
                i += 1
            seq = x[i:i+j]
            c = "+" + seq
            X[c] = 1 + X.get(c, 0)
            i += j
            continue

        if c == "-":
            # insertion - scan the digits, store the length
            i0 = i
            i += 1
            j = 0
            while '0' <= x[i] and x[i] <= '9':
                d = ord(x[i]) - ord('0')
                j = (10 * j) + d
                i += 1
            c = x[i0:i]
            X[c] = 1 + X.get(c, 0)
            i += j
            continue
    return X

for l in sys.stdin:
    t = l.split()
    ch = t[0]
    pos = int(t[1])
    x = parse_pileup_string(t[4])
    json.dump([ch, pos, x], sys.stdout)
    print(file=sys.stdout)
