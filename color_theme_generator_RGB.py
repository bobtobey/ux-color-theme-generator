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
    
    # 1) Interpolate brand -> light
    s_up   = interpolate(s_brand, s_light, steps)
    b_up   = interpolate(b_brand, b_light, steps)

    # 2) Interpolate brand -> dark
    s_down = interpolate(s_brand, s_dark,  steps)
    b_down = interpolate(b_brand, b_dark,  steps)

    # We'll gather them in two lists, then merge:
    up_shades = list(zip(s_up, b_up))      # [brand..light]
    up_shades = up_shades[::-1]           # reverse => [light..brand]

    down_shades = list(zip(s_down, b_down))  # [brand..dark]

    # Combine removing duplicate brand in the middle:
    palette = up_shades[:-1] + down_shades  # remove brand from first list’s end

    # Label them 100..900
    labels = [i * 100 for i in range(1, 10)]

    # Return list of (label, (H, S, B))
    return [(label, (h, s_val, b_val)) for label, (s_val, b_val) in zip(labels, palette)]

def hsb_to_hex(h, s, b):
    """
    Convert HSB (h=0..360, s=0..100, b=0..100) to a hex color string #RRGGBB.
    """
    s /= 100.0
    v = b / 100.0
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
    return f"#{r:02x}{g:02x}{b_:02x}"

if __name__ == "__main__":
    # Example brand color:
    H = 271
    S_brand = 77
    B_brand = 91

    # Generate 9 HSB swatches
    swatches = generate_shades(H, S_brand, B_brand)

    # Print each swatch as CSS custom property with HEX value
    # Format: --clr-primary-100: #badefe;
    for label, (h, s, b) in swatches:
        hex_val = hsb_to_hex(h, s, b)
        print(f"--clr-primary-{label}: {hex_val};")
