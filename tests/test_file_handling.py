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
        filename = '/Users/xxx/Projects/yyy/tests/data/SportsTracker-AlpineSkiing-20210215-602ab25caee48f193dbea82a.gpx'
        expected = 'AlpineSkiing'
        activity = fh.activity_from_filename(filename)
        assert (activity == expected)
        filename = 'SportsTracker-AlpineSkiing-20210215-602ab25caee48f193dbea82a.gpx'
        activity = fh.activity_from_filename(filename)
        assert (activity == expected)
        filename = './data/SportsTracker-AlpineSkiing-20210215-602ab25caee48f193dbea82a.gpx'
        activity = fh.activity_from_filename(filename)
        assert (activity == expected)

    def test_track_name_from_filename(self):
        filename = '/Users/xxx/Projects/yyy/tests/data/SportsTracker-AlpineSkiing-20210215-602ab25caee48f193dbea82a.gpx'
        expected = '602ab25caee48f193dbea82a'
        fh = GPXFileHandling()
        track_name = fh.track_name_from_filename(filename)
        assert (track_name == expected)
        filename = 'SportsTracker-AlpineSkiing-20210215-602ab25caee48f193dbea82a.gpx'
        track_name = fh.track_name_from_filename(filename)
        assert (track_name == expected)
        filename = './data/SportsTracker-AlpineSkiing-20210215-602ab25caee48f193dbea82a.gpx'
        track_name = fh.track_name_from_filename(filename)
        assert (track_name == expected)
        filename = '/Users/user/Projects/some-path/tests/data/SportsTracker-AlpineSkiing-20210215-602ab25caee48f193dbea82a.gpx'
        track_name = fh.track_name_from_filename(filename)
        assert (track_name == expected)
