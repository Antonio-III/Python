from PIL import ImageGrab
import pyautogui
import time

# This process is generally slow, so beware when using for game scripting.

def get_mouse_color(x: int, y: int) -> (float | tuple[int, ...] | None):
    """
    Return the rgb where the mouse points to.
    """
    img = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    rgb = img.getpixel((0, 0))
    return rgb

def main():
    while True:
        try:
            x, y = pyautogui.position()

            color = get_mouse_color(x,y)
            r,g,b = color if isinstance(color, (tuple, list)) else (0, 0, 0)
            
            print(f"rgb({r},{g},{b})")

            # To prevent CPU thrashing
            time.sleep(0.001)

        except KeyboardInterrupt:
            print("Exit!")
            return None

if __name__ == "__main__":
    main()