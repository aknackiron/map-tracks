import os.path
import sqlite3
import gpxpy
from file_handling import GPXFileHandling


class DBHandling:

    def create_db(self, db_name: str = 'gps_data.db'):
        return sqlite3.connect(db_name)


    def close_connection(self, connection: sqlite3.Connection):
        return connection.close()


    def create_gpx_db_table(self, connection: sqlite3.Connection):
        c = connection.cursor()
        # Create a table to store GPX data
        try:
            c.execute('''
                CREATE TABLE gpx_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    track_name TEXT,
                    latitude REAL,
                    longitude REAL,
                    elevation REAL,
                    time TEXT,
                    activity_type TEXT
                )
            ''')
            connection.commit()
            return True
        except sqlite3.OperationalError as e:
            print("table already exists")
            print(e)
            return False


    def insert_track_to_db(self, connection: sqlite3.Connection, track_name, activity, points):
        c = connection.cursor()
        for point in points:
            c.execute('''
                INSERT INTO gpx_data (track_name, latitude, longitude, elevation, time, activity_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (track_name, point.latitude, point.longitude, point.elevation, point.time, activity))
        connection.commit()


    def gpx_points_to_db(self, filename: str, connection: sqlite3.Connection):
        """
        Read GPX file for content and insert values to database
        :param filename: the filename
        :return: was storing successful or not
        """
        fh = GPXFileHandling()
        print(os.path.curdir)
        track_name = fh.track_name_from_filename(filename)
        activity = fh.activity_from_filename(filename)
        # Parse GPX file and insert data
        with open(filename, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                points = []
                for segment in track.segments:
                    points.extend(segment.points)
                self.insert_track_to_db(connection, track_name, activity, points)

