import math
import json
from pathlib import Path

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
        """ Render the font atlas to a png file. """
        print(f"Writing image: {png_file.as_posix()}")
        if not self._glyphs_generated:
            self.generate_glyphs()

        # Create new mask image
        size = self.calculate_image_dimensions()
        mask_image = Image.new('L', size)

        # Add glyphs to mask image
        for glyph in self.glyphs:
            mask_image.paste(glyph.image, box=(glyph.x, glyph.y))

        # Apply mask image
        image = Image.new("RGBA", mask_image.size, color="white")
        image.putalpha(mask_image)

        # Write image
        image.save(png_file)

    def write_font_data(self, font_data_file: Path) -> None:
        """ Write the font data to a file. """
        print(f"Writing font data: {font_data_file.as_posix()}")

        # Convert font data to dictionary
        font_data = {}
        for glyph in self.glyphs:
            font_data[glyph.char] = glyph.to_dict()

        # Write font data to file
        with font_data_file.open('w') as fp:
            data_str = json.dumps(font_data, indent=2)
            fp.write(data_str)

    def generate_glyphs(self) -> None:
        """ Generate glyphs from characters. """
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
        """ Get a list of all characters available in the font.
        Returns a list of (character_code, character) tuples
        """
        font = TTFont(self.ttf_font_file)
        cmap = font.getBestCmap()
        character_codes = list(cmap.keys())

        characters = []
        for code in character_codes:
            characters.append((code, chr(code)))
        return characters

    def set_grid_size(self) -> None:
        """ Set the number of rows and columns in the grid. """
        self.columns = math.ceil(math.sqrt(len(self.glyphs)))
        self.rows = math.floor(math.sqrt(len(self.glyphs)))

    def set_cell_size(self) -> None:
        """ Set the cell width and height on the atlas. """
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
        """ Set glyph positions on the atlas. """
        glyph_count = len(self.glyphs)
        for i in range(glyph_count):
            col = i % self.columns
            row = i // self.rows
            print(f"{i}: {col} x {row}")

            # Calculate X and Y position
            x = col * self.cell_width
            y = row * self.cell_height

            # Update glyph position
            glyph = self.glyphs[i]
            glyph.x = x
            glyph.y = y

    def calculate_image_dimensions(self) -> tuple[int, int]:
        """ Calculate the dimensions for the image. """
        # Get the width or height, whichever is larger
        width = self.columns * self.cell_width
        height = self.rows * self.cell_height
        max_side = max(width, height)

        # Step by powers of 2 until the width and height both fit
        size = 2
        while size < max_side:
            size *= 2

        return size, size
