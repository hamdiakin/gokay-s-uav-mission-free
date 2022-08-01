import time
from dronekit import (
    connect,
    VehicleMode,
    LocationGlobalRelative,
    Command,
    LocationGlobal,
)
from pymavlink import mavutil

# --------------------------------------------------
# -------------- INITIALIZE
# --------------------------------------------------
# -- Setup the commanded flying speed
gnd_speed = 7  # [m/s]
mode = "GROUND"

# --------------------------------------------------
# -------------- CONNECTION
# --------------------------------------------------
# -- Connect to the vehicle
print("Connecting...")
# vehicle = connect("udp:127.0.0.1:14551")
# vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)
try:
    vehicle = connect(
        "/dev/serial/by-id/usb-Hex_ProfiCNC_CubeOrange_20004B001351313139383237-if00",
        # "/dev/ttyS0",
        baud=115200,
        wait_ready=True,
    )
except:
    print("CANNOT CONNECT TO PIXHAWK")


def download_mission(vehicle):
    """
    Download the current mission from the vehicle.
    """
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()  # wait until download is complete.


def get_current_mission(vehicle):
    """
    Downloads the mission and returns the wp list and number of WP 
    
    Input: 
        vehicle
        
    Return:
        n_wp, wpList
    """

    print("Downloading mission")
    download_mission(vehicle)
    missionList = []
    n_WP = 0
    for wp in vehicle.commands:
        missionList.append(wp)
        n_WP += 1

    return n_WP, missionList


def get_location_list():
    n_WP, missionList = get_current_mission(vehicle)

    print("GET LOCATION LIST")
    print("n_WP: ", n_WP)
    # print("Number of WP: ", n_WP)
    # print("Mission List: ", missionList)

    # get gps location of the first waypoint
    # print("WP0: ", wp0)
    # print()
    # print("WP0 X", wp0.x, "Y", wp0.y)
    return missionList

def get_flight_mode():
    return vehicle.mode.name


def get_altitude():
    return vehicle.location.global_relative_frame.alt


def get_location():
    return vehicle.location.global_relative_frame


def get_vertical_speed():
    return vehicle.velocity.down


def get_speed():
    return vehicle.groundspeed


def get_battery():
    return vehicle.battery.voltage


def get_gps_lat():
    return vehicle.gps_0.lat


def get_gps_lon():
    return vehicle.gps_0.lon


def get_gps_alt():
    return vehicle.gps_0.alt


def get_gps_vel():
    return vehicle.gps_0.vel


def get_battery_percentage():
    return vehicle.battery.level


# get compass heading
def get_compass():
    return vehicle.heading


def get_yaw():
    return vehicle.attitude.yaw


# the list of parameter for the mission is
# location
# altitude
# speed
# mode
# command
# frame

