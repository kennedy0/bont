# bont

`bont` is a Python module for converting TrueType fonts to bitmap font texture atlas.

### What this is (and isn't)

I built `bont` for myself to make my own game development workflow smoother; it is not a general-purpose tool.

It is also **not stable**.
I add and remove features when my needs change.

If you find `bont` useful, I'd recommend forking the project and adapting it to your own needs.

## Usage

```python
from pathlib import Path

from bont import generate_bitmap_font

src = Path("/path/to/font.ttf")
dst = Path("/path/to/dst/folder")

generate_bitmap_font(src, dst, size=16)

```
