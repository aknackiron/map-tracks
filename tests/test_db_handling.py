import pytest

from db_handling import DBHandling
import os


def remove_db_file(dbfile):
    # if db file already exists remove it first
    if os.path.exists(dbfile):
        os.remove(dbfile)
        print("test db file existed and now removed: {}".format(dbfile))
    assert (not os.path.exists(dbfile))


@pytest.fixture(autouse=True, scope='class')
def setup(request):
    request.cls.db_filename = 'test.db'
    remove_db_file(request.cls.db_filename)


class TestDBHandling:

    def test_create_db(self):
        dbh = DBHandling()
        con = dbh.connect_to_db(self.db_filename)
        dbh.close_connection()
        assert (os.path.exists(self.db_filename))


    def test_create_gpx_table(self):
        dbh = DBHandling()
        con = dbh.connect_to_db(self.db_filename)
        dbh.create_gpx_table()
        sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
        cursor = con.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print(results)
        dbh.close_connection()
        assert (len(results) == 2)
        assert (('gpx_data',) in results)

    def test_insert_track_data(self):
        dbh = DBHandling()
        con = dbh.connect_to_db(self.db_filename)
        dbh.create_gpx_table()
        dbh.store_gpx_points('/Users/niko/Projects/sport-tracks/tests/data/SportsTracker-AlpineSkiing-20210215-602ab25caee48f193dbea82a.gpx')
        sql_query = "SELECT COUNT(*) FROM gpx_data;"
        cursor = con.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print(results)
        assert (int(results[0][0]) == 897)

    def test_get_all_track_names(self):
        dbh = DBHandling()
        con = dbh.connect_to_db(self.db_filename)
        dbh.create_gpx_table()
        dbh.store_gpx_points(
            '/Users/niko/Projects/sport-tracks/tests/data/SportsTracker-AlpineSkiing-20210215-602ab25caee48f193dbea82a.gpx')
        tracks = dbh.get_all_track_names()
        assert (len(tracks) == 1)
