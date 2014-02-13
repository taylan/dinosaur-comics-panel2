from sys import argv
from os import path
from dinosaurcomics import get_max_comic_id, panels
from dinosaurcomics.DCComic import DCComic


def main():
    try:
        comics_dir = argv[1]
    except IndexError:
        comics_dir = path.join(path.dirname(__file__), 'static/comics')

    for comic_id in range(1, get_max_comic_id()+1):
        comic = DCComic(comic_id, comics_dir)
        comic.save_comic()
        for panel in panels.keys():
            comic.save_panel(panel)

        print('Comic {0} complete.'.format(comic_id))


if __name__ == '__main__':
    main()