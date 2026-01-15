from PIL import Image
import os
import oxipng

# Configuration
INPUT_DIR = "."
# VRChat works great with both, but JPG is recommended for speed
OUTPUT_PNG = "posters.png"
OUTPUT_JPG = "posters.jpg"

COLUMNS = 5
ROWS = 2
OUTPUT_WIDTH = 2048
OUTPUT_HEIGHT = 1229

# Create output canvas in 'RGB' (No Alpha)
# VRAM Tip: 2048x1229 RGB takes ~7.5MB VRAM. RGBA takes ~10MB.
atlas = Image.new("RGB", (OUTPUT_WIDTH, OUTPUT_HEIGHT))

expected_files = COLUMNS * ROWS

for i in range(1, expected_files + 1):
    path = os.path.join(INPUT_DIR, f"{i}.png")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing input file: {path}")

    # Convert to RGB (Lossless conversion, removes transparency)
    img = Image.open(path).convert("RGB")

    index = i - 1
    col = index % COLUMNS
    row = index // COLUMNS

    # Float-based coordinates to eliminate gaps
    x_start = int(col * OUTPUT_WIDTH / COLUMNS)
    x_end = int((col + 1) * OUTPUT_WIDTH / COLUMNS)
    y_start = int(row * OUTPUT_HEIGHT / ROWS)
    y_end = int((row + 1) * OUTPUT_HEIGHT / ROWS)
    
    img = img.resize((x_end - x_start, y_end - y_start), Image.LANCZOS)
    atlas.paste(img, (x_start, y_start))

# --- SAVE OPTION 1: HIGH QUALITY JPEG (Recommended for VRChat) ---
# Quality 95 is "perceptually lossless" but 5x smaller than PNG
atlas.save(OUTPUT_JPG, "JPEG", quality=95, optimize=True)

# --- SAVE OPTION 2: OPTIMIZED RGB PNG ---
atlas.save(OUTPUT_PNG, optimize=True)
try:
    print("Optimizing PNG with oxipng (Lossless)...")
    oxipng.optimize(OUTPUT_PNG, level=4)
except Exception as e:
    print(f"oxipng failed: {e}")

# Results comparison
png_size = os.path.getsize(OUTPUT_PNG) / (1024 * 1024)
jpg_size = os.path.getsize(OUTPUT_JPG) / (1024 * 1024)

print(f"\nResults for VRChat:")
print(f"PNG Size: {png_size:.2f} MB (Lossless, slower download)")
print(f"JPG Size: {jpg_size:.2f} MB (95% Quality, much faster download)")