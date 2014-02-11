from requests import get
from bs4 import BeautifulSoup as BS
from re import compile

comic_id_re = compile(r'comic=(\d+)$')
DC_HOME_URL = 'http://www.qwantz.com/index.php'
hdrs = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36'}


def get_max_comic_id():
    max_id_url = BS(get(DC_HOME_URL, headers=hdrs).text).find('meta', attrs={'property': 'og:url'})['content']
    return comic_id_re.search(max_id_url).group(1)


__all__ = ['get_max_comic_id']