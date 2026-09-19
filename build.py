"""Build the site with Python 3.11+; no installation or network required."""
import datetime as dt
from html import escape, unescape
from io import BytesIO
import os
from pathlib import Path
import posixpath
import re
import shutil
from string import Template
import tomllib
from urllib.parse import urlsplit, urlunsplit
import xml.etree.ElementTree as ET

from vendor import markdown2
from image import thumbnail

ROOT = Path(__file__).resolve().parent
SOURCE, OUTPUT = ROOT / 'source', ROOT / 'public'
TITLE = 'parkermakes.uk'
SUBTITLE = "Alex Parker's Projects and Writing"
AUTHOR = 'Alex Parker'
DESCRIPTION = "Alex Parker's Projects and Writing"
SITE_URL = os.environ.get('SITE_URL', 'https://parkermakes.uk').rstrip('/')
MARKDOWN = markdown2.Markdown(extras=['fenced-code-blocks', 'highlightjs-lang', 'header-ids'])


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
        if 'date' in page and type(page['date']) is not dt.date:
            raise ValueError('date must be an unquoted YYYY-MM-DD date')
        page['post'] = path.parent.name == '_posts'
        page['url'] = f"/{page['date']:%Y/%m/%d}/{path.stem}/" if page['post'] else '/' + path.relative_to(SOURCE).with_suffix('').as_posix().removesuffix('index').rstrip('/')
        if not page['url'].endswith('/'):
            page['url'] += '/'
        page['body'] = captions(str(MARKDOWN.convert(body)))
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
                    f'<h2 class="title"><a href="{url}">{title_text}</a><small style="float:right">{date_html(page)}</small></h2>'
                    f'{escape(page["description"])}</div><div class="clearfix"></div>')
    footer = f'<div style="float:right"><a href="{more}">Read More</a></div>' if more else ''
    return article(title, ''.join(rows), footer)


def widget(title, posts):
    items = ''.join(f'<li><a href="{p["url"]}">{escape(p["title"])}</a></li>' for p in posts)
    return f'<div class="widget tag"><h3 class="title">{title}</h3><ul class="entry">{items}</ul></div>'


def build():
    pages = [read_page(p) for p in sorted(SOURCE.rglob('*.md'))]
    posts = sorted((p for p in pages if p['post']), key=lambda p: (p['date'], p['url']), reverse=True)
    groups = {name: [p for p in posts if name in p['categories']] for name in ('Writing', 'Projects')}
    sidebar = widget('Projects', list(reversed(groups['Projects']))) + widget('Writing', groups['Writing'])
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
            output = BytesIO()
            dimensions = thumbnail(source, output)
            path = 'thumbnails/' + url.lstrip('/')
            add(path, output.getvalue())
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
            body = article(page['title'], page['body'], footer=None)
            body += summary('Writing', groups['Writing'][:3], '/writing/')
            body += summary('Projects', groups['Projects'], '/projects/')
        elif layout in ('writing', 'projects'):
            body = summary(page['title'], groups[layout.title()])
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

    # This fixed directory is the only tree the builder is allowed to remove.
    if OUTPUT.is_symlink() or OUTPUT.resolve() != ROOT / 'public':
        raise ValueError('public must be a real directory inside the repository')
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    for path, content in outputs.items():
        target = OUTPUT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, Path):
            shutil.copyfile(content, target)
        elif isinstance(content, bytes):
            target.write_bytes(content)
        else:
            target.write_text(content, encoding='utf-8')
    print(f'Built {len(pages) + 1} pages, {len(posts)} posts, {len(outputs)} files in public/')


if __name__ == '__main__':
    try:
        build()
    except (ValueError, OSError) as error:
        raise SystemExit(str(error)) from error
