import os
import json
import argparse


BASE_PATH = "/tmp/nhnet"
# Instantiate the parser
parser = argparse.ArgumentParser()
parser.add_argument('base-path', type=str,
                    help='path to location of base dataset')
parser.add_argument('date', type=str,
                    help='current date')
parser.add_argument('--dataset-files', type=str, nargs='+',
                    help='name of files containing dataset')


def update_dataset(collected_data_path, input_data, output_data):
    with open(collected_data_path, "r") as base_dataset:
        base_data = json.load(base_dataset)
    for input_file, output_file in zip(input_data, output_data):
        with open(input_file, "r") as dataset:
            data = json.load(dataset)
        for record in data:
            articles = []
            for url in record["urls"]:
                if url in base_data:
                    articles.append(base_data[url])

            if not articles:
                continue

            record["articles"] = articles

        with open(output_file, "w") as dataset:
            json.dump(data, dataset, indent=4)


if __name__ == "__main__":
    args = vars(parser.parse_args())
    base_path = args["base-path"]
    current_date = args["date"]
    dataset_files = args["dataset_files"]

    collected_data_path = os.path.join(base_path, "base", current_date, "collected_data.json")
    input_dataset_files = [os.path.join(base_path, "base", current_date, file) for file in dataset_files]
    output_dataset_files = [os.path.join(base_path, "collected", current_date, file) for file in dataset_files]

    update_dataset(collected_data_path, input_dataset_files, output_dataset_files)