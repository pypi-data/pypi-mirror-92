""" A tool for augmenting a document of text with gpt-2.

    To use in an API class, follow the standard convention accessing the
    ``tools`` property that Sermos injects.

    Example::

        class DemoApiClass(object):
            def post(self, vectors: csr_matrix):
                augmenter_tool = self.tools['text_augmenter']\\
                    .restore_existing_search_index(model_name='my_model_name',
                                                   version_pattern='0.*.*',
                                                   force_search=True)
                augmented_results = augmenter_tool.augment_batch(
                    text_iter=text_list)
                ...

    To use in a worker method, follow the standard convention accessing the
    ``tools`` argument that Sermos injects.

    Example::

        def demo_worker_task(event, tools):
            augmenter_tool = tools['text_augmenter']\\
                    .restore_existing_search_index(model_name='my_model_name',
                                                   version_pattern='0.*.*',
                                                   force_search=True)
            augmented_results = augmenter_tool.augment_batch(
                text_iter=text_list)
    Note: First time you run, it will take considerable amount of time because of the following reasons -

    Downloads pre-trained gpt2-medium model (Depends on your Network Speed)
    Fine-tunes the gpt2 with your dataset (Depends on size of the data, Epochs, Hyperparameters, etc)

"""

from sermos_tools import SermosTool
#from sermos_utils.rho_model import load_rho_model, ModelNotFoundError, store_rho_model
from scipy.sparse import csr_matrix
from rho_ml import RhoModel, Version, load_rho_model,\
    store_rho_model, ModelNotFoundError
import attr
import logging
from typing import Any

logger = logging.getLogger(__name__)


@attr.s
class TextAugmenter(RhoModel):
    """ Generate augmented text vectors. """
    def validate_training_input(self, data: Any):
        pass

    def validate_training_output(self, data: Any):
        pass  # no output data

    def validate_prediction_input(self, data: Any):
        return self.validate_training_input(data=data)

    def validate_prediction_output(self, data: Any):
        pass

    def train_logic(self, *fit_args, **fit_kwargs) -> Any:
        """Trains on the dataset present in data/sample_dataset.txt. Refer to the sample to know the format of the data required for training.

        Returns:
            Model: Fine-tuned gpt-2 text-augmenter model
        """
        logger.info("Beginning fitting of textaugmenter...")
        fitted_augmenter = self.augmenter.run_training()
        logger.info("Finished fitting Rhotextaugmenter!")
        return fitted_augmenter

    def predict_logic(self, text_iter_n, *args, **kwargs) -> Any:
        result = self.augmenter.generate_text(sentences=text_iter_n)
        return result


class TextAugmenterTool(SermosTool):
    """ Augment an iterable of text using a fine-tuned gpt-2 model.

    This tool should almost always be instantiated via one of two classmethods,
    :meth:`~.TextAugmenterTool.create_new_augmenter` for building a new
    augmenter, and :meth:`~.TextAugmenterTool.restore_existing_augmenter`
    for pulling an existing augmenter from local or cloud storage.
    """

    tool_key = "text_augmenter"

    def __init__(self, augmenter_model: TextAugmenter):
        self.augmenter_model = augmenter_model

    @classmethod
    def restore_existing_augmenter(
            cls, model_name: str, version_pattern: str,
            force_search: bool) -> "RhotextaugmenterTool":
        """ Instantiate a text augmenter from local or cloud storage.

        Given the version pattern, load the appropriate model from local
        storage (if available) or cloud storage.  If force_search == True, cloud
        storage will always be checked to see if there is a higher version
        available in the cloud than locally.

        Args:
            model_name (str): augmenter name
            version_pattern (str): Version pattern (incl. wildcards) to search
                for
            force_search (bool): Check cloud storage for a higher version even
                if a matching local version exists.

        Returns:
            RhotextaugmenterTool: instantiated augmenter tool
        """
        try:
            model = load_rho_model(
                model_name=model_name,
                version_pattern=version_pattern,
                force_search=force_search,
            )
            logger.info(
                f"Loaded model {model.name}, version {model.version} to "
                f"augmenter tool")
            return cls(augmenter_model=model)
        except ModelNotFoundError:
            logger.warning(f"No model found by name {model_name}, version "
                           f"{version_pattern} (force search: {force_search}")
        return None

    @classmethod
    def create_new_augmenter(
        cls,
        model_name: str,
        version: Version,
        save_model: bool = True,
        **augmenter_params,
    ) -> "RhotextaugmenterTool":
        """ Create a new text augmenter from scratch.

        Args:
            model_name (str): model name for the new search tool
            version (str): version for the newly created tool
            save_model (bool): If `True` store the model in the cloud after
                indexing.
            **augmenter_params: Any of the sklearn text augmenter
            meth:`~.sklearn.feature_extraction.text.textaugmenter` params.

        Returns:
            RhotextaugmenterTool: instantiated augmenter tool
        """
        model = TextAugmenter(
            name=model_name,
            version=version,
        )
        model.train(run_validation=True)
        tool = cls(augmenter_model=model)
        logger.info(f"Created new augmenter model {model.name}, "
                    f"version {model.version}")
        if save_model:
            store_rho_model(model=model)
        return tool

    def augment_batch(self, text_iter_n) -> csr_matrix:
        """ Use text augmenter to transform texts into augmented text.

        Args:
            text_iter_n (int): No. of sentences from the dataset to augment
            using trained augmenter.

        Returns:
            augmented_text: Iterable of augmented texts
        """
        augmented_text = self.augmenter_model.predict(text_iter_n,
                                                      run_validation=True)
        return augmented_text
