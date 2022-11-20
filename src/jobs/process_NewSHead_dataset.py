import copy
import re
import os
import json
import random
import argparse

import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textaugment import EDA


parser = argparse.ArgumentParser()
parser.add_argument('base-path', type=str,
                    help='path to location of base dataset')
parser.add_argument('date', type=str,
                    help='current date')
parser.add_argument('--dataset-files', type=str, nargs='+',
                    help='name of files containing dataset')

args = vars(parser.parse_args())
base_path = args["base-path"]
current_date = args["date"]
dataset_files = args["dataset_files"]

input_data = os.path.join(base_path, "collected", current_date, "test.json")
processed_data = os.path.join(base_path, "processed", current_date, "test.json")
augmented_data = os.path.join(base_path, "augmented", current_date, "test.json")


with open(input_data, "r") as f:
    data = json.load(f)

lemmatizer = WordNetLemmatizer()


def lemmatize_text(text):
    word_list = nltk.word_tokenize(text)
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w.lower()) for w in word_list])
    return re.sub(r'[^A-Za-z.,:; ]', '', lemmatized_output)


def remove_stop_words(text):
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(text)

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return ' '.join(filtered_sentence)

# filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]


data_lem = []
for d in data:
    try:
        lem_txt = lemmatize_text(d['articles'][0])
        rem_stop = remove_stop_words(lem_txt)
        d['articles'][0] = rem_stop
        data_lem.append(d)
    except:
        pass


def compare_sets(text1, text2):
    x = set(text1.split(' '))
    y = set(text2.split(' '))
    return x.intersection(y)


def compare_dataset(text_list):
    list_of_count_common = []
    for i in range(len(text_list)):
        sum_common = 0
        for j in range(len(text_list)):
            if i != j:
                sum_common = sum_common + \
                             len(compare_sets(text_list[i]['articles'][0], text_list[j]['articles'][0]))
        list_of_count_common.append(sum_common)
    return list_of_count_common


list_of_compares = compare_dataset(data_lem)


def delete_outliers(list_of_compares, data_lem):
    del_count = 0
    for i in range(len(list_of_compares)):
        if list_of_compares[i] < len(data_lem) * 5:
            data_lem.pop(i - del_count)
            del_count = del_count + 1
    return data_lem


data_preprocessed = delete_outliers(list_of_compares, data_lem)

with open(processed_data, 'w') as f:
    json.dump(data_preprocessed, f)


def random_char_swap(text):
    list_of_words = text.split(' ')
    random_word_in = random.choice(np.arange(len(list_of_words)))
    while len(list_of_words[random_word_in]) == 1:
        random_word_in = random.choice(np.arange(len(list_of_words)))
    random_char_in = random.choice(np.arange(len(list_of_words[random_word_in]) - 1))
    swapped_word = list_of_words[random_word_in]
    swapped_word = swapped_word[:random_char_in] + swapped_word[random_char_in + 1] + swapped_word[
        random_char_in] + swapped_word[random_char_in + 2:]
    list_of_words[random_word_in] = swapped_word
    return ' '.join(list_of_words)


def augmentation(text_list):
    text_list_modif = []

    t = EDA()
    for tx in text_list:
        p_of_aug = np.random.rand(1)
        if p_of_aug < 0.2:
            text_augm = t.synonym_replacement(tx['articles'][0], n=int(0.05 * len(tx['articles'][0].split(' '))))
            tx['articles'][0] = text_augm
            text_list_modif.append(tx)
        if p_of_aug > 0.2 and p_of_aug < 0.4:
            text_augm = t.random_deletion(tx['articles'][0], p=0.05)
            tx['articles'][0] = text_augm
            text_list_modif.append(tx)
        if p_of_aug > 0.4 and p_of_aug < 0.6:
            text_augm = t.random_swap(tx['articles'][0], n=int(0.05 * len(tx['articles'][0].split(' '))))
            tx['articles'][0] = text_augm
            text_list_modif.append(tx)
        if p_of_aug > 0.6 and p_of_aug < 0.8:
            text_augm = t.random_insertion(tx['articles'][0], n=int(0.05 * len(tx['articles'][0].split(' '))))
            tx['articles'][0] = text_augm
            text_list_modif.append(tx)
        if p_of_aug > 0.8 and p_of_aug < 1:
            text_augm = random_char_swap(tx['articles'][0])
            tx['articles'][0] = text_augm
            text_list_modif.append(tx)
    return text_list_modif


augm_data = augmentation(data_preprocessed)

with open(augmented_data, 'w') as f:
    json.dump(augm_data, f)
