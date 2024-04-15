from Scraper.scraper import Scraper
class TradeLikePelosi:
    def __init__(self) -> None:
        self.scraper = Scraper()
        self.groq = None
        self.trader = None

def foo(bar: str) -> str:
    print("hello world")
    return bar


if __name__ == "__main__":  # pragma: no cover
    pelosi_bot = TradeLikePelosi()
    # pelosi_bot.scraper.save_to_file()
    pelosi_bot.scraper.parse(None,True)
