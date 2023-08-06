import requests
import sys
def download(url,filename):
    if sys.platform=='win32':
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        print("Downloading for Windows...")
    elif sys.platform=='darwin':
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        print("Downloading for MacOS X...")
    elif sys.platform=='linux' or sys.platform=='linux2':
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        print("Downloading for Linux...")
    else:
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)