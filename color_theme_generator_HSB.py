def interpolate(a, b, steps):
    """
    Returns a list of 'steps+1' values from a to b (inclusive),
    linearly spaced.
    """
    return [a + (b - a) * (t / steps) for t in range(steps+1)]

def generate_shades(h, s_brand, b_brand,
                    s_light=10, b_light=100,
                    s_dark=100, b_dark=30):
    """
    Generates a 9-color palette:
      - 100..400: From brand color up to 'lightest'
      - 500:      Brand color
      - 600..900: From brand color down to 'darkest'
    """
    # Number of intermediate steps in each direction (4 lighter, 4 darker)
    # I choose 4 steps for lightest/darkest shades to create a balanced palette between shades
    steps = 4

    # Interpolate from brand -> light
    s_up   = interpolate(s_brand, s_light, steps)
    b_up   = interpolate(b_brand, b_light, steps)

    # Interpolate from brand -> dark
    s_down = interpolate(s_brand, s_dark,  steps)
    b_down = interpolate(b_brand, b_dark,  steps)

    # The 'brand color' is included at index 0 of both s_up, s_down,
    # so we skip that index once when combining final results.
    # lightest will be the last in the up array, darkest is last in the down array.
    # We'll reverse the 'up' so it goes from lightest to brand, then join with brand->dark.

    # Shades 100..500
    up_shades = list(zip(s_up, b_up))  # from brand to light
    # up_shades[-1] is the lightest end. If we want them from 100->500, reverse them:
    up_shades = up_shades[::-1]  # now up_shades[0] is the lightest

    # Shades 500..900
    down_shades = list(zip(s_down, b_down))  # from brand to dark

    # Combine them so we get 100..900:
    # up_shades = 5 entries (indexes 0..4 => 100..500), 
    # down_shades = 5 entries (indexes 0..4 => 500..900)
    # But brand color is duplicated in both ( index 4 of up_shades and index 0 of down_shades ).
    # We'll remove one of the brand color duplicates.
    palette = up_shades[:-1] + down_shades  # remove the last from the first to avoid duplication

    # Now label them 100..900 in increments of 100
    labels = [i * 100 for i in range(1, 10)]
    
    # Build final list of (label, (h, s, b))
    final = []
    for label, (s_val, b_val) in zip(labels, palette):
        # Round or keep floats as you wish
        final.append((label, (h, round(s_val), round(b_val))))

    return final


# --- Demo ---
if __name__ == "__main__":
    # Brand color
    H = 271
    S_brand = 77
    B_brand = 91

    # Generate palette
    shades = generate_shades(H, S_brand, B_brand)

    # Print them
    for label, (h, s, b) in shades:
        print(f"{label}: HSB({h}, {s}, {b})")
