import os

BATCH_SIZE = int(os.environ.get("AUG_BATCH_SIZE", 32))
EPOCHS = int(os.environ.get("AUG_EPOCHS", 3))
LEARNING_RATE = int(os.environ.get("AUG_LEARNING_RATE", 3e-5))
WARMUP_STEPS = int(os.environ.get("AUG_WARMUP_STEPS", 300))
MAX_SEQ_LEN = int(os.environ.get("AUG_MAX_SEQ_LEN", 200))
MODEL_NAME = str(os.environ.get("AUG_MODEL_NAME", 'text_augmenter_model.pt'))
DATA_FILE = str(os.environ.get("AUG_DATA_FILE", './data/sample_dataset.txt'))
