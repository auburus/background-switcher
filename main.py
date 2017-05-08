import requests
import sys
import os
import os.path
from bs4 import BeautifulSoup

def get_pic_link():
    r = requests.get('http://fuckinghomepage.com')

    if r.status_code != 200:
        sys.stderr.write('Unable to access fuckinghomepage\n')
        sys.exit(1)

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
    if r.status_code != 200:
        sys.stderr.write('Unable to bypass tumblr redirect\n')
        sys.exit(1)

    soup = BeautifulSoup(r.text, "html.parser")

    return soup.title.string

def extract_img_link(link):
    ''' Handle special cases in some websites, or return
        the link hoping that is an image otherwise'''

    if "flickr" in link:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "html.parser")
        img = soup.select("#allsizes-photo > img")

        return img[0]['src']

    if 'i.reddituploads.com' in link:
        return link.replace(';', '')
    
    return link

def __main__():
    link = get_pic_link()
    original_link = tumblr_redirect(link)
    img_src = extract_img_link(original_link)

    r = requests.get(img_src, stream=True)
    if r.status_code != 200:
        sys.stderr.write('Unable to get image\n')
        sys.exit(1)

    directory = os.path.dirname(os.path.realpath(__file__))
    with open(directory + '/image', 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)
    
    os.system('xfdesktop --reload')

__main__()
