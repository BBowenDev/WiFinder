from folium.plugins import MarkerCluster

import requests
import folium

from .display import Display

# populate display for IP uploads
class IPDisplay(Display):
    def __init__(self):
        super().__init__(".ip, .txt", "Search", "Click to Search IPs", 'wifi')
        self.map_options.children[0].value = "CartoDB positron"

    # ====================
    # Interaction Methods
    # ====================

    # react to resolve button pressed
    def button_resolve_pressed(self, button):
        try:
            if len(self.upload.children[0].value) > 0:
                ips = self.upload.children[0].value[0].content.tobytes().decode().replace('\r', '').split('\n')

                for ip in ips:
                    self.data[ip] = {}
            self.upload.children[1].button_style = 'success'
            self.upload.children[2].button_style = 'info'
        except:
            self.upload.children[1].button_style = 'warning'

    # ====================
    # Collection Methods
    # ====================

    # query ipapi API for metadata
    def get_loc(self, ip_addr):
        try:
            return requests.get(f'https://ipapi.co/{ip_addr}/json/').json()
        except:
            return None

    # format returned metadata to data struct
    def format_meta(self, ip_addr, meta):
        if meta is None:
            self.data[ip_addr] = None
        elif 'error' in meta:
            self.data[ip_addr] = None
        elif meta['latitude'] is None or meta['longitude'] is None:
            self.data[ip_addr] = None
        else:
            self.data[ip_addr] = meta
            self.data[ip_addr]['coord'] = [meta['latitude'], meta['longitude']]

    # ====================
    # Metadata Methods
    # ====================

    # from metadata, get map object
    def build_map(self):
        self.marker_cluster = MarkerCluster()
        for ip in self.data:
            # for simplicity,
            if self.data[ip] is None:
                continue

            title = """
            <b>IP Address</b><br>
            {}<hr>
            <b>Organization</b><br>
            {}<hr>
            <b>Network</b><br>
            {}<hr>
            <b>Location</b><br>
            {}<hr>
            <b>Timezone</b><br>
            {}"""

            tool = ip

            # populate map by IP address
            title = title.format(self.data[ip]['ip'],
                                 self.data[ip]['org'],
                                 self.data[ip]['network'],
                                 "{}, {}, {} {}".format(self.data[ip]['city'],
                                                        self.data[ip]['region'],
                                                        self.data[ip]['country_name'],
                                                        "({})".format(self.data[ip]['postal']) if self.data[ip][
                                                                                                      'postal'] is not None else ""
                                                        ),
                                 self.data[ip]['timezone']
                                 )
            # add marker to marker cluster
            folium.Marker(location=(self.data[ip]['coord'][0],
                                    self.data[ip]['coord'][1]),
                          popup=title,
                          tooltip=tool
                          ).add_to(self.marker_cluster)

    # update map from options and display
    def get_map(self):
        start_coords = self.data[list(self.data.keys())[0]]['coord']
        self.map = folium.Map(location=[start_coords[0],
                                        start_coords[1]],
                              zoom_start=2,
                              tiles=self.map_options.children[0].value)
        self.marker_cluster.add_to(self.map)

        self.display(self.map)