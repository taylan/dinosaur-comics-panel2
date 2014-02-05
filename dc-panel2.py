from flask import Flask, request, render_template
from requests import get
from bs4 import BeautifulSoup as BS
from re import compile
from random import randrange
from os import path
from wand.image import Image

app = Flask(__name__)
hdrs = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'}
comic_id_re = compile(r'comic=(\d+)$')


def get_max_comic_id():
    return comic_id_re.search(BS(get('http://www.qwantz.com/index.php', headers=hdrs).text).find('meta', attrs={'property': 'og:url'})['content']).group(1)


def save_panel2(comic_id):
    r = get(BS(get('http://www.qwantz.com/index.php?comic={0}'.format(comic_id), headers=hdrs).text).select('.comic')[0]['src'], stream=True)
    fn = path.join(path.dirname(__file__), 'static/comics/{0}.png'.format(comic_id))
    if r.status_code == 200:
        with open(fn, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

    with Image(filename=fn) as img:
        img.crop(243, 0, width=131, height=244)
        img.save(filename=fn)


@app.route('/', methods=['GET'])
def index():
    max_comic_id = int(get_max_comic_id())
    comic_id = randrange(1, max_comic_id+1)
    save_panel2(comic_id)
    return render_template('index.html', comic_id=comic_id)


if __name__ == '__main__':
    app.run(debug=True)
