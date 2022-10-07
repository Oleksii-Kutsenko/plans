import concurrent.futures

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand


def load_url(url, timeout=60):
    response = requests.get(url, timeout=timeout)
    return response.content


class Command(BaseCommand):
    LAZY_PORTFOLIO_ROOT = "http://www.lazyportfolioetf.com/allocation/"

    def handle(self, *args, **options):
        response = requests.get(self.LAZY_PORTFOLIO_ROOT)
        soup = BeautifulSoup(response.content, "html.parser")

        portfolio_list = soup.find_all(lambda tag: tag.name == "ul" and tag.get("class") == ["w3-ul"])[0]
        portfolio_links = list()
        for portfolio in portfolio_list.find_all('li'):
            portfolio_links.append(portfolio.find("a")["href"])

        workers = len(portfolio_links) // 10
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_url = {executor.submit(load_url, url): url for url in portfolio_links}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    content = future.result()
                except Exception as exc:
                    print(f"{url}, {exc}")
                else:
                    print(f"{url}, {len(content)}")

        import pdb
        pdb.set_trace()
        return "http://www.lazyportfolioetf.com/allocation/"
