import streamlit as st
import pandas as pd

from listingMetricDataService import getDataByFeature
from hostMetricDataService import (
    column_main,
    column_main_max,
    column_main_min,
    column_not_specified,
)
from sql import getCountries, init
from mongo import get_mongo_client
from plotlyService import line_chart, pie_chart, vertical_bar_chart


def main():
    if "firstrun" not in st.session_state:
        st.session_state.firstrun = True

    page_icon_url = "https://github.com/user-attachments/assets/435bfa2f-76fb-48d6-af2b-e7cf7107fcff"
    st.set_page_config(
        page_title="Airbnb Data Analysis", page_icon=page_icon_url, layout="wide"
    )

    if st.session_state.firstrun:
        # st.balloons()
        init()
        st.session_state.firstrun = False
    st.subheader("⏩ Airbnb **Data Analysis** | _By Gopi_ ")
    listingmetric, hostmetric = st.tabs(
        ["Airbnb Listing Metric Analysis", "Airbnb Host Metric Analysis"]
    )
    with listingmetric:
        # vertical_bar chart for property type
        property_type = getDataByFeature("property_type")
        vertical_bar_chart(
            df=property_type,
            x="property_type",
            y="count",
            text="percentage",
            color="#5D9A96",
            title="Property Type",
            title_x=0.43,
        )

        # line & pie chart for Bed Type and    Room Type
        col1, col2 = st.columns(2)
        with col1:
            bed_type = getDataByFeature("bed_type")
            line_chart(
                df=bed_type,
                y="bed_type",
                x="count",
                text="percentage",
                color="#5cb85c",
                textposition=[
                    "top center",
                    "bottom center",
                    "middle right",
                    "middle right",
                    "middle right",
                ],
                title="Bed Type",
                title_x=0.50,
            )
        with col2:
            room_type = getDataByFeature("room_type")
            pie_chart(
                df=room_type, x="room_type", y="count", title="Room Type", title_x=0.30
            )

        # vertical_bar chart for Minimun nights and maximun nights
        tab1, tab2 = st.tabs(["Top 30 Minimum Nights", "Top 30 Maximum Nights"])
        with tab1:
            minimum_nights = getDataByFeature("minimum_nights")
            minimum_nights = minimum_nights.head(30)
            vertical_bar_chart(
                df=minimum_nights,
                x="y",
                y="count",
                text="percentage",
                color="#5cb85c",
                title="Minimum Nights",
                title_x=0.43,
            )
        with tab2:
            maximum_nights = getDataByFeature("maximum_nights")
            maximum_nights = maximum_nights.head(30)
            vertical_bar_chart(
                df=maximum_nights,
                x="y",
                y="count",
                text="percentage",
                color="#5cb85c",
                title="Maximum Nights",
                title_x=0.43,
            )

        # line chart for Cancellation policy
        cancellation_policy = getDataByFeature("cancellation_policy")
        line_chart(
            df=cancellation_policy,
            y="cancellation_policy",
            x="count",
            text="percentage",
            color="#5D9A96",
            textposition=[
                "top center",
                "top right",
                "top center",
                "bottom center",
                "middle right",
            ],
            title="Cancellation Policy",
            title_x=0.43,
        )

        # vertical_bar chart for accomdates
        accommodates = getDataByFeature("accommodates")
        vertical_bar_chart(
            df=accommodates,
            x="y",
            y="count",
            text="percentage",
            color="#5D9A96",
            title="Accommodates",
            title_x=0.43,
        )

        # vertical_bar chart for bedrooms beds and bathrooms
        tab1, tab2, tab3 = st.tabs(["Bedrooms", "Beds", "Bathrooms"])
        with tab1:
            bedrooms = getDataByFeature("bedrooms")
            vertical_bar_chart(
                df=bedrooms,
                x="y",
                y="count",
                text="percentage",
                color="#5cb85c",
                title="Bedrooms",
                title_x=0.43,
            )
        with tab2:
            beds = getDataByFeature("beds")
            vertical_bar_chart(
                df=beds,
                x="y",
                y="count",
                text="percentage",
                color="#5cb85c",
                title="Beds",
                title_x=0.43,
            )
        with tab3:
            bathrooms = getDataByFeature("bathrooms")
            vertical_bar_chart(
                df=bathrooms,
                x="y",
                y="count",
                text="percentage",
                color="#5cb85c",
                title="Bathrooms",
                title_x=0.43,
            )

        # top 50 vertical_bar chart for price cleaning fee Extra peopole Guests included
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Top 50 Price",
                "Top 50 Cleaning Fee",
                "Top 50 Extra People",
                "Top 50 Guests",
            ]
        )
        with tab1:
            price = getDataByFeature("price")
            price = price.head(50)
            vertical_bar_chart(
                df=price,
                x="y",
                y="count",
                text="percentage",
                color="#5D9A96",
                title="Price",
                title_x=0.43,
            )
        with tab2:
            cleaning_fee = getDataByFeature("cleaning_fee")
            cleaning_fee = cleaning_fee.head(50)
            vertical_bar_chart(
                df=cleaning_fee,
                x="y",
                y="count",
                text="percentage",
                color="#5D9A96",
                title="Cleaning Fee",
                title_x=0.43,
            )
        with tab3:

            extra_people = getDataByFeature("extra_people")
            extra_people = extra_people.head(50)
            vertical_bar_chart(
                df=extra_people,
                x="y",
                y="count",
                text="percentage",
                color="#5D9A96",
                title="Extra People",
                title_x=0.43,
            )
        with tab4:

            guests_included = getDataByFeature("guests_included")

            vertical_bar_chart(
                df=guests_included,
                x="y",
                y="count",
                text="percentage",
                color="#5D9A96",
                title="Guests Included",
                title_x=0.43,
            )

        # line chart for host response time
        host_response_time = getDataByFeature("host_response_time")
        line_chart(
            df=host_response_time,
            y="host_response_time",
            x="count",
            text="percentage",
            color="#5cb85c",
            textposition=[
                "top center",
                "top right",
                "top right",
                "bottom left",
                "bottom left",
            ],
            title="Host Response Time",
            title_x=0.43,
        )

        # vertical_bar chart HostResponse rate host Listings count
        tab1, tab2 = st.tabs(["Host Response Rate", "Host Listings Count"])
        with tab1:
            host_response_rate = getDataByFeature("host_response_rate")
            host_response_rate = host_response_rate.head(10)
            vertical_bar_chart(
                df=host_response_rate,
                x="y",
                y="count",
                text="percentage",
                color="#5cb85c",
                title="Host Response Rate",
                title_x=0.43,
            )
        with tab2:
            host_listings_count = getDataByFeature("host_listings_count")
            host_listings_count = host_listings_count.head(10)
            vertical_bar_chart(
                df=host_listings_count,
                x="y",
                y="count",
                text="percentage",
                color="#5cb85c",
                title="Host Listings Count",
                title_x=0.43,
            )

        # pie chart for host is superhost,Host has profile picture,host identity Verified
        tab1, tab2, tab3 = st.tabs(
            ["Host is Superhost", "Host has Profile Picture", "Host Identity Verified"]
        )
        with tab1:
            host_is_superhost = getDataByFeature("host_is_superhost")
            pie_chart(
                df=host_is_superhost,
                x="host_is_superhost",
                y="count",
                title="Host is Superhost",
                title_x=0.39,
            )
        with tab2:
            host_has_profile_pic = getDataByFeature("host_has_profile_pic")
            pie_chart(
                df=host_has_profile_pic,
                x="host_has_profile_pic",
                y="count",
                title="Host has Profile Picture",
                title_x=0.37,
            )
        with tab3:
            host_identity_verified = getDataByFeature("host_identity_verified")
            pie_chart(
                df=host_identity_verified,
                x="host_identity_verified",
                y="count",
                title="Host Identity Verified",
                title_x=0.37,
            )

        # vertical_bar,pie,map chart for market,country and location exact
        tab1, tab2, tab3 = st.tabs(["Market", "Country", "Location Exact"])
        with tab1:
            market = getDataByFeature("market")
            vertical_bar_chart(
                df=market,
                x="market",
                y="count",
                text="percentage",
                color="#5D9A96",
                title="Market",
                title_x=0.43,
            )
        with tab2:

            country = getDataByFeature("country")

            vertical_bar_chart(
                df=country,
                x="country",
                y="count",
                text="percentage",
                color="#5D9A96",
                title="Country",
                title_x=0.43,
            )
        with tab3:
            is_location_exact = getDataByFeature("is_location_exact")
            pie_chart(
                df=is_location_exact,
                x="is_location_exact",
                y="count",
                title="Location Exact",
                title_x=0.37,
            )

        # vertical_bar for availability 30,60,90,365
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Availability 30",
                "Availability 60",
                "Availability 90",
                "Availability 365",
            ]
        )
        with tab1:
            col1, col2 = st.columns([1, 9])
            with col1:
                availability_30 = getDataByFeature("availability_30")
                availability_30["y"] = clean_and_convert_to_int(availability_30["y"])
                min_val = int(availability_30["y"].min())
                max_val = int(availability_30["y"].max())
                end_range = (min_val + 20) if max_val > 20 else max_val
                selected_range = st.slider(
                    "Select range for availability_30",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, end_range),
                    step=20,
                )
            with col2:
                filtered_data = availability_30[
                    (availability_30["y"] >= selected_range[0])
                    & (availability_30["y"] <= selected_range[1])
                ]
                vertical_bar_chart(
                    df=filtered_data,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Availability 30",
                    title_x=0.45,
                )
        with tab2:
            col1, col2 = st.columns([1, 9])
            with col1:
                availability_60 = getDataByFeature("availability_60")
                availability_60["y"] = clean_and_convert_to_int(availability_60["y"])
                min_val = int(availability_60["y"].min())
                max_val = int(availability_60["y"].max())
                end_range = (min_val + 20) if max_val > 20 else max_val
                selected_range = st.slider(
                    "Select range for availability_60",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, end_range),
                    step=20,
                )
            with col2:
                filtered_data = availability_60[
                    (availability_60["y"] >= selected_range[0])
                    & (availability_60["y"] <= selected_range[1])
                ]
                vertical_bar_chart(
                    df=filtered_data,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Availability 60",
                    title_x=0.45,
                )
        with tab3:
            col1, col2 = st.columns([1, 9])
            with col1:
                navailability_90 = getDataByFeature("availability_90")
                navailability_90["y"] = clean_and_convert_to_int(navailability_90["y"])
                min_val = int(navailability_90["y"].min())
                max_val = int(navailability_90["y"].max())
                end_range = (min_val + 20) if max_val > 20 else max_val
                selected_range = st.slider(
                    "Select range for navailability_90",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, end_range),
                    step=20,
                )
            with col2:
                filtered_data = navailability_90[
                    (navailability_90["y"] >= selected_range[0])
                    & (navailability_90["y"] <= selected_range[1])
                ]
                vertical_bar_chart(
                    df=filtered_data,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Availability 90",
                    title_x=0.45,
                )
        with tab4:
            col1, col2 = st.columns([1, 9])
            with col1:
                availability_365 = getDataByFeature("availability_365")
                availability_365["y"] = clean_and_convert_to_int(availability_365["y"])
                min_val = int(availability_365["y"].min())
                max_val = int(availability_365["y"].max())
                end_range = (min_val + 20) if max_val > 20 else max_val
                selected_range = st.slider(
                    "Select range for Avaialbilty 365",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, end_range),
                    step=20,
                )
            with col2:
                filtered_data = availability_365[
                    (availability_365["y"] >= selected_range[0])
                    & (availability_365["y"] <= selected_range[1])
                ]
                vertical_bar_chart(
                    df=filtered_data,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Availability 365",
                    title_x=0.45,
                )

        # vertical_bar for Number of Reveiws ,maximun Number of review,Review Scores
        tab1, tab2, tab3 = st.tabs(
            ["Number of Reviews", "Maximum Number of Reviews", "Review Scores"]
        )
        with tab1:
            col1, col2 = st.columns([1, 9])
            with col1:
                number_of_reviews = getDataByFeature("number_of_reviews")
                number_of_reviews["y"] = clean_and_convert_to_int(
                    number_of_reviews["y"]
                )
                min_val = int(number_of_reviews["y"].min())
                max_val = int(number_of_reviews["y"].max())
                end_range = (min_val + 20) if max_val > 20 else max_val
                selected_range = st.slider(
                    "Select range for Number of Reviews",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, end_range),
                    step=20,
                )
            with col2:

                filtered_data = number_of_reviews[
                    (number_of_reviews["y"] >= selected_range[0])
                    & (number_of_reviews["y"] <= selected_range[1])
                ]
                vertical_bar_chart(
                    df=filtered_data,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Number of Reviews",
                    title_x=0.43,
                )
        with tab2:
            col1, col2 = st.columns([1, 9])
            with col1:
                max_number_of_reviews = getDataByFeature(
                    "number_of_reviews", order="number_of_reviews desc"
                )
                max_number_of_reviews["y"] = clean_and_convert_to_int(
                    max_number_of_reviews["y"]
                )
                min_val = int(max_number_of_reviews["y"].min())
                max_val = int(max_number_of_reviews["y"].max())
                end_range = (min_val + 20) if max_val > 20 else max_val
                selected_range = st.slider(
                    "Select range for Maximun Number of Reviews",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, end_range),
                    step=20,
                )
            with col2:

                filtered_data = max_number_of_reviews[
                    (max_number_of_reviews["y"] >= selected_range[0])
                    & (max_number_of_reviews["y"] <= selected_range[1])
                ]

                vertical_bar_chart(
                    df=filtered_data,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Maximum Number of Reviews",
                    title_x=0.35,
                )
        with tab3:
            col1, col2 = st.columns([1, 9])
            with col1:
                review_scores = getDataByFeature("rating")
                review_scores["y"] = clean_and_convert_to_int(review_scores["y"])
                min_val = int(review_scores["y"].min())
                max_val = int(review_scores["y"].max())
                end_range = (min_val + 20) if max_val > 20 else max_val
                selected_range = st.slider(
                    "Select range for Maximun Number of Reviews",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, end_range),
                    step=20,
                )
            with col2:
                filtered_data = review_scores[
                    (review_scores["y"] >= selected_range[0])
                    & (review_scores["y"] <= selected_range[1])
                ]
            vertical_bar_chart(
                df=filtered_data,
                x="y",
                y="count",
                text="percentage",
                color="#5D9A96",
                title="Ratings",
                title_x=0.43,
            )

    with hostmetric:
        col1, col2, col3 = st.columns(3)
        with col1:
            countries = getCountries()
            country = st.selectbox(label="Country", options=countries)
        if country:
            st.write("")
            # vertical_bar chart
            tab1 = st.tabs(["Property Type"])[0]
            with tab1:
                property_type = column_main(
                    values="property_type", label="Property Type", country=country
                )
                vertical_bar_chart(
                    df=property_type,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Property Type",
                    title_x=0.45,
                )

            # vertical_bar chart
            tab1, tab2 = st.tabs(["Room Type", "Bed Type"])
            with tab1:
                room_type = column_main(
                    values="room_type", label="Room Type", country=country
                )
                vertical_bar_chart(
                    df=room_type,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Room Type",
                    title_x=0.45,
                )
            with tab2:
                bed_type = column_main(
                    values="bed_type", label="Bed Type", country=country
                )
                vertical_bar_chart(
                    df=bed_type,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Bed Type",
                    title_x=0.45,
                )

            # vertical_bar chart
            tab1, tab2,tab3 = st.tabs(["Minimum Nights", "Maximum Nights","Cancellation Policy"])
            with tab1:
                minimum_nights = column_main(
                    values="minimum_nights", label="Minimum Nights", country=country
                )
                vertical_bar_chart(
                    df=minimum_nights,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Minimum Nights",
                    title_x=0.45,
                )
            with tab2:
                maximum_nights = column_main(
                    values="maximum_nights", label="Maximum Nights", country=country
                )
                vertical_bar_chart(
                    df=maximum_nights,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Maximum Nights",
                    title_x=0.45,
                )
            with tab3:
                # vertical_bar chart
                cancellation_policy = column_main(
                    values="cancellation_policy",
                    label="Cancellation Policy",
                    country=country,
                )
                vertical_bar_chart(
                    df=cancellation_policy,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Cancellation Policy",
                    title_x=0.45,
                )

            # vertical_bar chart
            tab1, tab2 = st.tabs(["Minimum Accommodates", "Maximum Accommodates"])
            with tab1:
                minimum_accommodates = column_main_min(
                    values="accommodates", label="Minimum Accommodates", country=country
                )
                vertical_bar_chart(
                    df=minimum_accommodates,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Minimum Accommodates",
                    title_x=0.45,
                )
            with tab2:
                maximum_accommodates = column_main_max(
                    values="accommodates", label="Maximum Accommodates", country=country
                )
                vertical_bar_chart(
                    df=maximum_accommodates,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Maximum Accommodates",
                    title_x=0.45,
                )

            # vertical_bar chart
            tab1, tab2, tab3, tab4 = st.tabs(
                ["Bedrooms", "Minimum Beds", "Maximum Beds", "Bathrooms"]
            )
            with tab1:
                bedrooms = column_main(
                    values="bedrooms", label="Bedrooms", country=country
                )
                vertical_bar_chart(
                    df=bedrooms,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Bedrooms",
                    title_x=0.45,
                )
            with tab2:
                minimum_beds = column_main_min(
                    values="beds", label="Minimum Beds", country=country
                )
                vertical_bar_chart(
                    df=minimum_beds,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Minimum Beds",
                    title_x=0.45,
                )
            with tab3:
                maximum_beds = column_main_max(
                    values="beds", label="Maximum Beds", country=country
                )
                vertical_bar_chart(
                    df=maximum_beds,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Maximum Beds",
                    title_x=0.45,
                )
            with tab4:
                bathrooms = column_main(
                    values="bathrooms", label="Bathrooms", country=country
                )
                vertical_bar_chart(
                    df=bathrooms,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Bathrooms",
                    title_x=0.45,
                )

            # vertical_bar chart
            tab1, tab2, tab3 = st.tabs(["Price", "Minimum Price", "Maximum Price"])
            with tab1:
                price = column_main(values="price", label="Price", country=country)
                vertical_bar_chart(
                    df=price,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Price",
                    title_x=0.45,
                )
            with tab2:
                minimum_price = column_main_min(
                    values="price", label="Minimum Price", country=country
                )
                vertical_bar_chart(
                    df=minimum_price,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Minimum Price",
                    title_x=0.45,
                )
            with tab3:
                maximum_price = column_main_max(
                    values="price", label="Maximum price", country=country
                )
                vertical_bar_chart(
                    df=maximum_price,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Maximum price",
                    title_x=0.45,
                )
            # vertical_bar chart
            tab1, tab2, tab3 = st.tabs(
                ["Cleaning Fee", "Minimum Cleaning Fee", "Maximum Cleaning Fee"]
            )
            with tab1:
                cleaning_fee = column_main(
                    values="cleaning_fee", label="Cleaning Fee", country=country
                )
                vertical_bar_chart(
                    df=price,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Cleaning Fee",
                    title_x=0.45,
                )
            with tab2:
                minimum_cleaning_fee = column_main_min(
                    values="cleaning_fee", label="Minimum Cleaning Fee", country=country
                )
                vertical_bar_chart(
                    df=minimum_cleaning_fee,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Minimum Cleaning Fee",
                    title_x=0.45,
                )
            with tab3:
                maximum_cleaning_fee = column_main_max(
                    values="cleaning_fee", label="Maximum Cleaning Fee", country=country
                )
                vertical_bar_chart(
                    df=maximum_cleaning_fee,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Maximum Cleaning Fee",
                    title_x=0.45,
                )

            # vertical_bar chart
            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "Guests Included",
                    "Cost at Extra People",
                    "Minimum Cost at Extra People",
                    "Maximum Cost at Extra People",
                ]
            )
            with tab1:
                guests_included = column_main(
                    values="guests_included", label="Guests Included", country=country
                )
                vertical_bar_chart(
                    df=guests_included,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Guests Included",
                    title_x=0.45,
                )
            with tab2:
                extra_people = column_main(
                    values="extra_people", label="Cost at Extra People", country=country
                )
                vertical_bar_chart(
                    df=extra_people,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Cost at Extra People",
                    title_x=0.45,
                )
            with tab3:
                extra_people_min_cost = column_main_min(
                    values="extra_people",
                    label="Minimum Cost at Extra People",
                    country=country,
                )
                vertical_bar_chart(
                    df=extra_people_min_cost,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Minimum Cost at Extra People",
                    title_x=0.45,
                )
            with tab4:
                extra_people_max_cost = column_main_max(
                    values="extra_people",
                    label="Maximum Cost at Extra People",
                    country=country,
                )
                vertical_bar_chart(
                    df=extra_people_max_cost,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Maximum Cost at Extra People",
                    title_x=0.45,
                )

            # vertical_bar chart
            tab1, tab2 = st.tabs(["Response Time", "Response Rate"])
            with tab1:
                host_response_time = column_main(
                    values="host_response_time", label="Response Time", country=country
                )
                vertical_bar_chart(
                    df=host_response_time,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Response Time",
                    title_x=0.45,
                )
            with tab2:
                host_response_rate = column_not_specified(
                    values="host_response_rate", label="Response Rate", country=country
                )
                vertical_bar_chart(
                    df=host_response_rate,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Response Rate",
                    title_x=0.45,
                )

            # vertical_bar chart
            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "Availability 30",
                    "Availability 60",
                    "Availability 90",
                    "Availability 365",
                ]
            )
            with tab1:
                availability_30 = column_main_max(
                    values="availability_30",
                    label="Availability of Next 30 Days",
                    country=country,
                )
                vertical_bar_chart(
                    df=availability_30,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Availability of Next 30 Days",
                    title_x=0.45,
                )
            with tab2:
                availability_60 = column_main_max(
                    values="availability_60",
                    label="Availability of Next 60 Days",
                    country=country,
                )
                vertical_bar_chart(
                    df=availability_60,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Availability of Next 60 Days",
                    title_x=0.45,
                )
            with tab3:
                availability_90 = column_main_max(
                    values="availability_90",
                    label="Availability of Next 90 Days",
                    country=country,
                )
                vertical_bar_chart(
                    df=availability_90,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Availability of Next 90 Days",
                    title_x=0.45,
                )
            with tab4:
                availability_365 = column_main_max(
                    values="availability_365",
                    label="Availability of Next 365 Days",
                    country=country,
                )
                vertical_bar_chart(
                    df=availability_365,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5cb85c",
                    title="Availability of Next 365 Days",
                    title_x=0.45,
                )

            # vertical_bar chart
            tab1, tab2 = st.tabs(["Number of Reviews", "Ratings"])
            with tab1:
                number_of_reviews = column_main_max(
                    values="number_of_reviews",
                    label="Number of Reviews",
                    country=country,
                )
                vertical_bar_chart(
                    df=number_of_reviews,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Number of Reviews",
                    title_x=0.45,
                )
            with tab2:
                review_scores = column_main_max(
                    values="rating", label="Ratings", country=country
                )
                vertical_bar_chart(
                    df=review_scores,
                    x="y",
                    y="count",
                    text="percentage",
                    color="#5D9A96",
                    title="Ratings",
                    title_x=0.45,
                )

        else:
            st.toast("Please select a country!")


def clean_and_convert_to_int(series):
    return (
        pd.to_numeric(series.str.replace("`", ""), errors="coerce")
        .fillna(0)
        .astype(int)
    )


if __name__ == "__main__":
    main()
