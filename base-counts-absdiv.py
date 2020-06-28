import gzip
import json
import sys

def kl_divergence(xs, ys):
    xt = float(sum(xs.values()))
    yt = float(sum(ys.values()))
    d = 0.0
    for (yk, yc) in ys.items():
        xc = xs[yk]
        xp = float(xc)/xt
        yp = float(yc)/yt
        d += yp * math.log(yp/xp)
    return d

def smart_open(fn):
    if fn.endswith(".gz"):
        return gzip.open(fn)
    return open(fn)

def read_counts(fn):
    with smart_open(fn) as f:
        for l in f:
            yield json.loads(l)
    yield None

def sqr(x):
    return x*x

def merge(xs, ys):
    x = xs.__next__()
    y = ys.__next__()

    while x is not None and y is not None:
        if x[0] != y[0]:
            # Hit chromosome boundary.
            # Whichever has the greater position was the
            # end of the previous chromosome, so comes first!
            if x[1] > y[1]:
                yield [x[0], x[1], sum([sqr(v) for v in x[2].values()]), sum(x[2].values()), 0]
                x = xs.__next__()
            else:
                yield [y[0], y[1], sum([sqr(v) for v in y[2].values()]), 0, sum(y[2].values())]
                y = ys.__next__()
            continue

        # Ok, both x and y are on the same chromosome.
        if x[1] < y[1]:
            yield [x[0], x[1], sum([sqr(v) for v in x[2].values()]), sum(x[2].values()), 0]
            x = xs.__next__()
            continue

        if x[1] > y[1]:
            yield [y[0], y[1], sum([sqr(v) for v in y[2].values()]), 0, sum(y[2].values())]
            y = ys.__next__()
            continue

        # Ok, both x and y are the same locus, so actually merge.
        yield [x[0], x[1], sum([sqr(x[2].get(k, 0) - y[2].get(k, 0)) for k in set(x[2].keys()) | set(y[2].keys())]), sum(x[2].values()), sum(y[2].values())]
        x = xs.__next__()
        y = ys.__next__()

    while x is not None:
        yield x
        x = xs.__next__()

    while y is not None:
        yield y
        y = ys.__next__()

for v in merge(read_counts(sys.argv[1]), read_counts(sys.argv[2])):
    #json.dump(v, sys.stdout)
    #print(file=sys.stdout)
    print('\t'.join(map(str, v)))

