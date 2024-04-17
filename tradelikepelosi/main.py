from Scraper.scraper import Scraper
from LLM.llm import ChatGPT
class TradeLikePelosi:
    def __init__(self) -> None:
        self.scraper = Scraper()
        self.llm = ChatGPT()
        self.trader = None


if __name__ == "__main__":  # pragma: no cover
    pelosi_bot = TradeLikePelosi()
    # pelosi_bot.scraper.save_trades_raw()
    # _, organized_pdf_trades, pdf_files_list = pelosi_bot.scraper.parse_trades_raw(year_filter=None,print=True,save=True)
    # print(organized_pdf_trades)
    # print(pdf_files_list)
    # pelosi_bot.scraper.generate_all_processed_cleaned_trades_database(organized_pdf_trades)
    pelosi_bot.scraper.download_trade_pdf("public_disc/ptr-pdfs/2023/20023192.pdf")
    print("\n",pelosi_bot.scraper.extract_trade_pdf_text(pdf_path="public_disc/ptr-pdfs/2023/20023192.pdf"),"\n")
    pelosi_bot.llm.process_text_dump_trade(text_dump="public_disc/ptr-pdfs/2023/20023192.pdf") 
    # pelosi_bot.scraper.download_trade_pdf("public_disc/ptr-pdfs/2019/20012288.pdf")
    # print("\n",pelosi_bot.scraper.extract_trade_pdf_text(pdf_path="public_disc/ptr-pdfs/2019/20012288.pdf"),"\n")
    # pelosi_bot.scraper.download_trade_pdf("/public_disc/ptr-pdfs/2023/20022664.pdf")
    # print("\n",pelosi_bot.scraper.extract_trade_pdf_text(pdf_path="public_disc/ptr-pdfs/2023/20022664.pdf"),"\n")
    # pelosi_bot.scraper.download_trade_pdf("public_disc/ptr-pdfs/2024/20024625.pdf")
    # print("\n",pelosi_bot.scraper.extract_trade_pdf_text(pdf_path="public_disc/ptr-pdfs/2024/20024625.pdf"),"\n")
    
# def foo(bar: str) -> str:
#     print("hello world")
#     return bar

