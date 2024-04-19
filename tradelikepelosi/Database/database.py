from Database.databaseconfig import FILE_NAME, PDF_FILE_NAME, JSON_PDF_POLITCIAN_TRADES, JSON_PDF_KEYS_FILE_NAME, DATABASE_FOLDER_NAME, JSON_POLITCIAN_TRADES, JSON_TRADE_KEYS_FILE_NAME, DATABASE
import os
import json
from bs4 import BeautifulSoup
import PyPDF2

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
    def load_trade_pdf():
        try:
            with open(_Database.format_to_database_path(PDF_FILE_NAME), "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return pdf_reader
        except PyPDF2.errors.PdfReadError as e:
            if "EOF marker not found" in str(e):
                print(f"Error: {str(e)}. Attempting to fix the PDF file...")
                try:
                    _Database.write_fix_to_pdf()
                    with open(_Database.format_to_database_path(PDF_FILE_NAME), "rb") as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        return pdf_reader
                except Exception as e:
                    print(f"Error: {str(e)}. Unable to fix the PDF file.")
            
            

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
    

