import concurrent.futures
import csv
import json
import logging

import requests
from bs4 import BeautifulSoup
from bs4 import ResultSet
from common import Constans
from common import OfferedBy
from crawler.exceptions import DataExtractionError
from crawler.listing import Listing
from models import AgencyDocument
from models import PropertyDocument
from mongoengine import connect as mongo_connect
from services import AgencyService
from services import PropertyService
from settings import Settings

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"  # noqa: E501
}


class Crawler:
    """
    A crawler for the otodom.pl website.

    The crawler is responsible for crawling the website and extracting the data.
    """

    def __init__(self):
        """
        Initialize the crawler.
        """
        self.settings: Settings = Settings()
        self.params: dict = self.generate_params()
        self.listings: list[Listing] = []
        mongo_connect(host=self.settings.mongo_db_host)

    def generate_search_url(self) -> str:
        """
        Generate the URL to crawl.

        :return: The URL to crawl
        """
        url = self.settings.base_url

        url += "/pl/wyniki/"
        url += self.settings.auction_type.value + "/"
        url += self.settings.property_type.value + "/"
        url += self.settings.province + "/"
        url += self.settings.city + "/"
        if self.settings.district is not None:
            url += self.settings.city + "/"
            url += self.settings.city + "/"
            url += self.settings.district + "/"

        return url

    def generate_params(self) -> dict:
        """
        Generate the parameters for the URL.

        :return: The parameters for the URL
        """
        return {
            "priceMin": self.settings.price_min,
            "priceMax": self.settings.price_max,
        }

    def count_pages(self) -> int:
        """
        Count the number of pages to crawl.

        :return: The number of pages to crawl
        """
        response = requests.get(
            url=self.generate_search_url(), params=self.params, headers=HEADERS
        )
        soup = BeautifulSoup(response.content, "html.parser")
        pages_element = soup.select("button[aria-current][data-cy]")
        if len(pages_element) == 0:
            logging.warning("No listings found with given parameters. Exiting...")
            exit(1)
        pages = pages_element[-1].text
        return int(pages)

    def extract_listings_from_page(self, page: int) -> set:
        """
        Crawl the given page.

        :param page: The page number to crawl
        :return: The listings on the page
        """
        params = self.params.copy()
        params["page"] = page
        response = requests.get(
            url=self.generate_search_url(), params=params, headers=HEADERS, timeout=10
        )
        logging.info(f"Extracting listings from page {page}")
        soup = BeautifulSoup(response.content, "html.parser")
        listings = soup.select("div[data-cy=listing-item]")
        return listings

    def extract_listing_data(self, listing_data: ResultSet) -> Listing | None:
        """
        Extract the data from the given listing.

        At this point, the data is being extracted from the listing page,
        and as the function is executed, the data is being saved to the database.

        It scrapes both the property and the agency data.

        :param listing: The listing
        :raises DataExtractionError: If the data extraction fails
        :return: The data from the listing
        """
        listing = Listing()
        property_ = PropertyDocument()
        property_.set_link(listing_data)
        property_.set_promoted(listing_data)
        soup = self.try_get_listing_page(url=property_.link)
        property_.extract_data(soup)
        if property_.offered_by == OfferedBy.ESTATE_AGENCY:
            agency = AgencyDocument()
            agency.extract_data(soup)
            agency_doc = AgencyService.get_by_otodom_id(agency.otodom_id)
            if agency_doc is None or agency_doc.otodom_id != agency.otodom_id:
                agency_doc = AgencyService.put(agency)
            property_.estate_agency = agency_doc.to_dbref()
            listing.agency = agency_doc
        if PropertyService.get_by_otodom_id(property_.otodom_id) is None:
            property_ = PropertyService.put(property_)
            listing.property_ = property_
            return listing
        return None

    def try_get_listing_page(self, url: str) -> BeautifulSoup:
        """
        Tries to get the listing page.

        :param url: The URL of the listing page
        :raises DataExtractionError: If the data extraction fails
        :return: The data from the listing
        """
        max_retries = 3
        while max_retries > 0:
            response = requests.get(url=url, headers=HEADERS)
            logging.info(f"Extracting data from {url}")
            soup = BeautifulSoup(response.content, "html.parser")
            if not PropertyDocument.informational_json_exists(soup):
                max_retries -= 1
                continue
            return soup
        raise DataExtractionError(url=url)

    def get_listings(self) -> list:
        """
        Get the listings.

        :return: The listings
        """
        return self.listings

    def to_json_file(self, filename: str) -> None:
        """
        Save the listings to a json file.

        :param filename: The name of the file
        """
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                [listing.to_dict() for listing in self.listings],
                file,
                ensure_ascii=False,
                default=str,
                indent=4,
            )

    def to_csv_file(self, filename: str) -> None:
        """
        Save the listings to a csv file.

        :param filename: The name of the file
        """
        data = [obj.to_dict() for obj in self.listings]

        keys = {key for dict_ in data for key in dict_.keys()}

        with open(filename, "w", newline="", encoding="utf-8") as output_file:
            dict_writer = csv.DictWriter(output_file, sorted(keys))
            dict_writer.writeheader()
            dict_writer.writerows(data)

    def start(self) -> None:
        """
        Start the crawler.

        The crawler starts crawling the website and extracting the data.
        """
        pages = self.count_pages()
        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            listings = list(
                executor.map(self.extract_listings_from_page, range(1, pages + 1))
            )

        existing_links = PropertyService.get_all_links()
        listings = {
            listing_data
            for sublist in listings
            for listing_data in sublist
            if Constans.DEFAULT_URL + PropertyDocument.extract_link(listing_data)
            not in existing_links
        }
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            listings: list[Listing] = list(
                filter(None.__ne__, executor.map(self.extract_listing_data, listings))
            )

        self.listings = listings
