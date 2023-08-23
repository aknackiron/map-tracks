import os.path
import sqlite3
import gpxpy
from file_handling import GPXFileHandling


class DBHandling:
    def __init__(self):
        self.connection = None
        self.db_name = ""

    def connect_to_db(self, db_name: str = 'gps_data.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        return self.connection


    def close_connection(self):
        return self.connection.close()


    def create_gpx_table(self):
        c = self.connection.cursor()
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
            self.connection.commit()
            return True
        except sqlite3.OperationalError as e:
            print("table already exists")
            print(e)
            return False


    def insert_track_to(self, connection: sqlite3.Connection, track_name, activity, points):
        c = connection.cursor()
        for point in points:
            c.execute('''
                INSERT INTO gpx_data (track_name, latitude, longitude, elevation, time, activity_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (track_name, point.latitude, point.longitude, point.elevation, point.time, activity))
        connection.commit()


    def store_gpx_points(self, filename: str):
        """
        Read GPX file for content and insert values to database
        :param filename: the filename
        :return: was storing successful or not
        """
        fh = GPXFileHandling()
        # print("current path:", os.path.curdir, "filename:", filename)
        track_name = fh.track_name_from_filename(filename)
        activity = fh.activity_from_filename(filename)
        # print("storing to DB track name '{}' and activity '{}'".format(track_name, activity))
        # Parse GPX file and insert data
        with open(filename, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                points = []
                for segment in track.segments:
                    points.extend(segment.points)
                self.insert_track_to(self.connection, track_name, activity, points)

    def get_all_track_names(self) -> [str]:
        """
        Returns all track names from the DB
        """
        sql_query = "SELECT DISTINCT track_name FROM gpx_data"
        cursor = self.connection.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        track_names = []
        for r in results:
            track_names.append(r[0])
        print("track names in DB:", track_names)
        return track_names
