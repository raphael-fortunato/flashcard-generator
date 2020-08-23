import argparse
import subprocess
from wordcards import wordcard
from phrasecards import phrasecard


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wordcard", action='store_true',
                        help='add if you want to create wordscards based on the 635 list', required=False)
    parser.add_argument('--phrasecard', action='store_true',
                        help='add if you want to create phrasecards', required=False)
    parser.add_argument('--csv', type=str,
                        help='file to retrieve data from', required=True)
    parser.add_argument("--deck", type=str,
                        help='name of the anki deck', required=True)

    args = parser.parse_args()

    if args.wordcard and args.phrasecard:
        raise ValueError('Can\'t create 2 sorts cards at the same time')

    if args.wordcard:
        file = wordcard(args.csv, args.deck)
        subprocess.call(['xdg-open', file])
    elif args.phrasecard:
        file = phrasecard(args.csv, args.deck)
        subprocess.call(['xdg-open', file])

"""
TODO:
    1. merge phrasecard and wordcard
    2. create verbcard
    3. improve image search

"""
