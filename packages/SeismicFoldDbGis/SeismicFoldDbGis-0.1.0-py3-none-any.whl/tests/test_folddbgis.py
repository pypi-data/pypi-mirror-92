import unittest
from shutil import copyfile
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.event import listen
from SeismicFoldDbGis.FoldDbGis import FoldDbGis


def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')


class FoldDbGisTestCase(unittest.TestCase):
    def test(self):
        csv_file = 'tests/data/test-simple.fold.csv'
        empty_file = 'tests/data/empty.sqlite'
        db_file = 'tests/data/fold.sqlite'
        copyfile(empty_file, db_file)

        engine = create_engine('sqlite:///' + db_file, echo=False)
        listen(engine, 'connect', load_spatialite)

        fold = FoldDbGis(db_engine=engine, verbose=True)

        fold.create_table()

        fold.delete_table()

        fold.create_table()

        fold.load_from_csv(csv_file)

        fold.update_from_csv(csv_file)

        rem = pathlib.Path(db_file)
        rem.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
