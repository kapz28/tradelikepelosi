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
        valid, official_stock_name = self.check_if_trade_valid_and_return_stock_name_if_valid(company,ticker)
        if valid and official_stock_name is not None:
            entry_market_date = self.convert_date_format(self.database.make_date_format_consistent(date))
            entry_price = self.markets.get_price_by_ticker_and_date(entry_market_date,self.format_ticker_string(ticker))
            if entry_price and entry_market_date:
                # Dates
                one_day_pass_exit_market_date = self.add_days_to_date(entry_market_date,1)
                seven_day_pass_exit_market_date = self.add_days_to_date(entry_market_date,7)
                fourteen_day_pass_exit_market_date = self.add_days_to_date(entry_market_date,14)
                thirty_day_pass_exit_market_date = self.add_days_to_date(entry_market_date,30)
                
                # Prices
                one_day_pass_exit_market_price = self.markets.get_price_by_ticker_and_date(one_day_pass_exit_market_date,self.format_ticker_string(ticker))
                seven_day_pass_exit_market_price = self.markets.get_price_by_ticker_and_date(seven_day_pass_exit_market_date,self.format_ticker_string(ticker))
                fourteen_day_pass_exit_market_price = self.markets.get_price_by_ticker_and_date(fourteen_day_pass_exit_market_date,self.format_ticker_string(ticker))
                thirty_day_pass_exit_market_price = self.markets.get_price_by_ticker_and_date(thirty_day_pass_exit_market_date,self.format_ticker_string(ticker))
                
                # ROI and PNL
                one_day_pass_exit_market_roi, one_day_pass_exit_market_pnl = self.calculate_roi_and_pnl(entry_price,one_day_pass_exit_market_price,ASSUMED_FAKE_AMOUNT,transaction_type)
                seven_day_pass_exit_market_roi, seven_day_pass_exit_market_pnl = self.calculate_roi_and_pnl(entry_price,seven_day_pass_exit_market_price,float(ASSUMED_FAKE_AMOUNT),transaction_type)
                fourteen_day_pass_exit_market_roi, fourteen_day_pass_exit_market_pnl = self.calculate_roi_and_pnl(entry_price,fourteen_day_pass_exit_market_price,float(ASSUMED_FAKE_AMOUNT),transaction_type)
                thirty_day_pass_exit_market_roi, thirty_day_pass_exit_market_pnl = self.calculate_roi_and_pnl(entry_price,thirty_day_pass_exit_market_price,float(ASSUMED_FAKE_AMOUNT),transaction_type)
                
                time_series_performance_dict = self.database.create_time_series_performance_dict(one_day_pass_exit_market_roi, one_day_pass_exit_market_pnl, seven_day_pass_exit_market_roi, seven_day_pass_exit_market_pnl, fourteen_day_pass_exit_market_roi, fourteen_day_pass_exit_market_pnl, thirty_day_pass_exit_market_roi, thirty_day_pass_exit_market_pnl)
                performance_dict_line = self.database.create_performance_line_dict(person,entry_market_date,self.format_ticker_string(ticker), official_stock_name, time_series_performance_dict,transaction_type)
                self.database.write_performance_line_dict_to_performance_db(performance_dict_line)
        else:
            print("stock names didn't match...skipping")
            return
        
    def backtest_entire_database_and_save_performance(self):
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
                    
                    self.backtest_one_trade_line_dict_and_save_performance(person,date,company,details['ticker'],details['transaction_type'],details['amount'])
                    
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
    
    def check_if_trade_valid_and_return_stock_name_if_valid(self,company:str,ticker:str):
        stock_api_name = self.markets.get_stock_name_using_ticker(self.format_ticker_string(ticker))
        print("chumma")
        print(stock_api_name)
        if stock_api_name is not None and self.similarity_between_strings(self.only_letters_and_space(company),self.only_letters_and_space(stock_api_name)) > 0.7:
            return True, stock_api_name
        else:
            return False, None
    
    def open_trade(self):
        pass
    
    def close_trade(self):
        pass
    
    def schedule_cloud_job_for_trade(self):
        pass
    
    def similarity_between_strings(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def format_ticker_string(self,ticker:str):
        return ''.join(filter(str.isalpha, ticker)).strip().upper()
    
    def only_letters_and_space(self,sentence:str):
        return ''.join(x for x in str(sentence).strip() if x.isalpha() or x == " ")
    
    def convert_date_format(self,date_input):
        # Input checking
        if not date_input:
            raise ValueError("Date input is empty.")

        if len(date_input) != 10:
            print(len(date_input))
            print(date_input)
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
    
    def calculate_roi_and_pnl(self, entry_price: float, exit_price: float, amount_invested: float, transaction_type: str):
        
        if exit_price is None or entry_price is None:
            return None, None
        # Calculate ROI
        roi = ((exit_price - entry_price) / entry_price) * 100

        # Calculate PnL
        pnl = (exit_price - entry_price) * amount_invested
        
        if transaction_type.strip() == "S":
            roi = roi*-1
            pnl = pnl*-1

        return round(roi,2), round(pnl,2)
        
        
        

        
        
