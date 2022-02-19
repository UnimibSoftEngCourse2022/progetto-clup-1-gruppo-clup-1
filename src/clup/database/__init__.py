from pathlib import Path

from sqlalchemy import create_engine

from src.clup.database.models import init_db

db_dir = Path(__file__).parent
db_file = db_dir / Path('clup.sqlite')

engine = create_engine(f'sqlite:///{db_file}')

if not db_file.exists():
    init_db(engine)
