import os


def load_keys():
    try:
        API_KEY = load_single_key("API_KEY")

        BASE_URL = load_single_key("BASE_URL")

        MODEL_NAME = load_single_key("MODEL_NAME")

        return API_KEY, BASE_URL, MODEL_NAME
    except Exception as e:
        print(e)


def load_single_key(key):
    KEY = os.getenv(key)

    if KEY:
        print(f"{key} retrieved successfully")

        return KEY
    else:
        raise Exception(f"{key} not found")
