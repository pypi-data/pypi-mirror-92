""" A tool for classifying document sets amongst pre-determined labels.

    To use in an API class, follow the standard convention accessing the
    ``tools`` property that Sermos injects.

    Example::

        class DemoApiClass(object):
            def post(self, document_list: Iterable[Iterable]):
                classifier_tool = self.tools['document_classifier']\\
                    .restore_existing_search_index(model_name='my_model_name',
                                                   version_pattern='0.*.*',
                                                   force_search=True)
                classified_results = classifier_tool.classify_batch(
                    text_iter=text_list)
                ...

    To use in a worker method, follow the standard convention accessing the
    ``tools`` argument that Sermos injects.

    Example::

        def demo_worker_task(event, tools):
            classifier_tool = tools['document_classifier']\\
                    .restore_existing_search_index(model_name='my_model_name',
                                                   version_pattern='0.*.*',
                                                   force_search=True)
            classified_results = classifier_tool.classify_batch(
                text_iter=text_list)

"""

import logging
from typing import Any, Dict, Iterable

import attr
from cytoolz.itertoolz import first, second
from numpy import array
from rho_ml import (RhoModel, ValidationFailedError, Version, load_rho_model,
                    ModelNotFoundError, store_rho_model)
from xgboost import XGBClassifier

from sermos_tools import SermosTool
from sermos_tools.catalog.tfidf_vectorizer import tfidf_vectorizer

logger = logging.getLogger(__name__)


@attr.s
class RhoDocumentClassifierModel(RhoModel):
    """ Classify documents into known labels/classes. The index
    is fixed after init (i.e. no dynamic updates) """

    classifier = attr.ib(default=None, kw_only=True)

    def validate_training_input(self, data: Any):
        """ Verify the input is in right format. Input should ideally be a
        list of two iterables. First element should be an Iterable of strings,
        second element should be an Iterable of integers representing the
        classes"""
        fst = first(data)
        scnd = second(data)
        if not isinstance(fst, Iterable) or not isinstance(scnd, Iterable):
            raise ValidationFailedError(
                "Need to pass a list of two iterables!")

    def validate_training_output(self, data: Any):
        pass  # no output data

    def validate_prediction_input(self, data: Any):
        return self.validate_training_input(data=data)

    def validate_prediction_output(self, data: Any):
        if not hasattr(data, "shape"):
            raise ValidationFailedError("Model output expected to be np.array "
                                        ", received {}".format(type(data)))

    def train_logic(self, training_data: Dict, *fit_args, **fit_kwargs) -> Any:
        logger.info("Beginning fitting of RhoDocumentClassifierModel...")
        fitted_classifier = self.classifier.fit(training_data[0],
                                                training_data[1], *fit_args,
                                                **fit_kwargs)
        logger.info("Finished fitting RhoDocumentClassifierModel!")
        return fitted_classifier

    def predict_logic(self, prediction_data: Iterable[str], *args,
                      **kwargs) -> Any:
        result = self.classifier.predict(prediction_data)
        return result


class DocumentClassifier(SermosTool):
    """ Create sparse TfIdf vectors for an iterable of text.

    Given an iterable of strings, generate a :meth:`~.scipy.sparse.csr_matrix`
    of TfIdf vectors.

    This tool should almost always be instantiated via one of two classmethods,
    :meth:`~.RhoDocumentClassifierTool.create_new_classifier` for building a new
    classifier, and :meth:`~RhoDocumentClassifierTool.restore_existing_classifier`
    for pulling an existing vectorizer from local or cloud storage.
    """

    tool_key = "document_classifier"

    def __init__(
        self,
        classifier_model: RhoDocumentClassifierModel,
        vectorizer_model: tfidf_vectorizer.TfidfVectorizer,
    ):
        self.classifier_model = classifier_model
        self.vectorizer_model = vectorizer_model

    @classmethod
    def restore_existing_classifier(
            cls, model_name: str, version_pattern: str,
            force_search: bool) -> "DocumentClassifier":
        """ Instantiate a xgboost Document Classifier model from local or cloud storage.

        Given the version pattern, load the appropriate model from local storage (if available) or cloud storage. If
        force_search == True, cloud storage will always be checked to see if there is a higher version
        available in the cloud than locally.

        Args:
            model_name (str): Classifier name
            version_pattern (str): Version pattern (incl. wildcards) to search
                for
            force_search (bool): Check cloud storage for a higher version even
                if a matching local version exists.

        Returns:
            DocumentClassifier: instantiated classifier tool
        """
        try:
            model = load_rho_model(
                model_name=model_name,
                version_pattern=version_pattern,
                force_search=force_search,
            )
            logger.info(
                f"Loaded model {model.name}, version {model.version} to "
                f"classifier tool")
            return cls(
                classifier_model=model.classifier_model,
                vectorizer_model=model.vectorizer_model,
            )
        except ModelNotFoundError:
            logger.warning(f"No model found by name {model_name}, version "
                           f"{version_pattern} (force search: {force_search}")
        return None

    @classmethod
    def create_new_classifier(
        cls,
        model_name: str,
        version: Version,
        text_iter: Iterable[str],
        classes: Iterable[str],
        save_model: bool = True,
        **classifier_params,
    ) -> "DocumentClassifier":
        """ Create a new xgboost Document Classifier model from scratch.

        Args:
            model_name (str): model name for the new search tool
            version (str): version for the newly created tool
            text_iter (Iterable[str]): Iterable of strings to fit the classifier with.
            classes (Iterable[int]): Iterable of integer encoded classes(target values) to fit the classifier with.
            save_model (bool): If `True` store the model in the cloud after indexing.
            **classifier_params: Any of the
            meth:`~.xgboost.XGBClassifier` params.

        Returns:
            DocumentClassifier: instantiated classifer tool
        """
        classifier = XGBClassifier(**classifier_params)
        classifier_model = RhoDocumentClassifierModel(name=model_name,
                                                      version=version,
                                                      classifier=classifier)
        vectorizer_tool = tfidf_vectorizer.TfidfVectorizer.create_new_vectorizer(
            model_name="temp1",
            version=Version.from_string("0.0.1"),
            text_iter=text_iter,
            save_model=False,
        )
        # text_iter_tfidf = cls._convert_batch_to_tfidf(text_iter)
        text_iter_tfidf = vectorizer_tool.vectorize_batch(text_iter)
        training_data = [text_iter_tfidf, classes]
        classifier_model.train(training_data=training_data,
                               run_validation=True)
        tool = cls(classifier_model=classifier_model,
                   vectorizer_model=vectorizer_tool)
        logger.info(f"Created new classifier model {classifier_model.name}, "
                    f"version {classifier_model.version}")
        if save_model:
            store_rho_model(model=classifier_model)
        return tool

    def classify_batch(self, text_iter: Iterable[str]) -> array:
        """ Use a fitted xgboost classifier model to predict class of each string.

        Args:
            text_iter (Iterable[str]): Iterable of strings to classify using trained classifier.

        Returns:
            classified_text: numpy array of size(n_samples) containing the predicted integer classes.
        """
        # text_iter_tfidf = self._convert_batch_to_tfidf(text_iter, test=True)
        text_iter_tfidf = self.vectorizer_model.vectorize_batch(text_iter)
        classified_text = self.classifier_model.predict(text_iter_tfidf,
                                                        run_validation=False)
        return classified_text
