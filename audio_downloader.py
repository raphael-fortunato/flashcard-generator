import pdb
from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import shutil
import unicodedata
from pathlib import Path

url = "https://www.collinsdictionary.com/dictionary/portuguese-english/{}"


def download(url, filename):
    print(f" downloading {filename} .....")
    req = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
    if req.status_code == 200:
        with open(filename, 'wb') as f:
            req.raw.decode_conten = True
            shutil.copyfileobj(req.raw, f)


def get_audio(word, filepath):
    succes = False
    _url = unicodedata.normalize(
        'NFKD', url.format(word.split(' ')[0])).encode('ascii', 'ignore').decode('utf-8')
    req = urllib.request.Request(_url, headers={
        'User-Agent': 'Mozilla/5.0'})
    source = urllib.request.urlopen(req)
    soup = bs(source, 'lxml')

    for lang in soup.find_all('a', attrs={"class": "hwd_sound sound audio_play_button icon-volume-up ptr"}):
        if "European Portuguese" in lang.find_parent().text:
            download(lang.get("data-src-mp3"), filepath)
            succes = True
            break

    if not succes:
        for lang in soup.find_all('a', attrs={"class": "hwd_sound sound audio_play_button icon-volume-up ptr"}):
            if "Portuguese" in lang['title']:
                download(lang.get("data-src-mp3"), filepath)
                succes = True
                break
    if not succes:
        lang = soup.find_all(
            'a', attrs={"class": "hwd_sound sound audio_play_button icon-volume-up ptr"})
        if len(lang) == 1:
            download(lang[0].get("data-src-mp3"), filepath)
            succes = True
    if not succes:
        Path(filepath).touch()

