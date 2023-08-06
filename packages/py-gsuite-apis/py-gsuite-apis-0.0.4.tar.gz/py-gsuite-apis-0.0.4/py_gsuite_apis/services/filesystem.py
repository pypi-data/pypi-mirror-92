from typing import Any
import json
import os
import pickle


data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")
# data_dir = os.path.dirname(os.path.abspath(__file__))


class FilesystemConnection:
    def __init__(self, *, base_dir: str = data_dir) -> None:
        self.base_dir = base_dir

    def fetch_data_from_json_file(self, *, filename: str) -> dict:
        with open(os.path.join(self.base_dir, filename), "r") as f:
            return json.load(f)

    def fetch_data_from_pickle_file(self, *, filename: str) -> dict:
        if os.path.exists(filename):
            with open(filename, "rb") as data:
                return pickle.load(data)

    def save_data_to_pickle_file(self, *, data: Any, filename: str) -> None:
        with open(filename, "wb") as token:
            pickle.dump(data, token)

    def fetch_google_oauth_token(self, filename: str = "token.pickle") -> dict:
        return self.fetch_data_from_pickle_file(filename=filename)

    def save_google_oauth_to_pickle_file(self, creds: Any, filename: str = "token.pickle") -> None:
        return self.save_data_to_pickle_file(data=creds, filename=filename)

    def is_file(self, *, filepath: str) -> bool:
        return os.path.isfile(os.path.join(self.base_dir, filepath))

    def get_file_path(self, *, filepath: str) -> str:
        return os.path.join(self.base_dir, filepath)
