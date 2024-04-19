import requests
from Scraper.scraperconfig import TARGET_DATA,TARGET_ENDPOINT, TARGET_HEADERS,  PDF_PREFIX_URL
from Database.database import _Database
import re
import os
from datetime import datetime

class Scraper:
    def __init__(self, url=TARGET_ENDPOINT, headers=TARGET_HEADERS, data=TARGET_DATA, year=None):
        self.url = url
        self.headers = headers
        self.data = data
        self.year = year

    def retreive_trades_raw(self, year=None, lastname=None,state=None,district=None):
        if year:
            self.data["FilingYear"] = year
        if lastname:
            self.data["LastName"] = lastname
        if state:
            self.data["State"] = state
        if district:
            self.data["District"] = district            
    
        response = requests.post(self.url, headers=self.headers, data=self.data)

        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: {response.status_code}")
            return None
            
    def save_trades_raw(self,response_content):

        if response_content:
            # Add line breaks and indentation to the HTML tags
            formatted_content = re.sub(r"(</?[a-zA-Z]+)\s*>", r"\1>\n    ", response_content.decode("utf-8"))

            # Save the formatted content to a text file
            _Database.save_trades_raw(formatted_content=formatted_content)
            
    def load_trades_raw(self):
        return _Database.load_trades_raw()

    def parse_trades_raw(self, html_content, print=False, year_filter: int = None):
        rows = html_content.find_all('tr')
        table_data = []

        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 0:
                data = {
                    'name': str(cells[0].text).strip(),
                    'office': str(cells[1].text).strip(),
                    'year': str(cells[2].text).strip(),
                    'file': str(cells[0].find('a')['href']) if cells[0].find('a') else None
                }

                if not year_filter or year_filter == data['year']:
                    table_data.append(data)
        
        if print:
            self.print_parsed_pdf_trades_raw_table(table_data=table_data)

        return table_data
            
    def print_parsed_pdf_trades_raw_table(self,table_data):
        print("{:<30} {:<10} {:<15} {:<20}".format('Name', 'Office', 'Filing Year', 'File'))
        print("="*75)
        for data in table_data:
            print("{:<30} {:<10} {:<15} {:<20}".format(data['name'], data['office'], data['year'], data['file']))
        
            
    # Function to download PDF from a URL
    def download_trade_pdf(self,pdf_suffix_path:str):
        response = requests.get(PDF_PREFIX_URL+pdf_suffix_path)
        _Database.save_trade_pdf(response.content)

    # Function to parse text from a PDF file
    def extract_trade_pdf_text(self):
        return self.read_pdf_with_fix()
    
    def read_pdf(self,pdf_reader,pdf_text:str):
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
        return pdf_text
    
    def read_pdf_with_fix(self):
        pdf_text = ""
        pdf_reader = _Database.load_trade_pdf()
        return self.read_pdf(pdf_reader,pdf_text)
    
    def clean_and_filter_name(self,name):        
        name = str(re.sub('[^a-zA-Z]+', ' ', name)).lower()
        prefixes = ["hon","ms","mr","dr"]
        for prefix in prefixes:
            name = name.replace(prefix, " ") 
        name = ' '.join(name.split())
        name = ' '.join( [namesub for namesub in name.split() if len(namesub)>1] )
        return name 
    
    def sift_parsed_pdf_trades_raw_data_and_update_higher_level_database(self, parsed_trades_raw_table_data):
        existing_pdf_files_keys_database = _Database.load_trades_pdf_keys_politician_db_to_dict()
        existing_organized_pdf_data_database = _Database.load_trades_pdf_politician_db_to_dict()
        
        for item in parsed_trades_raw_table_data:
            year = int(os.path.basename(os.path.dirname(item["file"])))
            name = self.clean_and_filter_name(name=item["name"])
            file = item["file"]
            
            print(year)
            print(name)
            print(file)

            if name not in existing_organized_pdf_data_database:
                existing_organized_pdf_data_database[name] = {}
                if year not in existing_organized_pdf_data_database[name]:
                    existing_organized_pdf_data_database[name][year] = []
                    existing_organized_pdf_data_database[name][year].append(file)
            if file not in existing_pdf_files_keys_database:
                existing_pdf_files_keys_database[file] = True

        _Database.save_trades_pdf_keys_politician_dict_to_db(existing_pdf_files_keys_database)
        _Database.save_trades_pdf_politician_dict_to_db(existing_organized_pdf_data_database)

        return existing_organized_pdf_data_database, existing_pdf_files_keys_database
      
 
    def make_date_format_consistent(self,date_str:str) -> None:
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

    
    
        

    

