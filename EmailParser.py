import os
import glob
import json


def parse_emails(root_folder: str, skip_file: str = None):
    emails = glob.glob(os.path.join(root_folder, '**/*.txt'), recursive=True)
    spam = 0
    not_spam = 0
    spam_dict: dict = {}
    not_spam_dict: dict = {}
    for email in emails:
        # keep the part 10 folder for testing
        if skip_file is not None:
            if email == skip_file:
                continue
        if not email.__contains__("part10"):
            with open(email, 'r') as file:
                words = file.read().split()
                for word in words:
                    if word.isalpha():
                        if email.split('\\')[-1].startswith("s"):
                            # if file name starts with s -> the email is classified as spam
                            add_to_dict(spam_dict, word.lower())
                            spam += 1
                        else:
                            add_to_dict(not_spam_dict, word.lower())
                            not_spam += 1

    return spam_dict, not_spam_dict, (spam / (spam + not_spam))


def add_to_dict(body: dict, string: str):
    if not body.get(string):
        body[string] = 1
    else:
        body[string] = 1 + body.get(string)


def create_data(spam_dict: dict, not_spam_dict: dict):
    data: dict = {}
    for key in spam_dict.keys():
        # in the data dict we save the probability that a word is found in a spam mail
        temp = not_spam_dict.get(key) if not_spam_dict.get(key) else 0
        data[key] = spam_dict.get(key) / (spam_dict.get(key) + temp)

    for key in not_spam_dict.keys():
        if not data.get(key):
            data[key] = 0.0

    return data


def write_data_to_json_file(root_folder: str):
    json_file_path = "data.json"
    prob_file_path = "spam_probability.txt"

    spam, not_spam, spam_probability = parse_emails(root_folder)
    with open(json_file_path, 'w') as file:
        json.dump(create_data(spam, not_spam), file)
    with open(prob_file_path, 'w') as file:
        file.write(str(spam_probability))