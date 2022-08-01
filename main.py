import green_detector as detector
import cv2
from mission import Mission
import demo_pixhawk as dp
import serbest_arayuz as ui
import servo_output as servo

# With key "q" camera app will be closed off
def cv2_close_with_q(camera, delay=0):
    # check if the user hit the 'q' key
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        # release the camera
        camera.release()
        cv2.destroyAllWindows()
        return True
    return False

def mission_start():
    camera = cv2.VideoCapture(0)
    mission = Mission()
    app = ui.App()
    app.start()

    while True:
        # If "q" pressed then break
        if cv2_close_with_q(camera):
            break
        # Get frames from the video input
        _, image = camera.read()
        current_location = dp.get_location()

        is_detected = detector.detect_green(image)
        polygon_list = app.get_polygon_list()
        is_in_area = Mission.check_if_in_area(current_location, polygon_list)

        if is_detected and is_in_area:
            servo.run_servo()

mission_start()









