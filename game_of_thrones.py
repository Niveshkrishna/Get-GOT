import requests
import validators
from lxml import html
import os
import sys
import math

def download_file(url):
    local_filename = "/home/username/Desktop/got_s08_e01.mkv" # {path where you want to download} ex: /home/username/Desktop/
    if os.path.exists(local_filename):
        return True
    
    with requests.get(url, stream=True) as r:
        print "Downloading %s" % local_filename
        total_length = r.headers.get('content-length')
        r.raise_for_status()
        dl = 0
        total_length = float(total_length)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    dl += len(chunk)
                    f.write(chunk)
                    done = int(math.ceil(dl * 50 / total_length))
                    percent = float(dl * 50 / total_length)
                    sys.stdout.write("\r[%s%s]%s%s " % ('=' * done, ' ' * (50-done), percent, "%") )    
                    sys.stdout.flush()
                    # f.flush()
    return local_filename


urls = [
        "http://dl20.mihanpix.com/94/series/game.of.throne/s8",
        "http://dl8.heyserver.in/serial/Game.of.Thrones/S08/", 
        "http://sv4avadl.uploadt.com/Serial/GOT/S08", 
        "http://dl.funsaber.net/serial/Game%20of%20Thrones/season%208/1080",
        "http://pz10028.parspack.net/S/Game%20of%20Thrones/S08/E/1080p/"
        ]
download = False
for url in urls :
    if download:
        break
    response = requests.get(url)
    if response.status_code != 404:
        content = html.fromstring(response.content)
        links = content.xpath('//a/@href')
        for link in links:
            print(link)https://github.com/Niveshkrishna/Get-GOT
            if link[-4:] == ".mkv":
                if validators.url(link):
                    if download_file(link):
                        print("Already downloaded")
                    download = True
                    break
if download == False:
    print("Not yet available ;(")

