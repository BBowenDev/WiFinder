# WiFinder
#### A Python-based approach to digital forensics geolocation
WiFinder is a Jupyter-based project that ingests iOS WiFi database files (i.e., `consolidated.db`) and outputs a map of locations with relevant metadata.

WiFinder will also ingest lists of IP addresses and output a map of locations with relevant metada.

## Installation
Ensure that `Python>=3.2` and `pip` are installed.

Clone the repository:
```
git clone https://github.com/BraedenLB/WiFinder.git
cd WiFinder
```

### Requirements
Create and activate a new virtual envinronment:
```
python3 -m venv wfenv
source wfenv/bin/activate
```

Install module requirenents:
```
pip install -r requirements.txt
```

## Usage 
The `wifinder` module contains data structure classes that do not perform advanced metadata querying on their own. API queries are defined per-class in the `2. Metadata Consumption` subsections of `WiFinder.ipynb`.

### Start Jupyter
Start Jupyter Lab and click the custom populated link.
```
jupyter-lab --port=8000
```

### Boilperplate Code
In `WiFinder.ipynb`, run the `Boilerplate > Setup` subsection. Per-class code is also included in `Boilerplate`, but import from the `wifinder` module is covered during import.

## DBDisplay 
Once the setup is complete, the `DBDisplay` section can run autonomously.

`DBDisplay` consists of an interactive settings UI, a code block, and an interactive map object. The `1. Data Ingest` subsection spawns the settings UI, in which `consolidated.db` can be uploaded. **File Settings** and **Map Settings** tabs are included, which allows users to limit queries. 

### Database Connections
Once desired settings are input, connect to the database with the `Connect` button. `DBDisplay` will read and store database-level data in **DBDisplay.data**. If the `Connect` button turns yellow, the uploaded file was unable to be read; if it turns green, processing occurred correctly. Once database-level processing is complete, subsection `2. Metadata Consumption`, which generates query-level metadata (e.g., MAC data, location data), can run.

### Saves and JSON Queries
The **Upload File** tab includes a `Save Results` button that formats extant metadata stored in the DBDisplay.data object to a local JSON dictionary. `DBDisplay` can ingest JSON files; if you do upload a previously created JSON dictionary, skip subsection `2. Metadata Consumption`. If the `Save Results` button turns yellow, metadata was unable to be saved; if it turns green, saving occurred successfully.

### Map Display
The `3. Map Plotting` subsection formats DBDisplay.data generated from subsection `2.` or read from a JSON dictionary into Folium Markers, which are plotted to a Folium Map. The map should automatically display once compiled.

## IPDisplay
Once the setup is complete, the `IPDisplay` section can run autonomously.

`IPDisplay` operates in the same framework as `DBDisplay`, but ingests a .txt/.ip list. JSON dictionary reading is not currently available, so `2. Metadata Consumption` is required.
