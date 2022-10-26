> Created for the course LIN354

# Text classification annotation UI for scraped tweets

This is a website implemented using `flask` to annotate tweets extracted using
`snscrape` for text classification tasks. It was built with dogwhistle
classification in mind (and still contains hardcoded elements of it), meaning
that it works by providing a list of expressions that will be used to extract
tweets containing those expressions, and the annotation will be classifying
those tweets according to number of set categories. In the scope of this task
that included whether the tweet was a dogwhistle or not.

Support for different users exists, however, not with passwords. In regards to
the complexity of this task I just didn't see the need for it. It supports
either user-by-user annotation (when each user has their seperate batch of
tweets) or coannotation (e.g. pilot annotation, when we want to
measure kappa value).

## Usage

This was not meant to be used for anything other than the dogwhistle project in
question, but adapting it to other classification tasks for tweets would be
trivial:

1. Gather data using `tweet_extractor.py`.
2. Edit `guidelines.md` to suit your needs
3. Edit template files and `app.py` to fit task at hand (i.e. edit button
   names, output labels, title for web page etc).
3. Set up webserver as you would any other flask application
4. [Use `generate_pilot_dataset.py` script to generate pilot annotation
   dataset, and then set according values in `app.py`]
5. Generate user dataset from the data gathered in (1) by using the
   `generate_user_dataset.py` in scripts folder

## Scripts

The scripts folder contains python/shell scripts for certain tasks you might
find useful:

- `calculate_kappa.py`: calculates kappa value for annotators (useful for pilot
  annotation)
- `print_xml.py`: prints tweet id as well as tweet content for a folder of
  xml-files generated through `tweet_extractor.py`
- `disagreeances.sh`: prints tweets where annotators disagreed (useful for
  pilot annotation)
- `get_csv.py`: generates csv for end result in pandas-friendly fashion (for
  ease-of-use later on)
