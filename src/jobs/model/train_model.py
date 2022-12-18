import os
import numpy as np
import torch
import mlflow
from mlflow import MlflowClient
from datasets import load_dataset
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments, pipeline

from data_preparation import *
from metrics import *

MODEL_NAME = "ner_transformers"
STAGE = "Production"


class TransformerNERModel(mlflow.pyfunc.PythonModel):
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def predict(self, context, model_input):
        batch = self.tokenizer(model_input, truncation=True, padding="longest", return_tensors="pt")
        translated = self.model.generate(**batch)
        # tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
        return translated


# def _load_pyfunc(data_path):
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     tokenizer = PegasusTokenizer.from_pretrained('google/pegasus-xsum')
#     model = PegasusForConditionalGeneration.from_pretrained(data_path).to(device)
#     # nlp = pipeline("ner", model=model, tokenizer=tokenizer, device=device)
#     return TransformerNERModel(model, tokenizer)


def get_mean_metric(data, steps=5):
    if len(data) < steps:
        return data[-1].value
    else:
        np.mean(list(map(lambda x: x.value, data[-steps:])))


if __name__ == "__main__":
    mlflow.set_tracking_uri("http://host.docker.internal:5000")
    mlflow.set_experiment("fine_tuning_train_test")
    with mlflow.start_run() as run:
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

        mlflow_client = MlflowClient()

        try:
            registered_models = mlflow_client.get_latest_versions(MODEL_NAME, stages=None)
            print("Registered models")
            print(registered_models) #['Production']
            reg_model = registered_models[0]

            best_model_history = mlflow_client.get_metric_history(reg_model.run_id, "loss")
            current_run_history = mlflow_client.get_metric_history(run.info.run_id, "loss")

            best_model_metric = get_mean_metric(best_model_history)
            current_run_history = get_mean_metric(current_run_history)

            if best_model_metric < current_run_history:
                print("Current run is not accepted")
                is_accepted = False
            else:
                print("Current run is recognized as the best. Starting registration.")
                model = PegasusForConditionalGeneration.from_pretrained("models")

                model_wrap = TransformerNERModel(model, tokenizer)
                mlflow.pyfunc.log_model(
                    artifact_path="model_sum",
                    registered_model_name=MODEL_NAME,
                    python_model=model_wrap
                )
                version = mlflow_client.get_latest_versions(MODEL_NAME, stages=None)[0].version

                mlflow_client.transition_model_version_stage(
                    name=MODEL_NAME,
                    version=version,
                    stage="Production"
                )
                is_accepted = True
        except mlflow.exceptions.RestException:
            print("No suitable models found. Current run is recognized as the best. Starting registration.")
            model = PegasusForConditionalGeneration.from_pretrained('models')

            model_wrap = TransformerNERModel(model, tokenizer)
            mlflow.pyfunc.log_model(
                artifact_path="model_sum",
                registered_model_name=MODEL_NAME,
                python_model=model_wrap
            )

            version = mlflow_client.get_latest_versions(MODEL_NAME, stages=None)[0].version

            mlflow_client.transition_model_version_stage(
                name=MODEL_NAME,
                version=version,
                stage="Production"
            )
            is_accepted = True

        if is_accepted:
            pyfunc_model = mlflow.pyfunc.load_model(
                model_uri=f"models:/{MODEL_NAME}/{STAGE}"
            )
            print("Saving best model")
            pyfunc_model.model.save_pretrained(f"./models/best-model/{MODEL_NAME}_{version}")
            print("Saving pyfunc_model")
            mlflow.pyfunc.save_model("./models/best-model/pyfunc_model", python_model=model)




        # batch = tokenizer(test_texts, truncation=True, padding="longest", return_tensors="pt")
        # translated = model.generate(**batch)
        # tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
        #
        # get_rouge(tgt_text,test_labels)
