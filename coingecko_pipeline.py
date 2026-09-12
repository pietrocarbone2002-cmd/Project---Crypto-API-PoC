import json
import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values
import requests
import datetime
import matplotlib.pyplot as ppl

#Global Variables

BASE_URL = "https://api.coingecko.com/api/v3/coins/"
load_dotenv()
key = os.getenv("COINGECKO_API_KEY")

#================================================================================================
#       Extract Data from Coingecko
#================================================================================================

def extract_coingecko_data(ticker_input: str):

    #Final query
    final_url = f"{BASE_URL}{ticker_input}/market_chart?vs_currency=usd&days=1"

    try:
        response = requests.get(final_url, timeout=30)
        response.raise_for_status()

    except requests.exceptions.Timeout as ex:
        raise RuntimeError("The CoinGecko request timed out") from ex
    
    except requests.exceptions.ConnectionError as ex:
        raise RuntimeError("Could not connect to the Coingecko API.") from ex

    except requests.exceptions.HTTPError as ex:
        raise RuntimeError(f"CoinGecko returned HTTP {response.status_code}:{response.text[:300]}") from ex

    except requests.exceptions.RequestException as ex:
        raise RuntimeError(f"The CoinGecko request failed: {ex}") from ex

    return response.json()

#Parameter for the Query

ticker = input("Enter API-ID: ")

#Data Fetching
raw_json = extract_coingecko_data(ticker)

#================================================================================================
#       Transform to DataFrame
#================================================================================================

def transform_to_dataframe(data:dict):

    #Input Validation

    if not isinstance(data, dict):
        raise TypeError("Data is not in a supported format!")

    #Extract Price Values
    prices = dict(raw_json["prices"])

    time_ms = prices.keys()
    time = [datetime.datetime.fromtimestamp(item/1000) for item in prices]

    price = list(prices.values())

    return pd.DataFrame({"Time" : time, "Price [$]" : price})

dataset = transform_to_dataframe(raw_json)

print(dataset)






