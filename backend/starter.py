import json
from typing import Dict, Iterable, List, Tuple
import requests
import sqlite3
import pymongo
import psycopg2

############
# Load the API key and server URL from secrets.json
############

with open("backend/secrets.json") as f:
    secrets = json.load(f)

API_KEY = secrets["api_key"]
SERVER_URL = secrets["server_url"]
MONGO_CONNECTION_STRING = secrets["mongo_connection_string"]
POSTGRES_CONNECTION_STRING = secrets["postgres_connection_string"]

############
# If DEBUG is True, print the details for each product that comes in
DEBUG = False
############


def reset_generator() -> None:
    """
    This will reset the generator on the server to the initial state to ensure that the same products are generated each time.
    """
    response = requests.post(f"{SERVER_URL}/api/reset", headers={'apikey': API_KEY})
    
    response.raise_for_status()
    print("Reset successful")


def product_generator() -> Iterable[Dict]:
    """
    Generator to get products from the server. Yields a dictionary with the product details. One product at a time.
    """

    while True:
        products = requests.get(f"{SERVER_URL}/api/products", headers={'apikey': API_KEY}).json()
        for product in products:
            if DEBUG:
                print(product)
            yield product


def sqlite3_example():
    """
    Example of how to use sqlite3. You will need to adjust the code to handle the other attributes and additional data.
    """

    # Create the table if it does not exist
    conn = sqlite3.connect("kb_starter.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, source TEXT, mpn TEXT, classification TEXT)")
    conn.commit()

    # Reset the generator to initial state
    reset_generator()

    # Insert the first 1000 products into the database
    for i, product in enumerate(product_generator()):
        mpn, source, classification, lifeycle_status, rohs_compliance, min_operating_temp, max_operating_temp = product["mpn"], product["source"], product["classification"], product["lifecycle_status"], product["rohs_compliance"], product["min_operating_temp"], product["max_operating_temp"]
        additional_data = product["additional_data"]

        cursor.execute("INSERT INTO products (source, mpn, classification) VALUES (?, ?, ?)", (source, mpn, classification))
        conn.commit()
        
        if i >= 1000:
            break
    
    cursor.execute("SELECT * FROM products ORDER BY id DESC LIMIT 1")
    print("Last item in Sqlite3", cursor.fetchone())


def mongo_example():
    """
    Example of how to use pymongo. You will need to adjust the code to handle the other attributes and additional data.
    """

    # Connect to the database and create the collection
    client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = client["kb_starter"]
    collection = db["products"]

    # Reset the generator to initial state
    reset_generator()

    # Insert the first 1000 products into the database
    for i, product in enumerate(product_generator()):
        source, mpn, classification, lifeycle_status, rohs_compliance, min_operating_temp, max_operating_temp = product["source"], product["mpn"], product["classification"], product["lifecycle_status"], product["rohs_compliance"], product["min_operating_temp"], product["max_operating_temp"]
        additional_data = product["additional_data"]

        collection.insert_one({"mpn": mpn, 'source': source, 'classification': classification})
        
        if i >= 1000:
            break
    
    print("Last item in Mongo", collection.find_one(sort=[('_id', pymongo.DESCENDING)]))


def postgres_example():
    """
    Example of how to use psycopg2 with PostgreSQL. You will need to adjust the code to handle the other attributes and additional data.
    """

    # Connect to the database
    conn = psycopg2.connect(POSTGRES_CONNECTION_STRING)
    cursor = conn.cursor()

    # Create the table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            source TEXT,
            mpn TEXT,
            classification TEXT
        )
    """)
    conn.commit()

    # Reset the generator to initial state
    reset_generator()

    # Insert the first 1000 products into the database
    for i, product in enumerate(product_generator()):
        mpn, source, classification, lifeycle_status, rohs_compliance, min_operating_temp, max_operating_temp = product["mpn"], product["source"], product["classification"], product["lifecycle_status"], product["rohs_compliance"], product["min_operating_temp"], product["max_operating_temp"]
        additional_data = product["additional_data"]

        cursor.execute("INSERT INTO products (source, mpn, classification) VALUES (%s, %s, %s)", (source, mpn, classification))
        conn.commit()
        
        if i >= 1000:
            break
    
    cursor.execute("SELECT * FROM products ORDER BY id DESC LIMIT 1")
    print("Last item in PostgreSQL", cursor.fetchone())
    
    cursor.close()
    conn.close()


def check_usage():
    """
    Check the usage of the API
    """
    response = requests.get(f"{SERVER_URL}/api/usage", headers={'apikey': API_KEY})
    print("Usage", response.json())

