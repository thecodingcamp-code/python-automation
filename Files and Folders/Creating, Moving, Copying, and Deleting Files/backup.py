from pathlib import Path
import shutil

reports = Path("reports")
backup = Path("reports_backup")
backup.mkdir(exist_ok=True)

for file in reports.glob("*.csv"):
    shutil.copy2(file, backup / file.name)