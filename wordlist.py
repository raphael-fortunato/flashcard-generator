import pdb
from googletrans import Translator
import pandas as pd

words = []

with open("wordlist.txt", 'r') as file:
    text = file.readlines()

portuguese = False
english = False
pt, eng, info = [], [], []
ipa = []
for index, word in enumerate(text):
    trans = Translator()
    if word == 'Speech\n':
        portuguese = True
        continue
    if word == 'Pronunciation\n':
        portuguese = False
        continue
    if text[index - 1] == "English\n" and text[index] == "Translation\n":
        english = True
        continue
    if word == "Notes\n":
        english = False
        continue
    if word == "\n":
        continue
    # if english:
        # if len(eng) == len(ipa):
        # target_word = word.replace("\n", "").strip()
        # ipa.append(target_word)
        # else:
        # target_word = word.replace("\n", "").strip()
        # eng.append(target_word)
        # print(target_word)
    elif portuguese:
        if len(pt) == len(info):
            target_word = word.replace("\n", '').strip()
            pt.append(target_word)
            print(target_word)
            eng.append(trans.translate(target_word).text)
        else:
            target_word = word.replace("\n", "").strip()
            info.append(target_word)
            print(target_word)
pdb.set_trace()

wordlist = dict()
wordlist["word"] = pt
wordlist["translation"] = eng
wordlist["info"] = info

df = pd.DataFrame(data=wordlist)
df.to_csv("625_wordlist.csv")
