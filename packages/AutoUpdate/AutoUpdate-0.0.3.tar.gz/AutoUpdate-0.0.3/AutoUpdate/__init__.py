import urllib.request

url = "https://raw.githubusercontent.com/ribkix/testr/main/AutoUpdateTest.txt"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

current = "0.0.1"

download_link = "https://raw.githubusercontent.com/ribkix/testr/main/AutoUpdate.py"

def set_url(url_):
    global url; url = url_

def get_latest_version():
    file = urllib.request.urlopen(url)

    lines = ""
    for line in file:
        lines += line.decode("utf-8")

    return lines

def set_current_version(current_):
    global current; current = current_

def set_download_link(link):
    global download_link; download_link = link

def is_up_to_date():
    return current + "\n" == get_latest_version()

def download(path_to_file):
    urllib.request.urlretrieve(download_link,path_to_file)