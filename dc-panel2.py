from flask import Flask, render_template
from random import randrange
from os import path
from dinosaurcomics import get_random_comic_id
from dinosaurcomics.DCComic import DCComic

app = Flask(__name__)
hdrs = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'}
comics_dir = path.join(path.dirname(__file__), 'static/comics')


def save_panel(comic_id, panel):
    comic = DCComic(comic_id, comics_dir)
    comic.save_comic()
    comic.save_panel(panel)


@app.route('/', methods=['GET'])
def index():
    comic_id = get_random_comic_id()
    panel = 6
    save_panel(comic_id, panel)
    return render_template('index.html', comic_id=comic_id, panel=panel)


if __name__ == '__main__':
    app.run(debug=True)
