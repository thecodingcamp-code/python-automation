from pathlib import Path
import os 

structure = {
    "project/src/main.py": "print('hello')",
    "project/src/utils.py": "def helper(): pass",
    "project/assets/logo.png": "fake image bytes",
    "project/assets/banner.jpg": "fake image bytes",
    "project/node_modules/pkg/index.js": "module.exports = {}",
    "project/.git/config": "git config data",
}

for path_str, content in structure.items():
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    
project = Path("project")
skip_folders = {".git", "node_modules"}
image_extensions = {".jpg", ".png"}

images = []
for dirpath, dirnames, filenames in os.walk("project"):
    dirnames[:] = [d for d in dirnames if d not in skip_folders]
    for name in filenames:
        candidate = Path(dirpath) / name
        if candidate.suffix.lower() in image_extensions:
            images.append(candidate)

print(images)