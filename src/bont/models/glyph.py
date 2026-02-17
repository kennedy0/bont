from PIL import Image, ImageFont


class Glyph:
    """Represents a single character."""

    def __init__(self, pil_font: ImageFont.FreeTypeFont, char: str) -> None:
        # The PIL font object
        self.pil_font: ImageFont.FreeTypeFont = pil_font

        # The character that this glyph represents
        self.char: str = char

        # The position on the atlas
        self.x: int = 0
        self.y: int = 0

        # The size of the image on the atlas
        self.width: int = 0
        self.height: int = 0

        # The PIL image for this glyph
        self.image: Image.Image = self._char_to_image()

    def _char_to_image(self) -> Image.Image:
        """Create an image from the glyph's character."""
        # Create full size image
        ascent, descent = self.pil_font.getmetrics()
        char_width = int(self.pil_font.getlength(self.char))
        char_height = ascent + descent
        image = Image.new("L", (char_width, char_height))

        # Update the width and height
        self.width = char_width
        self.height = char_height

        # Get char mask
        char_mask = self.pil_font.getmask(self.char)
        cmask_w, cmask_h = char_mask.size

        # If the height of the char mask is zero (for example, the space character), just return the full size image.
        if cmask_h == 0:
            return image

        # Convert char mask to image
        char_image = Image.frombytes("L", (cmask_w, cmask_h), bytes(char_mask))

        # Paste char image
        char_bbox = self.pil_font.getbbox(self.char)
        image.paste(char_image, box=char_bbox)

        return image

    def to_dict(self) -> dict:
        """Convert the glyph to a dict."""
        return {
            "char": self.char,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }
