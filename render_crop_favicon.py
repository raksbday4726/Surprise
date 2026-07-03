import os
from PIL import Image

def crop_to_content(img_path):
    if not os.path.exists(img_path):
        print(f"File not found: {img_path}")
        return
    img = Image.open(img_path)
    img = img.convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        left, upper, right, lower = bbox
        width = right - left
        height = lower - upper
        max_size = max(width, height)
        cx = left + width / 2
        cy = upper + height / 2
        new_left = max(0, int(cx - max_size / 2))
        new_upper = max(0, int(cy - max_size / 2))
        new_right = min(img.width, int(cx + max_size / 2))
        new_lower = min(img.height, int(cy + max_size / 2))
        cropped = img.crop((new_left, new_upper, new_right, new_lower))
        
        resample_filter = getattr(Image, 'Resampling', None)
        if resample_filter is not None:
            filter_type = resample_filter.LANCZOS
        else:
            filter_type = getattr(Image, 'LANCZOS', getattr(Image, 'ANTIALIAS', 2))
            
        cropped = cropped.resize((192, 192), filter_type)
        cropped.save(img_path, "PNG")
        print("Successfully cropped and optimized favicon.png.")
    else:
        print("No content found to crop.")

if __name__ == "__main__":
    crop_to_content("favicon.png")
