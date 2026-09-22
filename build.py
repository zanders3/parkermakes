"""Build the site with Python 3.11+; no installation or network required."""
import argparse
import datetime as dt
import hashlib
from html import escape, unescape
from io import BytesIO
import json
import os
from pathlib import Path
import posixpath
import re
import shutil
from string import Template
import time
import tomllib
from urllib.parse import urlsplit, urlunsplit
import xml.etree.ElementTree as ET

from vendor import markdown2
from highlight import highlight_code_blocks
from image import thumbnail

ROOT = Path(__file__).resolve().parent
SOURCE, OUTPUT = ROOT / 'source', ROOT / 'public'
TITLE = 'parkermakes.uk'
SUBTITLE = "Alex Parker's Projects and Writing"
AUTHOR = 'Alex Parker'
DESCRIPTION = "Alex Parker's Projects and Writing"
SITE_URL = os.environ.get('SITE_URL', 'https://parkermakes.uk').rstrip('/')
MARKDOWN = markdown2.Markdown(extras=['fenced-code-blocks', 'highlightjs-lang', 'header-ids'])
CACHE_VERSION = 1
THUMBNAIL_WIDTH = 200


def signature(path):
    try:
        info = path.stat()
        return [info.st_mtime_ns, info.st_size] if path.is_file() else None
    except FileNotFoundError:
        return None


def check_output():
    """Never follow links (including Windows junctions) in the generated tree."""
    def linked(path):
        return path.is_symlink() or bool(getattr(path.lstat(), 'st_file_attributes', 0) & 0x400)

    if OUTPUT.is_symlink() or OUTPUT.resolve() != ROOT / 'public':
        raise ValueError('public must be a real directory inside the repository')
    if OUTPUT.exists():
        if linked(OUTPUT) or not OUTPUT.is_dir():
            raise ValueError('public must be a real directory inside the repository')
        for directory, folders, files in os.walk(OUTPUT, followlinks=False):
            for name in folders + files:
                path = Path(directory) / name
                if linked(path):
                    raise ValueError(f'public must not contain links: {path}')


def load_cache(path):
    try:
        cache = json.loads(path.read_text(encoding='utf-8'))
        if (isinstance(cache, dict) and cache.get('version') == CACHE_VERSION
                and all(isinstance(cache.get(key), dict) for key in ('assets', 'thumbnails'))
                and all(isinstance(entry, dict) for key in ('assets', 'thumbnails')
                        for entry in cache[key].values())):
            return cache
    except (OSError, ValueError):
        pass
    return {'version': CACHE_VERSION, 'assets': {}, 'thumbnails': {}}


def read_page(path):
    try:
        opening, header, body = path.read_text(encoding='utf-8').split('+++', 2)
        if opening.strip():
            raise ValueError('expected +++ front matter')
        page = tomllib.loads(header)
        required = ['title', 'date', 'categories', 'thumbnail', 'description'] if path.parent.name == '_posts' else ['title']
        for key in required:
            if not page.get(key):
                raise ValueError(f'missing {key}')
        for key in ('title', 'thumbnail', 'description', 'layout'):
            if key in page and not isinstance(page[key], str):
                raise ValueError(f'{key} must be a string')
        for key in ('categories', 'tags'):
            if key in page and (not isinstance(page[key], list) or not all(isinstance(v, str) for v in page[key])):
                raise ValueError(f'{key} must be an array of strings')
        if 'game_credit' in page and not isinstance(page['game_credit'], bool):
            raise ValueError('game_credit must be a boolean')
        if 'date' in page and type(page['date']) is not dt.date:
            raise ValueError('date must be an unquoted YYYY-MM-DD date')
        page['post'] = path.parent.name == '_posts'
        page['url'] = f"/{page['date']:%Y/%m/%d}/{path.stem}/" if page['post'] else '/' + path.relative_to(SOURCE).with_suffix('').as_posix().removesuffix('index').rstrip('/')
        if not page['url'].endswith('/'):
            page['url'] += '/'
        page['body'] = captions(highlight_code_blocks(str(MARKDOWN.convert(body))))
        page['source'] = path
        return page
    except (ValueError, KeyError) as error:
        raise ValueError(f'{path.relative_to(ROOT)}: {error}') from error


def captions(body):
    def caption(match):
        image = match.group()
        alt = re.search(r'\balt="([^"]+)"', image)
        return image + (f'<span class="caption">{escape(unescape(alt[1]))}</span>' if alt else '')
    return re.sub(r'<img\b[^>]*>', caption, body)


