import requests
import yfinance as yf

class _Markets:
    @staticmethod
    def get_stock_name_and_stock_info_using_ticker_yahoo(ticker:str):
        # Create a Ticker object for a specific stock symbol (e.g., AAPL for Apple Inc.)
        yf_stock_object = yf.Ticker(ticker)

        # Get general information about the stock
        yf_stock_info = dict(yf_stock_object.info)

        # Extract the stock name from the general information
        yf_stock_name = yf_stock_info['longName']

        # Print the stock name along with other general information
        print("Stock Name:", yf_stock_name)
        print("General Information:")
        for key, value in yf_stock_info.items():
            print(f"{key}: {value}")
        
        return yf_stock_name, yf_stock_info
    
    @staticmethod
    def get_price_by_ticker_and_date(ticker:str, yf_stock_info,date:str):
        stock_data = yf_stock_info.history(start=date, end=date)
        if stock_data is not None and not stock_data.empty:
            return round(float(stock_data['Close'][0]),2)
        else:
            return None