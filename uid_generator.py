import datetime
import secrets
import hashlib
import string

ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits

def base62_encode(data: bytes, length: int):
    num = int.from_bytes(data, "big")
    chars = []

    while num > 0:
        num, rem = divmod(num, 62)
        chars.append(ALPHABET[rem])

    result = ''.join(reversed(chars))
    return result[:length].rjust(length, ALPHABET[0])


def generate_secure_uid():

    now = datetime.datetime.utcnow()

    # ---- RAW DATA ----
    date_raw = now.strftime("%Y%m%d0001").encode()
    hour_raw = now.strftime("%Y%m%d%H00").encode()

    # ---- HASH MASK ----
    date_hash = hashlib.sha256(date_raw).digest()
    hour_hash = hashlib.sha256(hour_raw).digest()

    repo_part = base62_encode(date_hash, 12)
    folder_part = base62_encode(hour_hash, 12)

    # ---- STRONG RANDOM USER PART ----
    user_random = secrets.token_bytes(12)
    user_part = base62_encode(user_random, 16)

    uid = f"VIDHWAAN{repo_part}{folder_part}{user_part}"

    return uid