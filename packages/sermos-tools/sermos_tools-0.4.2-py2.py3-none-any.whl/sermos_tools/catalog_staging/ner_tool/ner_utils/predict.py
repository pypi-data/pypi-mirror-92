import joblib
import torch

from sermos_tools.catalog_staging.ner_tool.ner_utils import config, dataset
from sermos_tools.catalog_staging.ner_tool import EntityModel


def predict(sentence='Popeye the sailor man loves spinach'):
    """
    Predicts ner and pos tags for the a given sentence, using the fine-tuned model
    """
    meta_data = joblib.load("meta.bin")
    enc_pos = meta_data["enc_pos"]
    enc_tag = meta_data["enc_tag"]

    num_pos = len(list(enc_pos.classes_))
    num_tag = len(list(enc_tag.classes_))

    tokenized_sentence = config.TOKENIZER.encode(sentence)

    sentence = sentence.split()
    print(sentence)
    print(tokenized_sentence)

    test_dataset = dataset.EntityDataset(texts=[sentence],
                                         pos=[[0] * len(sentence)],
                                         tags=[[0] * len(sentence)])

    device = torch.device("cuda")
    model = EntityModel(num_tag=num_tag, num_pos=num_pos)
    model.load_state_dict(torch.load(config.MODEL_PATH))
    model.to(device)

    with torch.no_grad():
        data = test_dataset[0]
        for k, v in data.items():
            data[k] = v.to(device).unsqueeze(0)
        tag, pos, _ = model(**data)
        tags = enc_tag.inverse_transform(
            tag.argmax(2).cpu().numpy().reshape(-1))[:len(tokenized_sentence)]
        pos = enc_pos.inverse_transform(
            pos.argmax(2).cpu().numpy().reshape(-1))[:len(tokenized_sentence)]

        assert tags == len(tokenized_sentence)
        assert pos == len(tokenized_sentence)
    return (tags, pos)
