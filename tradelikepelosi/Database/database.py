from Database.databaseconfig import FILE_NAME, PDF_FILE_NAME, JSON_PDF_POLITCIAN_TRADES, JSON_PDF_KEYS_FILE_NAME, DATABASE_FOLDER_NAME, JSON_POLITCIAN_TRADES, JSON_TRADE_KEYS_FILE_NAME, DATABASE, PERFORMANCE
import os
import json
from bs4 import BeautifulSoup
import PyPDF2
from typing import List
from datetime import datetime
import re

class _Database:
    
    @staticmethod
    def format_to_database_path(filename: str):
        return os.path.join(os.getcwd(), DATABASE_FOLDER_NAME, filename)
    
    @staticmethod
    def load_text_file_from_database(file_path):
        try:
            with open(_Database.format_to_database_path(file_path), 'r') as file:
                file_contents = file.read()
            return file_contents
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None
    
    @staticmethod    
    def load_trades_raw():
        content = _Database.load_text_file_from_database(FILE_NAME)
        return BeautifulSoup(content, 'html.parser')
    
    @staticmethod     
    def load_trade_pdf() -> str:
        try:
            with open(_Database.format_to_database_path(PDF_FILE_NAME), "rb") as file:
                pdf_text = ""
                pdf_reader = PyPDF2.PdfReader(file)
                return _Database.read_pdf(pdf_reader,pdf_text)
        except PyPDF2.errors.PdfReadError as e:
            if "EOF marker not found" in str(e):
                print(f"Error: {str(e)}. Attempting to fix the PDF file...")
                try:
                    _Database.write_fix_to_pdf()
                    with open(_Database.format_to_database_path(PDF_FILE_NAME), "rb") as file:
                        pdf_text = ""
                        pdf_reader = PyPDF2.PdfReader(file)
                        return _Database.read_pdf(pdf_reader,pdf_text)
                except Exception as e:
                    print(f"Error: {str(e)}. Unable to fix the PDF file.")
                 
    @staticmethod
    def read_pdf(pdf_reader,pdf_text:str):
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
        return pdf_text
            
            

    @staticmethod
    def load_json_to_dict_from_database(json_file) -> dict:
        with open(_Database.format_to_database_path(json_file), "r") as infile:
            dictionary = json.load(infile)
        return dictionary
    
    @staticmethod
    def load_trades_pdf_politician_db_to_dict() -> dict:
        return _Database.load_json_to_dict_from_database(JSON_PDF_POLITCIAN_TRADES)
    
    @staticmethod
    def load_trades_pdf_keys_politician_db_to_dict() -> dict:
        return _Database.load_json_to_dict_from_database(JSON_PDF_KEYS_FILE_NAME)
    
    @staticmethod
    def load_trades_politician_keys_db_to_dict() -> dict:
        return _Database.load_json_to_dict_from_database(JSON_TRADE_KEYS_FILE_NAME)
    
    @staticmethod
    def load_trades_politician_db_to_dict() -> dict:
        return _Database.load_json_to_dict_from_database(JSON_POLITCIAN_TRADES)
    
    @staticmethod
    def load_trade_database() -> dict:
        return _Database.load_json_to_dict_from_database(DATABASE)
    
    @staticmethod
    def load_trade_performance_db() -> dict:
        return _Database.load_json_to_dict_from_database(PERFORMANCE)
    
    @staticmethod
    def save_dict_to_json_into_database(data_dict: dict, json_file=None):
        with open(_Database.format_to_database_path(json_file), 'w') as outfile:
            json.dump(data_dict, outfile, indent=4)
            
    @staticmethod
    def save_trades_pdf_politician_dict_to_db(data_dict):
        _Database.save_dict_to_json_into_database(data_dict, JSON_PDF_POLITCIAN_TRADES)
        
    @staticmethod
    def save_trade_pdf(content):
        with open(_Database.format_to_database_path(PDF_FILE_NAME), "wb") as pdf_file:
            pdf_file.write(content)
       
    @staticmethod     
    def save_trades_raw(formatted_content):
        with open(_Database.format_to_database_path(FILE_NAME), "w") as f:
            f.write(formatted_content)
            print(f"Response content saved to {FILE_NAME}")
    
    
    @staticmethod
    def save_trades_pdf_keys_politician_dict_to_db(data_dict):
        _Database.save_dict_to_json_into_database(data_dict, JSON_PDF_KEYS_FILE_NAME)
        
    @staticmethod
    def save_trades_keys_politician_dict_to_db(data_dict):
        _Database.save_dict_to_json_into_database(data_dict, JSON_TRADE_KEYS_FILE_NAME)
        
    @staticmethod
    def save_trades_pdf_politician_dict_to_db(data_dict):
        _Database.save_dict_to_json_into_database(data_dict, JSON_PDF_POLITCIAN_TRADES)
        
    @staticmethod
    def save_trade_database(trade_database: dict):
        _Database.save_dict_to_json_into_database(trade_database, DATABASE)
        
    @staticmethod
    def save_trade_performance_db(performance_database: dict):
        _Database.save_dict_to_json_into_database(performance_database, PERFORMANCE)
        
        
    @staticmethod
    def write_fix_to_pdf():
        try:
            with open(_Database.format_to_database_path(PDF_FILE_NAME), "a") as file:
                file.write("%%EOF")
            print("PDF file fixed.")
        except Exception as e:
            print(f"Error: {str(e)}. Unable to open file: {PDF_FILE_NAME} for fixing.")
            
    @staticmethod
    def detect_odd_database_entries(name, ticker, stock_name, transaction_type, date_executed, amount) -> bool:
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
    
    @staticmethod
    def load_trade_line(trade_line : List[str],person:str) -> dict:
        if len(trade_line) != 6 or None in trade_line or "None" in trade_line:
            return None
        
        trade_dict = {
            "name": _Database.clean_and_filter_name(person).strip(),
            "ticker": trade_line[4].strip().upper(),
            "stock_name": trade_line[2].strip(),
            "transaction_type": trade_line[3].strip(),
            "date_executed": _Database.make_date_format_consistent(trade_line[1].strip()),
            "amount": trade_line[5].strip().replace("$","").replace(",","")
        }
        
        for key in trade_dict:
            if type(trade_dict[key]) != None and type(trade_dict[key]) == str and ":" in trade_dict[key]:
                chumma = trade_dict[key].split(":")
                print(chumma)
                trade_dict[key] = chumma[-1].strip()
        
        return trade_dict

    @staticmethod
    def unload_trade_line_dict(trade_dict : dict):
        name = trade_dict.get("name")
        ticker = trade_dict.get("ticker")
        stock_name = trade_dict.get("stock_name")
        transaction_type = trade_dict.get("transaction_type")
        date_executed = trade_dict.get("date_executed")
        amount = trade_dict.get("amount")
        return name, ticker, stock_name, transaction_type, date_executed, amount
    
    @staticmethod
    def write_trade_dict_line_to_database(trade_line_dict:dict) -> None:
        trade_database = _Database.load_trade_database()
        name, ticker, stock_name, transaction_type, date_executed, amount = _Database.unload_trade_line_dict(trade_line_dict)
        if _Database.detect_odd_database_entries(name, ticker, stock_name, transaction_type, date_executed, amount):
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
        _Database.save_trade_database(trade_database)
        
        
    @staticmethod
    def create_performance_line_dict(politician:str,date:str,ticker:str,stock_official_name:str, time_series_dict: dict) -> dict:
        performance_line_dict = {
            "politician": politician,
            "date": date,
            "ticker": ticker,
            "stock_official_name": stock_official_name,
            "performance": time_series_dict
        }

        return performance_line_dict
    
    
    @staticmethod
    def create_time_series_performance_dict(one_day_roi:float, one_day_pnl:float, seven_day_roi:float, seven_day_pnl:float, fourteen_day_roi:float, fourteen_day_pnl:float, thirty_day_roi:float, thirty_day_pnl:float) -> dict:
        time_series_performance_dict = {
            1: [one_day_roi,one_day_pnl],
            7: [seven_day_roi,seven_day_pnl],
            14: [fourteen_day_roi,fourteen_day_pnl], 
            30: [thirty_day_roi,thirty_day_pnl],         
        }
        
        return time_series_performance_dict
        
    @staticmethod
    def write_performance_line_dict_to_performance_db(performance_line_dict:dict) -> None:
        performance_database = _Database.load_trade_performance_db()

        if performance_line_dict['politician'] not in performance_database:
            performance_database[performance_line_dict['politician']] = {}
         
        trade_info = {
            "ticker":performance_line_dict['ticker'],
            "stock_official_name":performance_line_dict['stock_official_name'],
            "performance":performance_line_dict['performance']
        }   
        if performance_line_dict['date'] not in performance_database['politician']:
            performance_database[performance_line_dict['politician']][performance_line_dict['date']] = []

        performance_database[performance_line_dict['politician']][performance_line_dict['date']].append(trade_info)

        _Database.save_trade_performance_db(performance_database)
        
    @staticmethod
    def clean_and_filter_name(name):        
        name = str(re.sub('[^a-zA-Z]+', ' ', name)).lower()
        prefixes = ["hon","ms","mr","dr"]
        for prefix in prefixes:
            name = name.replace(prefix, " ") 
        name = ' '.join(name.split())
        name = ' '.join( [namesub for namesub in name.split() if len(namesub)>1] )
        return name
    
    @staticmethod
    def make_date_format_consistent(date_str:str) -> None:
        date_str = date_str.strip()
        date_str = date_str.replace("*","")
        try:
            date_obj = datetime.strptime(date_str, "%B %d, %Y")
            return date_obj.strftime("%m/%d/%Y")
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                return date_obj.strftime("%m/%d/%Y")
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, "%m/%d/%Y")
                    return date_obj.strftime("%m/%d/%Y")
                except ValueError:
                    try:
                        date_obj = datetime.strptime(date_str, "%m-%d-%Y")
                        return date_obj.strftime("%m/%d/%Y")
                    except ValueError:
                        try:
                            date_obj = datetime.strptime(date_str, "%b %d,%Y")
                            return date_obj.strftime("%m/%d/%Y")
                        except ValueError:
                            try:
                                date_obj = datetime.strptime(date_str, "%b %d, %Y")
                                return date_obj.strftime("%m/%d/%Y")
                            except ValueError:
                                try:
                                    date_obj = datetime.strptime(date_str, "%B %d, %Y")
                                    return date_obj.strftime("%m/%d/%Y")
                                except ValueError:
                                    try:
                                        date_obj = datetime.strptime(date_str, "%m/%d/%y")
                                        return date_obj.strftime("%m/%d/%Y")
                                    except ValueError:
                                        try:
                                            temp = date_str.split(" ")
                                            if len(temp) > 3:
                                                temp = temp[:3]
                                            temp = " ".join(temp)
                                            date_obj = datetime.strptime(temp, "%b %d %Y")
                                            return date_obj.strftime("%m/%d/%Y")
                                        except ValueError:
                                            return None
    

