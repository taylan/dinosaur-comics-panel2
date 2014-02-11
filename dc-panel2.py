from flask import Flask, render_template
from requests import get
from bs4 import BeautifulSoup as BS
from re import compile
from random import randrange
from os import path
from wand.image import Image

app = Flask(__name__)
hdrs = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'}
comic_id_re = compile(r'comic=(\d+)$')
COMIC_URL = 'http://www.qwantz.com/index.php?comic={0}'
DC_HOME_URL = 'http://www.qwantz.com/index.php'


def get_max_comic_id():
    max_id_url = BS(get(DC_HOME_URL, headers=hdrs).text).find('meta', attrs={'property': 'og:url'})['content']
    return comic_id_re.search(max_id_url).group(1)


panels = {
    1: {'left': 0, 'top': 0, 'width': 244, 'height': 244},
    2: {'left': 243, 'top': 0, 'width': 131, 'height': 244},
    3: {'left': 373, 'top': 0, 'width': 362, 'height': 244},
    4: {'left': 0, 'top': 242, 'width': 195, 'height': 244},
    5: {'left': 194, 'top': 242, 'width': 299, 'height': 244},
    6: {'left': 493, 'top': 242, 'width': 244, 'height': 244}
}


def _crop_panel(filename, panel):
    fn = path.splitext(filename)
    with Image(filename=filename) as img:
        img.crop(**panels[panel])
        img.save(filename='{0}_{1}{2}'.format(fn[0], panel, fn[1]))


def save_comic(comic_id):
    r = get(BS(get(COMIC_URL.format(comic_id), headers=hdrs).text).select('.comic')[0]['src'], stream=True)
    fn = path.join(path.dirname(__file__), 'static/comics/{0}.png'.format(comic_id))
    if r.status_code == 200:
        with open(fn, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def save_panel(comic_id, panel):
    fn = path.join(path.dirname(__file__), 'static/comics/{0}.png'.format(comic_id))
    save_comic(comic_id)
    _crop_panel(fn, panel)


@app.route('/', methods=['GET'])
def index():
    max_comic_id = int(get_max_comic_id())
    comic_id = randrange(1, max_comic_id + 1)
    panel = 6
    save_panel(comic_id, panel)
    return render_template('index.html', comic_id=comic_id, panel=panel)


if __name__ == '__main__':
    app.run(debug=True)
