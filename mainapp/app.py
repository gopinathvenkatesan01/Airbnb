import streamlit as st
import pandas as pd

from mongo import get_mongo_client


def main():
    st.set_page_config(page_title="Airbnb Data Analysis", page_icon="🏬", layout="wide")
    st.subheader("⏩ Airbnb **Data Analysis** | _By Gopi_ ")
    mongo = get_mongo_client()
    db = mongo['airbnb']  # Specify the correct database name
    collection = db['airbnb_sample']  # Specify the correct collection name

    airbnb_data = list(collection.find())
    df = pd.DataFrame(airbnb_data)
    df = df.drop(columns=["_id"])
    st.dataframe(df)


if __name__ == "__main__":
    main()
