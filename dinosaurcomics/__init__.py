from requests import get
from bs4 import BeautifulSoup as BS
from re import compile

comic_id_re = compile(r'comic=(\d+)$')
DC_HOME_URL = 'http://www.qwantz.com/index.php'
COMIC_URL = 'http://www.qwantz.com/index.php?comic={0}'
hdrs = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'}

panels = {
    1: {'left': 0, 'top': 0, 'width': 244, 'height': 244},
    2: {'left': 243, 'top': 0, 'width': 131, 'height': 244},
    3: {'left': 373, 'top': 0, 'width': 362, 'height': 244},
    4: {'left': 0, 'top': 242, 'width': 195, 'height': 244},
    5: {'left': 194, 'top': 242, 'width': 299, 'height': 244},
    6: {'left': 493, 'top': 242, 'width': 244, 'height': 244}
}


def get_max_comic_id():
    max_id_url = BS(get(DC_HOME_URL, headers=hdrs).text).find('meta', attrs={'property': 'og:url'})['content']
    return comic_id_re.search(max_id_url).group(1)


__all__ = ['get_max_comic_id', 'panels']