import os
import shutil
import threading
from pathlib import Path
from tkinter import filedialog

import requests
from bs4 import BeautifulSoup

downloaded_files_list = []
global chapter_name
document_path = os.path.expanduser('~\Documents')
image_count = 0

def get_manga_title(Url):
    getURL = requests.get("".join(Url), )  # or Mozilla/5.0 , Chrome/104.0.5112.80 headers={"User-Agent": "Chrome/104.0.5112.80"}
    soup = BeautifulSoup(getURL.text, 'html.parser')

    title = soup.find(id = 'chapter-title').find('a')
    print(title.text)
    return title.text



def download_file_from_link(link, save_dir=str(Path.home() / "Downloads")):
    filename = link.split("/")[-1]
    # downloaded_files_list.append(filename)
    r = requests.get(link, stream=True)
    r.raw.decode_content = True
    global chapter_name
    with open(save_dir + '/' + "".join(chapter_name) + '/' + filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return


def get_chapter_image_links(url):
    import re, json, requests
    Dynasty_banner = "https://dynasty-scans.com/"

    r = requests.get(url)

    print(url)
    return
    #TODO wywala gdy pobieram rozdział 53  z linku https://dynasty-scans.com/chapters/liar_satsuki_can_see_death_ch04


    # extract the data
    match = re.search('var pages = (\[.*?);', r.text).group(1)
    #match = re.search('var pages = (\[.*?\]);', r.text).group(1)

    # parse it into json
    match_json = json.loads(match)

    # iterate through it to get the links
    image_links = [img['image'] for img in match_json]

    for x in range(len(image_links)):
        image_links[x] = Dynasty_banner + image_links[x]

    global image_count
    image_count = len(image_links)
    return image_links


def dynasty_download(links, save_directory):
    threads = []
    for x in range(len(links)):
        t = threading.Thread(target=download_file_from_link(links[x], save_directory))
        t.daemon = True
        threads.append(t)

    for x in range(len(links)):
        threads[x].start()

    for x in range(len(links)):
        threads[x].join()

def multiple_download():
    global link
    print("Podaj link do rozdziału wybranej mangi: ", )
    link = list(input())
    #print(get_manga_title("".join(link)))

    # format link to delete #01 from end of link if exists
    erase = (''.join(link)).split("#")[-1]

    formatted_link = ''
    if '#' in formatted_link:
        formatted_link = ''.join(link)
        formatted_link = formatted_link.replace(erase, '')
        formatted_link = formatted_link.replace('#', '')
        link = formatted_link


    # ask for chapter range

    print("Specify from which to which chapter you want to download: ", )
    print("FROM: ")
    zakres1 = int(input())
    print("TO: ")
    zakres2 = int(input())
    zakres2 = zakres2 + 1

    # ask for save directory
    print("Chose Save Directory ? : ", )
    chosen_directory = filedialog.askdirectory()

    # create folder with manga title
    final_directory = os.path.join(chosen_directory,get_manga_title(link))
    print(final_directory)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


    global chapter_name
    chapter_name = list('chapter @')

    for x in range(zakres1, zakres2):
        chapter_name[8] = str(x)
        link = list(link)

        if x <= 10:
            link.pop(-1)
            link.pop(-1)
            link.append('0')
            link.append(x)
            if x == 10:
                link.pop(-2)

        else:
            link.pop(-1)
            link.append(x)
        print(link)
        save_path = os.path.join(final_directory, "".join(chapter_name))
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
        os.makedirs(save_path)



        link = [str(i) for i in link]  # convert all elements in list to strings
        download_ready_links = get_chapter_image_links("".join(link))
        dynasty_download(download_ready_links, final_directory)

    print('Download Finished')
