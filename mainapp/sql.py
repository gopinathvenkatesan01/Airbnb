import json
import pandas as pd
import psycopg2
import streamlit as st
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from processdata import processData


def psql_client():
    try:
        connection = psycopg2.connect(
            host="localhost", user="postgres", password="admin", database="airbnb"
        )
        return connection

    except Exception as e:

        st.warning(e)


def init():
    # Create the 'airbnb' database if it doesn't exist
    data_insertion.create_database("arnb")
    data_insertion.configure_database()
    data_insertion.data_migration()
    print("init")


class data_insertion:
    # Creating schema
    def create_database(database):
        print("creating schema:>>>>")
        conn = psql_client()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        try:

            sqlQuery = "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;"

            # Execute the query statement
            cursor.execute(sqlQuery)

            rows = cursor.fetchall()

            # Extract database names from the fetched rows
            database_names = [db[0] for db in rows]
            # st.write(database_names)

            # Check if the databse exists in the fetched database names
            if database in database_names:
                # Construct and execute the DROP DATABASE query
                query = "DROP SCHEMA {} CASCADE;".format(database)
                cursor.execute(query)
                conn.commit()
                st.toast("Database '{}' dropped successfully.".format(database))

            # create schema
            db_crt_qry = "create schema " + database + ";"
            cursor.execute(db_crt_qry)
            conn.commit()
            st.toast("Schema Created Successfully")

        except (psycopg2.Error, Exception) as e:
            # Handle database-related errors
            st.write("An error occurred:", e)

        finally:
            # Close cursor and connection in the 'finally' block
            if "connection" in locals():
                # Close the cursor
                cursor.close()
                # Close the connection
                conn.close()

    # Executing create statement
    @staticmethod
    def configure_database():
        connection = None

        # connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        try:
            # Read the SQL script to create tables
            with open("script.sql", "r") as file:
                sql = file.read()
                # Connect to the database
                connection = psql_client()
                cursor = connection.cursor()
                # Execute the SQL script
                cursor.execute(sql)

            # Commit the transaction
            connection.commit()

        except (psycopg2.Error, Exception) as e:
            # Handle database-related errors
            print("An error occurred:", e)

        finally:
            if connection:
                connection.close()

    def data_migration():
        connection = None
        try:
            airbnb = processData()
            connection = psql_client()
            cursor = connection.cursor()
            cursor.executemany(
                f"""INSERT INTO arnb.airbnb(
	_id, listing_url, name, summary, space, description, neighborhood_overview, notes, transit, access, interaction, house_rules, property_type, room_type, bed_type, minimum_nights, maximum_nights, cancellation_policy, last_scraped, calendar_last_scraped, first_review, last_review, accommodates, bedrooms, beds, number_of_reviews, bathrooms, amenities, price, security_deposit, cleaning_fee, extra_people, guests_included, images, reviews_per_month, street, suburb, government_area, market, country, country_code, latitude, longitude, is_location_exact, location_type, host_id, host_url, host_name, host_identity_verified, host_location, host_response_time, host_thumbnail_url, host_picture_url, host_neighbourhood, host_response_rate, host_is_superhost, host_has_profile_pic, host_listings_count, host_total_listings_count, host_verifications, availability_365, availability_30, availability_60, availability_90, rating, is_rated)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                airbnb.values.tolist(),
            )
            connection.commit()

        except (psycopg2.Error, Exception) as e:
            print(e)
            st.write("An error occurred:", e)
        finally:
            if connection:
                connection.close()


def getCountries():
    conn = None
    column_name = ["country"]
    try:
        conn = psql_client()
        cursor = conn.cursor()
        cursor.execute(
            f"""select distinct country
                           from arnb.airbnb
                           order by country asc;"""
        )
        tuples_list = cursor.fetchall()
        cursor.close()
        if tuples_list:
            data = pd.DataFrame(tuples_list, columns=column_name)
            data = data.rename_axis("S.No")
            data.index = data.index.map(lambda x: "{:^{}}".format(x, 10))
            return data
    except (psycopg2.Error, Exception) as e:
        st.write("An error occurred:", e)
    finally:
        if conn:
            conn.close()
