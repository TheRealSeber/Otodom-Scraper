
# Otodom Scraper

**Otodom Scraper** is a simple python module, which is capable of scraping **thousands of listings within a minutes** from the polish property marketplace site otodom.pl. From each of the listing, there may be **more than 30** parameters fetched.

Integrated with **MongoDB** gives a powerfull combo in managing found listings. It is possible to extract data to the both **CSV** and **JSON** file.

**Every module has a well-written documentatation** to make possibly future changes developer-friendly.


## Setup

1. Ensure you have Python 3.11+ installed on your machine.
2. Clone repository:
```bash
git clone https://github.com/TheRealSeber/Otodom-Listings-Scraper.git
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Prepare settings.json - open the example file and everything should be clear

## Usage

You can run **Crawler** with the following code:
```python
# main.py

from crawler import Crawler

crawler =  Crawler()
crawler.start()
crawler.to_csv_file("listings.csv")
```
There is also a method `to_json_file` which can save listings to JSON format. During the extraction of the data informational logs are going to be printed. **Crawler internally connects with MongoDB, host MUST BE defined in settings.json**

If you would like to **save the listings from the database** you can run following code:
```python
# main.py

from services import PropertyService
from services import connect_to_database

connect_to_database(host="mongodb://localhost:27017/otodomscraper")
PropertyService.to_json_file("properties.csv",  include_agencies=True)
```
For more details of the functions read the source code as everything have docstrings and is written in **KISS** convention, so it should be understandable :)

## Contributing

Pull requests are welcome. Please stick to **conventional commits** before pushing any changes. For major changes, please open an issue first to discuss what you would like to change.
