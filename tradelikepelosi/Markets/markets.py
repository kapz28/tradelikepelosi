import requests
import yfinance as yf
import requests
from Markets.marketsconfig import ALPHA_API_KEY, ALPHA_ENDPOINT

class _Markets:
    @staticmethod
    def get_stock_name_using_ticker(ticker:str) -> str:
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': ticker,
            'apikey': ALPHA_API_KEY,
            'datatype': 'json'
        }

        response = requests.get(ALPHA_ENDPOINT, params=params)
        data = response.json()
        print(data)

        if data is not None and 'bestMatches' in data:
            best_matches = data['bestMatches']
            if best_matches:
                first_match = best_matches[0]
                if first_match and '2. name' in first_match:
                    stock_name = first_match.get('2. name')
                    return ''.join(x for x in str(stock_name).strip() if x.isalpha() or x == " ")

        return None
    
    @staticmethod
    def get_price_by_ticker_and_date(ticker, date):
        # Set up the API query parameters
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': ticker,
            'apikey': ALPHA_API_KEY,
            'datatype': 'json'
        }

        # Make a request to the Alpha Vantage API
        response = requests.get(ALPHA_ENDPOINT, params=params)

        # Parse the JSON response
        data = response.json()

        print(data)
        # Extract the daily time series data
        if data is not None and 'Time Series (Daily)' in data:
            daily_data = data['Time Series (Daily)']
            if daily_data and date in daily_data and '1. open' in daily_data[date]:
                # Extract the open price for the given date
                open_price = round(float(daily_data[date]['1. open']),2)
            else:
                return None
            
        else:
            open_price = None

        # Return the open price
        return open_price
    
    @staticmethod
    def get_stock_name_using_ticker_free_api(ticker:str) -> str:
        pass
    
    @staticmethod
    def get_price_by_ticker_and_date_free_api(ticker:str, date:str):
        pass