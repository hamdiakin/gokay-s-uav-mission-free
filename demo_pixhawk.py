import time, os
from dronekit import (
    connect,
    VehicleMode,
    LocationGlobalRelative,
    Command,
    LocationGlobal,
)
from pymavlink import mavutil
import mission


class Pixhawk:
    def __init__(self):
        # --------------------------------------------------
        # -------------- INITIALIZE
        # --------------------------------------------------
        # -- Setup the commanded flying speed
        self.gnd_speed = 7  # [m/s]
        self.mode = "GROUND"
        self.connect_to_pixhawk()

    # --------------------------------------------------
    # -------------- CONNECTION
    # --------------------------------------------------
    def connect_to_pixhawk(self):
        # -- Connect to the vehicle
        print("Connecting...")
        # get files in '/dev/serial/by-id/'
        serial_ports = os.listdir("/dev/serial/by-id/")
        # vehicle = connect("udp:127.0.0.1:14551")
        # vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)
        for port in reversed(serial_ports):
            # if index != 1:
            #     continue
            print(port)
            try:
                self.vehicle = connect(
                    "/dev/serial/by-id/" + port,
                    baud=115200,
                    wait_ready=True,
                    timeout=5,
                    heartbeat_timeout=5,
                    # disable heartbeat logs
                    mavlink10=False,
                )

                print("Connected to Pixhawk")
                return self.vehicle
            except:
                print("Failed to connect to vehicle on port: " + port)
                return None

    def download_mission(self):
        """
        Download the current mission from the vehicle.
        """
        cmds = self.vehicle.commands
        cmds.download()
        cmds.wait_ready()  # wait until download is complete.
        return cmds

    def get_current_mission(self):
        """
        Downloads the mission and returns the wp list and number of WP  
        """
        print("Downloading mission")

        cmds = self.download_mission()
        missionList = []
        n_WP = 0
        for wp in cmds:
            missionList.append(wp)
            n_WP += 1
        return n_WP, missionList

    def ChangeMode(self, mode):
        retry = 0
        while self.vehicle.mode != VehicleMode(mode):
            self.vehicle.mode = VehicleMode(mode)
            time.sleep(0.5)
            retry += 1
            if retry > 5:
                break
            print("Retrying to change mode...")
        return True

    def get_flight_mode(self):
        return self.vehicle.mode.name

    def get_altitude(self):
        return self.vehicle.location.global_relative_frame.alt

    def get_location(self):
        return self.vehicle.location.global_relative_frame

    def get_vertical_speed(self):
        return self.vehicle.velocity.down

    def get_speed(self):
        return self.vehicle.groundspeed

    def get_battery(self):
        return self.vehicle.battery.voltage

    def get_gps_lat(self):
        return self.vehicle.gps_0.lat

    def get_gps_lon(self):
        return self.vehicle.gps_0.lon

    def get_gps_alt(self):
        return self.vehicle.gps_0.alt

    def get_gps_vel(self):
        return self.vehicle.gps_0.vel

    def get_battery_percentage(self):
        return self.vehicle.battery.level

    # get compass heading
    def get_compass(self):
        return self.vehicle.heading

    def get_yaw(self):
        return self.vehicle.attitude.yaw

    # the list of parameter for the mission is
    # location
    # altitude
    # speed
    # mode
    # command
    # frame

