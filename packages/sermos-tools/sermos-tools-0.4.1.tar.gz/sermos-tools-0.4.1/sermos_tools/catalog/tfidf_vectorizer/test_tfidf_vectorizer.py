""" Tests for sparse embedding search tool """
import scipy.sparse as sparse
from rho_ml import Version
from sermos_tools.catalog.tfidf_vectorizer.tfidf_vectorizer import TfidfVectorizer


def test_new_tfidf_vector():
    corpus = [
        'This is the first document.',
        'This document is the second document.',
        'And this is the third one.',
        'Is this the first document?',
    ]
    new_vectorizer_tool = TfidfVectorizer.create_new_vectorizer(
        model_name='some_name',
        version=Version.from_string("0.0.1"),
        text_iter=corpus,
        save_model=False)
    tfidf_vectorized_result = new_vectorizer_tool.vectorize_batch(
        text_iter=corpus)
    assert sparse.issparse(tfidf_vectorized_result)
    assert tfidf_vectorized_result.shape[0] == len(corpus)
