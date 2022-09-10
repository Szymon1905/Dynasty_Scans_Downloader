import Dynasty_scans_plugin
import time

start_time = time.time()

if __name__ == '__main__':
    #Dynasty_scans_plugin.get_manga_title('https://dynasty-scans.com/chapters/liar_satsuki_can_see_death_ch01')
    Dynasty_scans_plugin.multiple_download()
    print("--- %s seconds ---" % (time.time() - start_time))

# TODO Dodaj aby tworzył sam folder z nazwą mangi i tam wstawiał chaptery