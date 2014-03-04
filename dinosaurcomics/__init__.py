from requests import get
from bs4 import BeautifulSoup as BS
from re import compile
from random import randrange
from os.path import abspath, dirname, realpath, join, getmtime
from datetime import datetime as dt

comic_id_re = compile(r'comic=(\d+)$')
DC_HOME_URL = 'http://www.qwantz.com/index.php'
COMIC_URL = 'http://www.qwantz.com/index.php?comic={0}'
CACHE_FN = abspath(join(dirname(realpath(__file__)), '..', 'max_comic_id'))
hdrs = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'}

panels = {
    1: {'left': 0, 'top': 0, 'width': 243, 'height': 242},
    2: {'left': 243, 'top': 0, 'width': 130, 'height': 242},
    3: {'left': 373, 'top': 0, 'width': 362, 'height': 242},
    4: {'left': 0, 'top': 242, 'width': 194, 'height': 244},
    5: {'left': 194, 'top': 242, 'width': 299, 'height': 244},
    6: {'left': 493, 'top': 242, 'width': 244, 'height': 244}
}


def _get_max_comic_id_cached():
    try:
        if (dt.now() - dt.fromtimestamp(getmtime(CACHE_FN))).total_seconds() // 3600 > 24:
            return None
        with open(CACHE_FN) as cache_file:
            return int(cache_file.read())
    except (FileNotFoundError, ValueError, OSError):
        return None


def _cache_max_comic_id(max_comic_id):
    try:
        with open(CACHE_FN, mode='w') as cache_file:
            cache_file.write(str(max_comic_id))
    except:
        pass


def get_max_comic_id():
    max_comic_id = _get_max_comic_id_cached()
    if not max_comic_id:
        soup = BS(get(DC_HOME_URL, headers=hdrs).text)
        max_id_url = soup.find('meta', attrs={'property': 'og:url'})['content']
        max_comic_id = int(comic_id_re.search(max_id_url).group(1))
        _cache_max_comic_id(max_comic_id)

    return max_comic_id


def get_random_comic_id():
    return randrange(1, get_max_comic_id() + 1)


__all__ = ['get_max_comic_id', 'get_random_comic_id', 'panels']
