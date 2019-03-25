import requests
import sys
import os
import os.path
from bs4 import BeautifulSoup
from urllib import parse
from PIL import Image

def get_pic_link():
    """Navigate to fuckinghomepage.com and retrieve the picture link
    """

    r = requests.get('http://fuckinghomepage.com')

    if r.status_code != 200:
        sys.stderr.write('Unable to access the website\n')
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

    if not isPicture:
        sys.stderr.write(
                'The website doesn\'t contain the PICTURE OF THE DAY')
        sys.exit(1)

    return pic

def tumblr_redirect(link):
    """ Do tumblr js redirection
    """

    if "t.umblr.com/redirect" in link:
        o = parse.urlparse(link)
        q = parse.parse_qs(o.query)
        return q['z'][0]

    return link


def __main__():
    link = get_pic_link()
    img_src = tumblr_redirect(link)

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
