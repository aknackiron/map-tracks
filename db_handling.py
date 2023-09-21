import sqlite3
import gpxpy
from file_handling import GPXFileHandling


class DBHandling:
    def __init__(self, db_filename):
        self.connection = None
        self.db_name = db_filename
        self.connection = sqlite3.connect(self.db_name)

    def connect_to_db(self, db_name: str = 'gps_data.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        return self.connection


    def close_connection(self):
        return self.connection.close()


    def create_gpx_table(self):
        c = self.connection.cursor()
        table_name = 'gpx_data'
        table_query = '''SELECT name FROM sqlite_schema  
                            WHERE type='table' 
                            AND name='{}';'''.format(table_name)
        c.execute(table_query)
        result = c.fetchall()
        if len(result) > 0:
            # table already exists
            return True
        # Create a table to store GPX data
        c.execute('''
            CREATE TABLE IF NOT EXISTS gpx_data (
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


    def insert_track_to(self, track_name, activity, points, date=""):
        c = self.connection.cursor()
        if not points:
            c.execute('''
                INSERT INTO gpx_data (track_name, latitude, longitude, elevation, time, activity_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (track_name, "", "", "", date, activity))
        else:
            for point in points:
                c.execute('''
                    INSERT INTO gpx_data (track_name, latitude, longitude, elevation, time, activity_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (track_name, point.latitude, point.longitude, point.elevation, point.time, activity))
        self.connection.commit()


    def store_gpx_points(self, filename: str):
        """
        Read GPX file for content and insert values to database
        :param filename: the filename
        :return: was storing successful or not
        """
        fh = GPXFileHandling()
        track_name = fh.track_name_from_filename(filename)
        track_date = fh.date_from_filename(filename)
        activity = fh.activity_from_filename(filename)
        # print("storing to DB track name '{}' and activity '{}'".format(track_name, activity))
        # Parse GPX file and insert data
        with open(filename, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
            if not gpx.tracks:
                self.insert_track_to(track_name, activity, [], track_date)
            else:
                for track in gpx.tracks:
                    points = []
                    for segment in track.segments:
                        points.extend(segment.points)
                    self.insert_track_to(track_name, activity, points)
            print("store_gpx_points: {}: {}".format(track_name, gpx.tracks))
        return None

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
        print("tracks already in DB: {}", len(track_names))
        return track_names

    def get_activity_tracks(self, start: str, end: str, activity: str) -> [str]:
        sql_query = '''SELECT DISTINCT(track_name) FROM gpx_data 
                        WHERE date(time) >= date('{}') 
                        AND date(time) <= date('{}') 
                        AND activity_type = '{}' ORDER BY date(time);
        '''.format(start, end, activity)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            print("DB returned these tracks: {}".format(result))
            # clean the results
            tracks = []
            for res in result:
                tracks.append(res[0])
            return tracks
        except sqlite3.Error as e:
            print(e)
            print("Connection error - could not retrieve requested tracks: {}".format(sql_query))
        return []

    def get_track_points(self, track) -> list[(float, float)]:
        sql_query = '''SELECT latitude, longitude FROM gpx_data 
                        WHERE track_name = '{}' 
                        ORDER BY date(time) ;
        '''.format(track)
        # print("sql query for points: {}".format(sql_query))
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(e)
            print("Connection error - could not retrieve requested points: {}".format(sql_query))

        return []

    def get_track_start_date(self, track_name) -> str:
        sql_query = '''SELECT time from gpx_data WHERE track_name = '{}' 
                        ORDER BY date(time) LIMIT 1;'''.format(track_name)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(e)
            print("Connection error - could not retrieve requested track's start date: {}".format(sql_query))
        return ""