from PIL import Image, ImageDraw, ImageFilter

def create_squircle_mask(size, radius):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask

def process_app_icon(filename, out_filename):
    img = Image.open(filename).convert("RGBA")
    w, h = img.size
    
    # Simple logic: assume the background is a solid or gradient color around the edges.
    # We'll just crop a central square because we know app icons are usually centered.
    # Actually, we can find the bounding box of the non-background area.
    
    pixels = img.load()
    bg_color = pixels[0, 0]
    tolerance = 20
    
    min_x, min_y = w, h
    max_x, max_y = 0, 0
    
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # check distance from bg_color
            if abs(r - bg_color[0]) > tolerance or abs(g - bg_color[1]) > tolerance or abs(b - bg_color[2]) > tolerance:
                if x < min_x: min_x = x
                if y < min_y: min_y = y
                if x > max_x: max_x = x
                if y > max_y: max_y = y
                
    if min_x < max_x and min_y < max_y:
        # We found a bounding box
        # Add padding 
        padding = 0
        min_x = max(0, min_x - padding)
        min_y = max(0, min_y - padding)
        max_x = min(w, max_x + padding)
        max_y = min(h, max_y + padding)
        
        cropped = img.crop((min_x, min_y, max_x, max_y))
        cw, ch = cropped.size
        
        # Apple standard radius is roughly 22.5% of the icon width
        radius = int(min(cw, ch) * 0.225)
        mask = create_squircle_mask((cw, ch), radius)
        
        cropped.putalpha(mask)
        cropped.save(out_filename)
        print(f"Processed {filename} -> {out_filename} (Crop: {cw}x{ch})")
    else:
        # If we didn't find anything, just use the whole image with rounded corners
        radius = int(min(w, h) * 0.225)
        mask = create_squircle_mask((w, h), radius)
        img.putalpha(mask)
        img.save(out_filename)
        print(f"Fallback processed {filename} -> {out_filename}")

def process_workbuddy(filename, out_filename):
    # Floodfill from edges to make it transparent
    img = Image.open(filename).convert("RGBA")
    
    # Simple color replacement
    data = img.getdata()
    bg_color = data[0]
    tolerance = 15
    
    new_data = []
    for item in data:
        if abs(item[0]-bg_color[0]) < tolerance and \
           abs(item[1]-bg_color[1]) < tolerance and \
           abs(item[2]-bg_color[2]) < tolerance:
            new_data.append((255, 255, 255, 0)) # transparent
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    
    # We should also crop the transparent edges to tighten the bounding box
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(out_filename)
    print(f"Processed {filename} -> {out_filename} (Color replacement + crop)")

process_workbuddy('taobao_design/logo1.png', 'taobao_design/logo1_clean.png')
process_app_icon('taobao_design/logo2.png', 'taobao_design/logo2_clean.png')
process_app_icon('taobao_design/logo3.png', 'taobao_design/logo3_clean.png')
