import numpy as np


def px_to_int(pixel_value):
    """Takes a pixel string in the format '123px' and returns the int number.

    Parameters:
        pixel_value (str):
            The pixel value, written in the format '123px'.

    Returns:
        int:
            The number extracted from the pixel value.
    """
    if not pixel_value:
        return 0
    elif isinstance(pixel_value, str):
        pixel_value = int(pixel_value.strip("px"))
    else:
        pixel_value = int(pixel_value)
    return pixel_value


def make_white_image(height, width):
    """Generate a white background of appropriate height/width and return.

    Parameters:
        height (int):
            The height of the image to generate, in pixels.
        width (int):
            The width of the image to generate, in pixels.

    Returns:
        ndarray:
            An opencv compatible representation of the white image.
    """
    white_background = np.zeros([height, width, 3], dtype=np.uint8)
    white_background.fill(255)
    return white_background


def make_transparent_image(height, width):
    """Generate a transparent background of appropriate height/width and return.

    Parameters:
        height (int):
            The height of the image to generate, in pixels.
        width (int):
            The width of the image to generate, in pixels.

    Returns:
        ndarray:
            An opencv compatible representation of the transparent image.
    """
    transparent_background = np.zeros([height, width, 3], dtype=np.uint8)
    return transparent_background
