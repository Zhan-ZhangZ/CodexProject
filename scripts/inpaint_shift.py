import cv2
import numpy as np
from PIL import Image

# The image that the user said "可以" to (logos background removed, but titles not low enough)
img_path = '/Users/zz/.gemini/antigravity-ide/brain/80f0e72c-ed40-4e68-83d1-3f9f1619a8d7/edited_taobao_cover_1781707251886.png'
img = cv2.imread(img_path)
if img is None:
    print("Could not read image")
    exit(1)

# Define the region containing the titles (y=30 to y=320)
# We want to extract them and move them down by ~80px.
shift_y = 80
roi_y_start = 30
roi_y_end = 320
roi_height = roi_y_end - roi_y_start

# Extract the ROI
roi = img[roi_y_start:roi_y_end, :].copy()

# The titles are blue (#0960eb) on a light background.
# Convert to HSV to better isolate the blue/dark colors
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# Define range for blue/dark text and pill
# #0960eb is RGB(9, 96, 235), BGR(235, 96, 9)
# Also include dark colors for text anti-aliasing
lower_blue = np.array([100, 50, 50])
upper_blue = np.array([130, 255, 255])
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

# Also catch dark pixels for text shadows/edges
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
_, mask_dark = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

# Combine masks to capture all text and graphics in the ROI
mask = cv2.bitwise_or(mask_blue, mask_dark)

# Dilate the mask slightly to cover anti-aliasing artifacts during inpainting
kernel = np.ones((5,5), np.uint8)
inpaint_mask_roi = cv2.dilate(mask, kernel, iterations=1)

# Inpaint the original image to remove the text seamlessly
inpaint_mask = np.zeros(img.shape[:2], dtype=np.uint8)
inpaint_mask[roi_y_start:roi_y_end, :] = inpaint_mask_roi

print("Inpainting background... this might take a few seconds.")
# Use Navier-Stokes based inpainting
clean_bg = cv2.inpaint(img, inpaint_mask, 5, cv2.INPAINT_NS)

# Now we have a perfectly clean background (clean_bg)
# We need to overlay the original ROI onto the clean background, shifted down by shift_y.
# To do this cleanly, we use the mask to blend the pixels from the ROI into the shifted position.

# We'll create a full-size alpha channel from the mask to do a smooth alpha blend
alpha_roi = cv2.GaussianBlur(mask, (3, 3), 0) / 255.0

# Create the final image as a copy of the clean background
final_img = clean_bg.copy()

# Paste the ROI onto the new location
paste_y_start = roi_y_start + shift_y
paste_y_end = roi_y_end + shift_y

for c in range(3):
    final_img[paste_y_start:paste_y_end, :, c] = (
        alpha_roi * roi[:, :, c] +
        (1 - alpha_roi) * clean_bg[paste_y_start:paste_y_end, :, c]
    )

# Save result
out_path = '/Users/zz/Desktop/image.png'
cv2.imwrite(out_path, final_img)
print(f"Saved perfectly shifted image to {out_path}")
