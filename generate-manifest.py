#!/usr/bin/env python3
"""Run this script after adding or removing photos to update photos.json."""

import json
from pathlib import Path

PHOTOS_DIR = Path("photos")
ALLOWED = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def is_photo(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in ALLOWED


root_photos = sorted(f.name for f in PHOTOS_DIR.iterdir() if is_photo(f))

albums = {
    d.name: sorted(f.name for f in d.iterdir() if is_photo(f))
    for d in sorted(PHOTOS_DIR.iterdir())
    if d.is_dir()
}

manifest = {"root": root_photos, "albums": albums}

with open("photos.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"photos.json updated: {len(root_photos)} root photos, {len(albums)} albums")
