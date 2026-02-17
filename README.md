# bont

`bont` is a Python module for converting TrueType fonts to bitmap font texture atlas.

## Usage

```python
from pathlib import Path

from bont import generate_bitmap_font

src = Path("/path/to/font.ttf")
dst = Path("/path/to/dst/folder")

generate_bitmap_font(src, dst, size=16)

```

## Development
Create a virtual environment:
```sh
uv venv
```

Install requirements:
```sh
uv sync
```

## A note from Andrew
This is a module that I created and maintain for my own personal projects.
Please keep the following in mind:
- Features are added as I need them.
- Issues are fixed as my time and interest allow.
- Version updates may introduce breaking changes.
