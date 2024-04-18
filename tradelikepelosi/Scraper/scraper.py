import requests
from Scraper.scraperconfig import TARGET_DATA,TARGET_ENDPOINT, TARGET_HEADERS,  PDF_PREFIX_URL
from Database.databaseconfig import FILE_NAME, PDF_FILE_NAME, JSON_PDF_POLITCIAN_TRADES, JSON_PDF_KEYS_FILE_NAME, DATABASE_FOLDER_NAME, JSON_POLITCIAN_TRADES
import re
from bs4 import BeautifulSoup
import os
import PyPDF2
import json

class Scraper:
    def __init__(self, url=TARGET_ENDPOINT, headers=TARGET_HEADERS, data=TARGET_DATA, year=None):
        self.url = url
        self.headers = headers
        self.data = data
        self.year = year

    def retreive_trades_raw(self):
        response = requests.post(self.url, headers=self.headers, data=self.data)

        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: {response.status_code}")
            
    def save_trades_raw(self, file_name=FILE_NAME):
        response_content = self.retreive_trades_raw()

        if response_content:
            # Add line breaks and indentation to the HTML tags
            formatted_content = re.sub(r"(</?[a-zA-Z]+)\s*>", r"\1>\n    ", response_content.decode("utf-8"))

            # Save the formatted content to a text file
            with open(self.format_to_database_path(file_name), "w") as f:
                f.write(formatted_content)

            print(f"Response content saved to {file_name}")
            
    def load_trades_raw(self, file_name=FILE_NAME):
        with open(self.format_to_database_path(file_name), 'r') as file:
            content = file.read()
        return BeautifulSoup(content, 'html.parser')

    def parse_trades_raw(self, year_filter: int = None, print=False, save=False):
        html_content = self.load_trades_raw()
        rows = html_content.find_all('tr')
        table_data = []

        for row in rows:
            cells = row.find_all('td')
            # for index,value in enumerate(cells):
            #     print("index:",index,"value:",value)
            if len(cells) > 0:
                data = {
                    'name': cells[0].text.strip(),
                    'office': cells[1].text.strip(),
                    'year': cells[2].text.strip(),
                    'file': cells[0].find('a')['href'] if cells[0].find('a') else None
                }

                if not year_filter or year_filter == data['year']:
                    table_data.append(data)
        
        if print:
            self.print_parsed_pdf_trades_raw_table(table_data=table_data)
            
        organized_parsed_pdf_trades = None
        trades_pdf_files_list = None
            
        if save:
            organized_parsed_pdf_trades, trades_pdf_files_list = self.organize_and_save_parsed_pdf_trades_raw_data(table_data)

        return table_data, organized_parsed_pdf_trades, trades_pdf_files_list
            
    def print_parsed_pdf_trades_raw_table(self,table_data):
        print("{:<30} {:<10} {:<15} {:<20}".format('Name', 'Office', 'Filing Year', 'File'))
        print("="*75)
        for data in table_data:
            print("{:<30} {:<10} {:<15} {:<20}".format(data['name'], data['office'], data['year'], data['file']))
        
            
    # Function to download PDF from a URL
    def download_trade_pdf(self,pdf_suffix_path:str):
        response = requests.get(PDF_PREFIX_URL+pdf_suffix_path)
        with open(self.format_to_database_path(PDF_FILE_NAME), "wb") as pdf_file:
            pdf_file.write(response.content)

    # Function to parse text from a PDF file
    def extract_trade_pdf_text(self,pdf_path = PDF_FILE_NAME):
        pdf_file_path = self.format_to_database_path(pdf_path)
        return self.read_pdf_with_fix(pdf_file_path=pdf_file_path)
    
    def read_pdf_with_fix(self,pdf_file_path):
        try:
            pdf_text = ""
            with open(pdf_file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_text += page.extract_text()
            return pdf_text
        except PyPDF2.errors.PdfReadError as e:
            if "EOF marker not found" in str(e):
                print(f"Error: {str(e)}. Attempting to fix the PDF file...")
                try:
                    self.fix_pdf(pdf_file_path)
                    print("PDF file fixed. Trying to read the PDF file again...")
                    return self.read_pdf_with_fix(pdf_file_path)
                except Exception as e:
                    print(f"Error: {str(e)}. Unable to fix the PDF file.")
            else:
                print(f"Error: {str(e)}. Unable to read the PDF file.")
                return None

    def fix_pdf(self,pdf_file):
        try:
            with open(self.format_to_database_path(pdf_file), "a") as file:
                file.write("%%EOF")
            print("PDF file fixed.")
        except Exception as e:
            print(f"Error: {str(e)}. Unable to open file: {pdf_file} for fixing.")
    
    def clean_and_filter_name(self,name):
        
        name = str(re.sub('[^a-zA-Z]+', ' ', name)).lower()
        prefixes = ["hon","ms","mr","dr"]
        for prefix in prefixes:
            name = name.replace(prefix, " ") 
        name = ' '.join(name.split())
        name = ' '.join( [namesub for namesub in name.split() if len(namesub)>1] )
        return name 
    
    def organize_and_save_parsed_pdf_trades_raw_data(self, data_list, output_file=JSON_PDF_POLITCIAN_TRADES, out_pdf_keys_file=JSON_PDF_KEYS_FILE_NAME):
        organized_pdf_data = {}
        pdf_files = {}

        for item in data_list:
            year = int(os.path.basename(os.path.dirname(item["file"])))
            name = self.clean_and_filter_name(name=item["name"])
            file = item["file"]

            if name not in organized_pdf_data:
                organized_pdf_data[name] = {}

            if year not in organized_pdf_data[name]:
                organized_pdf_data[name][year] = []


            organized_pdf_data[name][year].append(file)
            pdf_files[file] = True

        with open(self.format_to_database_path(output_file), "w") as outfile:
            json.dump(organized_pdf_data, outfile, indent=4, sort_keys=True)

        with open(self.format_to_database_path(out_pdf_keys_file), "w") as pdf_outfile:
            json.dump(list(pdf_files.keys()), pdf_outfile, indent=4, sort_keys=True)
            
        return organized_pdf_data, list(pdf_files.keys())
            
    def load_json_to_dict(self,json_file):
        with open(self.format_to_database_path(json_file), "r") as infile:
            dictionary = json.load(infile)

        return dictionary
    
    def save_dict_to_json(self,data_dict:dict, json_file=None):
        with open(self.format_to_database_path(json_file), 'w') as outfile:
            print(self.format_to_database_path(json_file))
            print(data_dict)
            json.dump(data_dict, outfile, indent=4)
    
    # def generate_all_processed_cleaned_trades_database(self,organized_pdf_trades:dict = None):
    #     for person, years_data in organized_pdf_trades.items():
    #         for year, pdf_list in years_data.items():
    #             for pdf_suffix_path in pdf_list:
    #                 # Extracting name and year from the loop variables
    #                 name = person
    #                 year = year
    #                 # Passing name, year, and pdf_path to the function
    #                 self.download_trade_pdf(pdf_suffix_path)
    #                 self.extract_trade_pdf_text()
      
    def format_to_database_path(self,filename:str ):              
         return os.path.join(os.path.join(os.getcwd(),DATABASE_FOLDER_NAME),filename)
     
    def load_trades_pdf_politician_db_to_dict(self):
        return self.load_json_to_dict(self.format_to_database_path(JSON_PDF_POLITCIAN_TRADES))
    
    def load_trades_politician_db_to_dict(self):
        return self.load_json_to_dict(self.format_to_database_path(JSON_POLITCIAN_TRADES))

    
    
        

    

