from PIL import Image
import os

# Configuration
INPUT_DIR = "."
OUTPUT_FILE = "posters.png"

COLUMNS = 5
ROWS = 2

# Dimensions scaled to 2048 width (Original aspect ratio 5:3)
OUTPUT_WIDTH = 2048
OUTPUT_HEIGHT = 1229

# Create output canvas
atlas = Image.new("RGBA", (OUTPUT_WIDTH, OUTPUT_HEIGHT))

expected_files = COLUMNS * ROWS

for i in range(1, expected_files + 1):
    path = os.path.join(INPUT_DIR, f"{i}.png")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing input file: {path}")

    img = Image.open(path).convert("RGBA")

    index = i - 1
    col = index % COLUMNS
    row = index // COLUMNS

    # Calculate exact boundaries to eliminate rounding gaps
    # We calculate the start and end as floats, then cast to int
    x_start = int(col * OUTPUT_WIDTH / COLUMNS)
    x_end = int((col + 1) * OUTPUT_WIDTH / COLUMNS)
    
    y_start = int(row * OUTPUT_HEIGHT / ROWS)
    y_end = int((row + 1) * OUTPUT_HEIGHT / ROWS)
    
    # Calculate target dimensions for this specific tile
    target_w = x_end - x_start
    target_h = y_end - y_start

    # Resize and paste into the calculated slot
    img = img.resize((target_w, target_h), Image.LANCZOS)
    atlas.paste(img, (x_start, y_start))

atlas.save(OUTPUT_FILE, optimize=True)
print(f"Generated {OUTPUT_FILE} ({OUTPUT_WIDTH}x{OUTPUT_HEIGHT})")