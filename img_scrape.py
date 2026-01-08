import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, unquote

base_url = "https://hayday.fandom.com"
list_url = "/wiki/Production_Buildings_List"
headers = {"User-Agent": "Mozilla/5.0"}

print(f"Fetching {base_url + list_url}...")
resp = requests.get(base_url + list_url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

# Find the main table with production buildings
table = soup.find("table", {"class": "wikitable"})
if not table:
    print("Error: Could not find table with class 'wikitable'")
    exit(1)

rows = table.find_all("tr")[1:]  # Skip header row

output_dir = "production_building_images"
os.makedirs(output_dir, exist_ok=True)

print(f"Found {len(rows)} rows. Starting extraction...")

count = 1
for row in rows:
    cols = row.find_all("td")
    if not cols:
        continue

    # 1. Extract Building Name (usually in the first cell)
    # Try finding <b><a>...</a></b> or just <a>...</a>
    name_tag = cols[0].find("a", title=True)
    if not name_tag:
        # Fallback: sometimes text is just in the cell or bold tag
        name_text = cols[0].get_text(strip=True)
    else:
        name_text = name_tag["title"]
    
    building_name = name_text.strip().replace(" ", "_")
    if not building_name:
        continue

    # 2. Extract Image URL
    # Look for the thumbnail/image link
    img_link_tag = row.find("a", {"class": "image"})
    
    full_img_url = None
    
    if img_link_tag:
        href = img_link_tag.get("href")
        if href:
            # Check if it's a direct link to the static image or a wiki file page
            if "static.wikia.nocookie.net" in href:
                # Likely a direct link (or close to it)
                full_img_url = href
            elif href.startswith("/wiki/File:"):
                # It's a file page, we might need to follow it, OR checking the inner <img> src might be enough
                # The user's screenshot shows the <a> href is the file page, BUT the <img> src inside it is the thumbnail.
                # However, usually Fandom <a> hrefs on thumbnails point to the File: page.
                # BUT the screenshot shows <a href="...static..."> which implies a direct link in the anchor itself?
                # Let's re-read the screenshot visual.
                # Screenshot: <a href="https://static.wikia.../Bakery.png/..." class="mw-file-description image">
                # So the href IS the image URL (or a revision of it).
                full_img_url = href
    
    # If we didn't get it from the <a> href, check the <img> src as a fallback
    if not full_img_url:
        img_tag = row.find("img")
        if img_tag:
            # Fandom lazy loading often puts real src in data-src or we just take src
            src = img_tag.get("data-src") or img_tag.get("src")
            if src:
                # thumbnails usually have /scale-to-width-down/XXX in url
                # we can try to remove that to get full size, or just use what we have
                full_img_url = src.split("/revision")[0] # rudimentary cleaning

    if not full_img_url:
        print(f"Skipping {building_name}: No image found.")
        continue

    # 3. Download
    try:
        # Clean up URL if needed (sometimes they have query params for scaling)
        # Taking everything before '/revision/...' usually gives the original
        # Example: .../Bakery.png/revision/latest?cb=...
        
        # If the url contains revision, strip it for a cleaner path attempt, 
        # but the link in screenshot included it. 
        # actually, simply downloading the link found in href usually works.
        
        print(f"Downloading {building_name} ({count})...")
        img_data = requests.get(full_img_url, headers=headers).content
        
        # Determine extension
        parsed_path = urlparse(full_img_url).path
        ext = os.path.splitext(parsed_path)[1]
        if not ext:
            ext = ".png" # default backup
            
        # Handle cases like image.png/revision/latest -> .png
        if "/" in ext: 
            ext = ".png"

        filename = f"{count:02d}_{building_name}{ext}"
        save_path = os.path.join(output_dir, filename)
        
        with open(save_path, "wb") as f:
            f.write(img_data)
        
        count += 1
            
    except Exception as e:
        print(f"Failed to download {building_name}: {e}")

print("Done.")
