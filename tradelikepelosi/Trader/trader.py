from Database.database import _Database
from Markets.markets import _Markets
from difflib import SequenceMatcher

import re
from datetime import datetime, timedelta
from Trader.traderconfig import ASSUMED_FAKE_AMOUNT

class Trader:
    def __init__(self):
        self.database = _Database
        self.markets = _Markets
        
    def backtest_one_trade_line_dict_and_save_performance(self,person:str,date:str,company:str,ticker:str,transaction_type:str,amount:str):
        valid, stock_info = self.check_if_trade_valid_and_return_stock_info_if_valid(company,ticker)
        if valid and stock_info is not None:
            entry_market_date = self.convert_date_format(date)
            entry_price = self.markets.get_price_by_ticker_and_date(self.format_ticker_string(ticker),stock_info,entry_market_date)
            if entry_price and entry_market_date:
                # Dates
                one_day_pass_exit_market_date = self.add_days_to_date(entry_market_date,1)
                seven_day_pass_exit_market_date = self.add_days_to_date(entry_market_date,7)
                fourteen_day_pass_exit_market_date = self.add_days_to_date(entry_market_date,14)
                thirty_day_pass_exit_market_date = self.add_days_to_date(entry_market_date,30)
                
                # Prices
                one_day_pass_exit_market_price = self.markets.get_price_by_ticker_and_date(self.format_ticker_string(ticker),stock_info,one_day_pass_exit_market_date)
                seven_day_pass_exit_market_price = self.markets.get_price_by_ticker_and_date(self.format_ticker_string(ticker),stock_info,seven_day_pass_exit_market_date)
                fourteen_day_pass_exit_market_price = self.markets.get_price_by_ticker_and_date(self.format_ticker_string(ticker),stock_info,fourteen_day_pass_exit_market_date)
                thirty_day_pass_exit_market_price = self.markets.get_price_by_ticker_and_date(self.format_ticker_string(ticker),stock_info,thirty_day_pass_exit_market_date)
                
                # ROI and PNL
                one_day_pass_exit_market_roi, one_day_pass_exit_market_pnl = self.calculate_roi_and_pnl(entry_price,one_day_pass_exit_market_price,ASSUMED_FAKE_AMOUNT)
                seven_day_pass_exit_market_roi, seven_day_pass_exit_market_pnl = self.calculate_roi_and_pnl(entry_price,seven_day_pass_exit_market_price,float(ASSUMED_FAKE_AMOUNT))
                fourteen_day_pass_exit_market_roi, fourteen_day_pass_exit_market_pnl = self.calculate_roi_and_pnl(entry_price,fourteen_day_pass_exit_market_price,float(ASSUMED_FAKE_AMOUNT))
                thirty_day_pass_exit_market_roi, thirty_day_pass_exit_market_pnl = self.calculate_roi_and_pnl(entry_price,thirty_day_pass_exit_market_price,float(ASSUMED_FAKE_AMOUNT))
                
                time_series_performance_dict = self.database.create_time_series_performance_dict(one_day_pass_exit_market_roi, one_day_pass_exit_market_pnl, seven_day_pass_exit_market_roi, seven_day_pass_exit_market_pnl, fourteen_day_pass_exit_market_roi, fourteen_day_pass_exit_market_pnl, thirty_day_pass_exit_market_roi, thirty_day_pass_exit_market_pnl)
                performance_dict_line = self.database.create_performance_line_dict(person,entry_market_date,self.format_ticker_string(ticker), stock_info['longName'], time_series_performance_dict)
                self.database.write_performance_line_dict_to_performance_db(performance_dict_line)
        else:
            print("stock names didn't match...skipping")
            return
        
    def backtest_entire_database(self):
        data = self.database.load_trade_database()
        for person, transactions in data.items():
            print(f"Person: {person}")
            for date, companies in transactions.items():
                print(f"Date: {date}")
                for company, details in companies.items():
                    print(f"Company: {company}")
                    print(f"Ticker: {details['ticker']}")
                    print(f"Transaction Type: {details['transaction_type']}")
                    print(f"Amount: {details['amount']}")
                    
                    self.backtest_one_trade_line_dict_and_save_performance(self,person,date,company,details['ticker'],details['transaction_type'],details['amount'])
                    
                    print()
                print()
            print()
        pass
    
    def retreive_politician_performance(self,name:str):
        pass
    
    def retreive_politicians_performance(self):
        pass
    
    def rank_politician_performance(self, polticians_performance_list_dict):
        pass
    
    def plot_politician_performance(self):
        pass

    def plot_politicians_performance(self):
        pass
    
    def check_if_trade_valid_and_return_stock_info_if_valid(self,company:str,ticker:str):
        stock_api_name, stock_api_info = self.markets.get_stock_name_and_stock_info_using_ticker_yahoo(self.format_ticker_string(ticker))
        if self.similarity_between_strings(company,stock_api_name) > 0.7:
            print(company)
            print(stock_api_name)
            return True, stock_api_info
        else:
            return False, None
    
    def open_trade(self):
        pass
    
    def close_trade(self):
        pass
    
    def schedule_cloud_job_for_trade(self):
        pass
    
    def similarity_between_strings(a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def format_ticker_string(self,ticker:str):
        return ''.join(filter(str.isalpha, ticker)).strip().upper()
    
    def check_and_convert_date_string_datetime(self,ticker:str):
        return ''.join(filter(str.isalpha, ticker)).strip().upper()
    
    def convert_date_format(self,date_input):
        # Input checking
        if not date_input:
            raise ValueError("Date input is empty.")

        if len(date_input) != 10:
            raise ValueError("Date input is not in the correct length.")

        pattern = r'^(0[1-9]|1[0-2])/(0[1-9]|1[0-9]|2[0-9]|3[0-1])/((19|20)\d\d)$'
        if not re.match(pattern, date_input):
            raise ValueError("Date input is not in the correct format.")

        # Date conversion
        date_parts = date_input.split('/')
        converted_date = f"{date_parts[2]}-{date_parts[0].zfill(2)}-{date_parts[1].zfill(2)}"

        return converted_date
    
    def add_days_to_date(self, date_input:str, days:int):
        # Convert input string to datetime object
        date_object = datetime.strptime(date_input, "%Y-%m-%d")

        # Add the specified number of days
        date_object += timedelta(days=days)

        # Convert datetime object back to input string format
        output_string = date_object.strftime("%Y-%m-%d")

        return output_string
    
    def calculate_roi_and_pnl(self, entry_price: float, exit_price: float, amount_invested: float):
        # Calculate ROI
        roi = ((exit_price - entry_price) / entry_price) * 100

        # Calculate PnL
        pnl = (exit_price - entry_price) * amount_invested

        return roi, pnl
        
        
        

        
        
