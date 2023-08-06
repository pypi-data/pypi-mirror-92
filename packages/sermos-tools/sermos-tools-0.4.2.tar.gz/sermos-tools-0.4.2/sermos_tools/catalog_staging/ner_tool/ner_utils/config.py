import os
from transformers import BertTokenizer

MAX_LEN = int(os.environ.get("NER_MAX_SEQ_LEN", 128))
TRAIN_BATCH_SIZE = int(os.environ.get("NER_TRAIN_BATCH_SIZE", 32))
VALID_BATCH_SIZE = int(os.environ.get("NER_VALID_BATCH_SIZE", 8))
EPOCHS = int(os.environ.get("NER_TRAIN_BATCH_SIZE", 5))
BASE_MODEL = os.environ.get("NER_MODEL", "bert-base-uncased")
MODEL_PATH = "./model.bin"
TRAINING_FILE = "../input/ner_dataset.csv"
TOKENIZER = BertTokenizer.from_pretrained(BASE_MODEL, do_lower_case=True)
