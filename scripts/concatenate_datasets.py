import pandas as pd
import sys
import os
import datetime


def concatenate_datasets(filenames):
    """ Concatenates datasets in TSV format to one TSV file """
    export = pd.DataFrame({'id': int(), 'text': str(), 'label': int()}, index=[])
    for i in filenames:
        new_df = pd.read_csv(i, sep='\t')
        export = pd.concat([export, new_df], ignore_index=True)
    filename = "%s.tsv" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    assert not os.path.exists(filename)
    export.to_csv(filename, sep='\t')


if __name__ == "__main__":
    concatenate_datasets(sys.argv[1:])
