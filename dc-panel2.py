from flask import Flask, render_template, jsonify
from os import path
from dinosaurcomics import get_random_comic_id
from dinosaurcomics.DCComic import DCComic

app = Flask(__name__)
comics_dir = path.join(path.dirname(__file__), 'static/comics')


def save_panel(comic_id, panel):
    comic = DCComic(comic_id, comics_dir)
    comic.save_comic()
    comic.save_panel(panel)


def _do_random_panel(panel):
    comic_id = get_random_comic_id()
    save_panel(comic_id, panel)
    return comic_id


@app.route('/random-panel/<int:panel>', methods=['GET'])
def random_panel(panel=2):
    comic_id = _do_random_panel(panel)
    return render_template('index.html', comic_id=comic_id, panel=panel)


@app.route('/a/random-panel/<int:panel>', methods=['GET'])
def ajax_random_panel(panel=2):
    comic_id = _do_random_panel(panel)
    return jsonify({'comic': comic_id, 'panel': panel,
                    'panel_url': '/static/comics/{0}_{1}.png'.format(comic_id,
                                                                     panel),
                    'comic_url': 'http://www.qwantz.com/index.php?comic={0}'.format(
                        comic_id)}
    )


@app.route('/', methods=['GET'])
def index():
    comic_id = _do_random_panel(2)
    return render_template('index.html', comic_id=191, panel=2)


if __name__ == '__main__':
    app.run(debug=True)
