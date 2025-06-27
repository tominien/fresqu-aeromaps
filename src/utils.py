import colorsys




def generate_pastel_palette(number_of_colors: int) -> list[str]:
    """
    Generate a pastel color palette with `number_of_colors` colors.

    #### Arguments :
    - `number_of_colors (int)` : The number of colors to generate.

    #### Returns :
    - `list[str]` : A list of pastel colors in hexadecimal format.
    """
    if number_of_colors < 1:
        return []

    # Initialize the color palette :
    palette = []
    saturation = 0.8
    hsv_value  = 0.75

    for index in range(number_of_colors):
        hue = index / number_of_colors
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, hsv_value)
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(r * 255),
            int(g * 255),
            int(b * 255)
        )
        palette.append(hex_color)
    return palette


def float_to_int_string(value: float) -> str:
    """
    Convert a float value to an integer string.

    #### Arguments :
    - `value (float)` : The float value to convert.

    #### Returns :
    - `str` : The integer string representation of the float value.
    """
    return str(int(value))
