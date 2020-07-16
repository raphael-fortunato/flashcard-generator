import genanki
import os
import sys
import random
import cv2
import numpy as np
import pandas as pd
import shutil
from flashcard import phrase_model
from google_speech import Speech
from multiprocessing import Process
import time

X = -1
Y = -1


def string_path(searchterms):
    return os.path.join('dataset', ','.join(searchterms))


def longest_words(sentence):
    one, two, three = ' ', ' ', ' '
    for word in sentence.split(' '):
        if len(word) >= len(three):
            if len(word) >= len(two):
                if len(word) >= len(one):
                    three = two
                    two = one
                    one = word
                    continue
                else:
                    three = two
                    two = word
                    continue
        else:
            three = word
    return [one, two, three]


def Select_image(event, x, y, flags, param):
    global X, Y
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if(x > 0 and x < 1000 and y > 0 and y < 1000):
            X = int(x*5 / 1000)
            Y = int(y*5 / 1000)
            print(X, Y)


def search(searchterms, save_dir):
    os.system(f"./bbid.py -s \"{searchterms}\" -o \"{save_dir}\" --limit 25")


def SearchImage(sentence, word):
    searchterms = longest_words(sentence)
    global X, Y
    p1 = Process(target=search, args=(searchterms, word))
    p2 = Process(target=search, args=(sentence, word))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    canvas = np.zeros((1000, 1000, 3), dtype=np.uint8)
    images = os.listdir(word)

    for x in range(5):
        for y in range(5):
            try:
                image = cv2.imread(os.path.join(word, images[x * 5 + y]))
                image = cv2.resize(image, (200, 200))
                canvas[y*200:y*200 + 200, x * 200:x * 200 + 200, :] = image
            except Exception as e:
                print(e)
    cv2.namedWindow(' '.join(sentence))
    cv2.setMouseCallback(' '.join(sentence), Select_image)
    while True:
        cv2.imshow(' '.join(sentence), canvas)
        k = cv2.waitKey()
        if k == 27:
            return None
        if X != -1 and Y != -1 and k == ord(' '):
            if not os.path.isdir("selected_images"):
                os.makedirs("selected_images")
            selected = os.path.join("selected_images", f"{word}.jpg")
            os.rename(os.path.join(word, images[X * 5 + Y]), selected)
            X = -1
            Y = -1
            shutil.rmtree(word)
            cv2.destroyAllWindows()
            return selected


def phrasecard(filename, deck):
    deck = genanki.Deck(2059400110, 'Portuguese Frequency Dictionary')

    if not os.path.isdir('audio'):
        os.makedirs('audio')
    notes = []

    df = pd.read_csv("frequency_dict.csv")
    audio = []
    images = []
    delete_idx = []
    for index, row in df.iterrows():
        path = SearchImage(row['translation'].strip(),
                           row['word'].split(',')[0])
        if path is None:
            break
        speech = Speech(row['sentence'], "pt")
        audio_path = os.path.join('audio', f"{row['word'].split(',')[0]}.mp3")
        speech.save(audio_path)
        audio.append(audio_path)
        images.append(path)
        note = genanki.Note(
            model=my_model,
            fields=[row['sentence without word'],
                    row['word'],
                    row['part of speech'],
                    f'<img src="{row["word"]}.jpg">',
                    f'[sound:{os.path.abspath(audio_path)}]',
                    row['sentence']])
        notes.append(note)
        delete_idx.append(index)

    for n in notes:
        deck.add_note(n)
    df = df.drop(df.index[delete_idx])
    df.to_csv("frequency_dict.csv")

    my_package = genanki.Package(deck)
    media = [os.path.abspath(img) for img in images if img is not None]
    media.extend([os.path.abspath(aud) for aud in audio if aud is not None])
    my_package.media_files = media

    my_package.write_to_file(f'{time.time()}.apkg')
