from datetime import datetime
import re

def data_products(items):
    # Title
    title_tag = items.find('h3', class_='product-title')
    title = title_tag.text.strip() if title_tag else None

    # Price
    price_tag = items.find('span', class_='price')
    price = price_tag.text.strip() if price_tag else None

    # Rating: ambil <p> yang mengandung teks "Rating" dan parse angka float
    rating = None
    paragraphs = [p for p in items.find_all('p')]
    for p in paragraphs:
        text = p.get_text()
        match = re.search(r'(\d+\.\d+)', text)
        if "Rating" in text and match:
            rating = float(match.group(1))
            break

    # Colors
    colors = None
    for p in paragraphs:
        if "Colors" in p.text:
            colors = p.text.strip().split()[0]  # misalnya: "5 Colors" → ambil "5"
            break

    # Size
    size = None
    for p in paragraphs:
        if "Size:" in p.text:
            size = p.text.strip().replace("Size:", "").strip()
            break

    # Gender
    gender = None
    for p in paragraphs:
        if "Gender:" in p.text:
            gender = p.text.strip().replace("Gender:", "").strip()
            break

    # Timestamp
    timestamp = datetime.now().isoformat()

    fashion_products = {
        'Title': title,
        'Price': price,
        'Rating': rating,
        'Colors': colors,
        'Size': size,
        'Gender': gender,
        'Timestamp': timestamp
    }

    return  fashion_products