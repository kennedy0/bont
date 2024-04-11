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
