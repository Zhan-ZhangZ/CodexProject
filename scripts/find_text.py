from PIL import Image

img = Image.open('/Users/zz/Desktop/image.png')
img = img.convert('RGB')
width, height = img.size
print(f"Image size: {width}x{height}")

# Define a central horizontal region where the text is likely to be
# Assuming the text is in the upper half, between 20% and 40% of the height
# and horizontally centered (20% to 80% width)
start_y = int(height * 0.15)
end_y = int(height * 0.45)
start_x = int(width * 0.2)
end_x = int(width * 0.8)

# Calculate "darkness" or contrast per row to find the text line
row_stats = []
for y in range(start_y, end_y):
    dark_pixels = 0
    for x in range(start_x, end_x):
        r, g, b = img.getpixel((x, y))
        # Assuming text is dark
        if r < 100 and g < 100 and b < 100:
            dark_pixels += 1
    row_stats.append((y, dark_pixels))

# Print the y-coordinates with the most dark pixels
sorted_rows = sorted(row_stats, key=lambda item: item[1], reverse=True)
print("Top 10 rows with dark pixels:")
for y, count in sorted_rows[:10]:
    print(f"y: {y}, count: {count}")
