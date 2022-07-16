"""Accessing datasets."""

from dataclasses import dataclass
from enum import Enum
import os

from dataclasses_json import DataClassJsonMixin

BASE = os.path.abspath(os.path.dirname(__file__))

ATTR_NAME = "name"
ATTR_FILE_BOARDS = "file_boards"
ATTR_FILE_PRODUCTS = "file_products"
ATTR_URL_API = "url_api"
ATTR_URL_PRODUCTS = "url_products"
ATTR_URL_BOARDS = "url_boards"


@dataclass
class DatasetDescription(DataClassJsonMixin):
    """Dataset descriptor."""

    name: str
    boards_file: str | None = "boards.json"
    products_file: str | None = "products.json"
    api_url: str | None = None
    boards_path: str | None = None
    products_path: str | None = None


class DatasetValue(Enum):
    """Available dataset values."""

    NAME = ATTR_NAME
    BOARDS_FILE = ATTR_FILE_BOARDS
    PRODUCTS_FILE = ATTR_FILE_PRODUCTS
    API_URL = ATTR_URL_API
    BOARDS_URL = ATTR_URL_BOARDS
    PRODUCTS_URL = ATTR_URL_PRODUCTS


class Vendor:
    """Available vendors."""

    WORX = DatasetDescription(
        name="worx",
        boards_file="boards.json",
        products_file="products.json",
        api_url="api.worxlandroid.com",
        products_path="/api/v2/products",
        boards_path="/api/v2/products",
    )


class Dataset:
    """Handling the datasets."""

    __vendor: str

    def __init__(self, vendor: Vendor) -> None:
        """Initialize dataset object for vendor."""
        self.__vendor = vendor

    @property
    def vendor(self) -> DatasetDescription:
        """Return the vendor object for this dataset."""
        return self.__vendor

    def load(self, file: str) -> str:
        """Load specific dataset."""

        with open(f"{BASE}/{self.__vendor.name}/{file}", encoding="utf-8") as file:
            data = file.read()

        return data

    # def fetch(self, url: str) -> str:
    #     """Fetch URL resource"""
    #     request.get
