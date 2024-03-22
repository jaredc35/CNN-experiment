import streamlit as st

st.set_page_config(
    page_title="Covid Detection App",
    layout="centered",
    page_icon=":brain:",
    initial_sidebar_state="collapsed",
)

# PYMONGO Import
import pymongo
from decouple import config

# Worker Imports
import cv2 as cv
import pandas as pd
import numpy as np

# Local helper functions
from helpers import *


# MONGODB_KEY = config("MONGODB_KEY")
# myclient = pymongo.MongoClient(
#     "mongodb+srv://admin-jared:"
#     + MONGODB_KEY
#     + "@cluster0-42f7w.mongodb.net/test?retryWrites=true&w=majority"
# )
# rentDB = myclient["Rentearn"]
# realEstateCollection = rentDB["realEstateCollection"]

#


def app(activePing=False):
    st.title("Convolution Neural Network App")
    st.subheader(
        "This app is used to determine the rental price of a home using pictures of that house combined with other property data."
    )
    if activePing:
        cursor = realEstateCollection.find(
            {"housing_set": "Seattle"}
        )  # Grab all the homes from a specific area
        df = pd.DataFrame(list(cursor))
        df.to_pickle("./homedata.p")
    else:
        df = pd.read_pickle("./homedata.p")

    df_trimmed = df[
        [
            "property_id",
            "price",
            "photos",
            "street",
            "city",
            "zip",
            "latitude",
            "longitude",
            "rent",
        ]
    ]

    max_num_photos = len(df_trimmed["photos"].iloc[0])
    num_photos = st.slider(
        "Images to include", min_value=1, max_value=max_num_photos, value=5
    )
    #
    photo_urls = df_trimmed["photos"].iloc[0][:num_photos]

    # photo_url = df_trimmed["photos"].iloc[0][5]
    # image = get_image(photo_url)
    shrink_factor = st.slider("Pixels", value=500, min_value=50, max_value=500, step=5)
    # shrink = cv.resize(
    #     image, (shrink_factor, shrink_factor), interpolation=cv.INTER_AREA
    # )
    # # st.dataframe(shrink / 255)
    # st.image(shrink)
    # st.image(image)
    # st.dataframe(shrink)
    combined_image = combine_images(photo_urls, size=shrink_factor)

    st.image(combined_image)
    # st.write(combined_image.size)


#
# st.dataframe(df)


if __name__ == "__main__":
    app(activePing=False)
