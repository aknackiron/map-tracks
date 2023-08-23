import pytest
from file_handling import GPXFileHandling


class TestGPXFileHandling:

    def test_get_files_list(self):
        fh = GPXFileHandling()
        files = fh.get_file_listing('./data/', 'gpx', 'SportsTracker')
        assert (len(files) == 1)
        assert (files[0] == 'SportsTracker-AlpineSkiing-20210215-602ab25caee48f193dbea82a.gpx')

    def test_get_file_activity(self):
        # should be only one match
        fh = GPXFileHandling()
        files = fh.get_file_listing('./data/', 'gpx', 'SportsTracker')
        assert (len(files) == 1)
        activity = fh.activity_from_filename(files[0])
        assert (activity == 'AlpineSkiing')

    def test_track_name_from_filename(self):
        fh = GPXFileHandling()
        files = fh.get_file_listing('./data/', 'gpx', 'SportsTracker')
        assert (len(files) == 1)
        track_name = fh.track_name_from_filename(files[0])
        assert (track_name == '602ab25caee48f193dbea82a')