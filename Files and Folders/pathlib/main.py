from pathlib import Path

base_path = Path("data")
report_path = base_path / "reports" / "january.csv"
print(report_path)

relative = Path("data/reports/january.csv")
print(relative.resolve())

file_path = Path("reports/january.csv")
print(file_path.name)    # january.csv
print(file_path.stem)    # january
print(file_path.suffix)  # .csv

deep_path = Path("data/reports/2026/january.csv")
print(deep_path.parent)       # data/reports/2026
print(deep_path.parents[1])   # data/reports

target = Path("reports/january.csv")
print(target.exists())   # True or False
print(target.is_file())  # confirms it's a file
print(target.is_dir())   # confirms it's a folder

new_folder = Path("data/reports/2026")
new_folder.mkdir(parents=True, exist_ok=True)

current_dir = Path(".")
for item in current_dir.iterdir():
    print(item)
    
    

text_files = list(current_dir.glob("*.txt"))
print(text_files)

all_text_files = list(current_dir.rglob("*.txt"))


notes = Path("notes.txt")
notes.write_text("Automation notes for today.")
content = notes.read_text()
print(content)

old_file = Path("notes.txt")
old_file.unlink()

empty_folder = Path("data/temp")
empty_folder.rmdir()