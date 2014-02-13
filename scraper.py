from sys import argv
from os import path
from dinosaurcomics import get_max_comic_id, panels
from dinosaurcomics.DCComic import DCComic
from pyprind import ProgPercent


def main():
    try:
        comics_dir = argv[1]
    except IndexError:
        comics_dir = path.join(path.dirname(__file__), 'static/comics')

    max_comic_id = get_max_comic_id()
    print('Scraping {0} comics...'.format(max_comic_id))
    progbar = ProgPercent(max_comic_id, stream=1)
    for comic_id in range(1, max_comic_id+1):
        comic = DCComic(comic_id, comics_dir)
        comic.save_comic()
        for panel in panels.keys():
            comic.save_panel(panel)

        progbar.update()


if __name__ == '__main__':
    main()
