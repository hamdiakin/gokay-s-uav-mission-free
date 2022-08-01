import mission
import demo_pixhawk

# pixhawk = demo_pixhawk.Pixhawk()
mission = mission.Mission()


def test():
    # vehicle = pixhawk.connect_to_pixhawk()
    # n_wp, wps = pixhawk.get_current_mission()
    # for wp in wps:
    #     print(wp.seq)
    #     print(wp)
    # print("NEXT::", vehicle.commands.next)

    # print("change mode to mission")
    # pixhawk.ChangeMode("AUTO")

    # print("NEXT::", vehicle.commands.next)


    distance = mission.haversine(
        lon1=35.5443335, lat1=38.7091730, lon2=35.5443335, lat2=38.7095791
    )
    assert distance == 0.04515625971037496


test()
