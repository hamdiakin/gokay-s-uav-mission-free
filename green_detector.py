import numpy as np
import cv2
from time import sleep
import constants as const

def detect_green(image, draw=True, use_rgb=True):
    # convert the image to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # create a mask
    mask = np.zeros_like(rgb)
    # take the average of the green and blue channels
    avg_gb = rgb[:, :, 0] / 2 + rgb[:, :, 2] / 2

    # find the total average and return as an array
    # avg = np.average(rgb[:, :, :], axis=2) # ! FPS KILLER, I CHANGED IT WITH GRAYSCALE

    # if the red channel is red_ratio_threshold times greater than the average
    # of the (green+blue) channels and if the total average
    # is greater than min_brightness, set that pixel to 255 and all others to 0.
    mask[
        (rgb[:, :, 1] > avg_gb * const.RED_THRESH) & (gray > const.MIN_BRIGHTNESS)
    ] = 255
    output_img = mask
    cv2.imshow("Mask", output_img)
    hasGreen = np.sum(mask)
    is_green_detected = False
    if hasGreen > const.GREEN_SUM:
        print(hasGreen)
        is_green_detected = True
    else:
        is_green_detected = False

    return is_green_detected

camera = cv2.VideoCapture(0)

while True:
    dummy, img = camera.read()
    detect_green(img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        camera.release()
        cv2.destroyAllWindows()
        break