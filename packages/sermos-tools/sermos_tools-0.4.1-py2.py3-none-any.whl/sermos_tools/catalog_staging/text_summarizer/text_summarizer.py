""" A tool for extractive text summarization with BERT.

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
import logging
import attr
from sermos_tools import SermosTool
from summarizer import Summarizer

logger = logging.getLogger(__name__)


@attr.s
class TextSummarizer(SermosTool):
    """ Perform extractive text summarization on the given text.
        Usage::

            summarizer = TextSummarizer(full_text='my text here')
            summarized_text = summarizer.summarize()
    """
    text: str = attr.ib()

    def summarize(self) -> str:
        """Summarize the given text while initializer the TextSummarizer object.

        Returns:
            str: summarized text.
        """

        model = Summarizer()
        summarized_text = model(self.text)
        return summarized_text
