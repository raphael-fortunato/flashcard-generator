import time
from google_speech import Speech
import gtts
import genanki
import os
import sys
import random
import cv2
import time
import numpy as np
import pandas as pd
import shutil
from flashcard import word_model, phrase_model, verb_model
from audio_downloader import get_audio
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import urllib
import requests
import linecache

site = 'https://www.google.pt/search?tbm=isch&q='
urlopenheader = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}


def exists(file):
    if os.path.isfile(file):
        return file
    else:
        return None


def ispresent(driver):
    try:
        driver.find_element(
            By.XPATH, "/html/body/div[2]/c-wiz/div[4]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img")
        return True
    except:
        return False


def search_image(driver, query, word):
    url = site + query
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        return None
    img = None
    path = os.path.join('selected_images',
                        f'{word}_{random.randint(1 << 30, 1 << 31)}.jpg')
    i = 0
    while True:
        i += 1
        time.sleep(1)
        if ispresent(driver):
            break
        if i > 60:
            driver.close()
            return None
    try:
        img = driver.find_element(
            By.XPATH, "/html/body/div[2]/c-wiz/div[4]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img")
        request = urllib.request.Request(
            img.get_attribute('src'), None, urlopenheader)
        image = urllib.request.urlopen(request).read()
        with open(path, 'wb') as file:
            file.write(image)
    except Exception as e:
        print(e)
        return None
    try:
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
    except Exception as e:
        print(e)
        return None
    return path


def create_cards(card_type, filename, deck):
    deck = genanki.Deck(random.randint(1 << 30, 1 << 31), deck)

    driver = webdriver.Firefox()
    driver.maximize_window()

    if not os.path.isdir('selected_images'):
        os.makedirs('selected_images')
    if not os.path.isdir('audio'):
        os.makedirs('audio')
    notes = []

    df = pd.read_csv(filename)
    audio = []
    images = []
    delete_idx = []
    for index, row in df.iterrows():
        if card_type == 'wordcards':
            path = search_image(
                driver, row['word'].split(',')[0], row['word'].split(',')[0])
        else:
            path = search_image(
                driver, row['sentence'], row['word'].split(',')[0])
        if path is None:
            break
        images.append(path)

    for index, row in df.iterrows():
        if index >= len(images):
            break
        audio_path = os.path.join(
            'audio', f"{row['word'].split(',')[0]}_{random.randint(1 << 30, 1 << 31)}.mp3")
        audio.append(audio_path)
        if card_type == 'wordcards':
            get_audio(row["word"].split(",")[-1], audio_path)
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

        else:
            speech = gtts.gTTS(row['sentence'], lang='pt-pt')
            speech.save(audio_path)
            if card_type == 'phrasecards':
                note = genanki.Note(
                    model=phrase_model,
                    fields=[row['sentence without word'],
                            row['word'],
                            row['info'],
                            f'<img src="{images[index].split("/")[-1]}">',
                            f'[sound:{audio_path.split("/")[-1]}]',
                            row['sentence']])
            elif card_type == 'verbcards':
                note = genanki.Note(
                    model=verb_model,
                    fields=[row['sentence without word'],
                            row['word'],
                            row['info'],
                            f'<img src="{images[index].split("/")[-1]}">',
                            f'[sound:{audio_path.split("/")[-1]}]',
                            row['sentence']])

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
