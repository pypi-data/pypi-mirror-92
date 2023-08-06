""" A tool for vectorizing document sets.

    To use in an API class, follow the standard convention accessing the
    ``tools`` property that Sermos injects.

    Example::

        class DemoApiClass(object):
            def post(self, vectors: csr_matrix):
                vectorizer_tool = self.tools['tfidf_vectorizer']\\
                    .restore_existing_search_index(model_name='my_model_name',
                                                   version_pattern='0.*.*',
                                                   force_search=True)
                vectorized_results = vectorizer_tool.vectorize_batch(
                    text_iter=text_list)
                ...

    To use in a worker method, follow the standard convention accessing the
    ``tools`` argument that Sermos injects.

    Example::

        def demo_worker_task(event, tools):
            vectorizer_tool = tools['tfidf_vectorizer']\\
                    .restore_existing_search_index(model_name='my_model_name',
                                                   version_pattern='0.*.*',
                                                   force_search=True)
            vectorized_results = vectorizer_tool.vectorize_batch(
                text_iter=text_list)

"""

import logging
from typing import Any, Iterable

import attr
from cytoolz.itertoolz import first
from rho_ml import RhoModel, ValidationFailedError, Version, load_rho_model, \
    store_rho_model, ModelNotFoundError
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer \
    as SklearnTfidfVectorizer

from sermos_tools import SermosTool

logger = logging.getLogger(__name__)


@attr.s
class TfidfVectorizerModel(RhoModel):
    """ Generate sparse TfIdf document vectors. The index
    is fixed after init (i.e. no dynamic updates) """

    vectorizer = attr.ib(default=None, kw_only=True)

    def validate_training_input(self, data: Any):
        """ Verify the raw_texts are correct"""
        el = first(data)
        if not isinstance(el, str) or isinstance(data, str):
            raise ValidationFailedError("Need to pass an iterable of strings!")

    def validate_training_output(self, data: Any):
        pass  # no output data

    def validate_prediction_input(self, data: Any):
        return self.validate_training_input(data=data)

    def validate_prediction_output(self, data: Any):
        if not hasattr(data, "shape"):
            raise ValidationFailedError("Model output expected to be np.array "
                                        ", received {}".format(type(data)))

    def train_logic(self, training_data: Iterable[str], *fit_args,
                    **fit_kwargs) -> Any:
        logger.info("Beginning fitting of RhoTfidfVectorizer...")
        fitted_vectorizer = self.vectorizer.fit(training_data, *fit_args,
                                                **fit_kwargs)
        logger.info("Finished fitting RhoTfidfVectorizer!")
        return fitted_vectorizer

    def predict_logic(self, prediction_data: Iterable[str], *args,
                      **kwargs) -> Any:
        result = self.vectorizer.transform(raw_documents=prediction_data)
        return result


class TfidfVectorizer(SermosTool):
    """ Create sparse TfIdf vectors for an iterable of text.

    Given an iterable of strings, generate a :meth:`~.scipy.sparse.csr_matrix`
    of TfIdf vectors.

    This tool should almost always be instantiated via one of two classmethods,
    :meth:`~.RhoTfidfVectorizerTool.create_new_vectorizer` for building a new
    vectorizer, and :meth:`~RhoTfidfVectorizerTool.restore_existing_vectorizer`
    for pulling an existing vectorizer from local or cloud storage.
    """

    tool_key = "tfidf_vectorizer"

    def __init__(self, vectorizer_model: TfidfVectorizerModel):
        self.vectorizer_model = vectorizer_model

    @classmethod
    def restore_existing_vectorizer(cls, model_name: str, version_pattern: str,
                                    force_search: bool) -> "TfidfVectorizer":
        """ Instantiate a TfIdf Vectorizer from local or cloud storage.

        Given the version pattern, load the appropriate model from local
        storage (if available) or cloud storage.  If force_search == True, cloud
        storage will always be checked to see if there is a higher version
        available in the cloud than locally.

        Args:
            model_name (str): Vectorizer name
            version_pattern (str): Version pattern (incl. wildcards) to search
                for
            force_search (bool): Check cloud storage for a higher version even
                if a matching local version exists.

        Returns:
            TfidfVectorizer: instantiated vectorizer tool
        """
        try:
            model = load_rho_model(
                model_name=model_name,
                version_pattern=version_pattern,
                force_search=force_search,
            )
            logger.info(
                f"Loaded model {model.name}, version {model.version} to "
                f"vectorizer tool")
            return cls(vectorizer_model=model)
        except ModelNotFoundError:
            logger.warning(f"No model found by name {model_name}, version "
                           f"{version_pattern} (force search: {force_search}")
        return None

    @classmethod
    def create_new_vectorizer(
        cls,
        model_name: str,
        version: Version,
        text_iter: Iterable[str],
        save_model: bool = True,
        **vectorizer_params,
    ) -> "TfidfVectorizer":
        """ Create a new TfIdf Vectorizer from scratch.

        Args:
            model_name (str): model name for the new search tool
            version (str): version for the newly created tool
            text_iter (Iterable[str]): Iterable of strings to fit the vectorizer
            with.
            save_model (bool): If `True` store the model in the cloud after
                indexing.
            **vectorizer_params: Any of the sklearn TfIdf Vectorizer
            meth:`~.sklearn.feature_extraction.text.TfidfVectorizer` params.

        Returns:
            TfidfVectorizer: instantiated vectorizer tool
        """
        vectorizer = SklearnTfidfVectorizer(**vectorizer_params)
        model = TfidfVectorizerModel(
            name=model_name,
            version=version,
            vectorizer=vectorizer,
        )
        model.train(training_data=text_iter, run_validation=True)
        tool = cls(vectorizer_model=model)
        logger.info(f"Created new vectorizer model {model.name}, "
                    f"version {model.version}")
        if save_model:
            store_rho_model(model=model)
        return tool

    def vectorize_batch(self, text_iter: Iterable[str]) -> csr_matrix:
        """ Use TfIdf vectorizer to transform texts into sparse matrix.

        Args:
            text_iter (Iterable[str]): Iterable of strings to transform
            using trained vectorizer.

        Returns:
            vectorized_text: Sparse csr_matrix of size(n_samples, n_features) composed of Tfidf vectors.
        """
        vectorized_text = self.vectorizer_model.predict(text_iter,
                                                        run_validation=True)
        return vectorized_text
