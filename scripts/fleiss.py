import sys
from collections import Counter


# Adapted from `fleiss.py` from lab2 in LIN354 at Stockholm University,
# in order for it to use a function call instead of CLI
def fleiss(filename: str):
    if type(filename) != str:
        print('%s: ERROR: invalid datatype, str requested' % filename,
              file=sys.stderr)
        sys.exit(1)

    with open(filename) as f:
        data = f.readlines()

    data = [line.split() for line in data]
    set_len = {len(fields) for fields in data}
    n = list(set_len)[0]

    data_counts = [Counter(tags) for tags in data]
    Pis = [sum(nij*(nij-1) for nij in counts.values()) / (n*(n-1))
           for counts in data_counts]

    tag_counts = Counter(tag for tags in data for tag in tags)
    N = sum(tag_counts.values())
    pjs = [nj/N for nj in tag_counts.values()]

    Pe = sum(pj*pj for pj in pjs)
    P = sum(Pis) / len(Pis)

    print('Tag distribution:')
    for tag, n in sorted(tag_counts.items(), key=lambda t: (-t[1], t[0])):
        print('%6d  %s' % (n, tag))
    print('-'*72)
    print("P = %.3g   Pe = %.3g  Fleiss' kappa = %.3g" % (P, Pe, (P-Pe) / (1-Pe)))
