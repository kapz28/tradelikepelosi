from Scraper.scraper import Scraper
from LLM.llm import ChatGPT
from Database.databaseconfig import DATABASE, JSON_PDF_POLITCIAN_TRADES, JSON_TRADE_KEYS_FILE_NAME
import os
from typing import List
from datetime import datetime
import copy
class TradeLikePelosi:
    def __init__(self) -> None:
        self.scraper = Scraper()
        self.llm = ChatGPT()
        self.trader = None
        
    def load_trade_line(self,trade_line : List[str],person:str) -> dict:
        if len(trade_line) != 6 or None in trade_line or "None" in trade_line:
            return None
        
        trade_dict = {
            "name": self.scraper.clean_and_filter_name(person).strip(),
            "ticker": trade_line[4].strip().upper(),
            "stock_name": trade_line[2].strip(),
            "transaction_type": trade_line[3].strip(),
            "date_executed": self.scraper.make_date_format_consistent(trade_line[1].strip()),
            "amount": trade_line[5].strip().replace("$","").replace(",","")
        }
        
        for key in trade_dict:
            if ":" in trade_dict[key]:
                chumma = trade_dict[key].split(":")
                print(chumma)
                trade_dict[key] = chumma[-1].strip()
        
        return trade_dict

    def unload_trade_line_dict(self,trade_dict : dict):
        name = trade_dict.get("name")
        ticker = trade_dict.get("ticker")
        stock_name = trade_dict.get("stock_name")
        transaction_type = trade_dict.get("transaction_type")
        date_executed = trade_dict.get("date_executed")
        amount = trade_dict.get("amount")
        return name, ticker, stock_name, transaction_type, date_executed, amount
    
    def embed_trade_dict_line_to_database(self,trade_line_dict:dict,trade_database:dict) -> None:
        name, ticker, stock_name, transaction_type, date_executed, amount = self.unload_trade_line_dict(trade_line_dict)
        if self.detect_odd_database_entries(name, ticker, stock_name, transaction_type, date_executed, amount):
            return trade_database
        
        print(trade_line_dict)
        if name not in trade_database:
            trade_database[name] = {}
        if date_executed not in trade_database[name]:
            trade_database[name][date_executed] = {}
        if stock_name not in trade_database[name][date_executed]:
            trade_database[name][date_executed][stock_name] = {
                "ticker": ticker,
                "transaction_type": transaction_type,
                "amount": amount
            }
        return trade_database
    
    def save_trade_database(self,trade_database:dict):
        self.scraper.save_dict_to_json_into_database(trade_database,DATABASE)
        return
    
    def load_trade_database(self) -> dict:
        return self.scraper.load_json_to_dict_from_database(DATABASE)
    
    def detect_odd_database_entries(self,name, ticker, stock_name, transaction_type, date_executed, amount) -> bool:
        if name == None or stock_name == None or transaction_type == None or date_executed == None or amount ==None:
            return True
        if "None" in name or "None" in stock_name or "None" in transaction_type or "None" in date_executed or "None" in amount:
            return True
        if name == "N/A"  or stock_name == "N/A" or transaction_type == "N/A" or date_executed == "N/A" or amount =="N/A":
            return True
        if name == "n/a"  or stock_name == "n/a" or transaction_type == "n/a" or date_executed == "n/a" or amount =="n/a":
            return True
        if "date" in str(date_executed).lower() or "not available" in str(date_executed).lower():
            return True
        
        
        return False       

        
    def process_one_trade_pdf_into_database(self, pdf_suffix_path : str,person:str) -> None:
        db = self.scraper.load_trades_politician_db_to_dict()
        self.scraper.download_trade_pdf(pdf_suffix_path=pdf_suffix_path)
        try:
            trade_processed_result = self.llm.process_text_dump_trade(text_dump=self.scraper.extract_trade_pdf_text())
        except:
            print(f"LLM couldn't process trade line.")
            return
        # print(repr(trade_processed_result))
        trade_lines = str(trade_processed_result).split("\n")
        if ";" not in trade_lines[0]:
            del trade_lines[0]
            
        if len(trade_lines):
            for idx in range(0,len(trade_lines)):
                trade_line = trade_lines[idx].strip().split(";")
                if trade_line[-1].strip() == '':
                    del trade_line[-1]
                trade_line_dict = self.load_trade_line(trade_line=trade_line,person=person)
                if trade_line_dict:
                    db = self.embed_trade_dict_line_to_database(trade_line_dict=trade_line_dict,trade_database=db)
                    self.save_trade_database(db)
                else:
                    print("Corrupted line trade detected: ")   
                    print(trade_line)
        else:
            print(f"No Trades detected in this file.")
            return
        
    def process_all_trades_in_pdf_politician_json_into_database(self,organized_pdf_trades=None,force_refresh=False) -> None:
        if organized_pdf_trades == None:
            organized_pdf_trades = self.scraper.load_json_to_dict_from_database(JSON_PDF_POLITCIAN_TRADES)
        trades_keys = self.scraper.load_json_to_dict_from_database(JSON_TRADE_KEYS_FILE_NAME)
        trigger = False
        for person, years_data in organized_pdf_trades.items():
            if person == "engel eliot":
                trigger = True
            if trigger:
                for year, pdf_list in years_data.items():
                    for pdf_suffix_path in pdf_list:
                        print("Processing the following pdf trade: "+pdf_suffix_path)
                        if pdf_suffix_path not in trades_keys or force_refresh:
                            self.process_one_trade_pdf_into_database(pdf_suffix_path=pdf_suffix_path,person=person)
                            trades_keys[pdf_suffix_path] = True
                            self.scraper.save_dict_to_json_into_database(trades_keys,JSON_TRADE_KEYS_FILE_NAME)

        
    def parse_through_database(self) -> None:
        db = self.load_trade_database()
        db_copy = copy.deepcopy(db)
        for politician, date_execution_orig in db_copy.items():
            for date_execution, stock_name_orig in date_execution_orig.items():
                for stock_name, trade_dict in stock_name_orig.items():
                    ticker = trade_dict["ticker"]
                    transaction_type = trade_dict["transaction_type"]
                    amount = trade_dict["amount"]
                    # print(politician)
                    # print(date_execution)
                    # print(ticker)
                    # print(transaction_type)
                    # print(amount)
                    # This is extra just to play around filter and stuff post process
                    # formatted_date_execution = self.make_date_format_consistent(date_execution)
                    # print(formatted_date_execution)

                    # if formatted_date_execution == None:
                    #     if politician in db and date_execution in db[politician]:
                    #         print(politician)
                    #         print(date_execution)
                    #         del db[politician][date_execution]
                    # db[politician][formatted_date_execution] = dict(db[politician]).pop(date_execution)
                    # try:
                    #     print(db[politician][date_execution][stock_name]["ticker"])      
                    #     db[politician][date_execution][stock_name]["ticker"] = str(db[politician][date_execution][stock_name]["ticker"]).upper()
                        
                    # except:
                    #     print("PPEWAP")
                    #     db[politician][date_execution][stock_name]["ticker"] = None
                    # temp = db[politician][date_execution]
                    
    def pull_all_trades_and_update_database(self) -> None:
        self.scraper.save_trades_raw(self.scraper.retreive_trades_raw(year=2024))
        parsed_trades_raw_table_data = self.scraper.parse_trades_raw(self.scraper.load_trades_raw(),print=True)
        existing_organized_pdf_data_database, _ = self.scraper.sift_parsed_pdf_trades_raw_data_and_update_higher_level_database(parsed_trades_raw_table_data)
        # self.process_all_trades_in_pdf_politician_json_into_database(existing_organized_pdf_data_database,force_refresh=True)            
        
        
        
         
        
        


