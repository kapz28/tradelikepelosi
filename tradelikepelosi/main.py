from Scraper.scraper import Scraper
from LLM.llm import ChatGPT
from Database.databaseconfig import DATABASE
import os
from typing import List
class TradeLikePelosi:
    def __init__(self) -> None:
        self.scraper = Scraper()
        self.llm = ChatGPT()
        self.trader = None
        
    def load_trade_line(self,trade_line : List[str] ):
        trade_dict = {
            "name": self.scraper.clean_and_filter_name(trade_line[0]),
            "ticker": "$"+trade_line[1],
            "stock_name": trade_line[2],
            "transaction_type": trade_line[3],
            "date_executed": trade_line[4],
            "amount": trade_line[5]
        }
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
        print("BEFORE")
        print(trade_database)
        if name not in trade_database:
            trade_database[name] = {}
        if date_executed not in trade_database[name]:
            trade_database[name][date_executed] = {}
        if ticker not in trade_database[name][date_executed]:
            trade_database[name][date_executed][ticker] = {
                "stock_name": stock_name,
                "transaction_type": transaction_type,
                "amount": amount
            }
        print("AFTER")
        print(trade_database)
        return trade_database
    
    def save_trade_database(self,trade_database:dict):
        self.scraper.save_dict_to_json(trade_database,DATABASE)
        return

        
    def process_one_trade_pdf_into_database(self, pdf_suffix_path : str) -> None:
        db = self.scraper.load_trades_politician_db_to_dict()
        print(db)
        self.scraper.download_trade_pdf(pdf_suffix_path=pdf_suffix_path)
        trade_processed_result = self.llm.process_text_dump_trade(text_dump=self.scraper.extract_trade_pdf_text())
        trade_lines = trade_processed_result.split("\n")
        headers = trade_lines[0].lower().split(",")
        if len(trade_lines) > 1:
            for idx in range(1,len(trade_lines)):
                trade_line = trade_lines[idx].split(",")
                trade_line_dict = self.load_trade_line(trade_line=trade_line)
                print(trade_line_dict)
                db = self.embed_trade_dict_line_to_database(trade_line_dict=trade_line_dict,trade_database=db)
                self.save_trade_database(db)
                
                
                    
                    
                    
                
        else:
            print(f"No Trades detected in this file.")
            return 
        
         
        
        


if __name__ == "__main__":  # pragma: no cover
    pelosi_bot = TradeLikePelosi()
    # pelosi_bot.scraper.save_trades_raw()
    # _, organized_pdf_trades, pdf_files_list = pelosi_bot.scraper.parse_trades_raw(year_filter=None,print=True,save=True)
    # print(organized_pdf_trades)
    # print(pdf_files_list)
    # pelosi_bot.scraper.generate_all_processed_cleaned_trades_database(organized_pdf_trades)
    pelosi_bot.process_one_trade_pdf_into_database(pdf_suffix_path="public_disc/ptr-pdfs/2023/20023192.pdf")
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

