from PIL import Image
import os

# Configuration
INPUT_DIR = "."
OUTPUT_FILE = "posters.png"

COLUMNS = 5
ROWS = 2

OUTPUT_WIDTH = 1600
OUTPUT_HEIGHT = 960

TILE_WIDTH = OUTPUT_WIDTH // COLUMNS   # 320
TILE_HEIGHT = OUTPUT_HEIGHT // ROWS    # 480

# Create output canvas
atlas = Image.new("RGBA", (OUTPUT_WIDTH, OUTPUT_HEIGHT))

expected_files = COLUMNS * ROWS

for i in range(1, expected_files + 1):
    path = os.path.join(INPUT_DIR, f"{i}.png")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing input file: {path}")

    img = Image.open(path).convert("RGBA")

    # Resize while forcing exact tile size (aspect ratio already matches)
    img = img.resize((TILE_WIDTH, TILE_HEIGHT), Image.LANCZOS)

    index = i - 1
    col = index % COLUMNS
    row = index // COLUMNS

    x = col * TILE_WIDTH
    y = row * TILE_HEIGHT

    atlas.paste(img, (x, y))

atlas.save(OUTPUT_FILE, optimize=True)
print(f"Generated {OUTPUT_FILE} ({OUTPUT_WIDTH}x{OUTPUT_HEIGHT})")
