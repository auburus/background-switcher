import requests
import sys
from bs4 import BeautifulSoup

def get_pic_link():
    r = requests.get('http://fuckinghomepage.com/')

    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.select(".PostBody > p")

    isPicture = False
    for p in items:
        if isPicture:
            pic = p.select('a')[0]['href']
            break

        if "PICTURE OF THE DAY" in p.text:
            isPicture = True

    return pic

''' Do tumblr js redirection
'''
def tumblr_redirect(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")

    return soup.title.string

def __main__():
    link = get_pic_link()
    pic_link = tumblr_redirect(link)

    r = requests.get(pic_link, stream=True)
    if r.status_code != 200:
        sys.exit(1)

    with open('./image', 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)

__main__()
