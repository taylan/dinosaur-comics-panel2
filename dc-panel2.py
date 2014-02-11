from flask import Flask, render_template
from random import randrange
from os import path
from wand.image import Image
from dinosaurcomics import get_max_comic_id, panels
from dinosaurcomics.DCComic import DCComic

app = Flask(__name__)
hdrs = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'}
comics_dir = path.join(path.dirname(__file__), 'static/comics')


def _crop_panel(filename, panel):
    fn = path.splitext(filename)
    with Image(filename=filename) as img:
        img.crop(**panels[panel])
        img.save(filename='{0}_{1}{2}'.format(fn[0], panel, fn[1]))


def save_panel(comic_id, panel):
    fn = path.join(path.dirname(__file__), 'static/comics/{0}.png'.format(comic_id))
    comic = DCComic(comic_id, comics_dir)
    comic.save_comic()
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
