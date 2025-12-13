from datetime import timedelta
from pathlib import Path


BASE_DIR = [
    subpath
    for path in Path(".").absolute().parents
    for subpath in path.iterdir()
    if subpath.name == "recipes_htmx"
][0]
DB_PATH = BASE_DIR/"resources"/"db_file.db"
A_DB_URL = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

VERIFICATION_CODE_LIMIT = timedelta(minutes=5)

if __name__ == "__main__":
    print(f"{DB_URL=}")