from pathlib import Path

downloads = Path("sample_downloads")

for file in downloads.iterdir():
    if file.is_file():
        extension = file.suffix.lstrip(".") or "misc"
        target_folder = downloads / extension
        target_folder.mkdir(exist_ok=True)
        file.rename(target_folder / file.name)