import csv
import curses
import textwrap
import webbrowser
from pathlib import Path

DATA_FILE = Path(__file__).parent / 'data' / 'apps.csv'


def load_apps():
    with DATA_FILE.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def draw(stdscr, apps, current):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    title = "Awesome CLI Apps Browser - j/k or arrows to move, Enter to open, q to quit"
    stdscr.addstr(0, 0, title[: width - 1])

    max_lines = height - 4
    start = max(0, min(current - max_lines // 2, len(apps) - max_lines))
    for idx, app in enumerate(apps[start : start + max_lines]):
        line = f"{app['name']} ({app['category']})"
        if start + idx == current:
            stdscr.addstr(idx + 1, 0, line[: width - 1], curses.A_REVERSE)
        else:
            stdscr.addstr(idx + 1, 0, line[: width - 1])

    desc = apps[current]['description']
    desc_lines = textwrap.wrap(desc, width - 1)
    for i, line in enumerate(desc_lines):
        stdscr.addstr(height - len(desc_lines) + i - 1, 0, line)

    stdscr.refresh()


def open_link(app):
    url = app.get('homepage') or app.get('git')
    if url:
        webbrowser.open(url)


def main(stdscr):
    curses.curs_set(0)
    apps = load_apps()
    current = 0
    draw(stdscr, apps, current)
    while True:
        key = stdscr.getch()
        if key in (ord('q'), 27):
            break
        elif key in (curses.KEY_DOWN, ord('j')) and current < len(apps) - 1:
            current += 1
        elif key in (curses.KEY_UP, ord('k')) and current > 0:
            current -= 1
        elif key in (curses.KEY_ENTER, ord('\n'), ord('\r')):
            open_link(apps[current])
        draw(stdscr, apps, current)


if __name__ == '__main__':
    curses.wrapper(main)
