from pathlib import Path

from bont.models.font_atlas import FontAtlas


def generate_bitmap_font(ttf_font_file: Path, output_folder: Path, size: int) -> None:
    """Generate a bitmap font from a TTF font."""
    font_atlas = FontAtlas(ttf_font_file, size)
    font_name = f"{ttf_font_file.stem}.{size}"
    font_atlas.write_image(output_folder / f"{font_name}.png")
    font_atlas.write_font_data(output_folder / f"{font_name}.fontdata")
