"""Screenshot the scoreboard section of index.html in both themes (local file, Playwright Chromium).
Usage: python _shot.py out_prefix
"""
import sys, pathlib
from playwright.sync_api import sync_playwright
here = pathlib.Path(__file__).parent.resolve()
out = sys.argv[1] if len(sys.argv) > 1 else str(here / '_shot')
with sync_playwright() as p:
    b = p.chromium.launch()
    for theme in ('dark', 'light'):
        pg = b.new_page(viewport={'width': 1100, 'height': 900}, device_scale_factor=1)
        pg.goto((here / 'index.html').as_uri())
        pg.evaluate(f"document.documentElement.setAttribute('data-theme','{theme}')")
        pg.wait_for_timeout(1200)
        el = pg.query_selector('#scoreboard')
        el.screenshot(path=f'{out}_{theme}.png')
        pg.close()
    pg = b.new_page(viewport={'width': 420, 'height': 900})
    pg.goto((here / 'index.html').as_uri()); pg.wait_for_timeout(800)
    pg.query_selector('#scoreboard').screenshot(path=f'{out}_mobile.png')
    b.close()
print('ok')
