import time
from multiprocessing import Process
from google_speech import Speech
import genanki
import os
import sys
import random
import cv2
import numpy as np
import pandas as pd
import shutil
from flashcard import word_model
from audio_downloader import get_audio

X = -1
Y = -1


def string_path(searchterms):
    return os.path.join('dataset', ','.join(searchterms))


def Select_image(event, x, y, flags, param):
    global X, Y
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if(x > 0 and x < 1000 and y > 0 and y < 1000):
            X = int(x*5 / 1000)
            Y = int(y*5 / 1000)
            print(X, Y)


def search(searchterms, save_dir):
    os.system(f"./bbid.py -s \"{searchterms}\" -o \"{save_dir}\" --limit 20")


def exists(file):
    if os.path.isfile(file):
        return file
    else:
        return None


def SearchImage(word, translation):
    global X, Y
    p1 = Process(target=search, args=(translation, word))
    p2 = Process(target=search, args=(word, word))
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
    cv2.namedWindow(translation)
    cv2.setMouseCallback(translation, Select_image)
    while True:
        cv2.imshow(translation, canvas)
        k = cv2.waitKey()
        if k == 27:
            return None
        if X != -1 and Y != -1 and k == ord(' '):
            if not os.path.isdir("selected_images"):
                os.makedirs("selected_images")
            selected = os.path.join(
                "selected_images", f"{word}.jpg")
            image = cv2.imread(os.path.join(word, images[X * 5 + Y]))
            if image.shape[0] > 512 or image.shape[1] > 512:
                shape = image.shape
                if shape[0] <= shape[1]:
                    image = cv2.resize(
                        image, (int((shape[0]/shape[1]) * 512), 512))
                else:
                    image = cv2.resize(
                        image, (512, int((shape[1]/shape[0]) * 512)))
                cv2.imwrite(selected, image)
            X = -1
            Y = -1
            shutil.rmtree(word)
            cv2.destroyAllWindows()
            return selected


def wordcard(filename, deck):
    deck = genanki.Deck(random.randint(1 << 30, 1 << 31), deck)

    if not os.path.isdir('audio'):
        os.makedirs('audio')
    notes = []

    df = pd.read_csv(filename)
    audio = []
    images = []
    delete_idx = []
    for index, row in df.iterrows():
        path = SearchImage(row['word'], row['translation'])
        if path is None:
            break
        images.append(path)

    for index, row in df.iterrows():
        if index >= len(images):
            break
        audio_path = os.path.join(
            'audio', f"{row['word']}.mp3")
        get_audio(row["word"], audio_path)
        audio.append(audio_path)
        if row['info'] == 'f. noun':
            word = f"a {row['word']}"
        elif row['info'] == 'm. noun':
            word = f"o {row['word']}"
        elif row['info'] == 'f. pl. noun':
            word = f"as {row['word']}"
        elif row['info'] == 'm. pl. noun':
            word = f"os {row['word']}"
        else:
            word = row['word']
        note = genanki.Note(
            model=word_model,
            fields=[word,
                    row['info'],
                    f'<img src="{images[index].split("/")[-1]}">',
                    f'[sound:{os.path.abspath(audio_path)}]'])
        notes.append(note)
        delete_idx.append(index)

    for n in notes:
        deck.add_note(n)

    my_package = genanki.Package(deck)
    media = [os.path.abspath(img) for img in images if exists(img) is not None]
    media.extend([os.path.abspath(aud) for aud in audio if aud is not None])
    my_package.media_files = media
    file = f'{time.time()}.apkg'
    my_package.write_to_file(file)

    df = df.drop(df.index[delete_idx])
    df.to_csv(filename)

    return file
