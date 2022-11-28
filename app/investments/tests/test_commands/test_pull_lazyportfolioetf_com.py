from unittest.mock import patch, MagicMock

import requests
from bs4 import BeautifulSoup
from django.core.management import call_command
from django.test import TestCase
from factory import BUILD_STRATEGY

from investments.management.commands.pull_lazyportfolioetf_com import Command
from investments.models import Portfolio, Ticker, PortfolioTicker
from investments.tests.factories.portfolio import (
    PortfolioTickerFactory,
    PortfolioFactory,
)


def generate_portfolio_page() -> str:
    """
    Generates a portfolio page HTML
    """
    portfolio = PortfolioFactory.build()
    portfolio_tickers = PortfolioTickerFactory.generate_batch(
        BUILD_STRATEGY, size=4, weight=25
    )
    portfolio_html = f"""
    <html>
    <h1 class="title entry-title">
        {portfolio.name}: ETF allocation and returns
    </h1>
    <table id="portfolioAllocation"
           class="w3-table table-padding-small w3-small font-family-arial table-valign-middle"
           style="border:0; width:99%;">
        <tbody>
    """
    for portfolio_ticker in portfolio_tickers:
        portfolio_html += f"""
        <tr class="w3-border-bottom" style="line-height:16px;">
            <td class="w3-center" style=""><b>{portfolio_ticker.weight}%</b></td>
            <!--<td style="background-color:#f44336;padding:0px !important;"></td>-->
            <td class=""
                style="padding:0px !important;height:34px;">
                <div style="background-color:#f44336; height:80%;">
                </div>
            </td>
            <td class="w3-center">
                <a href="">
                    <b>{portfolio_ticker.ticker.symbol}</b>
                </a>
            </td>
            <td>
                <a href="">
                    {portfolio_ticker.ticker.name}
                </a>
            </td>
            <td>
                {portfolio_ticker.ticker.asset_type}
            </td>
        </tr>
        """
    portfolio_html += """
        </tbody>
    </table>
    </html>
    """
    return portfolio_html


class PullLazyPortfolioETFcomTestCase(TestCase):
    """
    TestCases for pull_lazyportfolioetf_com command
    """

    @patch("investments.management.commands.pull_lazyportfolioetf_com.load_url")
    def test_pull_lazyportfolioetf_com(self, mock_load_url: MagicMock) -> None:
        """
        Test that the command pulls portfolios correctly
        Args:
            mock_load_url: load_url function mock, that prevents actual requests

        Returns:
            None
        """

        mock_load_url.side_effect = lambda url: generate_portfolio_page()
        response = requests.get(Command.LAZY_PORTFOLIO_ROOT, timeout=60)
        portfolio_root_soup = BeautifulSoup(response.content, "html.parser")
        expected_portfolios_number = len(
            Command.get_portfolio_links(portfolio_root_soup)
        )

        call_command("pull_lazyportfolioetf_com")

        self.assertEqual(Portfolio.objects.count(), expected_portfolios_number)

    def tearDown(self) -> None:
        PortfolioTicker.objects.all().delete()
        Portfolio.objects.all().delete()
        Ticker.objects.all().delete()
