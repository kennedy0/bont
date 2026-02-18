import math
import json
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from fontTools.ttLib import TTFont
from PIL import Image, ImageFont

from bont.models.glyph import Glyph


class FontAtlas:
    def __init__(self, ttf_font_file: Path, size: int) -> None:
        # The font file
        self.ttf_font_file: Path = ttf_font_file

        # The point size of the font
        self.size: int = size

        # The PIL Font object
        self.pil_font: ImageFont.FreeTypeFont = ImageFont.truetype(ttf_font_file.as_posix(), size)

        # The glyphs that are included in the font atlas
        self.glyphs: list[Glyph] = []

        # The number of rows and columns in the grid
        self.columns: int = 0
        self.rows: int = 0

        # The size of each cell
        # This will allow the glyphs to be laid out in a grid, even though their actual sizes may vary
        self.cell_width: int = 0
        self.cell_height: int = 0

        # Tracks whether or not the glyphs have been generated
        self._glyphs_generated: bool = False

    def write_image(self, png_file: Path) -> None:
        """Render the font atlas to a png file."""
        if not self._glyphs_generated:
            self.generate_glyphs()

        # Create new mask image
        width = self.columns * self.cell_width
        height = self.rows * self.cell_height
        mask_image = Image.new("L", (width, height))

        # Add glyphs to mask image
        for glyph in self.glyphs:
            mask_image.paste(glyph.image, box=(glyph.x, glyph.y))

        # Apply mask image
        image = Image.new("RGBA", mask_image.size, color="white")
        image.putalpha(mask_image)

        # Write image
        image.save(png_file)

    def write_font_data(self, font_data_file: Path) -> None:
        """Write the font data to a file."""
        # Convert font data to dictionary
        font_data = {}
        for glyph in self.glyphs:
            font_data[glyph.char] = glyph.to_dict()

        # Write font data to file
        with font_data_file.open("w") as fp:
            data_str = json.dumps(font_data, indent=2)
            fp.write(data_str)

    def generate_glyphs(self) -> None:
        """Generate glyphs from characters."""
        for code, char in self.get_characters():
            glyph = Glyph(self.pil_font, char)
            self.glyphs.append(glyph)

        # Update atlas with glyph-dependent data
        self.set_grid_size()
        self.set_cell_size()

        # Set glyph positions on the atlas
        self.set_glyph_positions()

        self._glyphs_generated = True

    def get_characters(self) -> list[tuple[int, str]]:
        """Get a list of all characters available in the font.
        Returns a list of (character_code, character) tuples
        """
        font = TTFont(self.ttf_font_file)

        with self._suppress_fonttools_warning_logs():
            cmap = font.getBestCmap()

        character_codes = list(cmap.keys())
        character_codes.sort()

        characters = []
        for code in character_codes:
            characters.append((code, chr(code)))
        return characters

    def set_grid_size(self) -> None:
        """Set the number of rows and columns in the grid."""
        self.columns = math.ceil(math.sqrt(len(self.glyphs)))
        self.rows = math.floor(math.sqrt(len(self.glyphs)))

    def set_cell_size(self) -> None:
        """Set the cell width and height on the atlas."""
        # Find max glyph width
        max_width = 0
        max_height = 0
        for glyph in self.glyphs:
            if glyph.width > max_width:
                max_width = glyph.width
            if glyph.height > max_height:
                max_height = glyph.height

        self.cell_width = max_width
        self.cell_height = max_height

    def set_glyph_positions(self) -> None:
        """Set glyph positions on the atlas."""
        glyph_count = len(self.glyphs)
        for i in range(glyph_count):
            col = i % self.columns
            row = i // self.rows

            # Calculate X and Y position
            x = col * self.cell_width
            y = row * self.cell_height

            # Update glyph position
            glyph = self.glyphs[i]
            glyph.x = x
            glyph.y = y

    @contextmanager
    def _suppress_fonttools_warning_logs(self) -> Generator:
        """Context manager to suppress (noisy, pointless) warning logs from fonttools."""
        fonttools_loggers: list[tuple[logging.Logger, int]] = []

        for name, logger in logging.root.manager.loggerDict.items():
            if name.startswith("fontTools.") and hasattr(logger, "level"):
                fonttools_loggers.append((logger, logger.level))
                logger.setLevel(logging.ERROR)

        yield

        for logger, original_level in fonttools_loggers:
            logger.setLevel(original_level)
