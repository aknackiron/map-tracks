import sys
import matplotlib.pyplot as plt
import folium
import argparse
import pandas as pd

from gpxpy.gpx import GPX
from file_handling import GPXFileHandling
from db_handling import DBHandling


def get_gpx_lat_lon(gpx: GPX) -> tuple[list[float], list[float]]:
    latitudes = []
    longitudes = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                latitudes.append(point.latitude)
                longitudes.append(point.longitude)
    return latitudes, longitudes


def draw_track_points(latitudes: list[float], longitudes: list[float]) -> None:
    # Create a simple plot using Matplotlib
    plt.plot(longitudes, latitudes, '-o')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('GPS Track')
    plt.show()
    return


def create_html_map(gpx: GPX) -> None:
    # Create a folium map centered around the first track point
    map_center = [gpx.tracks[0].segments[0].points[0].latitude, gpx.tracks[0].segments[0].points[0].longitude]
    my_map = folium.Map(location=map_center, zoom_start=12)

    # Add track points as markers to the map
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                folium.Marker([point.latitude, point.longitude]).add_to(my_map)

    # Save the map to an HTML file
    my_map.save('track_map.html')


def draw_track_line(track: ([float], [float]), tooltip_comment: str = "") -> folium.Map:
    """
    Creates a Folium map object centered at the start of the give track
    @param: track the track to be drawn as a tuple of lat and lon lists of coordinates
    @param: tooltip_comment what should be tooltip for the track
    @return the newly created Folium map object
    """
    mid_point = int(len(track) / 2)
    center = [track[mid_point][0], track[mid_point][1]]
    my_map = folium.Map(location=center, zoom_start=15)
    folium.PolyLine(track, tooltip=tooltip_comment).add_to(my_map)

    return my_map


def add_line_to_map(track: ([float], float), track_map: folium.Map, new_color: str = 'green',
                    tooltip_comment: str = "") -> folium.Map:
    folium.PolyLine(track, tooltip=tooltip_comment, color=new_color).add_to(track_map)

    return track_map

def add_info_marker_to_map(map: folium.Map, lat: float, lon:float, text: str) -> folium.Map:
    folium.Marker([lat, lon], popup=text).add_to(map)
    return map

def save_map_to_file(track_map: folium.map, filename: str = 'track_map.html'):
    track_map.save(filename)

    return True


def lists_to_tuple_list(lat: [float], lon: [float]) -> ([float], [float]):
    tuple_list: list[tuple[float, float]] = []
    if len(lat) != len(lon):
        print("Longitude and latitude lists are of different sizes")
        sys.exit(0)
    for i in range(len(lat)):
        tuple_list.append((lat[i], lon[i]))
    return tuple_list


# Press the green button in the gutter to run the script.
def fit_map(tracks_and_points, track_map):
    data = {'Lat': [], 'Long': []}
    for values in tracks_and_points.values():
        for value in values:
            data['Lat'].append(value[0])
            data['Long'].append(value[1])
    df = pd.DataFrame(data)
    sw = df[['Lat', 'Long']].min().values.tolist()
    ne = df[['Lat', 'Long']].max().values.tolist()
    print("sw point", sw, "ne point", ne)
    track_map.fit_bounds([sw, ne])

    return track_map


if __name__ == '__main__':
    # Create the main parser
    parser = argparse.ArgumentParser(description='Tool to read SportsTracker exported GPX files and draws these on map')

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Define a command 'create-db' with its own set of arguments: read gpx files and store these to the DB
    parser_create_db = subparsers.add_parser('create-db', help='Create or update a tracks DB based on provided GPX files')
    parser_create_db.add_argument('--path_to_files', type=str, help='Path from where GPX files are to be read')
    parser_create_db.add_argument('--db_filename', type=str, help='Name of the existing or new DB file to update or create')

    # Define a command 'command2' with its own set of arguments
    parser_create_map = subparsers.add_parser('create-map', help='Create an HTML map from the tracks in the provided DB')
    parser_create_map.add_argument('--db_filename', type=str, help='DB filename to read the track information')
    # TODO single file name should be optional
    parser_create_map.add_argument('--gpx_filename', type=str, help='A single GPX file to be included on a map')
    parser_create_map.add_argument('--start_date', type=str, help='Start date (included) from which activities are added to map')
    parser_create_map.add_argument('--end_date', type=str, help='End date (included) to which activities are added to map')
    parser_create_map.add_argument('--html_output', type=str, help='Generated html file name')
    # TODO providing activity should be optional?
    parser_create_map.add_argument('--activity', type=str, help='Which activity is picked from the date range. If nothing '
                                                                'provided, then first\'s track\'s activity is used')
    # Parse the command-line arguments
    args = parser.parse_args()

    # Check which command was provided
    if args.command == 'create-db':
        print("Running create-db with params: {}".format(args))
        db_name = args.db_filename
        path_to_tracks = args.path_to_files
        # open and create db
        dbh = DBHandling(db_name)
        dbh.create_gpx_table()
        # create or update db file
        fh = GPXFileHandling()
        fh.store_track_files_to_db(path_to_tracks + "/", dbh)

    elif args.command == 'create-map':
        print("Running create-map with params: {}".format(args))
        db_name = args.db_filename
        single_file = args.gpx_filename
        start_date = args.start_date
        end_date = args.end_date
        output_file = args.html_output
        activity = args.activity

        # draw planned track points to map
        new_map = folium.Map()
        if single_file:
            fh = GPXFileHandling()
            gpx_points = fh.open_gpx(single_file)
            lat, lon = get_gpx_lat_lon(gpx_points)
            latlon = lists_to_tuple_list(lat, lon)
            # TODO, this activity needs to be passed as argument too
            new_map = draw_track_line(latlon, "Planned route")

        dbh = DBHandling(db_name)
        tracks = dbh.get_activity_tracks(start_date, end_date, activity)
        # print("tracks for {} between {} - {}\n{}".format(activity, start_date, end_date, tracks))
        tracks_points = {}
        for track in tracks:
            # print("Getting points for track: {}".format(track))
            latlon = dbh.get_track_points(track)
            track_start_date = dbh.get_track_start_date(track)
            tracks_points.update({track: latlon})
            new_map = add_line_to_map(latlon, new_map, tooltip_comment=activity)
            new_map = add_info_marker_to_map(new_map, latlon[0][0], latlon[0][1], track_start_date)

        new_map = fit_map(tracks_points, new_map)
        save_map_to_file(new_map, output_file)

    else:
        # Handle when no command is provided or an invalid command is given
        print('Invalid command or no command provided.')

    sys.exit(0)