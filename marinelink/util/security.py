from uuid import uuid4
import random
import hashlib
from models.dbModel import User
import base64
import util.constant as const
import time

def string2secret_key(a_string: str):
    return b''.join([(a // 2 + 1).to_bytes(1, 'big') for a in a_string.encode('utf-8')]).decode('utf-8')


def string_encoding(a_string: str):
    return hashlib.sha256(a_string.encode('utf-8')).hexdigest()


def token_encrypt(a_string: str):
    a_string = (a_string + const.G_PAD_SEP_KEYWORD + const.G_AUTH_SECRETE_KET).encode('utf-8')
    return base64.urlsafe_b64encode(a_string)


def get_pdf_file_checksum(a_file_path: str):
    sha256_hash = hashlib.sha256()
    with open(a_file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def token_decrypt(a_string: str):
    a_string = base64.urlsafe_b64decode(a_string).decode('utf-8')
    return a_string.split(const.G_PAD_SEP_KEYWORD)[0]


def generate_token():
    idx = int(random.random() * 9) // 3 + 1
    return str(uuid4()).split('-')[0] + str(uuid4()).split('-')[idx] + str(uuid4()).split('-')[-1]

def generate_contract_id():
    # return hashlib.sha256((str(time.time_ns())[:10] + generate_token() + str(time.time_ns())[-10:]).encode('utf-8')).hexdigest()
    return hashlib.sha256((str(time.time())[:10] + generate_token() + str(time.time())[-10:]).encode('utf-8')).hexdigest()

def check_token(token):
    a_string = token_decrypt(token)
    user_id, user_token = a_string.split(const.G_TOKEN_SEP_KEYWORD)

    try:
        user = User.select(id=user_id)[0]
        if user.token_key == user_token:
            return user
    except IndexError:
        return None
    return None


def decode_people_info(string):
    name, phone = base64.b64decode(string).decode('utf-8').split(const.G_PAD_SEP_KEYWORD)

    return name, phone