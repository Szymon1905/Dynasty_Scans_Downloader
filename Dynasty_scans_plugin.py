import os
import shutil
from pathlib import Path
from tkinter import filedialog
import requests

downloaded_files_list = []
global nazwa_rozdzialu



def download_file_from_link(link, save_dir=str(Path.home() / "Downloads")):
    filename = link.split("/")[-1]
    #downloaded_files_list.append(filename)
    r = requests.get(link, stream=True)
    r.raw.decode_content = True
    global nazwa_rozdzialu
    #print('STOP ',save_dir + '/' + "".join(nazwa_rozdzialu) +'/'+ filename)
    with open(save_dir + '/' + "".join(nazwa_rozdzialu) +'/'+ filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return


def get_chapter_image_links(url):
    import re, json, requests
    Dynasty_banner = "https://dynasty-scans.com/"

    r = requests.get(url)

    # extract the data
    match = re.search('var pages = (\[.*?\]);', r.text).group(1)

    # parse it into json
    match_json = json.loads(match)

    # iterate through it to get the links
    image_links = [img['image'] for img in match_json]

    for x in range(len(image_links)):
        image_links[x] = Dynasty_banner + image_links[x]

    return image_links


def dynasty_download(links,save_directory):
    for link in links:
        download_file_from_link(link,save_directory)


def move_downloaded_images_to_new_folder(download_folder):
    try:
        directory = os.getcwd()
        for file_name in downloaded_files_list:
            shutil.move(directory + "/" + file_name, download_folder)
    except:
        print("failed to move image")


def multiple_download():
    global link
    print("Podaj link do rozdziału wybranej mangi: ", )
    link = list(input())

    # formatowanie linku aby usunąć
    erase = (''.join(link)).split("#")[-1]
    print(erase)
    formatted_link = ''.join(link)
    formatted_link = formatted_link.replace(erase, '')
    formatted_link = formatted_link.replace('#', '')
    link = formatted_link

    if link[-1] == '#':
        print(link)
        link.pop(-1)
    print(link)

    print("Podaj zakres rozdzialow do pobrania: ", )
    zakres1, zakres2 = int(input()), int(input())
    zakres2 = zakres2 + 1
    print("Gdzie zapisać ? : ", )
    chosen_directory = filedialog.askdirectory()

    current_directory = os.getcwd()
    global nazwa_rozdzialu
    nazwa_rozdzialu = list('chapter @')

    for x in range(zakres1, zakres2):
        nazwa_rozdzialu[8] = str(x)
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


        save_path = os.path.join(chosen_directory, "".join(nazwa_rozdzialu))
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
        os.makedirs(save_path)


        link = [str(i) for i in link]  # convert all elements in list to strings
        download_ready_links = get_chapter_image_links("".join(link))
        dynasty_download(download_ready_links,chosen_directory)

    print('Download Finished')

