""" Tests for documnet classifier tool """
from rho_ml import Version
from sermos_tools.catalog.document_classifier.document_classifier import (
    DocumentClassifier, )
from sklearn.datasets import fetch_20newsgroups


def test_new_classifier():
    train = fetch_20newsgroups(subset="train", shuffle=True)
    test = fetch_20newsgroups(subset="test", shuffle=True)
    x_train, y_train = train.data[:100], train.target[:100]
    x_test, y_test = test.data[:10], test.target[:10]
    new_classifier_tool = DocumentClassifier.create_new_classifier(
        model_name="some_name",
        version=Version.from_string("0.0.1"),
        text_iter=x_train,
        classes=y_train,
        save_model=False,
    )
    classified_result = new_classifier_tool.classify_batch(text_iter=x_test)

    assert classified_result.shape == y_test.shape
