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
from helpers import get_image


# MONGODB_KEY = config("MONGODB_KEY")
# myclient = pymongo.MongoClient(
#     "mongodb+srv://admin-jared:"
#     + MONGODB_KEY
#     + "@cluster0-42f7w.mongodb.net/test?retryWrites=true&w=majority"
# )
# rentDB = myclient["Rentearn"]
# realEstateCollection = rentDB["realEstateCollection"]

# This function
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
        ]
    ]

    photo_url = df_trimmed["photos"].iloc[0][5]

    image = get_image(photo_url)
    shrink_factor = st.slider("Pixels", value=250, min_value=50, max_value=500, step=5)
    shrink = cv.resize(
        image, (shrink_factor, shrink_factor), interpolation=cv.INTER_AREA
    )

    # st.dataframe(shrink / 255)
    st.image(shrink)

    #


# st.dataframe(df)


if __name__ == "__main__":
    app(activePing=False)
    #
