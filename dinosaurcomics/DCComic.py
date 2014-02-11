from dinosaurcomics import panels, COMIC_URL, hdrs
from requests import get
from bs4 import BeautifulSoup as BS
from os import path


class DCComic():
    def __init__(self, comic_id, comics_dir):
        self._comic_id = comic_id
        self._comics_dir = comics_dir

    @property
    def comic_id(self):
        return self._comic_id

    def save_comic(self):
        r = get(BS(get(COMIC_URL.format(self._comic_id), headers=hdrs).text).select('.comic')[0]['src'], stream=True)
        fn = path.join(self._comics_dir, '{0}.png'.format(self._comic_id))
        if r.status_code == 200:
            with open(fn, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
