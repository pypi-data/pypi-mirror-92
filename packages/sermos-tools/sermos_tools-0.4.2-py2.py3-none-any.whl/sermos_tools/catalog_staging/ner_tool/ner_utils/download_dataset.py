""" A utility to download a dataset locally in your current directory.
    To use in an API class, follow the standard convention accessing the
    ``tools`` property that Sermos injects.

    Example::

        class DemoApiClass(object):
            def post(self):
                TODO: Example

    To use in a worker method, follow the standard convention accessing the
    ``tools`` argument that Sermos injects.

    Example::

        def demo_worker_task(event, tools):
            TODO: Example

"""
import wget
import os
import logging
from sermos.tools import SermosTool

logger = logging.getLogger(__name__)


class RhoDatasetDownloader(SermosTool):
    """ Download dataset from the given url.
        Usage::

            downloader = RhoDatasetDownloader(url='/my_dataset_link')
            dataset = downloader.get_dataset()
    """
    def get_dataset(self, url: str):
        """Get the dataset from the given url in your current directory.

        Args:
            url (str): The url of the dataset passed as a string.
        """
        name = url.split("/")[-1]
        if not os.path.exists("./sermos/tools/ner_tool/input/" + name):
            wget.download(url, "./sermos/tools/ner_tool/input/" + name)
        logger.info(f"Downloaded {name}")


if __name__ == "__main__":
    url_train = (
        "https://groups.csail.mit.edu/sls/downloads/restaurant/restauranttrain.bio"
    )
    url_test = (
        "https://groups.csail.mit.edu/sls/downloads/restaurant/restauranttest.bio"
    )
    downloader = RhoDatasetDownloader()
    downloader.get_dataset(url_train)
    downloader.get_dataset(url_test)
