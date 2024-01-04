class DataExtractionError(Exception):
    """
    Exception raised when the data extraction from the HTML fails.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, url=None, message="Error during extracting the data!") -> None:
        if url is not None:
            message += f" URL: {url}"
        super().__init__(message)
