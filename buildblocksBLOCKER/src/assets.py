from pathlib import Path
import os

# Create assets directory structure
ASSETS_DIR = Path(__file__).parent / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
BACKGROUNDS_DIR = ASSETS_DIR / "backgrounds"
DECORATIONS_DIR = ASSETS_DIR / "decorations"

# Create directories if they don't exist
for directory in [ASSETS_DIR, ICONS_DIR, BACKGROUNDS_DIR, DECORATIONS_DIR]:
    directory.mkdir(exist_ok=True) 