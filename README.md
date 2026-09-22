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
thumbnail = "my-post/photo.png"
description = "A short description for the listing pages."
+++

Write ordinary Markdown here.

![A caption](my-post/photo.jpg)
```

The `+++` block is TOML. Dates are unquoted; strings are quoted. Title,
date, categories, thumbnail and description are required for posts. Tags
are optional. Use `Writing` or `Projects` for the respective section;
all posts also appear in `/archives/`. Posts sort newest first.
Set the optional `game_credit` boolean on a Projects post to show it in the
Game Credits section ahead of the other cards on `/projects/`.

Put images and downloads in `source/_posts/my-post/`. The example is
published at `/2026/09/17/my-post/`; its filename and date determine its URL.
Keep those stable after publishing. Images, downloads and thumbnails can use
paths relative to the Markdown file, so images also work in local Markdown
previews. Shared assets use the same rule: another post can reference
`my-post/photo.jpg`, and `source/index.md` can reference
`../assets/css/images/toplogo.png`. The builder maps these files to their
published URLs. Root-relative content links remain supported; generated links
are relative so the output also works under a GitLab project subpath.

Standalone pages use `source/name/index.md` with a title in TOML front matter.
The homepage introduction is `source/index.md`. `layout = "home"`,
`"writing"` and `"projects"` select the three listing layouts.
Other files under `source/` are copied as static assets.

Markdown supports headings, lists, links, images, fenced and indented code,
and raw HTML. Image alt text becomes a caption. Labelled C, C++, C#, shell,
GNU linker script and NASM fences receive build-time syntax highlighting;
common labels include `c`, `cpp`, `c++`, `csharp`, `cs`, `sh`, `ld` and `nasm`.
Unlabelled and unsupported code remains plain:

````markdown
```csharp
public static void Main() { }
```
````

Content is trusted author-written HTML, not sanitized user submissions.
YouTube embeds can use ordinary HTML:

```html
<div class="video-container"><iframe src="https://www.youtube.com/embed/VIDEO_ID" title="Video title" allowfullscreen></iframe></div>
```
