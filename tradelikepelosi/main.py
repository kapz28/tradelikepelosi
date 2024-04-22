from Database.database import _Database
from LLM.llm import ChatGPT
from Scraper.scraper import Scraper
from Trader.trader import Trader

from typing import List
import copy
class TradeLikePelosi:
    def __init__(self) -> None:
        self.database= _Database
        self.llm = ChatGPT()
        self.scraper = Scraper()
        self.trader = Trader()

        
    def process_one_trade_pdf_into_database(self, pdf_suffix_path : str,person:str) -> None:
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
                trade_line_dict = self.database.load_trade_line(trade_line=trade_line,person=person)
                if trade_line_dict:
                    self.database.write_trade_dict_line_to_database(trade_line_dict=trade_line_dict)
                else:
                    print("Corrupted line trade detected: ")   
                    print(trade_line)
        else:
            print(f"No Trades detected in this file.")
            return
        
    def process_all_trades_in_pdf_politician_json_into_database(self,organized_pdf_trades=None,force_refresh=False) -> None:
        if organized_pdf_trades == None:
            organized_pdf_trades = self.database.load_trades_pdf_politician_db_to_dict()
        trades_keys = self.database.load_trades_politician_keys_db_to_dict()
        for person, years_data in organized_pdf_trades.items():
            for year, pdf_list in years_data.items():
                for pdf_suffix_path in pdf_list:
                    print("Processing the following pdf trade: "+pdf_suffix_path)
                    if pdf_suffix_path not in trades_keys or force_refresh:
                        self.process_one_trade_pdf_into_database(pdf_suffix_path=pdf_suffix_path,person=person)
                        trades_keys[pdf_suffix_path] = True
                        self.database.save_trades_keys_politician_dict_to_db(trades_keys)

        
    def parse_through_trade_database(self) -> None:
        db = self.database.load_trade_database()
        db_copy = copy.deepcopy(db)
        for politician, date_execution_orig in db_copy.items():
            for date_execution, stock_name_orig in date_execution_orig.items():
                for stock_name, trade_dict in stock_name_orig.items():
                    ticker = trade_dict["ticker"]
                    transaction_type = trade_dict["transaction_type"]
                    amount = trade_dict["amount"]
                    print(politician)
                    print(date_execution)
                    print(ticker)
                    print(transaction_type)
                    print(amount)
                    # This is extra just to play around filter and stuff post process
                    # formatted_date_execution = self.database.make_date_format_consistent(date_execution)
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
                    
    def pull_all_trades_and_update_trade_database(self) -> None:
        self.scraper.save_trades_raw(self.scraper.retreive_trades_raw())
        parsed_trades_raw_table_data = self.scraper.parse_trades_raw(self.scraper.load_trades_raw(),print=True)
        existing_organized_pdf_data_database, _ = self.scraper.sift_parsed_pdf_trades_raw_data_and_update_higher_level_database(parsed_trades_raw_table_data)
        self.process_all_trades_in_pdf_politician_json_into_database(existing_organized_pdf_data_database,force_refresh=True)            
        
        
        
         
        
        


if __name__ == "__main__":  # pragma: no cover
    pelosi_bot = TradeLikePelosi()
    pelosi_bot.pull_all_trades_and_update_trade_database()
    # pelosi_bot.pull_all_trades_and_update_database()
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

