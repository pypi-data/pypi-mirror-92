""" Test Text Summarizer Tooling
"""
from sermos_tools.catalog_staging.text_summarizer.text_summarizer import TextSummarizer


class TestToolsSummarizer:
    """ Test text Summarizer
    """
    with open('tests/fixtures/text/sample-pdf-1-text.txt', 'r') as f:
        sample_text = f.read()

    def test_summarizer_on_text(self):
        """ Test summarizing string of text.
        """
        summarizer = TextSummarizer(text=self.sample_text)

        # Test proper summarization
        summarized = summarizer.summarize()
        assert isinstance(summarized, str)
        assert len(summarized) <= len(self.sample_text)