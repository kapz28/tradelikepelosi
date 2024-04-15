import requests
from Scraper.scraperconfig import TARGET_DATA,TARGET_ENDPOINT, TARGET_HEADERS, FILENAME
import re
from bs4 import BeautifulSoup
import os

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
            
    def save_to_file(self, file_name=FILENAME):
        response_content = self.retreive_trades_raw()

        if response_content:
            # Add line breaks and indentation to the HTML tags
            formatted_content = re.sub(r"(</?[a-zA-Z]+)\s*>", r"\1>\n    ", response_content.decode("utf-8"))

            # Save the formatted content to a text file
            with open(file_name, "w") as f:
                f.write(formatted_content)

            print(f"Response content saved to {file_name}")
            
    def load_trades_raw(self, file_path=os.path.join(os.getcwd(),FILENAME)):
        with open(file_path, 'r') as file:
            content = file.read()
        return BeautifulSoup(content, 'html.parser')

    def parse(self, year_filter: int = None, print=False):
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
            print_trades_table(table_data=table_data)

        return table_data
            
def print_trades_table(table_data):
    print("{:<30} {:<10} {:<15} {:<20}".format('Name', 'Office', 'Filing Year', 'Filing'))
    print("="*75)
    for data in table_data:
        print("{:<30} {:<10} {:<15} {:<20}".format(data['name'], data['office'], data['year'], data['file']))
    

