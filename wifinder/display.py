from IPython.display import display, clear_output

import ipywidgets as widgets

import json as js

# display base class
class Display(object):
    def __init__(self,
                 accepted_filetypes: str,
                 button_desc: str,
                 button_tooltip: str,
                 button_icon: str
                 ):
        self.output = widgets.Output()
        self.data = {}

        # create upload tab
        uploader = widgets.FileUpload(accept=accepted_filetypes,
                                      multiple=False)
        button_resolve = widgets.Button(description=button_desc,
                                        disabled=False,
                                        tooltip=button_tooltip,
                                        button_style='info',
                                        icon=button_icon)
        button_resolve.on_click(self.button_resolve_pressed)
        button_save = widgets.Button(description="Save Results",
                                     disabled=False,
                                     tooltip="Save Metadata to JSON",
                                     button_style='info',
                                     icon='download')
        button_save.on_click(self.button_save_pressed)
        self.upload = widgets.HBox([uploader, button_resolve, button_save])

        # create file options tab
        check_unique = widgets.Checkbox(value=True,
                                        description='Include duplicate entries',
                                        disabled=False,
                                        indent=False)
        check_zeroes = widgets.Checkbox(value=False,
                                        description='Include unresolved entries',
                                        disabled=False,
                                        indent=False)
        int_max = widgets.IntText(value=None,
                                  description="Max entries",
                                  disabled=False,
                                  layout=widgets.Layout(width='initial'))
        self.options = widgets.HBox([check_unique, check_zeroes, int_max])

        # create map options tab
        dropdown_map = widgets.Dropdown(options=['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner',
                                                 'Stamen Watercolor', 'CartoDB positron', 'CartoDB dark_matter'],
                                        value='OpenStreetMap',
                                        description='Map type',
                                        disabled=False)
        self.map_options = widgets.HBox([dropdown_map])

        # create struct object (contains all other objects)
        self.struct = widgets.Tab()
        self.struct.children = [self.upload, self.options, self.map_options]
        self.struct.titles = ["Upload File", " File Options", "Map Options"]
        self.display(self.struct)

    # ====================
    # Interaction Methods
    # ====================

    # react to resolve button pressed
    def button_resolve_pressed(self, button):
        return None

    # react to JSON save button pressed
    def button_save_pressed(self, button):
        try:
            json_dict = dict([(str(key), self.data[key]) for key in list(self.data.keys())])
            json_obj = js.dumps(json_dict, indent=4)
            with open("./json_{}.json".format(self.upload.children[0].value[0].name), "w", encoding="utf-8") as jf:
                jf.write(json_obj)
            self.upload.children[2].button_style = 'success'
        except:
            self.upload.children[2].button_style = 'warning'

    # ====================
    # Visualization Methods
    # ====================

    # create temporary progress bar
    def get_progress(self, val: int):
        return widgets.IntProgress(
            value=0,
            min=0,
            max=val,
            description="Processing",
            bar_style="success",
            style={"bar_color": "yellow"},
            orientation="horizontal")

    def display(self, obj):
        clear_output()
        display(obj)