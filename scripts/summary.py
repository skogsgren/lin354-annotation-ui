import sys
import pandas as pd


def main(filename):
    """ prints summary of annotation tsv for the proportion of dogwhistles"""
    df = pd.read_csv(filename, sep='\t')
    res = {'word': [], 'dogwhistle_proportion': [], 'number_of_tweets': []}

    for i in df.word.unique():
        h = len(df.loc[(df['word'] == i) & (df['label'] == 1)])
        k = len(df.loc[(df['word'] == i) & (df['label'] == 0)])
        res['word'].append(i)
        res['dogwhistle_proportion'].append(round(h/(h+k), 2))
        res['number_of_tweets'].append(h+k)

    print(pd.DataFrame(res))
    print()
    print(pd.DataFrame(res).to_latex(index=False))


if __name__ == '__main__':
    main(sys.argv[1])
