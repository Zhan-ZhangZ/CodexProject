from PIL import Image

img = Image.open('/Users/zz/Desktop/image.png')
img = img.convert('RGB')
width, height = img.size

# Find the white background blocks
# Let's scan the middle region (y=400 to 750) to find the bounding boxes of the white blocks
white_pixels = []
for y in range(400, 750):
    for x in range(width):
        r, g, b = img.getpixel((x, y))
        if r > 240 and g > 240 and b > 240:
            white_pixels.append((x, y))

if white_pixels:
    min_x = min(p[0] for p in white_pixels)
    max_x = max(p[0] for p in white_pixels)
    min_y = min(p[1] for p in white_pixels)
    max_y = max(p[1] for p in white_pixels)
    print(f"White blocks roughly found at X:{min_x}-{max_x}, Y:{min_y}-{max_y}")

# Find the titles
dark_rows = []
for y in range(0, 350):
    dark_count = 0
    for x in range(width):
        r, g, b = img.getpixel((x, y))
        # Blue pill badge or dark blue text
        if (r < 50 and g < 150 and b > 200) or (r < 50 and g < 50 and b < 50) or (r < 100 and g < 150 and b > 200):
            dark_count += 1
    if dark_count > 50:
        dark_rows.append(y)

if dark_rows:
    print(f"Titles roughly span from Y:{min(dark_rows)} to Y:{max(dark_rows)}")
