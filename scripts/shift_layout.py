from PIL import Image

img = Image.open('/Users/zz/.gemini/antigravity-ide/brain/80f0e72c-ed40-4e68-83d1-3f9f1619a8d7/edited_taobao_cover_1781707251886.png')
img = img.convert('RGB')
width, height = img.size

# We want to move the titles (y=40 to y=310) down by 80 pixels.
# The gap is y=310 to y=460.
# So we extract the 80px from the gap (y=310 to y=390) and move it ABOVE the titles (to y=40).
# Then the titles move to y=120 to y=390.

shift_amount = 80
y_title_start = 40
y_title_end = 310

# Create a new image to hold the shifted result
new_img = Image.new('RGB', (width, height))

# 1. Copy top section (unchanged)
top_section = img.crop((0, 0, width, y_title_start))
new_img.paste(top_section, (0, 0))

# 2. Copy the gap that will be moved up
gap_section = img.crop((0, y_title_end, width, y_title_end + shift_amount))
new_img.paste(gap_section, (0, y_title_start))

# 3. Copy the titles and paste them below the moved gap
title_section = img.crop((0, y_title_start, width, y_title_end))
new_img.paste(title_section, (0, y_title_start + shift_amount))

# 4. Copy the rest of the image (unchanged)
rest_section = img.crop((0, y_title_end + shift_amount, width, height))
new_img.paste(rest_section, (0, y_title_end + shift_amount))

# To smooth out the seams, we can apply a slight vertical blur exactly at the seam lines.
# Seam 1: y = y_title_start (40)
# Seam 2: y = y_title_start + shift_amount (120)
# Seam 3: y = y_title_end + shift_amount (390)

pixels = new_img.load()
def blend_seam(y_seam, blend_radius=3):
    for x in range(width):
        for dy in range(-blend_radius, blend_radius + 1):
            if dy == 0: continue
            # simple linear interpolation across the seam
            y_above = y_seam - blend_radius - 1
            y_below = y_seam + blend_radius + 1
            
            w_below = (dy + blend_radius + 1) / (2 * blend_radius + 2)
            w_above = 1.0 - w_below
            
            c_above = pixels[x, y_above]
            c_below = pixels[x, y_below]
            
            r = int(c_above[0] * w_above + c_below[0] * w_below)
            g = int(c_above[1] * w_above + c_below[1] * w_below)
            b = int(c_above[2] * w_above + c_below[2] * w_below)
            
            pixels[x, y_seam + dy] = (r, g, b)

blend_seam(y_title_start, 5)
blend_seam(y_title_start + shift_amount, 5)
blend_seam(y_title_end + shift_amount, 5)

out_path = '/Users/zz/Desktop/image.png'
new_img.save(out_path)
print(f"Shifted titles down by {shift_amount}px seamlessly!")
