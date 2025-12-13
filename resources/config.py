from pathlib import Path


BASE_DIR = [
    subpath
    for path in Path(".").absolute().parents
    for subpath in path.iterdir()
    if subpath.name == "recipes_htmx"
][0]
DB_PATH = BASE_DIR/"resources"/"db_file.db"
A_DB_URL = f"sqlite+aiosqlite:////{DB_PATH}"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

if __name__ == "__main__":
    print(f"{DB_URL=}")