import bs4
from django.test import TestCase

from countries.management.commands.pull_nature_index_data import Command


class PullNatureIndexDataCommandTestCases(TestCase):
    """
    Tests for the pull_nature_index_data command
    """

    def test_get_raw_nature_index_data(self) -> None:
        """
        Tests that get_raw_nature_index_data method returns correct data
        Returns:
            None
        """
        expected_countries_names = [
            "China",
            "United States of America (USA)",
            "Germany",
        ]
        expected_countries_codes = ["CHN", "USA", "DEU"]
        expected_values = [18298.42, 17364.68, 4257.38]
        expected_year = 2022
        html_sample = f"""
        <html>
        <p class="font-weight-light">1 October 2021 - 30 September {expected_year}</p>
        <table class="c-sortable-table table table-bordered c-data-table" id="simpleTable">
            <tbody>
            <tr>
                <td>1</td>
                <td>
                    <a href="/nature-index/country-outputs/China" title="China">
                        {expected_countries_names[0]}
                    </a>
                </td>
                <td class="u-text-right">22398</td>
                <td class="u-text-right sorted" title="18298.4239967">
                    {expected_values[0]}
                </td>
            </tr>
            <tr>
                <td>2</td>
                <td><a href="/nature-index/country-outputs/United%20States%20of%20America%20%28USA%29"
                       title="United States of America (USA)">{expected_countries_names[1]}</a></td>
                <td class="u-text-right">24825</td>
                <td class="u-text-right sorted" title="17364.6770155">
                    {expected_values[1]}
                </td>
            </tr>
            <tr>
                <td>3</td>
                <td>
                    <a href="/nature-index/country-outputs/Germany" title="Germany">
                        {expected_countries_names[2]}
                    </a>
                </td>
                <td class="u-text-right">8441</td>
                <td class="u-text-right sorted" title="4257.3759768">
                    {expected_values[2]}
                </td>
            </tr>
            </tbody>
        </table>
        </html>
        """
        beautiful_soup = bs4.BeautifulSoup(html_sample, "html.parser")

        raw_nature_index_data = Command.get_raw_nature_index_data(beautiful_soup)

        for expected_county_code, expected_value in zip(
            expected_countries_codes, expected_values
        ):
            self.assertIn(
                (expected_county_code, expected_year, expected_value),
                raw_nature_index_data,
            )
