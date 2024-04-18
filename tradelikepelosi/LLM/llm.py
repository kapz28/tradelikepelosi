from openai import OpenAI


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
            "content": "There is a blob of text which contains different trades done by someone. Can you filter this out and give me a csv-like response with the name of the person who did the trade, the stock/asset they purchased (P) or sold (S) or exchanged (E), the ticker symbol associated with the stock on markets, the date they executed the trade, and the average amount as well (only one number)?"
            },
            {
            "role": "assistant",
            "content": "If you can't process a particular field for the text dump leave it as None"
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
            "content": "keep the headers though and when providing response keep the ticker and asset/stock type seperate and keep transaction type",
            },
            {
            "role": "assistant",
            "content": "The headers should be name, ticker, stock/asset name, transaction type, date executred, amount",
            },
            
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    
        print(response.choices[0].message.content)
        return response.choices[0].message.content