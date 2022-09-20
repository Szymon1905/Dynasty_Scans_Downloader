import Dynasty_scans_plugin
import time



if __name__ == '__main__':
    start_time = time.time()
    Dynasty_scans_plugin.multiple_download()
    print("--- %s seconds ---" % (time.time() - start_time))

