import xml.etree.ElementTree as ET
import datetime
import os
import sys
from fleiss import fleiss


def main(usernames: list[str], state: str, dataset: int):
    """ Calculates kappa value for annotations by users in username list,
    calculated from the XML-files in the relevant 'annotated_tweets' folder for
    that user."""

    # Initialize variables
    tweet_ids = os.listdir(f"../dataset/{dataset}/{state}")
    current_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # Create directories if missing
    if not os.path.exists("kappa_results"):
        os.mkdir("kappa_results")
    assert not os.path.exists("kappa_results/{current_date}")

    # Iterate over each tweet for each user, add to export dictionary (each key
    # in dict corresponds to one tweet and line in export file)
    export = {x: [] for x in tweet_ids}
    for user in usernames:
        user_dir = f"../annotated_tweets/{state}/{user}"
        if not os.path.exists(user_dir):
            print(f"ERROR: {user} has no annotated tweets for state {state}")
            sys.exit(2)
        if len(os.listdir(user_dir)) != len(export):
            print(f"ERROR: Annotation mismatch length for {user}")
            sys.exit(3)
        for i in tweet_ids:
            root = ET.parse(f"{user_dir}/{i}").getroot()
            export[i].append(root.get("annotation"))

    # Write each tweet to a line, separated by tabs
    with (open(f"kappa_results/{current_date}", 'w') as f,
          open(f"kappa_results/{current_date}_raw", 'w') as raw):
        for i in export:
            f.write("%s\t%s\n" %(i, '\t'.join(export[i])))  # tweet&annotated data
            raw.write("%s\n" %'\t'.join(export[i]))  # solely annotated data

    # Calculate kappa value for exported file
    fleiss(f"kappa_results/{current_date}_raw")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERROR: Cannot calculate kappa value for less than 2 users")
        sys.exit(3)
    main(sys.argv[1:], "pilot_two", 20221006121322)
