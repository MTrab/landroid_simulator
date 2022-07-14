"""Accessing datasets."""

from enum import Enum
import os

BASE = os.path.abspath(os.path.dirname(__file__))

class DatasetType(Enum):
    """Available dataset types."""

    BOARDS = "boards.json"
    PRODUCTS = "products.json"


class VendorName(Enum):
    """Available vendors."""

    WORX = "worx"


class Dataset:
    """Handling the datasets."""

    __vendor: str

    def __init__(self, vendor: VendorName) -> None:
        """Initialize dataset object for vendor."""
        self.__vendor = vendor.value

    def load(self, dataset: DatasetType) -> str:
        """Load specific dataset."""
        with open(f"{BASE}/{self.__vendor}/{dataset.value}", encoding="utf-8") as file:
            data = file.read()

        return data
