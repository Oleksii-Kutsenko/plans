from unittest import TestCase

from countries.management.commands.counties_mapping import ProblematicCountriesSolver


class CountiesMappingTests(TestCase):
    def test_problematic_country_mapping(self) -> None:
        problematic_countries_solver = ProblematicCountriesSolver()
        expected_country_name = "United Arab Emirates"
        problematic_country = "UAE"

        country_name = problematic_countries_solver.get_country_name(
            problematic_country
        )

        self.assertEqual(country_name, expected_country_name)

    def test_non_problematic_country_mapping(self) -> None:
        problematic_countries_solver = ProblematicCountriesSolver()
        expected_country_name = "United States"
        country_name = "United States"

        mapped_country_name = problematic_countries_solver.get_country_name(
            country_name
        )

        self.assertEqual(mapped_country_name, expected_country_name)
