import tkinter
import customtkinter
from tkintermapview import TkinterMapView
import pixhawk
import time

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):

    APP_NAME = "GOKAY S UAV"
    WIDTH = 1600
    HEIGHT = 900

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand("tk::mac::Quit", self.on_closing)

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(
            master=self, width=150, corner_radius=0
        )
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(
            master=self, corner_radius=0, fg_color=self.fg_color
        )
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.button_1 = customtkinter.CTkButton(
            master=self.frame_left,
            text="Set Marker",
            command=self.set_marker_event,
            width=120,
            height=30,
            border_width=0,
            corner_radius=8,
        )
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(
            master=self.frame_left,
            text="Clear Markers",
            command=self.clear_marker_event,
            width=120,
            height=30,
            border_width=0,
            corner_radius=8,
        )
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.button_3 = customtkinter.CTkButton(
            master=self.frame_left,
            text="Refresh Coordinates",
            command=self.refresh_coordinates,
            width=120,
            height=30,
            border_width=0,
            corner_radius=8,
        )
        self.button_3.grid(pady=(20, 0), padx=(20, 20), row=2, column=0)

        self.button_4 = customtkinter.CTkButton(
            master=self.frame_left,
            text="Clear polygons",
            command=self.clear_polygons,
            width=120,
            height=30,
            border_width=0,
            corner_radius=8,
        )
        self.button_4.grid(pady=(20, 0), padx=(20, 20), row=3, column=0)
        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(2, weight=0)

        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        # add info to the top of right frame
        self.info_flight_mode = customtkinter.CTkLabel(
            master=self.frame_right,
            text=f"Flight Mode:{pixhawk.get_flight_mode()}",
            width=120,
            height=30,
            anchor="w",
        )
        self.info_flight_mode.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.info_battery_percentage = customtkinter.CTkLabel(
            master=self.frame_right,
            text=f"Battery Percentage:{pixhawk.get_battery_percentage()}",
            width=120,
            height=30,
            anchor="w",
        )
        self.info_battery_percentage.grid(pady=(20, 0), padx=(20, 20), row=0, column=1)

        self.info_speed = customtkinter.CTkLabel(
            master=self.frame_right,
            text=f"Speed:{pixhawk.get_speed()}",
            width=120,
            height=30,
            anchor="w",
        )
        self.info_speed.grid(pady=(20, 0), padx=(20, 20), row=0, column=2)

        # ============ create map widget ============
        self.map_widget = TkinterMapView(self.frame_right, corner_radius=11)
        self.map_widget.grid(
            row=1,
            rowspan=1,
            column=0,
            columnspan=3,
            sticky="nswe",
            padx=(20, 20),
            pady=(20, 0),
        )
        # self.map_widget.set_address("Berlin")

        self.entry = customtkinter.CTkEntry(
            master=self.frame_right,
            placeholder_text="type address",
            width=140,
            height=30,
            corner_radius=8,
        )
        self.entry.grid(row=2, column=0, sticky="we", padx=(20, 0), pady=20)
        self.entry.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(
            master=self.frame_right,
            height=30,
            text="Search",
            command=self.search_event,
            border_width=0,
            corner_radius=8,
        )
        self.button_5.grid(row=2, column=1, sticky="w", padx=(20, 0), pady=20)

        self.slider_1 = customtkinter.CTkSlider(
            master=self.frame_right,
            width=200,
            height=16,
            from_=0,
            to=19,
            border_width=5,
            command=self.slider_event,
        )
        self.slider_1.grid(row=2, column=2, sticky="e", padx=20, pady=20)
        self.slider_1.set(self.map_widget.zoom)

        # ============ DRAW PATHS TO MAP ============

        self.loc_list = pixhawk.get_location_list()

        self.loc_x_list = []
        self.loc_y_list = []
        self.path_list = []
        self.polygon_list = []

        # place marker for each location and write the index of the location to the marker
        for index, loc in enumerate(self.loc_list, 1):
            self.place_marker(loc.x, loc.y, text=str(index))
            self.loc_x_list.append(loc.x)
            self.loc_y_list.append(loc.y)
            self.path_list.append((loc.x, loc.y))

        # draw path
        self.map_widget.set_path(self.path_list)

        # go to the average of the locations
        self.map_widget.set_position(
            sum(self.loc_x_list) / len(self.loc_x_list),
            sum(self.loc_y_list) / len(self.loc_y_list),
        )

        # zoom to the average of the locations
        self.map_widget.set_zoom(16)
        self.map_widget.add_left_click_map_command(self.left_click_event)
        self.loc_download_time = time.time()

        self.update_app()

    def update_app(self):
        battery_percentage = pixhawk.get_battery_percentage()
        self.info_battery_percentage.configure(
            text=f"Battery Percentage:{battery_percentage}"
        )

        speed = pixhawk.get_speed()
        self.info_speed.configure(text=f"Speed:{speed}")

        flight_mode = pixhawk.get_flight_mode()
        self.info_flight_mode.configure(text=f"Flight Mode:{flight_mode}")

        self.after(100, self.update_app)

    def clear_polygons(self):
        # get current x,y
        x, y = self.map_widget.get_position()
        # clear polygons
        self.polygon_list = (x, y)
        self.map_widget.set_polygon(self.polygon_list)

    def get_polygon_list(self):
        return self.polygon_list

    def refresh_coordinates(self):
        self.loc_download_time = time.time()
        self.loc_list = pixhawk.get_location_list()
        path_list = []
        # place marker for each location and write the index of the location to the marker
        for index, loc in enumerate(self.loc_list, 1):
            self.place_marker(loc.x, loc.y, text=str(index))
            self.loc_x_list.append(loc.x)
            self.loc_y_list.append(loc.y)
            self.path_list.append((loc.x, loc.y))

        # draw path
        self.map_widget.set_path(self.path_list)

    def left_click_event(self, coordinates_tuple):
        # add a point to polygon list
        self.polygon_list.append(coordinates_tuple)
        # reset polygons
        self.map_widget.set_polygon(self.polygon_list)

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())
        self.slider_1.set(self.map_widget.zoom)

    def slider_event(self, value):
        self.map_widget.set_zoom(value)

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(
            self.map_widget.set_marker(current_position[0], current_position[1])
        )

    def place_marker(self, lat, lon, text=""):
        print("place_marker", lat, lon)
        # self.map_widget.set_position(lat, lon)
        self.marker_list.append(self.map_widget.set_marker(lat, lon, text=text))

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
