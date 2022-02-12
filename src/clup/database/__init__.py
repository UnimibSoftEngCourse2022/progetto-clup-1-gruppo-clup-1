from pathlib import Path

from sqlalchemy import create_engine

from src.clup.database.models import create_initial_data


db_dir = Path(__file__).parent
db_file = db_dir / Path('clup.sqlite')

if not db_file.exists():
    engine = create_engine(f'sqlite:///{db_file}')
    create_initial_data(engine)
