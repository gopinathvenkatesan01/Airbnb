import pandas as pd
import psycopg2
from sql import psql_client
import streamlit as st


def column_value(country, column_name):
    conn = None
    columns_ = [column_name, "count"]
    try:
        conn = psql_client()
        cursor = conn.cursor()
        cursor.execute(
            f"""select {column_name}, count({column_name}) as count
                               from arnb.airbnb
                               where country='{country}'
                               group by {column_name}
                               order by count desc;"""
        )
        s = cursor.fetchall()
        cursor.close()
        data = pd.DataFrame(s, columns=columns_)
        return data[column_name].values.tolist()
    except (psycopg2.errors, Exception) as e:
        st.error("An error Occured:: {}", e)
    finally:
        if conn:
            conn.close()


def column_value_names(country, column_name, order="desc"):
    conn = None
    columns_ = [column_name, "count"]
    try:
        conn = psql_client()
        cursor = conn.cursor()
        cursor.execute(
            f"""select {column_name}, count({column_name}) as count
                           from arnb.airbnb
                           where country='{country}'
                           group by {column_name}
                           order by {column_name} {order}
                           ;"""
        )
        conn.commit()
        s = cursor.fetchall()
        cursor.close()
        data = pd.DataFrame(s, columns=columns_)
        return data[column_name].values.tolist()
    except (psycopg2.errors, Exception) as e:
        st.error("An error Occured:: {}", e)
    finally:
        if conn:
            conn.close()


def column_value_count_not_specified(country, column_name):
    conn = None
    columns_ = [column_name, "count"]
    try:
        conn = psql_client()
        cursor = conn.cursor()
        cursor.execute(
            f"""select {column_name}, count({column_name}) as count
                           from arnb.airbnb
                           where country='{country}' and {column_name}!='Not Specified'
                           group by {column_name}
                           order by count desc
                           ;"""
        )
        conn.commit()
        s = cursor.fetchall()
        data = pd.DataFrame(s, columns=columns_)
        return data[column_name].values.tolist()
    except (psycopg2.errors, Exception) as e:
        st.error("An error Occured:: {}", e)
    finally:
        if conn:
            conn.close()


def host(country, column_name, column_value):
    conn = None
    columns_ = ["host_id", "count"]
    try:
        conn = psql_client()
        cursor = conn.cursor()
        cursor.execute(
            f"""select distinct host_id, count(host_id) as count
                           from arnb.airbnb
                           where country='{country}' and {column_name}='{column_value}'
                           group by host_id
                           order by count desc
                           ;"""
        )
        conn.commit()
        s = cursor.fetchall()
        i = [i for i in range(1, len(s) + 1)]
        data = pd.DataFrame(s, columns=columns_, index=i)
        data = data.rename_axis("S.No")
        data.index = data.index.map(lambda x: "{:^{}}".format(x, 10))
        data["percentage"] = data["count"].apply(
            lambda x: str("{:.2f}".format(x / 55.55)) + "%"
        )
        data["y"] = data["host_id"].apply(lambda x: str(x) + "`")
        return data
    except (psycopg2.errors, Exception) as e:
        st.error("An error Occured:: {}", e)
    finally:
        if conn:
            conn.close()


def column_main(values, label, country):
    col1, col2, col3 = st.columns(3)
    with col1:
        a = str(values) + "_column_value_list"
        b = str(values) + "_column_value"
        a = column_value(country=country, column_name=values)
        b = st.selectbox(label=label, options=a)
        values = host(country=country, column_name=values, column_value=b)
        return values


def column_main_min(values, label, country):
    col1, col2, col3 = st.columns(3)
    with col1:
        a = str(values) + "_column_value_list"
        b = str(values) + "_column_value"
        a = column_value_names(country=country, column_name=values, order="asc")
        b = st.selectbox(label=label, options=a)
        values = host(country=country, column_name=values, column_value=b)
        return values


def column_main_max(values, label, country):
    col1, col2, col3 = st.columns(3)
    with col1:
        a = str(values) + "_column_value_list"
        b = str(values) + "_column_value"
        a = column_value_names(country=country, column_name=values, order="desc")
        b = st.selectbox(label=label, options=a)
        values = host(country=country, column_name=values, column_value=b)
        return values


def column_not_specified(values, label, country):
    col1, col2, col3 = st.columns(3)
    with col1:
        a = str(values) + "_column_value_list"
        b = str(values) + "_column_value"
        a = column_value_count_not_specified(country=country, column_name=values)
        b = st.selectbox(label=label, options=a)
        values = host(country=country, column_name=values, column_value=b)
        return values
