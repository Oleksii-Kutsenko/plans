class MappingSolver:
    """
    Class that returns the correct country or city name when the raw name is different from the
    one in the database
    """

    CITIES_MAPPING = {
        "jersey": "Jersey City",
        "malta": "Valletta",
        "cayman islands": "George Town",
        "guernsey": "St Peter Port",
        "bermuda": "Hamilton",
        "liechtenstein": "Vaduz",
        "gift city -gujarat": "Ahmedabad",
        "cyprus": "Nicosia",
        "isle of man": "Douglas",
        "bahrain": "Manama",
        "british virgin islands": "Road Town",
        "mauritius": "Port Louis",
        "bahamas": "Nassau",
        "trinidad and tobago": "Port of Spain",
        "barbados": "Bridgetown",
    }

    COUNTRIES_MAPPING = {
        "korea, rep.": "Korea, Republic of",
        "bahamas, the": "Bahamas",
        "liechtenstein*": "Liechtenstein",
        "st. lucia": "Saint Lucia",
        "yemen, rep.": "Yemen",
        "st. vincent and the grenadines": "Saint Vincent and the Grenadines",
        "micronesia, fed. sts.": "Micronesia, Federated States of",
        "st. kitts and nevis": "Saint Kitts and Nevis",
        "iran, islamic rep.": "Iran, Islamic Republic of",
        "egypt, arab rep.": "Egypt",
        "lao pdr": "Lao People's Democratic Republic",
        "gambia, the": "Gambia",
        "congo, dem. rep.": "Congo, The Democratic Republic of the",
        "democratic republic of congo": "Congo, The Democratic Republic of the",
        "congo, rep.": "Republic of the Congo",
        "republic of congo": "Republic of the Congo",
        "venezuela, rb": "Venezuela, Bolivarian Republic of",
        "niger": "Republic of the Niger",
        "uae": "United Arab Emirates",
        "china, people's republic of": "China",
        "congo, dem. rep. of the": "Congo, The Democratic Republic of the",
        "congo, republic of": "Republic of the Congo",
        "lao p.d.r.": "Lao People's Democratic Republic",
        "micronesia, fed. states of": "Micronesia, Federated States of",
        "south sudan, republic of": "South Sudan",
        "türkiye, republic of": "Turkey",
        "bahrain, kingdom of": "Kingdom of Bahrain",
        "democratic republic of the congo": "Congo, The Democratic Republic of the",
        "kuwait, the state of": "State of Kuwait",
        "saudi arabia, kingdom of": "Kingdom of Saudi Arabia",
        "türkiye": "Turkey",
        "ivory coast": "Republic of Côte d'Ivoire",
        "laos": "Lao People's Democratic Republic",
        "united states of america (usa)": "United States",
        "united kingdom (uk)": "United Kingdom",
        "cape verde": "Republic of Cabo Verde",
        "china (beijing, shanghai, jiangsu, zhejiang)": "China",
    }

    @classmethod
    def get_country_name(cls, country_name: str) -> str:
        """
        Returns country name from COUNTRIES_MAPPING if it exists
        Args:
            country_name: problematic country name

        Returns:
            str: valid country name
        """
        if country_name.lower() in cls.COUNTRIES_MAPPING:
            return cls.COUNTRIES_MAPPING[country_name.lower()]
        return country_name

    @classmethod
    def get_city_name(cls, city_name: str) -> str:
        """
        Returns city name from CITIES_MAPPING if it exists
        Args:
            city_name: possible problematic city name

        Returns:
            str: valid city name
        """
        if city_name.lower() in cls.CITIES_MAPPING:
            return cls.CITIES_MAPPING[city_name.lower()]
        return city_name


territories_regions_unrecognized_countries = {
    "Hong Kong SAR",
    "Hong Kong",
    "Macao SAR",
    "Kosovo",
    "Taiwan Province of China",
    "West Bank and Gaza",
    "Africa (Region)",
    "Asia and Pacific",
    "Australia and New Zealand",
    "Caribbean",
    "Central America",
    "Central Asia and the Caucasus",
    "East Asia",
    "East Asia & Pacific",
    "Eastern Europe",
    "Europe",
    "Europe & Central Asia",
    "Middle East (Region)",
    "Middle East & North Africa",
    "North Africa",
    "North America",
    "Pacific Islands",
    "South America",
    "South Asia",
    "Southeast Asia",
    "Sub-Saharan Africa (Region)",
    "Western Europe",
    "Western Hemisphere (Region)",
    "ASEAN-5",
    "Advanced economies",
    "Emerging and Developing Asia",
    "Emerging and Developing Europe",
    "Emerging market and developing economies",
    "Euro area",
    "European Union",
    "Latin America & Caribbean",
    "Latin America and the Caribbean",
    "Major advanced economies (G7)",
    "Middle East and Central Asia",
    "Other advanced economies",
    "Sub-Saharan Africa",
    "World",
    "OECD high income",
    "Taiwan, China",
    "Hong Kong SAR, China",
    "Chinese Taipei",
    "Hong Kong, China",
    "Macao, China",
    "Aruba",
    "Aruba, the Netherlands with respect to",
    "Wallis and Futuna Islands",
    "Curaçao",
    "Sint Maarten",
    "Puerto Rico",
    "Taiwan, Province of China",
    "Taipei",
    "Taiwan",
    "American Samoa",
    "Bermuda",
    "Cayman Islands",
    "Cook Islands",
    "French Polynesia",
    "Greenland",
    "Guam",
    "Montserrat",
    "Bonaire, Sint Eustatius and Saba",
    "New Caledonia",
    "Niue",
    "Northern Mariana Islands",
    "Anguilla",
    "Saint Pierre and Miquelon",
    "Tokelau",
    "Turks and Caicos Islands",
    "Guernsey",
    "Virgin Islands, British",
    "Gibraltar",
    "International",
    "Palestinian territories",
    "Vatican City State (Holy See)",
    "Reunion",
    "Faroe Islands",
    "Martinique",
    "Macao",
}
