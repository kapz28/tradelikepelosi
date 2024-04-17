# Example usage
TARGET_ENDPOINT = "https://disclosures-clerk.house.gov/FinancialDisclosure/ViewMemberSearchResult"
TARGET_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded"
}
TARGET_DATA = {
    # Add the necessary data fields here
}
FILE_NAME = "tradesdump.txt"
PDF_FILE_NAME = "trade.pdf"
JSON_PDF_KEYS_FILE_NAME = "tradespdfkeys.json"
JSON_PDF_POLITCIAN_TRADES = "tradespdfpolitcian.json"
PDF_PREFIX_URL = "https://disclosures-clerk.house.gov/"
