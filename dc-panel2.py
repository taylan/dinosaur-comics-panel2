from flask import Flask, render_template, jsonify, redirect, request
from os import path
from json import loads
from dinosaurcomics import get_random_comic_id, get_max_comic_id, panels
from dinosaurcomics.DCComic import DCComic
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
comics_dir = path.join(path.dirname(__file__), 'static/comics')
comic_img_template = '/static/comics/{0}_{1}.png'
comic_url_template = 'http://www.qwantz.com/index.php?comic={0}'
app.jinja_env.globals['PANELS'] = panels

assets = Environment(app)
assets.register('all_js',
                Bundle('js/jquery-2.1.0.min.js', 'js/bootstrap.min.js',
                       'js/spin.min.js', 'js/mustache.js',
                       'js/jquery.mustache.js', 'js/dc-panel2.js',
                       'js/ZeroClipboard.min.js', filters='rjsmin',
                       output='gen/weightmon-packed.js'))
assets.register('all_css', Bundle('css/bootstrap.min.css', 'css/dc-panel2.css',
                                  output='gen/dc-panel2-packed.css'))


def save_panel(comic_id, panel):
    c = DCComic(comic_id, comics_dir)
    c.save_comic()
    c.save_panel(panel)


def _do_panel(panel, comic_id=None):
    comic_id = comic_id or get_random_comic_id()
    save_panel(comic_id, panel)
    return comic_id


def _parse_panels(ps):
    segments = ps.split('_')
    if len(segments) != len(panels.keys()):
        return None
    pnls = dict()
    for s in segments:
        k = list(map(int, s.split('-')))
        if k[0] not in panels.keys() or not (0 < k[1] < get_max_comic_id()):
            return None
        pnls[k[0]] = k[1]

    if len(pnls.keys()) != len(pnls.keys()):
        return None

    return pnls


@app.route('/a/random-comic', methods=['POST'])
def random_panels():
    pnls = loads(request.form.get('p', '{}'))
    rnd_panels = []
    for p in panels.keys():
        comic_id = _do_panel(p, pnls.get(str(p), None))
        rnd_panels.append({'comic_id': comic_id,
                            'panel': p,
                            'panel_url': comic_img_template.format(comic_id, p),
                            'comic_url': comic_url_template.format(comic_id)})

    panelids = ['{0}-{1}'.format(x['panel'], x['comic_id']) for x in rnd_panels]
    return jsonify({'panels': rnd_panels, 'panel_ids': '_'.join(panelids)})


@app.route('/a/random-panel/<int:panel>/comic/', methods=['GET'])
@app.route('/a/random-panel/<int:panel>/comic/<int:comic_id>', methods=['GET'])
def ajax_random_panel(panel=2, comic_id=0):
    cid = None if not comic_id or comic_id > get_max_comic_id() else comic_id
    comic_id = _do_panel(panel, cid)
    return jsonify({'comic_id': comic_id,
                    'panel': panel,
                    'panel_url': comic_img_template.format(comic_id, panel),
                    'comic_url': comic_url_template.format(comic_id)})


@app.route('/', methods=['GET'])
@app.route('/random-panel/<int:panel>', endpoint='rand-panel', methods=['GET'])
@app.route('/random-panel/<int:panel>/comic/', endpoint='rand-panel-no-comic',
           defaults={'comic_id': None}, methods=['GET'])
@app.route('/random-panel/<int:panel>/comic/<int:comic_id>',
           endpoint='rand-panel-specific-comic', methods=['GET'])
def random_panel(panel=2, comic_id=None):
    panel = panel if panel in panels.keys() else 2
    if comic_id and not 0 < comic_id < get_max_comic_id():
        return redirect('/')
    return render_template('index.html', comic_id=comic_id, panel=panel)


@app.route('/random-comic', defaults={'ps': None})
@app.route('/random-comic/p/<ps>', endpoint='rand-comic-w-panels')
def random_comic(ps=None):
    pnls = _parse_panels(ps) if ps else None
    return render_template('comic.html', pnls=pnls)


if __name__ == '__main__':
    app.run(debug=True)
