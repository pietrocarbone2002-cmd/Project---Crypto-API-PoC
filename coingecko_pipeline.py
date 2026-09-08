import json
import pandas as pd
import os
from dotenv import load_dotenv, dotenv_values
import requests

#Extract Data from Coingecko

BASE_URL = "https://pro-api.coingecko.com/api/v3/simple/price?ids"
load_dotenv()

def extract_data(ticker_input: str):

    #Final query
    final_url = f"{BASE_URL}{ticker_input}&vs_currencies=usd"

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

#Input:
ticker = input("Enter the API-ID or CA: ")

dataset = extract_data(ticker)

print(dataset)
   






