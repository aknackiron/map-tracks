import sys
import matplotlib.pyplot as plt
import folium

from gpxpy.gpx import GPX
from file_handling import GPXFileHandling


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

def add_line_to_map(track: ([float], float), track_map: folium.Map, new_color: str='green') -> folium.Map:
    folium.PolyLine(track, tooltip="Something else", color=new_color).add_to(track_map)
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
    gpx_points = fh.open_gpx('tracks/SportsTracker-Cycling-20230803-64cbb65a281fe01c2345297a.gpx')
    lat, lon = get_gpx_lat_lon(gpx_points)
    latlon = lists_to_tuple_list(lat, lon)
    # draw_track_points(lat, lon)
    # create_html_map(gpx_points)
    new_map = draw_track_line(latlon)
    gpx_points = fh.open_gpx('tracks/Bike Ride Nice - Brussels.gpx')
    lat, lon = get_gpx_lat_lon(gpx_points)
    latlon = lists_to_tuple_list(lat, lon)
    new_map = add_line_to_map(latlon, new_map)