import EmailParser as ep
import json
import os


def get_words_from_email(email):
    email_words = []
    with open(email, 'r') as file:
        words = file.read().split()
        for word in words:
            if word.isalpha():
                email_words.append(word)
    return email_words


def load_attributes_from_json() -> dict:
    json_file_path = "data.json"

    try:
        with open(json_file_path, 'r') as json_file:
            attributes = json.load(json_file)
            return attributes
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")


def load_test_emails() -> list:
    folder_path = "lingspam_public/bare/part10"
    files_in_folder = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    emails = []
    for file_name in files_in_folder:
        file_path = os.path.join(folder_path, file_name)
        emails.append(file_path)

    return emails


def naive_bayes_learn():
    attributes: dict = load_attributes_from_json()
    with open("spam_probability.txt") as file:
        spam_probability = float(file.read())
    not_spam_probability = 1.0 - spam_probability

    attribute_probabilities = {}
    for key in attributes.keys():
        p_spam = spam_probability * attributes.get(key)
        p_not_spam = not_spam_probability * (1.0 - attributes.get(key))
        attribute_probabilities[key] = (p_spam, p_not_spam)

    return spam_probability, not_spam_probability, attribute_probabilities


def classify_new_instance(email):
    words = get_words_from_email(email)
    spam_probability, not_spam_probability, attribute_probabilities = naive_bayes_learn()

    spam_conditional_value = 1.0
    for word in words:
        if attribute_probabilities.get(word):
            spam_conditional_value *= attribute_probabilities.get(word)[0]
        else:
            spam_conditional_value *= 0.5
    email_spam_prob = spam_probability * spam_conditional_value

    not_spam_conditional_value = 1.0
    for word in words:
        if attribute_probabilities.get(word):
            not_spam_conditional_value *= attribute_probabilities.get(word)[1]
        else:
            not_spam_conditional_value *= 0.5
    email_not_spam_prob = not_spam_probability * not_spam_conditional_value

    email_val = email.split('\\')[-1]
    if email_spam_prob > email_not_spam_prob:
        print(f"Email {email_val} is spam")
        return "spam"
    else:
        print(f"Email {email_val} is not spam")
        return "not_spam"


def validate_model():
    wrong = 0
    correct = 0
    emails = load_test_emails()

    for email in emails:
        result = classify_new_instance(email)
        if not check_email_classifier_result(email, result):
            wrong += 1
        else:
            correct += 1

    return correct / (correct + wrong)


def check_email_classifier_result(email, result):
    if email.split('\\')[-1].startswith("s"):
        if result == "spam":
            return True
        else:
            return False
    else:
        if result == "not_spam":
            return True
        else:
            return False


if __name__ == '__main__':
    # ep.write_data_to_json_file("lingspam_public/bare")
    # Result was 87%
    correct_percentage = validate_model()
    print(f"Valid Percentage: {correct_percentage}")
