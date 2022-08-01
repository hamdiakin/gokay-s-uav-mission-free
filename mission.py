from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import time
from math import sqrt
import pandas as pd
import constants as c
import pandas as pd
import demo_pixhawk as dp
import math
from dronekit import (
    connect,
    VehicleMode,
    LocationGlobalRelative,
    Command,
    LocationGlobal,
)
from math import radians, cos, sin, asin, sqrt



# import pixhawk_mission as pm

# COMMAND 129 is CONDITION_DELAY


class Mission:
    def __init__(self):
        # inherit variables from mission class
        self.tour_no = 1
        self.servo_no = 0
        self.wp_list = []
        self.red_loc_list = []
        self.elapsed_time_undetected = 0
        # self.first_undetected_time = -1
        self.first_detected = False
        # dp.connect_to_pixhawk() # FIXME: uncomment
        self.DEFAULT_ALTITUDE = 20

    # Checks if the current point is within the given polygon
    def check_if_in_area(self, current_location, polygon_list):
        point = Point(current_location.lat, current_location.long)
        polygon = Polygon(polygon_list)
        print(polygon.contains(point))
        return polygon.contains(point)

    # TODO: 1. GDC Algorithm has to be implemented in this particular function
    def detect_location(self, gps_location, camera_location, altitude, comfpass_heading):
        # GDC Algorithm will be implemented here
        # Parameters needed: Location of the image on the camera, the image itself, the area of the red box
        # focal length 3.21mm
        # pixel count 2592*1944 = 5038848
        # Sensor size: 3.67mm x 2.74mm
        altitude = self.DEFAULT_ALTITUDE
        relative_y = altitude * c.gsd_y_constant
        relative_x = altitude * c.gsd_g_constant
        print(f"relative_y: {relative_y}")
        print(f"relative_x: {relative_x}")
        # convert relative_x meters to latitude

    # TODO: Add the locations
    def add_up_locations(self, area, target_cam_loc, gps_location):
        self.first_detected = True
        self.detection_time = time.time()
        altitude = 20
        calculated_location = self.detect_location(
            gps_location, target_cam_loc, altitude
        )
        # Add GPS location of the red box
        self.red_loc_list.append(calculated_location)

    # TODO: upload to the vehicle
    def add_target_waypoint(self,):
        """
        Add the target waypoint to the waypoint list
        """
        for wp in self.wp_list:
            if wp.command == 129 and wp.param1 == 1:
                target_loc = self.find_actual_target_location()

                # create a new Command object
                new_wp = Command(0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                new_wp.command = 16
                new_wp.param1 = 0
                new_wp.param2 = 0
                new_wp.param3 = 0
                new_wp.param4 = 0
                new_wp.x = target_loc.lat
                new_wp.y = target_loc.lon
                new_wp.z = target_loc.alt
                new_wp.frame = 3
                new_wp.current = 0
                new_wp.autocontinue = 1

                print(f"ADD New Waypoint: {new_wp}")
                # FIXME: Check if the waypoint is added successfully
                # replace the current wp with the target waypoint
                self.wp_list[self.wp_list.index(wp)] = target_loc
                self.red_loc_list = []
                return True
        pass

    # def haversine(self, lon1, lat1, lon2, lat2):
    #     """
    #     Calculate the great circle distance in kilometers between two points 
    #     on the earth (specified in decimal degrees lat-lon)
    #     """
    #     # convert decimal degrees to radians
    #     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    #     # haversine formula
    #     dlon = lon2 - lon1
    #     dlat = lat2 - lat1
    #     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    #     c = 2 * asin(sqrt(a))
    #     r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    #     return c * r

    # TODO: find the middle point of each subsequent set of waypoint locations and
    # todo: find the closest point to the red box
    def detect_closest_waypoints(self):
        # * FIXME: this function may be unnecessary
        # waypoint_data = self.get_waypoints(self.vehicle)
        # num_of_waypoints = waypoint_data[1]
        # waypoint_list = waypoint_data[0]

        # subsequent_distance = []
        # for i in range(num_of_waypoints):
        #     subsequent_distance.append(
        #         self.find_center_location(waypoint_list[i], waypoint_list[i + 1])
        #     )

        # red_box = self.find_actual_target_location()
        # for val in subsequent_distance:
        #     if self.distance_between_locations(
        #         red_box, val
        #     ) < self.distance_between_locations(red_box, self.closest_waypoint):
        #         self.closest_waypoint = val
        # return self.closest_waypoint
        pass

    # Get closest waypoint and find the index of it and add up the red box location between the closest waypoint and the next one
    def add_return_waypoint(self):
        """
        Add the return waypoint to the waypoint list
        """
        # closest_waypoint = self.detect_closest_waypoints()
        # wp_list = self.get_waypoints(self.vehicle)
        # index_of_wp = wp_list.index(closest_waypoint)

        # new_wp_list = []

        # for index, wp in enumerate(wp_list):
        #     if index == index_of_wp:
        #         new_wp_list.append(self.find_actual_target_location())
        #     new_wp_list.append(wp)

        # return new_wp_list
        pass

    def get_waypoints(vehicle):
        """
        Get the waypoints from the vehicle
        """
        waypoint_list = dp.get_current_mission(vehicle)[0]
        n_waypoints = dp.get_current_mission(vehicle)[1]
        return waypoint_list, n_waypoints

    # TODO: TEST HERE
    def find_actual_target_location(self):
        """
        Find the actual target location by using the waypoint list that is stored
        """
        # remove outliers
        new_red_loc_list = self.remove_outliers()
        return sum(new_red_loc_list) / len(new_red_loc_list)
    
    # this function will remove the outliers from the red_loc_list
    def remove_outliers(self, list_of_distances):
        sorted_list = sorted(list_of_distances)
        thereshold_index = int(len(sorted_list) * 0.75)
        high = sorted_list[thereshold_index]
        detected_indices = []
        for i in range(len(list_of_distances)):
            if list_of_distances[i] > high:
                list_of_distances.pop(i)
                detected_indices.append(i)
        for index in detected_indices:
            self.red_loc_list.pop(index)
        
    def find_middle_point(self, red_loc_list):
        sum_lat = 0
        sum_lon = 0
        for i in range(len(red_loc_list)):
            sum_lat += red_loc_list[i][0]
            sum_lon += red_loc_list[i][1]
        return [sum_lat/len(red_loc_list), sum_lon/len(red_loc_list)]

    # distance between two points
    def distance_between_locations(loc1, loc2):
        return ((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)**0.5

    # this function will provide a list of distances between every single point and the middle point
    # has to be called first for detection of the red box
    def distance_list_provider(self):
        middle_point = self.find_middle_point(self.red_loc_list)
        raw_distances = []
        for loc in self.red_loc_list:
            raw_distances.append(loc, middle_point)
        return raw_distances


    # TODO: TEST HERE
    def is_tour_finished(self):
        """
        Check if the tour is finished
        """
        for wp in self.wp_list:
            if wp.command == 129 and wp.param1 == 0:
                print("Tour finished")
                return True
            if wp.current == 1:
                return False
        return False

    # TODO: TEST HERE
    def remove_tour_waypoint(self):
        """
        Remove the next tour waypoint from the waypoint list
        """
        for wp in self.wp_list:
            if wp.command == 129 and wp.param1 == 0:
                self.wp_list.remove(wp)
                return True
        return False

    # TODO: check if the drone is in the correct location to launch the bomb
    def is_close(self):
        speed = 20  # Requires Telemetry Data
        alt = 20  # Requires Altimeter Data
        time = sqrt(alt / 5)
        distance = 50  # Requires Image Process Data
        if speed * time <= distance:
            return 1  # Requires Servo Connection Data

    # todo: use free shot (serbest atış) logic to check if the drone is in the correct location
    def is_launch_eligible(self):
        # find the ideal launch distance from the red box (its not certain yet)
        launch_distance = 0.5  # for the distance check out the formulas in the report
        drone_loc = self.vehicle.get_location()
        if (
            self.distance_between_locations(drone_loc, self.closest_waypoint)
            < launch_distance
        ):
            return True

    # Find the center of two locations that returns float value
    def find_center_location(self, location1, location2):
        return (location1.lat + location2.lat) / 2, (location1.lon + location2.lon) / 2

    # Find the distnce between two locations
    def distance_between_locations(self, loc1, loc2):
        return ((loc1.lat - loc2.lat) ** 2 + (loc1.lon - loc2.lon) ** 2) ** 0.5

