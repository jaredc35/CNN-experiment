import numpy as np
import requests
from io import BytesIO
import cv2 as cv
from PIL import Image


# This function takes in a photo URL as a string value and
# returns the image as a numpy array
def get_image(url):
    response = requests.get(url)
    if response.status_code == 200 and response.headers["Content-Type"] in [
        "image/jpeg",
        "image/png",
        "image/jpg",
    ]:
        img = np.asarray(bytearray(response.content), dtype="uint8")
        img = cv.imdecode(img, cv.IMREAD_GRAYSCALE)
        return img
        # return Image.open(BytesIO(response.content))
        # return np.array(response)
    else:
        raise Exception("The URL does not contain a valid image")
