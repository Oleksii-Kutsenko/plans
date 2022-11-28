"""
Lazy Portfolio ETFs scraper
"""
import concurrent.futures
from typing import Optional

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand, CommandParser

from investments.models import Ticker, Portfolio, PortfolioTicker

TICKER_TYPES_MAPPING = {
    "Bond": Ticker.TickerTypes.BONDS,
    "Bonds": Ticker.TickerTypes.BONDS,
    "Commodity": Ticker.TickerTypes.COMMODITIES,
    "Commodities": Ticker.TickerTypes.COMMODITIES,
    "Equity": Ticker.TickerTypes.STOCKS,
    "Fixed Income": Ticker.TickerTypes.BONDS,
    "Preferred Stock": Ticker.TickerTypes.STOCKS,
    "Real Estate": Ticker.TickerTypes.REAL_ESTATE,
    "Stocks": Ticker.TickerTypes.STOCKS,
}

LEVERAGED_ASSET_TYPES = {"2x"}


def load_url(url: str, timeout: int = 60) -> bytes:
    """
    Loads given URL
    Args:
        url: URL that will be gotten
        timeout: Request timeout in seconds

    Returns:
        Web page in bytes
    """
    response = requests.get(url, timeout=timeout)
    return response.content


class Command(BaseCommand):
    """
    Parses http://www.lazyportfolioetf.com/allocation/ web page and all related web pages
    """

    LAZY_PORTFOLIO_ROOT = "http://www.lazyportfolioetf.com/allocation/"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--limit", nargs="?", type=int)

    def handle(self, *args: tuple, **options: dict) -> None:
        response = requests.get(self.LAZY_PORTFOLIO_ROOT, timeout=60)
        portfolio_root_soup = BeautifulSoup(response.content, "html.parser")
        portfolio_links = self.get_portfolio_links(portfolio_root_soup)

        limit: Optional[int] = options.get("limit", None)
        portfolio_links = portfolio_links[:limit]

        workers = len(portfolio_links) // 10 + 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_url = {
                executor.submit(load_url, url): url for url in portfolio_links
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    content = future.result()
                except Exception as exc:
                    print(f"{url}, {exc}")
                    raise Exception("Error to fetch portfolio") from exc
                else:
                    self.process_portfolio_web_page(content)

    def process_portfolio_web_page(self, content: bytes) -> None:
        """
        Processes portfolio web page, creates LazyPortfolio and LazyPortfolioTicker objects

        Args:
            content: Raw portfolio web page

        Returns:
            None
        """
        portfolio_soup = BeautifulSoup(content, "html.parser")
        portfolio_name = (
            portfolio_soup.find("h1", class_="title entry-title")
            .text.split(":")[0]
            .strip()
        )
        lazy_portfolio, created = Portfolio.objects.get_or_create(name=portfolio_name)
        if created:
            print(f"New portfolio {lazy_portfolio} has been created")
            self.create_lazy_portfolio_tickers(lazy_portfolio, portfolio_soup)

    def create_lazy_portfolio_tickers(
        self, portfolio: Portfolio, portfolio_soup: BeautifulSoup
    ) -> None:
        """
        Creates LazyPortfolioTicker objects for the given LazyPortfolio instance from the portfolio
         web page packed in the Beautiful Soup container

        Args:
            portfolio: Instance of LazyPortfolio class
            portfolio_soup: Container with portfolio web page content

        Returns:
            None
        """
        portfolio_table = portfolio_soup.find_all("table", id="portfolioAllocation")[
            0
        ].find("tbody")
        portfolio_tickers = []

        for portfolio_table_row in portfolio_table.find_all("tr"):
            portfolio_table_data = portfolio_table_row.find_all("td")
            weight = float(portfolio_table_data[0].text.replace("%", ""))
            symbol = portfolio_table_data[2].text.strip()
            name = portfolio_table_data[3].text.strip()
            asset_type = self.map_asset_type(portfolio_table_data[4].text.strip())

            ticker = Ticker.objects.filter(symbol=symbol).first()
            if ticker is None:
                ticker = Ticker.objects.create(
                    name=name, symbol=symbol, asset_type=asset_type
                )
            portfolio_tickers.append(
                PortfolioTicker(
                    portfolio=portfolio,
                    ticker=ticker,
                    weight=weight,
                )
            )
        portfolio.create_portfolio_tickets(portfolio_tickers)

    @staticmethod
    def get_portfolio_links(portfolio_root_soup: BeautifulSoup) -> list[str]:
        """
        Fetches all portfolio links from lazyportfolioetf.com root web page

        Args:
            portfolio_root_soup: lazyportfolioetf.com root web page which packed in
                                 the BeautifulSoup container

        Returns:
            List with portfolio links
        """
        portfolio_list = portfolio_root_soup.find_all(
            lambda tag: tag.name == "ul" and tag.get("class") == ["w3-ul"]
        )[0]
        portfolio_links = []
        for portfolio in portfolio_list.find_all("li"):
            portfolio_link = portfolio.find("a")
            portfolio_name = portfolio_link.text
            if Portfolio.objects.filter(name=portfolio_name).exists():
                continue
            portfolio_links.append(portfolio_link["href"])
        return portfolio_links

    @staticmethod
    def map_asset_type(asset_type_data: str) -> Ticker.TickerTypes:
        """
        Maps lazyportfolioetf.com asset type to internal asset type

        Args:
            asset_type_data: Raw lazyportfolioetf.com asset type

        Returns:
            Instance of TickerTypes Enum
        """
        asset_types = asset_type_data.split(",")
        if asset_types[0] in TICKER_TYPES_MAPPING:
            return Ticker.TickerTypes(TICKER_TYPES_MAPPING.get(asset_types[0].strip()))
        if asset_types[0] in LEVERAGED_ASSET_TYPES:
            return Ticker.TickerTypes(TICKER_TYPES_MAPPING.get(asset_types[1].strip()))
        raise Exception("Unexpected asset type")
