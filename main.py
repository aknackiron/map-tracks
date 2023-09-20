import sys
import matplotlib.pyplot as plt
import folium
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
        print("Lon and lat of different sizes")
        sys.exit(0)
    for i in range(len(lat)):
        tuple_list.append((lat[i], lon[i]))
    return tuple_list


# Press the green button in the gutter to run the script.
def fit_bounds(tracks_and_points, track_map):
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
    fh = GPXFileHandling()

    # open and create db
    new_db_filename = 'gps_data.db'
    dbh = DBHandling(new_db_filename)
    dbh.connect_to_db(new_db_filename)
    dbh.create_gpx_table()

    # create or update db file
    # fh.store_track_files_to_db('/Users/niko/Projects/sport-tracks/tracks/', dbh)

    output_filename = 'track_map.html'

    # draw planned track points to map
    single_filename = 'tracks/Bike Ride Nice - Brussels.gpx'
    gpx_points = fh.open_gpx(single_filename)
    lat, lon = get_gpx_lat_lon(gpx_points)
    latlon = lists_to_tuple_list(lat, lon)
    # TODO, this activity needs to be passed as argument too
    new_map = draw_track_line(latlon, "Planned route")

    # get actual traveled points and add to map
    start_date = '2023-07-22'
    end_date = '2023-08-07'
    activity = 'Cycling'

    tracks = dbh.get_activity_tracks(start_date, end_date, activity)
    # print("tracks for {} between {} - {}\n{}".format(activity, start_date, end_date, tracks))
    tracks_points = {}
    markers =
    for track in tracks:
        # print("Getting points for track: {}".format(track))
        latlon = dbh.get_track_points(track)
        track_start_date = dbh.get_track_start_date(track)
        tracks_points.update({track: latlon})
        new_map = add_line_to_map(latlon, new_map, tooltip_comment=activity)
        new_map = add_info_marker_to_map(new_map, latlon[0][0], latlon[0][1], track_start_date)

    new_map = fit_bounds(tracks_points, new_map)
    save_map_to_file(new_map, output_filename)
