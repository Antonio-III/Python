from PIL import ImageGrab

# This process is generally slow, so beware when using for game scripting.

def get_mouse_color(x: int, y: int) -> (float | tuple[int, ...] | None):
    """
    Return the rgb where the mouse points to.
    """
    img = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    rgb = img.getpixel((0, 0))
    return rgb