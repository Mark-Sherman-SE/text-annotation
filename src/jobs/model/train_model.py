import os
import torch
import mlflow
from datasets import load_dataset
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments

from data_preparation import *
from metrics import *


if __name__ == "__main__":
    mlflow.set_tracking_uri("http://host.docker.internal:5000")
    mlflow.set_experiment("fine_tuning_train_test")
    dataset = load_dataset("cc_news")

    train_labels, train_texts = dataset['train']['title'][:10], dataset['train']['text'][:10]
    val_labels, val_texts = dataset['train']['title'][100:105], dataset['train']['text'][100:105]
    test_labels, test_texts = dataset['train']['title'][150:155], dataset['train']['text'][150:155]

    model_name = 'google/pegasus-xsum'
    train_dataset, val_dataset, test_dataset, tokenizer = prepare_data(model_name, train_texts, train_labels,
                                                                       val_texts, val_labels, test_texts, test_labels)
    trainer = prepare_fine_tuning(model_name, tokenizer, train_dataset, val_dataset)
    trainer.train()

    model_dir = './models/'
    trainer.save_model(model_dir)

    model = PegasusForConditionalGeneration.from_pretrained('models')

    batch = tokenizer(test_texts, truncation=True, padding="longest", return_tensors="pt")
    translated = model.generate(**batch)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

    get_rouge(tgt_text,test_labels)