def links(html, url, absolute=False):
    """Relativize site-root links; leave external URLs and iframe parameters alone."""
    def replace(match):
        target = urlsplit(unescape(match[2]))
        path = SITE_URL + target.path if absolute else posixpath.relpath(target.path, url)
        if target.path.endswith('/') and not path.endswith('/'):
            path += '/'
        return match[1] + escape(urlunsplit(('', '', path, target.query, target.fragment)), quote=True) + match[3]
    return re.sub(r'''((?:href|src)=["'])(/(?!/)[^"']*)(["'])''', replace, html)


def date_html(page, linked=False):
    date = page['date']
    month = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()[date.month - 1]
    label = f'{month} {date.day} {date.year}'
    if linked:
        label = f'<a href="{page["url"]}">{label}</a>'
    return f'<time datetime="{date.isoformat()}">{label}</time>'


def article(title, body, footer='', date='', kind='post', heading_class=''):
    return (f'<article class="{kind}"><div class="post-content"><header>{date}'
            f'<h1 class="{heading_class}">{escape(title)}</h1></header><div class="entry">{body}</div>'
            + (f'<footer>{footer}<div class="clearfix"></div></footer>' if footer is not None else '')
            + '</div></article>')


def summary(title, posts, more=''):
    rows = []
    for page in posts:
        title_text, url = escape(page['title']), page['url']
        dimensions = page.get('thumbnail_dimensions')
        size = f' width="{dimensions[0]}" height="{dimensions[1]}"' if dimensions else ''
        rows.append(f'<div class="imageitem"><a href="{url}"><img src="{escape(page["thumbnail"])}"{size} class="nofancybox" alt="" /></a>'
                    f'<h2 class="title"><a href="{url}">{title_text}</a><small class="dateimageitem">{date_html(page)}</small></h2><p class="dateimagedesc">'
                    f'{escape(page["description"])}</p></div><div class="clearfix"></div>')
    footer = f'<div style="float:right"><a href="{more}">Read More</a></div>' if more else ''
    return article(title, ''.join(rows), footer)


def card_summary(title_text, posts, more='', kind='', show_date=False):
    cards = []
    for page in posts:
        title, url = escape(page['title']), page['url']
        tags = ''.join(f'<span>{escape(tag)}</span>' for tag in page.get('tags', [])
                       if tag.lower() != 'highlights')
        action = 'View project' if 'Projects' in page['categories'] else 'Read article'
        card_date = date_html(page) if show_date else ''
        cards.append(f'<div class="highlight-card"><a class="highlight-image" href="{url}">'
                     f'<img src="{escape(page["thumbnail"])}" class="nofancybox" alt="" /></a>'
                     f'<div class="highlight-card-content"><div class="highlight-tags">{tags}</div>'
                     f'<h2><a href="{url}">{title}</a></h2>{card_date}'
                     f'<p>{escape(page["description"])}</p>'
                     f'<a class="highlight-link" href="{url}">{action} <span aria-hidden="true">&rarr;</span></a>'
                     f'</div></div>')
    footer = f'<div style="float:right"><a href="{more}">Read More</a></div>' if more else None
    return article(title_text, '<div class="highlight-grid">' + ''.join(cards) + '</div>',
                   footer=footer, kind=f'card-list {kind}'.rstrip())


def widget(title, posts):
    items = ''.join(f'<li><a href="{p["url"]}">{escape(p["title"])}</a></li>' for p in posts)
    return f'<div class="widget tag"><h3 class="title">{title}</h3><ul class="entry">{items}</ul></div>'


