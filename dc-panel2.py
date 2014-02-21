from flask import Flask, render_template, jsonify, redirect
from os import path
from dinosaurcomics import get_random_comic_id, get_max_comic_id, panels
from dinosaurcomics.DCComic import DCComic
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
comics_dir = path.join(path.dirname(__file__), 'static/comics')
comic_img_template = '/static/comics/{0}_{1}.png'
comic_url_template = 'http://www.qwantz.com/index.php?comic={0}'

assets = Environment(app)
assets.register('all_js', Bundle('js/jquery-2.1.0.min.js', 'js/bootstrap.min.js', 'js/spin.min.js', 'js/mustache.js',
                                 'js/jquery.mustache.js', 'js/dc-panel2.js', filters='rjsmin', output='gen/weightmon-packed.js'))
assets.register('all_css', Bundle('css/bootstrap.min.css', 'css/dc-panel2.css', output='gen/dc-panel2-packed.css'))


def save_panel(comic_id, panel):
    comic = DCComic(comic_id, comics_dir)
    comic.save_comic()
    comic.save_panel(panel)


def _do_panel(panel, comic_id=None):
    comic_id = comic_id or get_random_comic_id()
    save_panel(comic_id, panel)
    return comic_id


@app.route('/', methods=['GET'])
@app.route('/random-panel/<int:panel>', methods=['GET'])
@app.route('/random-panel/<int:panel>/comic/', endpoint='rand-panel-no-comic', defaults={'comic_id': None}, methods=['GET'])
@app.route('/random-panel/<int:panel>/comic/<int:comic_id>', endpoint='rand-panel-specific-comic', methods=['GET'])
def random_panel(panel=2, comic_id=None):
    panel = panel if panel in panels.keys() else 2
    if comic_id and not 0 < comic_id < get_max_comic_id():
        return redirect('/')
    return render_template('index.html', comic_id=comic_id, panel=panel)


@app.route('/a/random-panel/<int:panel>/comic/', methods=['GET'])
@app.route('/a/random-panel/<int:panel>/comic/<int:comic_id>', methods=['GET'])
def ajax_random_panel(panel=2, comic_id=0):
    cid = None if not comic_id or comic_id > get_max_comic_id() else comic_id
    comic_id = _do_panel(panel, cid)
    return jsonify({'comic_id': comic_id,
                    'panel': panel,
                    'panel_url': comic_img_template.format(comic_id, panel),
                    'comic_url': comic_url_template.format(comic_id)})


if __name__ == '__main__':
    app.run(debug=True)
