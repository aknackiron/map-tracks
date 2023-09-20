import os
import gpxpy
import datetime
from gpxpy.gpx import GPX

"""
This script is used to read in all GPX tracks from files and storing all tracks to a single database.
Only new tracks that are not yet present in the database are added. The track id is used as the identifier.

The time of the activity is read from the file name. All tracks are downloaded using the method described
in this Github repository and discussion: https://gist.github.com/KonstantinosSykas/dfe4c5e392e299ab9341d6e16299454f
Tracks in DB are also added the activity type that is available in the file name of the tracks.
"""


class GPXFileHandling:

    def get_file_listing(self, path: str, file_ending: str = "", file_name_starts_with: str = "") -> [str]:
        """
        Provides a list of file names found in the given path with provided file ending
        :param path: the path to look for files with file ending
        :param file_ending: the file extension to look for
        :return: a list of files found
        """
        files = os.listdir(path)
        files = [f for f in files if os.path.isfile(path + '/' + f)]  # remove any directories
        # filter only files with ending
        if len(file_ending) > 0:
            files = list(filter(lambda f: f.split('.')[1] == file_ending, files))
        if len(file_name_starts_with) > 0:
            files = list(filter(lambda f: f.startswith(file_name_starts_with), files))

        return files

    def activity_from_filename(self, filename: str) -> str:
        """
        Assuming correct file name format is provided, no extra checking at this point
        :param filename: the file from which to extract activity type
        :return: activity type name
        """
        try:
            activity = filename.split('/')[-1].split('-')[1]
            # print("Activity from filename:", activity)
        except IndexError as e:
            activity = "NA"
            print("Unexpected filename format, file format should be SportsTracker-[activity]-....gpx\n\n{}".format(e))
        return activity

    def date_from_filename(self, filename: str) -> str:
        """
        Assuming correct file name is provided, return the activity date stored in the file name in DB assumed syntax
        :param filename: the filename to parse
        :return: date in format %Y-%M-%d
        """
        try:
            track_date = datetime.datetime.strptime(filename.split('/')[-1].split('-')[2], '%Y%m%d').strftime('%Y-%m-%d')
        except IndexError as e:
            track_date = "NA"
            print("Unexpected filename format, file format should be SportsTracker-<activity>-<date>-<track name>.gpx\n\n{}".format(e))
        return track_date


    def track_name_from_filename(self, filename: str) -> str:
        """
        Returns the track identifier from the filename
        :param filename: the SportsTracker exported track name
        :return: track name
        """
        # print("filename '{}' has track name '{}'".format(filename, filename.split('-')[3].split('.')[0]))
        return filename.split('/')[-1].split('.')[0].split('-')[3]

    def open_gpx(self, filename: str) -> GPX:
        """
        Open the .gpx file and return the GPX object read from file
        :param filename: the file to be read
        :return: GPX object
        """
        with open(filename, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
        return gpx

    def store_track_files_to_db(self, path_to_track_files, db) -> None:
        path_to_tracks = path_to_track_files

        # get all tracks files
        track_files = self.get_file_listing(path_to_tracks, 'gpx', 'SportsTracker')
        db_tracks = db.get_all_track_names()
        new_tracks = []
        existing_tracks = []
        # get file track name, check if track name is already in DB
        for f in track_files:
            track_name = self.track_name_from_filename(path_to_tracks + f)
            if track_name in db_tracks:
                # already exists, do nothing
                existing_tracks.append(track_name)
                pass
            else:
                db.store_gpx_points(path_to_tracks + f)
                new_tracks.append(track_name)
        # print("tracks already in DB: \n'{}'".format(existing_tracks))
        # print("new tracks to DB: \n{}".format(new_tracks))
        print("stored {} new tracks to DB with {} already found in DB".format(len(new_tracks), len(existing_tracks)))
        return
