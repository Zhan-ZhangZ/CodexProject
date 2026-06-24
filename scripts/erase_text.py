from PIL import Image

# Open the image
img_path = '/Users/zz/Desktop/image.png'
img = Image.open(img_path)
img = img.convert('RGB')
width, height = img.size

# Define the bounding box to erase
# Based on previous analysis, text is around y=353 to 385.
# Let's use a slightly larger box: y from 330 to 410.
# We will erase across a wide horizontal section to catch the text and any side lines.
start_y = 330
end_y = 410
start_x = 100
end_x = width - 100

pixels = img.load()

# Perform vertical interpolation to seamlessly erase the content
for x in range(start_x, end_x):
    # Get colors at the boundaries
    color_top = pixels[x, start_y - 1]
    color_bottom = pixels[x, end_y + 1]
    
    dist = end_y - start_y + 1
    
    for y in range(start_y, end_y + 1):
        # Linear interpolation weight
        w_bottom = (y - start_y + 1) / dist
        w_top = 1.0 - w_bottom
        
        r = int(color_top[0] * w_top + color_bottom[0] * w_bottom)
        g = int(color_top[1] * w_top + color_bottom[1] * w_bottom)
        b = int(color_top[2] * w_top + color_bottom[2] * w_bottom)
        
        pixels[x, y] = (r, g, b)

out_path = '/Users/zz/Desktop/image_fixed.png'
img.save(out_path)
print(f"Erased text between y={start_y} and y={end_y}.")
print(f"Saved to {out_path}")
