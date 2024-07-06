import pymongo as mongodb
import streamlit as st
import pandas as pd
import numpy as np
from mongo import get_mongo_client
import json

mongo = get_mongo_client()
db = mongo["airbnb"]  
collection = db["airbnb_sample"]


def extract_address_components(address):
    # Extracting components from the nested address dictionary
    street = address.get("street", None)
    suburb = address.get("suburb", None)
    government_area = address.get("government_area", None)
    market = address.get("market", None)
    country = address.get("country", None)
    country_code = address.get("country_code", None)

    # Extracting nested location information
    location = address.get("location", {})
    location_type = location.get("type", None)
    coordinates = location.get("coordinates", [None, None])
    latitude = coordinates[1]
    longitude = coordinates[0]
    is_location_exact = location.get("is_location_exact", None)

    return (
        street,
        suburb,
        government_area,
        market,
        country,
        country_code,
        latitude,
        longitude,
        is_location_exact,
        location_type,
    )


def sortAmenties(amenites):
    a = amenites
    a.sort(reverse=False)
    return a


def extractHostinfo(hostDetails):
    host_id = hostDetails.get("host_id", None)
    host_url = hostDetails.get("host_url", None)
    host_name = hostDetails.get("host_name", None)
    host_identity_verified = hostDetails.get("host_identity_verified", None)
    host_location = hostDetails.get("host_location", None)
    host_response_time = hostDetails.get("host_response_time", None)
    host_thumbnail_url = hostDetails.get("host_thumbnail_url", None)
    host_picture_url = hostDetails.get("host_picture_url", None)
    host_neighbourhood = hostDetails.get("host_neighbourhood", None)
    host_response_rate = hostDetails.get("host_response_rate", None)
    host_is_superhost = hostDetails.get("host_is_superhost", None)
    host_has_profile_pic = hostDetails.get("host_has_profile_pic", None)
    host_listings_count = hostDetails.get("host_listings_count", None)
    host_total_listings_count = hostDetails.get("host_total_listings_count", None)
    host_verifications = hostDetails.get("host_verifications", None)
    return (
        host_id,
        host_url,
        host_name,
        host_identity_verified,
        host_location,
        host_response_time,
        host_thumbnail_url,
        host_picture_url,
        host_neighbourhood,
        host_response_rate,
        host_is_superhost,
        host_has_profile_pic,
        host_listings_count,
        host_total_listings_count,
        host_verifications,
    )


def extract_availability(availability):
    availability_365 = availability.get("availability_365", None)
    availability_30 = availability.get("availability_30", None)
    availability_60 = availability.get("availability_60", None)
    availability_90 = availability.get("availability_90", None)
    return availability_365, availability_30, availability_60, availability_90


def percentage_to_stars(percentage):
    if percentage is None:
        return None
    return (percentage / 100) * 5


def extract_rating(review_scores):
    rating = percentage_to_stars(review_scores.get("review_scores_rating", None))
    return rating


def processValues(value):
    if value is None:
        return "Not specified"
    else:
        return value
    
def processnanValues(value):
    if value == "nan":
        return "Not specified"
    else:
        return value


