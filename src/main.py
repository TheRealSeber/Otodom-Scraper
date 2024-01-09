from crawler import Crawler


def main():
    crawler = Crawler()
    crawler.start()
    crawler.to_csv_file("listings.csv")


if "__main__" == __name__:
    main()
