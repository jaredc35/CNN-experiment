import numpy as np
import requests

# from io import BytesIO
import cv2 as cv
from io import BytesIO
from PIL import Image
import math


# This function takes in a photo URL as a string value and
# returns the image as a numpy array
def get_image(url):
    #
    response = requests.get(url)
    if response.status_code == 200 and response.headers["Content-Type"] in [
        "image/jpeg",
        "image/png",
        "image/jpg",
    ]:
        # img = np.asarray(bytearray(response.content), dtype="uint8")
        # img = cv.imdecode(img, cv.IMREAD_GRAYSCALE)
        # return img

        return Image.open(BytesIO(response.content))
        # return np.array(response)
    else:
        raise Exception("The URL does not contain a valid image")


def calculate_max_width(X, size):

    # Start with theoretical max
    max_w = int((size**2 / X) ** 0.5)

    # Keep decreasing w until criteria is satisfied
    while True:
        if max_w / 4 * X <= size:
            return max_w
        max_w -= 1
        # Break if w would be less than 1
        if max_w < 1:
            return 1


# This function takes in a list of photo URLs and returns
# size x size img of as many small images as it can fit into the
# size x size img
def combine_images(house_photos, size=500):
    photos = []

    for url in house_photos:
        photos.append(get_image(url))

    # Calculate the dimensions of the grid
    n = len(photos)

    if n > 0:
        # w = int((size**2 / n) ** 0.5)
        w = calculate_max_width(n, size)
        print("max width for", n, " photos is: ", w)
    else:
        w = size

    #
    # Create a final image with any excess area filled white
    combined = Image.new("L", (size, size), color=255)

    # Paste images into the final
    x_offset = 0
    y_offset = 0
    for img in photos:
        img = img.resize((w, w))
        region = (x_offset, y_offset, x_offset + w, y_offset + w)
        combined.paste(img, region)
        x_offset += w
        if x_offset >= size:
            x_offset = 0
            y_offset += w

    return combined
