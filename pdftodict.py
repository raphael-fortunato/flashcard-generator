from collections import OrderedDict
import re
import pandas as pd
import numpy as np
import Levenshtein


abbreviations = {'aj': 'adjective', 'av': 'adverb', 'at': 'article', 'cj': 'conjunction', 'nc': 'noun - common', 'nf': 'noun feminine', 'nm': 'noun masculine',
                 'n': 'noun', 'nmf': 'noun - mas or fem', 'num': 'number', 'obj': 'object', 'pl': 'plural', 'prp': 'preposition', 'pn': 'pronoun', 'v': 'verb'}


def read_dict():
    data = []
    with open('frequency_dict.txt', 'r') as file:
        text = file.readlines()

    for index, word in enumerate(text):
        if word[0] == chr(8226):
            succes = False
            lookforward = 2
            lookback = 1
            row = {}
            while not succes:
                try:
                    target_word = text[index - lookback].split(' ')[1]
                    part_of_speech = text[index - lookback].split(' ')[2]
                    succes = True
                except Exception as e:
                    lookback += 1

            target_sentence = word + " " + text[index + 1]
            while True:
                if chr(124) in target_sentence:
                    target_sentence = target_sentence.replace(
                        '\n', ' ').strip()
                    target_sentence = target_sentence[:target_sentence.find(
                        chr(124))]
                    target_sentence = target_sentence[1:]
                    portuguese = target_sentence[:target_sentence.find(
                        " – ")]
                    english = target_sentence[target_sentence.find(" – ") + 3:]
                    for char in reversed(range(len(english))):
                        if english[char] == '.' or english[char] == '?' or english[char] == '!':
                            english = english[:char+1]
                            break
                    english = english.replace('\n', ' ')
                    break
                elif "\n \n" in target_sentence:
                    target_sentence = target_sentence.replace('\n', '')
                    target_sentence = target_sentence[1:]
                    target_sentence = target_sentence.strip()
                    portuguese = target_sentence[:target_sentence.find(" – ")]
                    english = target_sentence[target_sentence.find(" – ") + 3:]
                    break
                else:
                    target_sentence = target_sentence + \
                        " " + text[index + lookforward]
                    lookforward += 1

            row['word'] = target_word
            row['sentence'] = portuguese
            row['translation'] = english
            row['part of speech'] = part_of_speech
            data.append(row)

    df = pd.DataFrame(data)
    for key in abbreviations.keys():
        df['part of speech'] = df['part of speech'].replace(
            key, abbreviations[key])
    sentence_without = []
    for index, row in df.iterrows():
        if '/' in row['part of speech']:
            try:
                part_of_speech = row['part of speech'].split('/')
                part_of_speech = [abbreviations[word]
                                  for word in part_of_speech]
                row['part of speech'] = '/'.join(part_of_speech)
            except:
                import pdb
                pdb.set_trace()
        # edge cases
        if row['word'] == 'ser':
            sentence_without.append(row['sentence'].replace('é', ' __ '))
            row['word'] = f"é, ({row['word']})"
            continue
        if row['word'] == 'ter':
            sentence_without.append(row['sentence'].replace('teve', ' __ '))
            row['word'] = f"teve, ({row['word']})"
            continue
        row['sentence'] = row['sentence'].replace(',', ' ,')
        row['sentence'] = row['sentence'].replace('-', ' -')
        sentence_without.append(row['sentence'].replace(
            ' '+row['word'] + ' ', ' __ '))
        if not '__' in sentence_without[-1]:
            sentence_without[-1] = sentence_without[-1].strip()
            sentence_split = sentence_without[-1].split(' ')
            distances = [Levenshtein.distance(
                w, row['word']) for w in sentence_split]
            index = np.argmin(distances)
            sentence_without[-1] = sentence_without[-1].replace(
                sentence_split[index], ' __ ')
            row['word'] = f"{sentence_split[index]}, ({row['word']})"
    df['sentence without word'] = sentence_without
    df.to_csv('frequency_dict.csv')


read_dict()
