import cv2

def image_to_gray(image):

    return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
