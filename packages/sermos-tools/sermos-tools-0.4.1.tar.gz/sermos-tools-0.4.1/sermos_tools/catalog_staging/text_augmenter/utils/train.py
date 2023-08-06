import csv
import os
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from torch.utils.data import Dataset, DataLoader
from transformers import AdamW, get_cosine_with_hard_restarts_schedule_with_warmup
import warnings
import sermos_tools.catalog_staging.text_augmenter.utils.config as config
warnings.filterwarnings('ignore')


class MyDataset(Dataset):
    def __init__(self, data_file_name, data_dir='.data/'):
        super().__init__()

        data_path = os.path.join(data_file_name)

        self.data_list = []
        self.end_of_text_token = " <|endoftext|> "

        with open(data_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')

            for row in csv_reader:
                data_str = f"{row[0]}: {row[1]}{self.end_of_text_token}"
                self.data_list.append(data_str)

    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, item):
        return self.data_list[item]


def get_data_loader(data_file_name):
    dataset = MyDataset(data_file_name)
    data_loader = DataLoader(dataset, batch_size=1, shuffle=True)
    return data_loader


def train(epochs, data_loader, batch_size, tokenizer, model, device):
    batch_counter = 0
    sum_loss = 0.0

    for epoch in range(epochs):
        print(f'Running {epoch+1} epoch')

        for idx, txt in enumerate(data_loader):
            txt = torch.tensor(tokenizer.encode(txt[0]))
            txt = txt.unsqueeze(0).to(device)
            outputs = model(txt, labels=txt)
            loss, _ = outputs[:2]
            loss.backward()
            sum_loss += loss.data

            if idx % batch_size == 0:
                batch_counter += 1
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
                model.zero_grad()

            if batch_counter == 10:
                print(f"Total Loss is {sum_loss}"
                      )  #printed after every 10*batch_size
                batch_counter = 0
                sum_loss = 0.0

    return model


def save_model(model, name):
    """
	Summary:
		Saving model to the Disk
	Parameters:
		model: Trained model object
		name: Name of the model to be saved
	"""
    print("Saving model to Disk")
    torch.save(model.state_dict(), f"{name}.pt")
    return


def load_models():
    """
	Summary:
		Loading Pre-trained model
	"""
    print('Loading/Downloading GPT-2 Model')
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
    model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
    return tokenizer, model


def run_training():

    BATCH_SIZE = config.BATCH_SIZE
    EPOCHS = config.EPOCHS
    LEARNING_RATE = config.LEARNING_RATE
    WARMUP_STEPS = config.WARMUP_STEPS
    MAX_SEQ_LEN = config.MAX_SEQ_LEN
    MODEL_NAME = config.MODEL_NAME
    DATA_FILE = config.DATA_FILE

    TOKENIZER, MODEL = load_models()
    LOADER = get_data_loader(DATA_FILE)

    DEVICE = 'cpu'
    if torch.cuda.is_available():
        DEVICE = 'cuda'

    model = MODEL.to(DEVICE)
    model.train()
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    scheduler = get_cosine_with_hard_restarts_schedule_with_warmup(
        optimizer, num_warmup_steps=WARMUP_STEPS, num_training_steps=-1)

    model = train(EPOCHS, LOADER, BATCH_SIZE, TOKENIZER, MODEL, DEVICE)
    save_model(model, MODEL_NAME)
    return model
