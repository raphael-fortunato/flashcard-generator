import argparse
import subprocess
from card_creator import create_cards
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wordcard", action='store_true',
                        help='add if you want to create wordscards based on the 635 list', required=False)
    parser.add_argument("--verbcard", action='store_true',
                        help='add if you want to create verbcards', required=False)
    parser.add_argument('--phrasecard', action='store_true',
                        help='add if you want to create phrasecards', required=False)
    parser.add_argument('--csv', type=str,
                        help='file to retrieve data from', required=True)
    parser.add_argument("--deck", type=str,
                        help='name of the anki deck', required=True)

    args = parser.parse_args()

    if args.wordcard:
        file = create_cards('wordcards', args.csv, args.deck)
        subprocess.call(['xdg-open', file])
    elif args.phrasecard:
        file = create_cards('phrasecards', args.csv, args.deck)
        subprocess.call(['xdg-open', file])
    elif args.verbcard:
        file = create_cards('verbcards', args.csv, args.deck)
        subprocess.call(['xdg-open', file])


"""
TODO:
    1. merge phrasecard and wordcard
    2. create verbcard
"""
