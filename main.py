import sys
import matplotlib.pyplot as plt
import folium

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


def draw_track_line(track: ([float], float)) -> folium.Map:
    center = [track[0][0], track[0][1]]
    my_map = folium.Map(location=center, zoom_start=15)
    folium.PolyLine(track, tooltip="Run").add_to(my_map)
    my_map.save('track_map.html')
    return my_map


def add_line_to_map(track: ([float], float), track_map: folium.Map, new_color: str = 'green', comment="") -> folium.Map:
    folium.PolyLine(track, tooltip=comment, color=new_color).add_to(track_map)
    track_map.save('track_map.html')

    return track_map


def lists_to_tuple_list(lat: [float], lon: [float]) -> ([float], [float]):
    tuple_list: list[tuple[float, float]] = []
    if len(lat) != len(lon):
        print("Lon and lat of different sizes")
        sys.exit(0)
    for i in range(len(lat)):
        tuple_list.append((lat[i], lon[i]))
    return tuple_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fh = GPXFileHandling()
    dbh = DBHandling()
    # open and create db
    dbh.connect_to_db()
    dbh.create_gpx_table()

    # create or update db file
    # fh.store_track_files_to_db('/Users/niko/Projects/sport-tracks/tracks/', dbh)

    # draw planned track points to map
    gpx_points = fh.open_gpx('tracks/Bike Ride Nice - Brussels.gpx')
    lat, lon = get_gpx_lat_lon(gpx_points)
    latlon = lists_to_tuple_list(lat, lon)
    new_map = draw_track_line(latlon)

    # get actual traveled points and add to map
    start_date = '2023-07-22'
    end_date = '2023-08-07'
    activity = 'Cycling'
    tracks = dbh.get_activity_tracks(start_date, end_date, activity)
    print("tracks for {} between {} - {}\n{}".format(activity, start_date, end_date, tracks))
    tracks_points = {}
    for track in tracks:
        print("Getting points for track: {}".format(track))
        latlon = dbh.get_track_points(track)
        tracks_points.update({track: latlon})
        new_map = add_line_to_map(latlon, new_map)
