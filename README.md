# README #

I wanted to play with Python's Panda libraries and do some GPX visualization and what better source of data than 
my own tracks that I have cycled or ran. Let's see what everything I get to track and graph here. 



### What is this repository for? ###

A tool to draw maps based on tracks read from Suunto's Sports-Tracker app. I made this as I wanted to write blogs about 
my trips and didn't want to only add an image of the trip. I could have added links to the maps available in most sports 
tracking applications. Nevertheless, I wanted to create something, so I did this. 



### How do I get set up? ###

Running the Python script is straight forward, but getting the necessary GPX files from sports-tracker.com (or any 
other service) may be more work. 
 
* Download this repository locally
* Create a pip virtual environment (`venv3`) to not mess your local setup: `python3 -m venv venv3`
* Pip install all necessary requirements from the requirements.txt file: `pip install -r requirements.txt`
* Getting SportStracker data. I used the scripts from this [Github repository](https://gist.github.com/KonstantinosSykas/dfe4c5e392e299ab9341d6e16299454f)
  * Be sure to take the newer approach into use that stores the tracks with activity and date in the file name. I use 
    this information when storing the tracks to a local DB
  * Save all downloaded .gpx files into one directory
* This script has two use cases:
  * Read all .gpx files and store track points, time, date and activity type to a local sqlite DB
  * Create an html page based on the data from the DB

### Example Uses ###

There is a basic help available.

```python
✗ python track-map.py --help
usage: track-map.py [-h] {create_db,create_map} ...

Tool to read SportsTracker exported GPX files and draws these on map

positional arguments:
  {create_db,create_map}
                        Available commands
    create_db           Create or update a tracks DB based on provided GPX files
    create_map          Create an HTML map from the tracks in the provided DB

options:
  -h, --help            show this help message and exit
```

To create the local DB from the downloaded gpx files, use the `create_db` command.

```python
✗ python track-map.py create_db --path_to_files tracks/ --db_file out.db 
```

To create a web page of your activity, run the script with `create_map`.

```python
✗ python track-map.py create_map --db_file out.db --start_date 2023-06-06 --end_date 2023-06-07 --html_output route.html --activity Cycling --gpx_file ~/Downloads/2023-09-21_1318006646_my_gpx.gpx 
```

The generated html can be viewed with any web browser. 

Help for knowing what parameters are required/available you can do

```python
 ✗ python track-map.py create_map --help
usage: track-map.py create_map [-h] [--db_file DB_FILE] [--gpx_file GPX_FILE] [--start_date START_DATE] [--end_date END_DATE] [--html_output HTML_OUTPUT]
                               [--activity ACTIVITY]

options:
  -h, --help            show this help message and exit
  --db_file DB_FILE     DB filename to read the track information
  --gpx_file GPX_FILE   A single GPX file to be included on a map
  --start_date START_DATE
                        Start date (included) from which activities are added to map
  --end_date END_DATE   End date (included) to which activities are added to map
  --html_output HTML_OUTPUT
                        Generated html file name
  --activity ACTIVITY   Which activity is picked from the date range. If nothing provided, then first's track's activity is used
```

### To Do or Wishlist ###

I have several ideas on how to improve this. I want to make it easier to include the created maps to a Sphinx 
documentation project. Let's see if and how this proceeds. Below is my backlog :-) of some things I've done or may do 
in the future. 

* ~I want to draw a planned route (from GPX) with an actual route on same map~
* ~store all my activities in a sqlite3 database and make queries for segments and track points there~
* try to include some energy consumption information per each segment? It could be interesting to get to know how the 
  algorithms for calculating these work?
  * total energy consumed over a period of time
* get information on max and min speeds over a period of time - there's probably a library for this already I could use?
* get max and min temperatures for segments over a period of time for the locations in the segments (maybe only start 
 and stop location is enough?)
* get max and min altitudes for segments over a period of time
* check if there are extra requirements in requirements.txt file
