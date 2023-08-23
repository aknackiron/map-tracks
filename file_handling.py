import os
import gpxpy
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
        Open the GPX file and return the gpx object read from the file
        :param filename: the file to be read
        :return: GPX object
        """
        with open(filename, 'r') as gpx_file:
            gpx = gpxpy.parse(gpx_file)
        return gpx
