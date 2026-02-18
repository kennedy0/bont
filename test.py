from pathlib import Path

from bont import generate_bitmap_font


src = Path("/home/akennedy/git/hexx/assets/fonts/antiquity-print.ttf")
dst = Path.home() / "Desktop"
generate_bitmap_font(src, dst, 13)

src = Path("/home/akennedy/git/hexx/assets/fonts/habit_mono.ttf")
dst = Path.home() / "Desktop"
generate_bitmap_font(src, dst, 16)
