""" Test Text Extraction tooling
"""
import re
from sermos_tools.catalog.text_extractor import TextExtractor


class TestToolsTextExtractor:
    """ Test Text Extractor
    """
    with open('tests/fixtures/pdfs/sample-pdf-1.pdf', 'rb') as f:
        sample_pdf = f.read()

    with open('tests/fixtures/html/sample-html-1.html', 'rb') as f:
        sample_html = f.read()

    with open('tests/fixtures/text/sample-pdf-1-text.txt', 'r') as f:
        sample_pdf_text = f.read()

    with open('tests/fixtures/text/sample-html-1-text.txt', 'r') as f:
        sample_html_text = f.read()

    def test_text_extractor_on_pdf(self):
        """ Test loading PDF object bytes and extracting text.
        """
        text_extractor = TextExtractor(document_bytes=self.sample_pdf)

        fulltext = text_extractor.full_text
        assert _normalize_text(fulltext) == _normalize_text(
            self.sample_pdf_text)

    def test_text_extractor_on_html(self):
        """ Test loading HTML object bytes and extracting text w/o tags.
        """
        text_extractor = TextExtractor(document_bytes=self.sample_html)
        fulltext = text_extractor.full_text
        assert _normalize_text(fulltext) == _normalize_text(
            self.sample_html_text)


def _normalize_text(text: str) -> str:
    """ Normalize all whitespace to a single space"""
    return re.sub(r'\s+', ' ', text)
