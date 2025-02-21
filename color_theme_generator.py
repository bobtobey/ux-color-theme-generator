import os
from jinja2 import Environment, FileSystemLoader

# Capture the theme name from user input
theme_name = input("Enter theme name: ")

# define a prompt function for postive integers
def get_int(prompt):
    while True:
        try:
            n = int(input(prompt))
            if 0 <= n <= 360:
                return n
            else:
                print("Please enter a positive integer between 0 and 360.")
        except ValueError:
            pass

def interpolate(a, b, steps):
    """
    Returns a list of 'steps+1' values from a to b (inclusive),
    linearly spaced.
    """
    return [a + (b - a) * (t / steps) for t in range(steps + 1)]

def generate_shades(h, s_brand, b_brand,
                    s_light=10, b_light=100,
                    s_dark=100, b_dark=30):
    """
    Generates a 9-color palette (HSB):
      - 100..400: from brand color up to 'lightest'
      - 500:      brand color
      - 600..900: from brand color down to 'darkest'
    """
    # 4 increments in each direction (4 brand->light, 4 brand->dark)
    # I choose 4 steps for lightest/darkest shades to create a balanced palette between shades
    steps = 4  

    # Interpolate from brand -> light
    s_up   = interpolate(s_brand, s_light, steps)
    b_up   = interpolate(b_brand, b_light, steps)

    # Interpolate from brand -> dark
    s_down = interpolate(s_brand, s_dark,  steps)
    b_down = interpolate(b_brand, b_dark,  steps)

    # We'll gather them in two lists, then merge:  
    # [brand..light]
    up_shades = list(zip(s_up, b_up)) 
    # reverse => [light..brand]
    up_shades = up_shades[::-1]     
    # [brand..dark]
    down_shades = list(zip(s_down, b_down))

    # Combine removing duplicate brand in the middle:
    # Remove duplicate brand from up_shades and merge
    palette = up_shades[:-1] + down_shades

    # Label them 100..900
    labels = [i * 100 for i in range(1, 10)]

    # Return list of (label, (H, S, B))
    # Using list comprehension to pair each label (e.g. 100, 200, ... 900)
    # with the corresponding (s_val, b_val) from 'palette', and include the fixed hue 'h'.
    # This constructs a list of tuples like:
    #   (100, (h, s_val, b_val)), (200, (h, s_val, b_val)), ..., (900, (h, s_val, b_val)).
    return [(label, (h, s_val, b_val)) for label, (s_val, b_val) in zip(labels, palette)]

# Convert HSB to RGB
def hsb_to_rgb(h, s, b):
    """
    Convert HSB (h=0..360, s=0..100, b=0..100) to an (R, G, B) tuple in 0..255.
    """
    # Normalize s, b
    s /= 100.0
    v = b / 100.0
    # Hue as fraction of 1
    h /= 360.0

    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    i_mod = i % 6
    if i_mod == 0:
        r, g, b_ = v, t, p
    elif i_mod == 1:
        r, g, b_ = q, v, p
    elif i_mod == 2:
        r, g, b_ = p, v, t
    elif i_mod == 3:
        r, g, b_ = p, q, v
    elif i_mod == 4:
        r, g, b_ = t, p, v
    else:  # i_mod == 5
        r, g, b_ = v, p, q

    r = round(r * 255)
    g = round(g * 255)
    b_ = round(b_ * 255)
    return (r, g, b_)

# Convert RGB to Hex
def rgb_to_hex(r, g, b):
    """
    Convert (R, G, B) in 0..255 to #RRGGBB format.
    """
    return f"#{r:02x}{g:02x}{b:02x}"

# Generate HTML file displaying the color palette
def generate_html(template_name, color_vars, class_names, theme_name, template_dir='templates'):
    """
    Generates an HTML file displaying the color palette.
    """
    # Load the Jinja2 template
    env = Environment(loader=FileSystemLoader(template_dir))
    # Load the template file
    template = env.get_template('color_theme.html')

    # Render the template with the colors data
    html_content = template.render(colors=color_vars, classnames=class_names, theme_name=theme_name)

    # Write the rendered HTML to a file
    with open(template_name, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == "__main__":
    # Example brand color (MangoMouse = HSB(33, 92, 99))
    # H = 271
    # S_brand = 77
    # B_brand = 91
    # Capture user input for HSB values
    H = get_int("Enter the hue value (0..360): ")
    S_brand = get_int("Enter the saturation value (0..100): ")  
    B_brand = get_int("Enter the brightness value (0..100): ")  

    # Generate 9 HSB swatches
    swatches = generate_shades(H, S_brand, B_brand)

    # Create 3 empty lists for each color format
    hsb_list = []
    rgb_list = []
    hex_list = []
    hex_list_classname = []

    # Single pass: generate HSB, RGB, HEX swatches, store in separate lists
    for label, (h, s, b) in swatches:
        # Round or keep floats as you prefer
        h_rounded = round(h)
        s_rounded = round(s)
        b_rounded = round(b)

        # Convert to RGB
        (r, g, b_) = hsb_to_rgb(h_rounded, s_rounded, b_rounded)

        # Convert to Hex
        hex_val = rgb_to_hex(r, g, b_)

        # Build string swatches in three formats:
        # 1) HSB(271, 77, 91)
        hsb_line = f"{label}: HSB({h_rounded}, {s_rounded}, {b_rounded})"        
        # 2) RGB(234, 230, 255)
        rgb_line = f"{label}: RGB({r}, {g}, {b_})"
        # 3) --cst-primary-100: #eae6ff;
        hex_line = f"--cst-primary-{label}: {hex_val};"
        # 4) --cst-primary-100: rgb(234, 230, 255);
        hex_line_classname = f"cst-primary-{label}"

        # Append swatches to the separate lists
        hsb_list.append(hsb_line)
        rgb_list.append(rgb_line)
        hex_list.append(hex_line)
        hex_list_classname.append(hex_line_classname)

        # Print the combined three formats:
        # print(f"{label}: HSB({h_rounded}, {s_rounded}, {b_rounded})")
        # print(f"     RGB({r}, {g}, {b_})")
        # print(f"     {hex_line}\n")

    # Print each list of swatches
    print("HSB Values:")
    for line in hsb_list:
        print(f"  {line}")

    print("\nRGB Values:")
    for line in rgb_list:
        print(f"  {line}")

    print("\nHEX Custom Properties:")
    for line in hex_list:
        print(f"  {line}")

    # Save the hex list to a text file
    # Using a 'with open(...) as file:' block to ensure the file is properly closed after writing
    # Open the file in "w" mode (write mode)
    with open("rendered_HSB_color_theme.txt", "w", encoding="utf-8") as file:
        file.write(f"/* {theme_name} color theme */\n\n")
        for line in hex_list:
            file.write(line + "\n")

    # Generate HTML file to display the color palette
    generate_html(
        template_name="rendered_palette.html",  # the output HTML file
        color_vars=hex_list,                    # the hex_list for your template
        class_names=hex_list_classname,         # the hex_list_classname for your template
        theme_name=theme_name,
        template_dir="templates"                # the folder that contains color_theme.html
    )