def processData():
    st.toast('Processing Data')
    airbnb_data = list(collection.find())
    df = pd.DataFrame(airbnb_data)

    airbnb = df.copy()
    airbnb.shape

    # date format conversion
    airbnb["last_scraped"] = pd.to_datetime(
        airbnb["last_scraped"], format="%Y-%m-%d %H:%M:%S"
    )
    airbnb["calendar_last_scraped"] = pd.to_datetime(
        airbnb["calendar_last_scraped"], format="%Y-%m-%d %H:%M:%S"
    )
    airbnb["first_review"] = pd.to_datetime(
        airbnb["first_review"], format="%Y-%m-%d %H:%M:%S"
    )
    airbnb["last_review"] = pd.to_datetime(
        airbnb["last_review"], format="%Y-%m-%d %H:%M:%S"
    )

    airbnb["first_review"] = airbnb["first_review"].dt.strftime("%Y-%m-%d")
    airbnb["last_review"] = airbnb["last_review"].dt.strftime("%Y-%m-%d")
    airbnb["last_scraped"] = airbnb["last_scraped"].dt.strftime("%Y-%m-%d")
    airbnb["calendar_last_scraped"] = airbnb["calendar_last_scraped"].dt.strftime(
        "%Y-%m-%d"
    )

    airbnb["first_review"] = pd.to_datetime(airbnb["first_review"], format="%Y-%m-%d")
    airbnb["last_review"] = pd.to_datetime(airbnb["last_review"], format="%Y-%m-%d")
    airbnb["last_scraped"] = pd.to_datetime(airbnb["last_scraped"], format="%Y-%m-%d")
    airbnb["calendar_last_scraped"] = pd.to_datetime(
        airbnb["calendar_last_scraped"], format="%Y-%m-%d"
    )

    # Apply the custom function to the 'address' column and expand the result into multiple columns
    airbnb[
        [
            "street",
            "suburb",
            "government_area",
            "market",
            "country",
            "country_code",
            "latitude",
            "longitude",
            "is_location_exact",
            "location_type",
        ]
    ] = airbnb["address"].apply(lambda x: pd.Series(extract_address_components(x)))

    # extracting host information
    airbnb[
        [
            "host_id",
            "host_url",
            "host_name",
            "host_identity_verified",
            "host_location",
            "host_response_time",
            "host_thumbnail_url",
            "host_picture_url",
            "host_neighbourhood",
            "host_response_rate",
            "host_is_superhost",
            "host_has_profile_pic",
            "host_listings_count",
            "host_total_listings_count",
            "host_verifications",
        ]
    ] = airbnb["host"].apply(lambda x: pd.Series(extractHostinfo(x)))

    # Extracting Availabilities
    airbnb[
        ["availability_365", "availability_30", "availability_60", "availability_90"]
    ] = airbnb["availability"].apply(lambda x: pd.Series(extract_availability(x)))

    # Rating
    airbnb[["rating"]] = airbnb["review_scores"].apply(
        lambda x: pd.Series(extract_rating(x))
    )
    # amenties
    airbnb["amenities"] = airbnb["amenities"].apply(lambda x: sortAmenties(x))

    # host_verification
    airbnb["host_verifications"] = airbnb["host_verifications"].apply(
        lambda x: sortAmenties(x)
    )

    airbnb["amenities"] = airbnb["amenities"].apply(json.dumps)
    airbnb["host_verifications"] = airbnb["host_verifications"].apply(json.dumps)

    # Street handling
    airbnb["street"] = airbnb["street"].str.split(",").str[0]

    #  Impute missing data
    airbnb = airbnb.fillna({"reviews_per_month": 0, "rating": 0})

    # Create is_rated column
    is_rated = np.where(airbnb["rating"].isna() == True, 0, 1)
    airbnb["is_rated"] = is_rated

    # Image url
    airbnb["images"] = airbnb["images"].apply(lambda x: x["picture_url"])

    # filling nan values
    airbnb["bedrooms"].fillna(0, inplace=True)
    airbnb["beds"].fillna(0, inplace=True)
    airbnb["bathrooms"].fillna(0, inplace=True)
    airbnb['bathrooms'].round()

    # converting data types
    airbnb["latitude"] = airbnb["latitude"].apply(lambda x: float(x))
    airbnb["longitude"] = airbnb["longitude"].apply(lambda x: float(x))
    airbnb["price"] = airbnb["price"].astype("float")
    airbnb["weekly_price"] = airbnb["weekly_price"].astype("float")
    airbnb["cleaning_fee"] = airbnb["cleaning_fee"].astype("float")
    airbnb["minimum_nights"] = airbnb["minimum_nights"].astype(int)
    airbnb["maximum_nights"] = airbnb["maximum_nights"].astype(int)
    airbnb["bedrooms"] = airbnb["bedrooms"].astype(int)
    airbnb["beds"] = airbnb["beds"].astype(int)
    airbnb["bathrooms"] = airbnb["bathrooms"].astype(str).astype(float)
    airbnb["price"] = airbnb["price"].astype(str).astype(float).astype(int)
    airbnb["extra_people"] = (
        airbnb["extra_people"].astype(str).astype(float).astype(int)
    )
    airbnb["guests_included"] = airbnb["guests_included"].astype(str).astype(int)

    # Processing Nan values to Not specified
    airbnb["host_response_time"] = airbnb["host_response_time"].apply(
        lambda x: processValues(x)
    )
    airbnb['host_response_rate'] = airbnb['host_response_rate'].astype(str)
    airbnb["host_response_rate"] = airbnb["host_response_rate"].apply(
        lambda x: processnanValues(x)
    )

    # Processing true & false to Yes & no
    airbnb["host_is_superhost"] = airbnb["host_is_superhost"].map(
        {False: "No", True: "Yes"}
    )
    airbnb["host_has_profile_pic"] = airbnb["host_has_profile_pic"].map(
        {False: "No", True: "Yes"}
    )
    airbnb["host_identity_verified"] = airbnb["host_identity_verified"].map(
        {False: "No", True: "Yes"}
    )
    airbnb["is_location_exact"] = airbnb["is_location_exact"].map(
        {False: "No", True: "Yes"}
    )

    # Filling Security deposit with median values
    sd_median_value = airbnb["security_deposit"].median()
    cf_median_value = airbnb["cleaning_fee"].median()
    airbnb["security_deposit"] = airbnb["security_deposit"].fillna(sd_median_value)
    airbnb["cleaning_fee"] = airbnb["cleaning_fee"].fillna(cf_median_value)

    # Using forward fill to fill first and last review
    airbnb["first_review"] = airbnb["first_review"].ffill()
    airbnb["last_review"] = airbnb["last_review"].ffill()
    airbnb = airbnb.map(
        lambda x: "Not Specified" if isinstance(x, str) and x.strip() == "" else x
    )

    airbnb.drop("host", axis=1, inplace=True)
    airbnb.drop("availability", axis=1, inplace=True)
    airbnb.drop("reviews", axis=1, inplace=True)
    airbnb.drop("address", axis=1, inplace=True)
    airbnb.drop("weekly_price", axis=1, inplace=True)
    airbnb.drop("monthly_price", axis=1, inplace=True)
    airbnb.drop("review_scores", axis=1, inplace=True)

    return airbnb
