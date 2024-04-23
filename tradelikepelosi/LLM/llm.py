from openai import OpenAI
import re


class ChatGPT:
    def __init__(self):
        self.client = OpenAI(
        organization='org-yaTmwEs28DcgQnJU3SJ44ef3',
        project='proj_edNDOqNT9sOHf1ZMeGY4uBv9',
        )

    def process_text_dump_trade(self, text_dump: str) -> str:
        text_dump_prompt = "The following is the blob of text that you need to process:\n"+ text_dump
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "You are a helpful assistant that can process blob of text and extract information"
            },
            {
            "role": "user",
            "content": "There is a blob of text which contains different trades done by someone. Can you filter this out and give me a response with semi-colons seperating the data with the name of the person who did the trade, the date they executed the trade, the stock/asset name they purchased, and transaction type (P) or sold (S) or exchanged (E), the ticker symbol associated with the stock on markets, and the average amount as well (only one number)?"
            },
            {
            "role": "assistant",
            "content": "If you can't process a particular field for the text dump leave it as None"
            },
            {
            "role": "assistant",
            "content": "Seperate the different trades with new lines for example name 1, date executed 1, stock/asset name 1, transaction type 1, ticker 1, amount 1, newline, name 2, date executed 2, stock/asset name 2, transaction type 2, ticker 2, amount 2"
            },
            {
            "role": "assistant",
            "content": text_dump_prompt
            },
            {
            "role": "assistant",
            "content": "just provide the response nothing else and also don't mention (average of) just provide the average amount without no explanation"
            },
            {
            "role": "assistant",
            "content": "keep the ticker and asset/stock type seperate and keep transaction type",
            },
            {
            "role": "assistant",
            "content": "The headers should be name, date executed, stock/asset name, transaction type, ticker, amount",
            },
            {
            "role": "assistant",
            "content": "For the amount data value if there is a range provided take the average of the two numbers and give one single number",
            },     
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    
        # print(response.choices[0].message.content)
        return response.choices[0].message.content
    
    def get_stock_name_using_ticker_llm(self, ticker:str) -> str:
        prompt = "can you get me the stock name associated with this ticker $" + ticker + " when you give me a response for the stock name only give me the stock name no other words nothing at all just the stock name don't say any other words, if you can't find it return None"
        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "You are a helpful assistant that can extract information about stocks such as prices and stock names"
            },
            {
            "role": "user",
            "content": prompt
            },
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        try:
            response = re.sub(r'[^a-zA-Z ]+',  '', str(response)).strip()
            if response is not '' or response is not 'None':
                return response
            else:
                return None
        except:
            return None
    
    # def get_price_by_ticker_and_date_llm(self, ticker:str, date:str) -> float:
    #     prompt = "given this date " + date + " it's in the format of YYYY-MM-DD and this stock ticker $"+ ticker + " can you give me the price it opened at on that date." + " When you give me a response for the price only give me the price no other words nothing at all just the price with two decimal places don't say any other words or numbers, if you can't find it return None"
    #     response = self.client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {
    #         "role": "system",
    #         "content": "You are a helpful assistant that can extract information about stocks such as prices and stock names"
    #         },
    #         {
    #         "role": "user",
    #         "content": prompt
    #         },
    #     ],
    #     temperature=1,
    #     max_tokens=256,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    #     )
    #     try:
    #         response = re.sub('[^\d\.]', '', str(response)).strip()
    #         if response is not '' or response is not 'None':
    #             return round(float(response),2)
    #         else:
    #             return None

    #     except:
    #         return None