import gzip
import sys
import json

def smart_open(fn):
    if fn.endswith(".gz"):
        return gzip.open(fn)
    return open(fn)

def read_counts(fn):
    with smart_open(fn) as f:
        for l in f:
            yield json.loads(l)
    yield None

def merge(xs, ys):
    x = xs.__next__()
    y = ys.__next__()

    while x is not None and y is not None:
        if x[0] != y[0]:
            # Hit chromosome boundary.
            # Whichever has the greater position was the
            # end of the previous chromosome, so comes first!
            if x[1] > y[1]:
                yield x
                x = xs.__next__()
            else:
                yield y
                y = ys.__next__()
            continue

        # Ok, both x and y are on the same chromosome.
        if x[1] < y[1]:
            yield x
            x = xs.__next__()
            continue

        if x[1] > y[1]:
            yield y
            y = ys.__next__()
            continue

        # Ok, both x and y are the same locus, so actually merge.
        for (yk, yc) in y[2].items():
            x[2][yk] = yc + x[2].get(yk, 0)
        yield x
        x = xs.__next__()
        y = ys.__next__()

    while x is not None:
        yield x
        x = xs.__next__()

    while y is not None:
        yield y
        y = ys.__next__()

if len(sys.argv[1:]) == 0:
    sys.exit()

streams = [read_counts(arg) for arg in sys.argv[1:]]
while len(streams) > 1:
    tmp = []
    i = 0
    while i + 1 < len(streams):
        x = merge(streams[i], streams[i+1])
        tmp.append(x)
        i += 2
    if i < len(streams):
        tmp.append(streams[i])
    # Flip the order to improve balance.
    streams = tmp[::-1]

for x in streams[0]:
    json.dump(x, sys.stdout)
    print(file=sys.stdout)
