import json
import shutil
import os


def load_json(a_json_file_path):
    try:
        with open(a_json_file_path, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_contract_info_to_json(a_contract, a_tar_json_path):
    pass


def save_json(file_path, a_json: dict):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(a_json, f, indent=2)


def copy_json(src_path, tar_path):
    dir_path = os.path.split(tar_path)[0]
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    try:
        shutil.copy(src_path, tar_path)
    except:
        pass