if __name__ == "__main__":  # pragma: no cover
    pelosi_bot = TradeLikePelosi()
    pelosi_bot.pull_all_trades_and_update_database()
    # pelosi_bot.parse_through_database()
    # pelosi_bot.scraper.save_trades_raw()
    # _, organized_pdf_trades, pdf_files_list = pelosi_bot.scraper.parse_trades_raw(year_filter=None,print=True,save=True)
    # print(organized_pdf_trades)
    # print(pdf_files_list)
    # pelosi_bot.scraper.generate_all_processed_cleaned_trades_database(organized_pdf_trades)
    # pelosi_bot.process_one_trade_pdf_into_database(pdf_suffix_path="public_disc/ptr-pdfs/2023/20023192.pdf")
    # pelosi_bot.process_all_trades_in_pdf_politician_json_into_database()
    # pelosi_bot.scraper.download_trade_pdf(pdf_suffix_path="public_disc/ptr-pdfs/2023/20023192.pdf")
    # print("\n",pelosi_bot.scraper.extract_trade_pdf_text(),"\n")
    # pelosi_bot.llm.process_text_dump_trade(text_dump=pelosi_bot.scraper.extract_trade_pdf_text()) 
    # pelosi_bot.scraper.download_trade_pdf("public_disc/ptr-pdfs/2019/20012288.pdf")
    # print("\n",pelosi_bot.scraper.extract_trade_pdf_text(pdf_path="public_disc/ptr-pdfs/2019/20012288.pdf"),"\n")
    # pelosi_bot.scraper.download_trade_pdf("/public_disc/ptr-pdfs/2023/20022664.pdf")
    # print("\n",pelosi_bot.scraper.extract_trade_pdf_text(pdf_path="public_disc/ptr-pdfs/2023/20022664.pdf"),"\n")
    # pelosi_bot.scraper.download_trade_pdf("public_disc/ptr-pdfs/2024/20024625.pdf")
    # print("\n",pelosi_bot.scraper.extract_trade_pdf_text(pdf_path="public_disc/ptr-pdfs/2024/20024625.pdf"),"\n")
    
# def foo(bar: str) -> str:
#     print("hello world")
#     return bar

