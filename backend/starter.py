import json
from typing import Dict, Iterable, List, Tuple
import requests
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


def check_usage():
    """
    Check the usage of the API
    """
    response = requests.get(f"{SERVER_URL}/api/usage", headers={'apikey': API_KEY})
    print("Usage", response.json())

