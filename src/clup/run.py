import pathlib

from app import app
import sys

current = pathlib.Path(__file__).resolve()
project_root = current.parent.parent.parent
sys.path.append(str(project_root))

if __name__ == "__main__":
    app.run(debug=True)