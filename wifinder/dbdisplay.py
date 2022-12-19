from folium.plugins import MarkerCluster
from sqlite3 import connect
from pathlib import Path

import folium
import json as js
import os

from .display import Display

# populate display for DB upload
class DBDisplay(Display):
    def __init__(self):
        super().__init__(".db, .json", "Connect", "Click to Connect to DB", 'database')

    # ====================
    # Visualization Methods
    # ====================

    def get_struct(self):
        return self.data[list(self.data.keys())[0]]

    # ====================
    # Interaction Methods
    # ====================

    # react to resolve button pressed
    def button_resolve_pressed(self, button):
        try:
            self.db_connect()
            self.upload.children[1].button_style = 'success'
            self.upload.children[2].button_style = 'info'
        except:
            self.upload.children[1].button_style = 'warning'

    # ====================
    # Background Methods
    # ====================

    # create temporary db file
    def tmp_save(self):
        if len(self.upload.children[0].value) > 0:
            os.makedirs("./.tmp", exist_ok=True)
            self.tmp_file = Path(os.path.join("./.tmp", self.upload.children[0].value[0].name)).expanduser().resolve()

            with open(self.tmp_file, "wb") as fp:
                fp.write(self.upload.children[0].value[0].content)
        else:
            return False
        return True

    # delete temporary db file
    def tmp_del(self):
        os.remove(self.tmp_file)

    # ====================
    # Metadata Methods
    # ====================

    # connect to and read database
    def db_connect(self):
        # handle .db/.json upload
        if len(self.upload.children[0].value) > 0:
            ext = self.upload.children[0].value[0].name.split(".")[-1]
            # if .json is uploaded, read from memory and block re-parsing later
            if ext == "json":
                data_raw = js.loads(self.upload.children[0].value[0].content.tobytes())
                data = {}

                for coord_raw in data_raw:
                    coord = tuple([float(k) for k in coord_raw.strip("()").split(", ")])

                    if self.options.children[1].value is False:
                        if coord[0] == 0.0 and coord[1] == 0.0:
                            continue

                    # if duplicate entries is true, always add MAC entry
                    # if duplicate entries is false, only add one MAC entry
                    data[coord] = {'db_meta': [],
                                   'loc_meta': {}}

                    data[coord]['db_meta'] = data_raw[coord_raw]['db_meta'] if self.options.children[
                                                                                   0].value is True else \
                    data_raw[coord_raw]['db_meta'][0]
                    data[coord]['loc_meta'] = data_raw[coord_raw]['loc_meta']

            # if .db is uploaded, save to temp database and connect
            elif ext == "db":
                if not self.tmp_save():
                    # break and pass to error handler if saving cannot occur
                    assert False

                # read sql database
                conn = connect(self.tmp_file)
                cur = conn.cursor()
                cur.execute("SELECT * from WifiLocation")
                rows = cur.fetchall()

                self.tmp_del()

                data = {}
                # format: (lat, lon): [MAC address, 802.11 TSFT Timestamp]
                for row in [r[0:4] for r in rows]:
                    coord = row[2:4]
                    if coord not in data:
                        if self.options.children[1].value is False and (coord[0] == 0.0 and coord[1] == 0.0):
                            continue

                    data[coord] = {'db_meta': [],
                                   'loc_meta': {}
                                   }

                    # if duplicate entries is true, always add MAC entry
                    entry = {'mac': row[0],
                             'manf': "",
                             'cfabsolute': row[1],
                             'timestamp': ""
                             }
                    if self.options.children[0].value is True:
                        data[coord]["db_meta"].append(entry)
                    # if duplicate entries is false, only add one MAC entry
                    elif len(data[coord]["db_meta"]) == 0:
                        data[coord]["db_meta"].append(entry)

            # trim from value cap option
            if self.options.children[2].value > 0:
                data = dict([(key, data[key]) for key in list(data.keys())[0:int(self.options.children[2].value)]])

            self.data = data

    # from metadata, get map object
    def build_map(self):
        self.marker_cluster = MarkerCluster()

        for coord in self.data:
            title = """
            <b>Location:</b><br>
            {}<hr>
            <b>Coordinates:</b><br>
            {} {}<hr>
            <b>MAC Address:</b><br>
            {} <hr>
            <b>Timestamp:</b><br>
            {}"""

            tool = "{} {}".format(coord[0], coord[1])

            if self.options.children[0].value is True:
                # populate by MAC occurance
                for entry in self.data[coord]['db_meta']:
                    title = title.format(self.data[coord]['loc_meta']['display_name'],  # location
                                         coord[0], coord[1],  # coordinates
                                         "{} ({})".format(entry['mac'], entry['manf']) if entry['manf'] != "" else
                                         entry['mac'],  # MAC address
                                         entry['timestamp'])  # timestamp
                    # create point
                    folium.Marker(location=(coord[0], coord[1]),
                                  popup=title,
                                  tooltip=tool
                                  ).add_to(self.marker_cluster)

            else:
                # populate by coord occurance
                entry = self.data[coord]['db_meta'][0]
                title = title.format(self.data[coord]['loc_meta']['display_name'],  # location
                                     coord[0], coord[1],
                                     "{} ({})".format(entry['mac'], entry['manf']) if entry['manf'] != "" else entry[
                                         'mac'],
                                     entry['timestamp'])
                # create point
                folium.Marker(location=(coord[0],
                                        coord[1]),
                              popup=title,
                              tooltip=tool
                              ).add_to(self.marker_cluster)

    # update map from options and display
    def get_map(self):
        start_coords = list(self.data.keys())[0]
        self.map = folium.Map(location=[start_coords[0],
                                        start_coords[1]],
                              zoom_start=2,
                              tiles=self.map_options.children[0].value)
        self.marker_cluster.add_to(self.map)

        self.display(self.map)