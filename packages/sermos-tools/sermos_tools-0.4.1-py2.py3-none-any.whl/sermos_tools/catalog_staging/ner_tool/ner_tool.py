""" A tool for fine-tuning BERT-base for NER.

    To use in an API class, follow the standard convention accessing the
    ``tools`` property that Sermos injects.

    Example::

        class DemoApiClass(object):
            def post(self, vectors: csr_matrix):
                ner_tool = self.tools['ner_tool']\\
                    .restore_existing_search_index(model_name='my_model_name',
                                                   version_pattern='0.*.*',
                                                   force_search=True)
                ner_results = ner_tool.augment_batch(
                    text_iter=text_list)
                ...

    To use in a worker method, follow the standard convention accessing the
    ``tools`` argument that Sermos injects.

    Example::

        def demo_worker_task(event, tools):
            ner_tool = tools['text_ner']\\
                    .restore_existing_search_index(model_name='my_model_name',
                                                   version_pattern='0.*.*',
                                                   force_search=True)
            augmented_results = ner_tool.augment_batch(
                text_iter=text_list)

    Note: First time you run, it will take considerable amount of time because of the following reasons -

    Downloads pre-trained BERT-base model (Depends on your Network Speed)
    Fine-tunes the BERT with your dataset (Depends on size of the data, Epochs, Hyperparameters, etc)

"""

from sermos_tools import SermosTool
from scipy.sparse import csr_matrix
from rho_ml import RhoModel, Version, load_rho_model,\
    store_rho_model, ModelNotFoundError
import attr
import logging
from typing import Any
from sermos_tools.catalog_staging.ner_tool import predict
from sermos_tools.catalog_staging.ner_tool.ner_utils import train

logger = logging.getLogger(__name__)


@attr.s
class Ner(RhoModel):
    """ Generate NER and POS tags for text vectors using a fine-tuned BERT model. """
    def validate_training_input(self, data: Any):
        pass

    def validate_training_output(self, data: Any):
        pass  # no output data

    def validate_prediction_input(self, data: Any):
        return self.validate_training_input(data=data)

    def validate_prediction_output(self, data: Any):
        pass

    def train_logic(self, *fit_args, **fit_kwargs) -> Any:
        """Trains on the dataset present in input/ner_dataset.txt. Refer to the sample to know the format of the data required for training.

        Returns:
            Model: Fine-tuned BERT- NER model
        """
        logger.info("Beginning fitting of textner...")
        fitted_ner = train.run_training()
        logger.info("Finished fitting Rhotextner!")
        return fitted_ner

    def predict_logic(self, sentence, *args, **kwargs) -> Any:
        """Returns the predicted NER ans POS tags for a given sentence using the fine-tuned model.

        Args:
            sentence ([str]): A text string to generate the tags for.

        Returns:
            ner_tags, pos_tags: Returns the lists of ner and pos tags as a tuple with two items.
        """
        ner_tags, pos_tags = predict.predict(sentence=sentence)
        return ner_tags, pos_tags


class NerTool(SermosTool):
    """ Tool for Fine-tuning BERT for Named Entity and POS tag generation.

    This tool should almost always be instantiated via one of two classmethods,
    :meth:`~.TextnerTool.create_new_ner` for building a new
    ner, and :meth:`~.TextnerTool.restore_existing_ner`
    for pulling an existing ner from local or cloud storage.
    """

    tool_key = "ner_tool"

    def __init__(self, ner_model: Ner):
        self.ner_model = ner_model

    @classmethod
    def restore_existing_ner_tool(cls, model_name: str, version_pattern: str,
                                  force_search: bool) -> "NerTool":
        """ Instantiate a text ner from local or cloud storage.

        Given the version pattern, load the appropriate model from local
        storage (if available) or cloud storage.  If force_search == True, cloud
        storage will always be checked to see if there is a higher version
        available in the cloud than locally.

        Args:
            model_name (str): ner model name
            version_pattern (str): Version pattern (incl. wildcards) to search
                for
            force_search (bool): Check cloud storage for a higher version even
                if a matching local version exists.

        Returns:
            NerTool: instantiated ner tool
        """
        try:
            model = load_rho_model(
                model_name=model_name,
                version_pattern=version_pattern,
                force_search=force_search,
            )
            logger.info(
                f"Loaded model {model.name}, version {model.version} to "
                f"NER tool")
            return cls(ner_model=model)
        except ModelNotFoundError:
            logger.warning(f"No model found by name {model_name}, version "
                           f"{version_pattern} (force search: {force_search}")
        return None

    @classmethod
    def create_new_ner_tool(
        cls,
        model_name: str,
        version: Version,
        save_model: bool = True,
    ) -> "NerTool":
        """ Create a new ner tool from scratch.

        Args:
            model_name (str): model name for the new search tool
            version (str): version for the newly created tool
            save_model (bool): If `True` store the model in the cloud after
                indexing.

        Returns:
            NerTool: instantiated ner tool
        """
        model = Ner(
            name=model_name,
            version=version,
        )
        model.train(run_validation=True)
        tool = cls(ner_model=model)
        logger.info(f"Created new ner model {model.name}, "
                    f"version {model.version}")
        if save_model:
            store_rho_model(model=model)
        return tool

    def predict_tags(self, text_iter_n) -> csr_matrix:
        """ Use text ner to transform texts into augmented text.

        Args:
            text_iter_n (int): No. of sentences from the dataset to augment
            using trained ner.

        Returns:
            augmented_text: Iterable of augmented texts
        """
        ner_tags, pos_tags = self.ner_model.predict(sentence,
                                                    run_validation=True)
        return ner_tags, pos_tags
