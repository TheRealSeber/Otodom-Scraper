from listing import Listing


def remove_duplicated_listings(listings: list) -> set:
    """
    Remove duplicated listings.

    :param listings: The listings
    :return: The listings without duplicates
    """
    flattened_set = {value for sublist in listings for value in sublist}
    links = set()
    filtered_set = set()
    for listing in flattened_set:
        link = Listing.extract_link(listing)
        if link not in links:
            filtered_set.add(listing)
        links.add(link)

    return filtered_set
