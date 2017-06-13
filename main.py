import requests
import sys
import os
import os.path
from bs4 import BeautifulSoup
from urllib import parse
from PIL import Image

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
    if "t.umblr.com/redirect" in link:
        o = parse.urlparse(link)
        q = parse.parse_qs(o.query)
        return q['z'][0]

    return link

def extract_img_link(link):
    ''' Handle special cases in some websites, or return
        the link hoping that is an image otherwise'''

    return link

    # I leave those here, because it was some special case somewhere,
    # and this might come handy in the future
    if "www.flickr.com" in link:
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
    download = directory + '/.image'
    with open(download, 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)
    
    # Check if it's a valid image, and replace the original one
    # if that's the case
    try:
        Image.open(download)
    except IOError:
        sys.stderr.write('Invalid image format\n')
        os.remove(download)
        sys.exit(1)

    os.rename(download, directory + '/image')

    # Finally, reload the desktop
    os.system('xfdesktop --reload')

__main__()
