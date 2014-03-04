from dinosaurcomics import panels, COMIC_URL, hdrs
from requests import get
from bs4 import BeautifulSoup as BS
from os import path
from wand.image import Image


class DCComic():
    def __init__(self, comic_id, comics_dir):
        self._comic_id = comic_id
        self._comics_dir = comics_dir

    @property
    def comic_id(self):
        return self._comic_id

    @property
    def comic_path(self):
        return path.join(self._comics_dir, '{0}.png'.format(self._comic_id))

    def save_comic(self):
        fn = path.join(self._comics_dir, '{0}.png'.format(self._comic_id))
        if path.exists(fn):
            return

        soup = BS(get(COMIC_URL.format(self._comic_id), headers=hdrs).text)
        r = get(soup.select('.comic')[0]['src'], stream=True)
        if r.status_code == 200:
            with open(fn, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

    def save_panel(self, p):
        fn = path.splitext(self.comic_path)
        panel_fn = '{0}_{1}{2}'.format(fn[0], p, fn[1])
        if path.exists(panel_fn):
            return

        with Image(filename=self.comic_path) as img:
            img.crop(**panels[p])
            img.save(filename=panel_fn)
