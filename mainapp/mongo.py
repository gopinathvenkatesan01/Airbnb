import pymongo as mongodb
import streamlit as st


def get_mongo_client():
    """Get MongoDB client instance."""
    return mongodb.MongoClient(
        "mongodb+srv://gopinath:guvi13@cluster0.ikuevcw.mongodb.net/"
        "?retryWrites=true&w=majority&appName=Cluster0"
    )