def build(force=False):
    started = time.perf_counter()
    check_output()
    cache_path = ROOT / '.cache/build.json'
    cache = load_cache(cache_path) if not force else {'assets': {}, 'thumbnails': {}}
    manifest = {'version': CACHE_VERSION, 'assets': {}, 'thumbnails': {}}
    generator = hashlib.sha256()
    for name in ('build.py', 'image.py'):
        generator.update((ROOT / name).read_bytes())
    generator = generator.hexdigest()
    generated = reused = copied = skipped = 0
    pages = [read_page(p) for p in sorted(SOURCE.rglob('*.md'))]
    posts = sorted((p for p in pages if p['post']), key=lambda p: (p['date'], p['url']), reverse=True)
    groups = {name: [p for p in posts if name in p['categories']] for name in ('Writing', 'Projects')}
    highlighted = [p for p in posts if any(tag.lower() == 'highlights' for tag in p.get('tags', []))]
    sidebar = widget('Projects', groups['Projects']) + widget('Writing', groups['Writing'])
    sidebar += '<div class="widget"><h3 class="title"><a href="/archives/">All posts</a></h3></div>'
    template = Template((ROOT / 'templates/page.html').read_text(encoding='utf-8'))
    outputs = {}

    def add(path, content):
        if path in outputs:
            raise ValueError(f'duplicate output: {path}')
        outputs[path] = content

    # Collect assets before rendering so thumbnail URLs resolve through the same
    # mapping as published files, including images shared by several posts.
    for page in posts:
        if page['source'].with_suffix('').is_dir():
            for asset in sorted(page['source'].with_suffix('').rglob('*')):
                if asset.is_file():
                    add(page['url'].lstrip('/') + asset.relative_to(page['source'].with_suffix('')).as_posix(), asset)
    for folder in (ROOT / 'assets', SOURCE):
        for asset in sorted(folder.rglob('*')):
            if asset.is_file() and asset.suffix != '.md' and '_posts' not in asset.relative_to(folder).parts:
                add(asset.relative_to(folder).as_posix(), asset)

    thumbnails = {}
    for page in posts:
        url = page['thumbnail']
        if not url.lower().endswith('.png'):
            continue  # Keep the existing animated GIF as-is.
        if url not in thumbnails:
            source = outputs.get(url.lstrip('/'))
            if not url.startswith('/') or not isinstance(source, Path):
                raise ValueError(f'{page["source"]}: thumbnail must reference a local PNG asset: {url}')
            path = 'thumbnails/' + url.lstrip('/')
            inputs = {'source': source.relative_to(ROOT).as_posix(),
                      'signature': signature(source), 'width': THUMBNAIL_WIDTH,
                      'generator': generator}
            previous = cache['thumbnails'].get(path, {})
            dimensions = previous.get('dimensions')
            existing = signature(OUTPUT / path)
            if (previous.get('inputs') == inputs
                    and existing is not None and previous.get('output') == existing
                    and isinstance(dimensions, list) and len(dimensions) == 2
                    and all(type(value) is int and value > 0 for value in dimensions)):
                add(path, None)  # Keep the existing thumbnail without decoding it.
                reused += 1
            else:
                output = BytesIO()
                dimensions = thumbnail(source, output, width=THUMBNAIL_WIDTH)
                add(path, output.getvalue())
                generated += 1
            manifest['thumbnails'][path] = {'inputs': inputs, 'dimensions': dimensions}
            thumbnails[url] = ('/' + path, dimensions)
        page['thumbnail'], page['thumbnail_dimensions'] = thumbnails[url]

    def render(url, title, body, description=DESCRIPTION, is_page=False, active_nav=''):
        nav = {name: '' for name in ('home', 'about', 'projects', 'writing')}
        if active_nav:
            nav[active_nav] = ' class="active" aria-current="page"'
        html = template.substitute(title=escape(title + ' | ' + SUBTITLE if title else SUBTITLE),
                                   site_title=escape(TITLE), subtitle=escape(SUBTITLE), author=escape(AUTHOR),
                                   description=escape(description), year=dt.date.today().year,
                                   canonical=escape(SITE_URL + url), body=body, sidebar='' if is_page else sidebar,
                                   **{f'nav_{name}': value for name, value in nav.items()})
        add(url.lstrip('/') + 'index.html', links(html, url))

    for page in pages:
        layout = page.get('layout', '')
        if layout == 'home':
            body = article(page['title'], page['body'], footer=None, kind='home-intro')
            if highlighted:
                body += card_summary('Highlights', highlighted, kind='highlights')
            body += summary('Writing', groups['Writing'][:3], '/writing/')
        elif layout in ('writing', 'projects'):
            if layout == 'projects':
                game_credits = [post for post in groups['Projects'] if post.get('game_credit', False)]
                projects = [post for post in groups['Projects'] if not post.get('game_credit', False)]
                body = card_summary('Game Credits', game_credits, kind='project-cards', show_date=True)
                body += card_summary(page['title'], projects, kind='project-cards', show_date=True)
            else:
                body = summary(page['title'], groups['Writing'])
        elif layout:
            raise ValueError(f'{page["source"]}: unknown layout {layout!r}')
        else:
            footer = ''.join(f'<div class="{key}">{escape(", ".join(page.get(key, [])))}</div>' for key in ('categories', 'tags') if page.get(key))
            body = article(page['title'], page['body'], footer, date_html(page, linked=True) if page['post'] else '',
                           'post' if page['post'] else 'page', 'title')
        active_nav = layout if layout in ('home', 'projects', 'writing') else ''
        if page['url'] == '/about/':
            active_nav = 'about'
        if page['post']:
            active_nav = next((name.lower() for name in ('Projects', 'Writing')
                               if name in page.get('categories', [])), '')
        render(page['url'], '' if layout == 'home' else page['title'], body,
               page.get('description', DESCRIPTION), not page['post'] and not layout, active_nav)
    render('/archives/', 'All posts', summary('All posts', posts))

    feed = ET.Element('feed', xmlns='http://www.w3.org/2005/Atom')
    for tag, value in [('title', TITLE), ('id', SITE_URL + '/'), ('updated', posts[0]['date'].isoformat() + 'T00:00:00Z')]:
        ET.SubElement(feed, tag).text = value
    ET.SubElement(feed, 'link', href=SITE_URL + '/atom.xml', rel='self')
    ET.SubElement(feed, 'link', href=SITE_URL + '/')
    ET.SubElement(ET.SubElement(feed, 'author'), 'name').text = AUTHOR
    for page in posts:
        entry = ET.SubElement(feed, 'entry')
        for tag, value in [('title', page['title']), ('id', SITE_URL + page['url']), ('updated', page['date'].isoformat() + 'T00:00:00Z')]:
            ET.SubElement(entry, tag).text = value
        ET.SubElement(entry, 'link', href=SITE_URL + page['url'])
        ET.SubElement(entry, 'content', {'type': 'html', 'xml:base': SITE_URL + page['url']}).text = links(page['body'], page['url'], absolute=True)
    sitemap = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for path in sorted(outputs):
        if path.endswith('index.html'):
            ET.SubElement(ET.SubElement(sitemap, 'url'), 'loc').text = SITE_URL + '/' + path.removesuffix('index.html')
    for name, document in [('atom.xml', feed), ('sitemap.xml', sitemap)]:
        add(name, ET.tostring(document, encoding='unicode', xml_declaration=True))

    # Validate every destination before modifying existing outputs.
    for path in outputs:
        relative = Path(path)
        if (relative.is_absolute() or '..' in relative.parts
                or not (OUTPUT / relative).resolve().is_relative_to(OUTPUT.resolve())):
            raise ValueError(f'output must stay inside public: {path}')
        if any(parent.as_posix() in outputs for parent in relative.parents if parent != Path('.')):
            raise ValueError(f'output is both a file and directory: {path}')
    check_output()
    # Generation succeeded. Remove obsolete files and empty directories first,
    # which also permits an old file to become a directory (and vice versa).
    for directory, folders, files in os.walk(OUTPUT, topdown=False):
        directory = Path(directory)
        for name in files:
            target = directory / name
            if target.relative_to(OUTPUT).as_posix() not in outputs:
                target.unlink()
        for name in folders:
            target = directory / name
            if not any(target.iterdir()):
                target.rmdir()
    for path, content in outputs.items():
        target = OUTPUT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, Path):
            inputs = {'source': content.relative_to(ROOT).as_posix(), 'signature': signature(content)}
            previous = cache['assets'].get(path, {})
            existing = signature(target)
            if (previous.get('inputs') == inputs and existing is not None
                    and previous.get('output') == existing):
                skipped += 1
            else:
                shutil.copyfile(content, target)
                copied += 1
            manifest['assets'][path] = {'inputs': inputs, 'output': signature(target)}
        elif content is not None:
            # Match write_text's platform newline translation used by old builds.
            data = content if isinstance(content, bytes) else content.replace('\n', os.linesep).encode('utf-8')
            if force or not target.is_file() or target.read_bytes() != data:
                target.write_bytes(data)
    for path, entry in manifest['thumbnails'].items():
        entry['output'] = signature(OUTPUT / path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = cache_path.with_suffix('.tmp')
    temporary.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    temporary.replace(cache_path)
    print(f'Built {len(pages) + 1} pages, {len(posts)} posts, {len(outputs)} files in public/')
    print(f'Thumbnails: {generated} generated, {reused} reused; '
          f'assets: {copied} copied, {skipped} skipped; {time.perf_counter() - started:.3f}s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true', help='regenerate all outputs without using the cache')
    args = parser.parse_args()
    try:
        build(force=args.force)
    except (ValueError, OSError) as error:
        raise SystemExit(str(error)) from error
