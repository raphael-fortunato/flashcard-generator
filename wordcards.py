import time
from multiprocessing import Process
from google_speech import Speech
import genanki
import os
import sys
import random
import cv2
import time
import numpy as np
import pandas as pd
import shutil
from flashcard import word_model
from audio_downloader import get_audio
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import urllib.request

site = 'https://www.google.com/search?tbm=isch&q='


def exists(file):
    if os.path.isfile(file):
        return file
    else:
        return None


def ispresent(driver):
    try:
        driver.find_element_by_class_name("n3VNCb")
        return True
    except:
        return False


def search_image(driver, query, word):
    try:
        url = site + query
        driver.get(url)
        img = None
        path = os.path.join('selected_images', f'{word}.jpg')
        i = 0
        while True:
            i += 1
            time.sleep(2)
            if ispresent(driver):
                break
            if i > 30:
                driver.close()
                return None
        img = driver.find_element_by_class_name("n3VNCb")
        urllib.request.urlretrieve(img.get_attribute('src'), path)
        image = cv2.imread(path)
        if image.shape[0] > 512 or image.shape[1] > 512:
            shape = image.shape
            if shape[0] <= shape[1]:
                image = cv2.resize(
                    image, (int((shape[0]/shape[1]) * 512), 512))
            else:
                image = cv2.resize(
                    image, (512, int((shape[1]/shape[0]) * 512)))
            cv2.imwrite(path, image)
        return path
    except:
        return None


def wordcard(filename, deck):
    deck = genanki.Deck(random.randint(1 << 30, 1 << 31), deck)

    driver = webdriver.Firefox()
    driver.maximize_window()

    if not os.path.isdir('audio'):
        os.makedirs('audio')
    notes = []

    df = pd.read_csv(filename)
    audio = []
    images = []
    delete_idx = []
    for index, row in df.iterrows():
        path = search_image(driver, row['translation'], row['word'])
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
                    f'[sound:{audio_path.split("/")[-1]}]'])
        notes.append(note)
        delete_idx.append(index)

    for n in notes:
        deck.add_note(n)

    my_package = genanki.Package(deck)
    media = [os.path.abspath(img) for img in images if exists(img) is not None]
    media.extend([aud for aud in audio if exists(aud) is not None])
    my_package.media_files = media
    file = f'{time.time()}.apkg'
    my_package.write_to_file(file)

    df = df.drop(df.index[delete_idx])
    df.to_csv(filename)

    return file
