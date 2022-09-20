import os
import shutil
import threading
import time
from itertools import repeat
from pathlib import Path
from tkinter import filedialog
import multiprocessing as mp
from itertools import repeat
import requests
from bs4 import BeautifulSoup

download_ready_links = []

chapter_name = ''
final_directory = ''

document_path = os.path.expanduser('~\Documents')
image_count = 0



def get_manga_title(Url):
    getURL = requests.get("".join(Url), )  # or Mozilla/5.0 , Chrome/104.0.5112.80
    soup = BeautifulSoup(getURL.text, 'html.parser')

    title = soup.find(class_='tag-title').find('b')
    return title.text


def download_file_from_link(link,dir,chapter_name):
    filename = link.split("/")[-1]
    # downloaded_files_list.append(filename)
    r = requests.get(link, stream=True)
    r.raw.decode_content = True

    print(dir + '/' + "".join(chapter_name) + '/' + filename)
    with open(dir + '/' + "".join(chapter_name) + '/' + filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return 'success'


def get_chapter_image_links(url):
    import re, json, requests
    Dynasty_banner = "https://dynasty-scans.com/"

    r = requests.get(url)
    if r.status_code != 200:
        return
    # extract the data
    match = re.search('var pages = (\[.*?);', r.text).group(1)
    # match = re.search('var pages = (\[.*?\]);', r.text).group(1)

    # parse it into json
    match_json = json.loads(match)

    # iterate through it to get the links
    image_links = [img['image'] for img in match_json]

    for x in range(len(image_links)):
        image_links[x] = Dynasty_banner + image_links[x]

    global image_count
    image_count = len(image_links)
    print(image_links)
    return image_links

def multiprocess_download(dir,chapter_name):
    with mp.Pool() as pool:
        for result in pool.starmap(download_file_from_link, zip(download_ready_links, repeat(dir), repeat(chapter_name)),):
            print(f'Got result: {result}', flush=True)


def multiple_download():
    global url
    print("Link to desired manga: ", )
    # url = str(input())

    url = 'https://dynasty-scans.com/series/liar_satsuki_can_see_death'
    # ask for chapter range
    print("Specify from which to which chapter you want to download: ", )
    print("FROM: ")
    zakres1 = 1  # int(input())

    print("TO: ")
    zakres2 = 13  # int(input())

    zakres2 = zakres2 + 1

    # ask for save directory
    print("Chose Save Directory ? : ", )
    chosen_directory = document_path  # filedialog.askdirectory()

    # create folder with manga title
    global final_directory
    final_directory = os.path.join(chosen_directory, get_manga_title(url))
    print(final_directory)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    url = str(url)
    url = url.replace('series', 'chapters')
    url = url + '_ch'

    global chapter_name
    chapter_name = list('chapter @')

    global download_ready_links
    # name chapters

    for x in range(zakres1, zakres2):
        chapter_name[8] = str(x)

        save_path = os.path.join(final_directory, "".join(chapter_name))
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
        os.makedirs(save_path)

        if x < 10:
            url = url + '0' + str(x)
            download_ready_links = get_chapter_image_links("".join(url))
            multiprocess_download(final_directory,chapter_name)
            url = url[:len(url) - 2]
        if x == 10:
            url = url + str(x)
            download_ready_links = get_chapter_image_links("".join(url))
            multiprocess_download(final_directory,chapter_name)
            url = url[:len(url) - 2]
        if x > 10:
            url = url + str(x)
            download_ready_links = get_chapter_image_links("".join(url))
            multiprocess_download(final_directory,chapter_name)
            url = url[:len(url) - 2]
    print('Download Finished')
