import pandas as pd
import psycopg2
from sql import psql_client
import streamlit as st


def getDataByFeature(feature, order="count desc"):


    conn = None
    column_name = [feature, "count", "total_count"]

    try:
        conn = psql_client()
        cursor = conn.cursor()
        query = f"""SELECT DISTINCT airbnb.{feature}, 
                           COUNT(airbnb.{feature}) AS count,
                           SUM(COUNT(airbnb.{feature})) OVER () AS total_count
                    FROM arnb.airbnb
                    GROUP BY airbnb.{feature}
                    ORDER BY {order};"""
        cursor.execute(query)
        tuples_list = cursor.fetchall()
        cursor.close()

        # DataFrame creation and manipulation
        if tuples_list:
            data = pd.DataFrame(tuples_list, columns=column_name)
            total_count = int(data.iloc[0]["total_count"])
            data = data.rename_axis("S.No")
            data.index = data.index.map(lambda x: "{:^{}}".format(x, 10))
            data["percentage"] = data["count"].apply(
                lambda x: str("{:.2f}".format((x / total_count) * 100)) + "%"
            )
            data["y"] = data[feature].apply(lambda x: str(x) + "`")
            return data
        else:
            return None

    except (psycopg2.Error, Exception) as e:
        st.write("An error occurred:", e)
    finally:
        if conn:
            conn.close()
