import csv
import json

from crawler.listing import Listing


def to_csv_file(filename: str, listings: list[Listing]) -> None:
    """
    Save the listings to a csv file.

    :param filename: The name of the file
    """
    data = [obj.to_dict() for obj in listings]

    keys = {key for dict_ in data for key in dict_.keys()}

    with open(filename, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, sorted(keys))
        dict_writer.writeheader()
        dict_writer.writerows(data)


def to_json_file(filename: str, listings: list[Listing]) -> None:
    """
    Save the listings to a json file.

    :param filename: The name of the file
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            [listing.to_dict() for listing in listings],
            file,
            ensure_ascii=False,
            default=str,
            indent=4,
        )
