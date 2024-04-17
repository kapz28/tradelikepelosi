import openai
from LLM.llmconfig import CHATGPT_API_KEY

class ChatGPT:
    def __init__(self, api_key: str = CHATGPT_API_KEY):
        openai.api_key = api_key

    def process_prompt(self, text_dump: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that can process text dumps and extract information in a tabular format."},
                {"role": "user", "content": f"The following text dump contains 4 different trades done by someone. Can you filter this out and give me a table-like response with the name of the person who did the trade, the stock/asset they purchased (P) or sold (S) or exchanged (E), the ticker symbol associated with the stock on markets, the date they executed the trade, and the average amount as well?\n\n{text_dump}"}
            ]
        )
        return response['choices'][0]['message']['content']