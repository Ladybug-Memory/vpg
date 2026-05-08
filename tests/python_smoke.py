import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from python import EmbeddedPostgres, initdb


DATA_DIR = Path("/tmp/vpg_python_smoke_data")


def main() -> None:
    shutil.rmtree(DATA_DIR, ignore_errors=True)
    try:
        initdb(str(DATA_DIR), "postgres")
        with EmbeddedPostgres(str(DATA_DIR), "postgres", "postgres") as pg:
            pg.query("CREATE TABLE py_people (id INT PRIMARY KEY, name TEXT NOT NULL);")
            pg.query("INSERT INTO py_people (id, name) VALUES (1, 'Ada'), (2, 'Grace');")
            result = pg.query("SELECT id, name FROM py_people ORDER BY id;")
            print(result, end="")
            assert "1,Ada" in result
            assert "2,Grace" in result
    finally:
        shutil.rmtree(DATA_DIR, ignore_errors=True)


if __name__ == "__main__":
    main()
