from pathlib import Path

downloads = Path("sample_downloads")
downloads.mkdir(exist_ok=True)

sample_files = [
    "invoice_march.pdf",
    "vacation_photo.jpg",
    "notes.txt",
    "budget.csv",
    "presentation.pptx",
    "screenshot.png",
    "readme.txt",
]

for filename in sample_files:
    (downloads / filename).write_text("sample content")