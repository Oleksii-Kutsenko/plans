class ProblematicCountriesSolver:
    """
    Class that returns correct country name for problematic countries names
    """

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
