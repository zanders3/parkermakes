# parkermakes.uk

Python 3.11+ is the only build requirement.

## Build and preview

```sh
python -S build.py
python -m http.server --directory public
```

Open http://localhost:8000. The builder replaces `public/` on every run;
keep original files in `source/` or `assets/`, never in `public/`.
`-S` disables installed site packages and is optional.

## Write a post

Create `source/_posts/my-post.md`:

```markdown
+++
title = "My post"
date = 2026-09-17
categories = ["Writing"]
tags = ["Python"]
thumbnail = "/2026/09/17/my-post/photo.png"
description = "A short description for the listing pages."
+++

Write ordinary Markdown here.

![A caption](/2026/09/17/my-post/photo.jpg)
```

The `+++` block is TOML. Dates are unquoted; strings are quoted. Title,
date, categories, thumbnail and description are required for posts. Tags
are optional. Use `Writing` or `Projects` for the respective section;
all posts also appear in `/archives/`. Posts sort newest first.

Put images and downloads in `source/_posts/my-post/`. The example is
published at `/2026/09/17/my-post/`; its filename and date determine its URL.
Keep those stable after publishing. Root-relative content links are converted
to relative links so the output also works under a GitLab project subpath.

Standalone pages use `source/name/index.md` with a title in TOML front matter.
The homepage introduction is `source/index.md`. `layout = "home"`,
`"writing"` and `"projects"` select the three listing layouts.
Other files under `source/` are copied as static assets.

Markdown supports headings, lists, links, images, fenced and indented code,
and raw HTML. Image alt text becomes a caption. Code uses plain styled boxes.
Content is trusted author-written HTML, not sanitized user submissions.
YouTube embeds can use ordinary HTML:

```html
<div class="video-container"><iframe src="https://www.youtube.com/embed/VIDEO_ID" title="Video title" allowfullscreen></iframe></div>
```
