import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.decrepit.ciphers import algorithms as decrepit_algorithms


def _derive_key(secret: str, salt: bytes, length: int) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(secret.encode())


def encrypt_aes_cipher(msg: str, secret: str) -> str:
    salt = os.urandom(16)
    key = _derive_key(secret, salt, 32)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    msg_bytes = msg.encode()
    padding_length = 16 - (len(msg_bytes) % 16)
    msg_bytes += bytes([padding_length] * padding_length)

    encrypted = encryptor.update(msg_bytes) + encryptor.finalize()

    return base64.b64encode(salt + iv + encrypted).decode()


def decrypt_aes_cipher(msg: str, secret: str) -> str:
    data = base64.b64decode(msg.encode())

    salt = data[:16]
    iv = data[16:32]
    encrypted = data[32:]

    key = _derive_key(secret, salt, 32)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    msg_bytes = decryptor.update(encrypted) + decryptor.finalize()
    padding_length = msg_bytes[-1]
    msg_bytes = msg_bytes[:-padding_length]

    return msg_bytes.decode()


def encrypt_des_cipher(msg: str, secret: str) -> str:
    salt = os.urandom(8)
    key = _derive_key(secret, salt, 24)
    iv = os.urandom(8)

    cipher = Cipher(decrepit_algorithms.TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    msg_bytes = msg.encode()
    padding_length = 8 - (len(msg_bytes) % 8)
    msg_bytes += bytes([padding_length] * padding_length)

    encrypted = encryptor.update(msg_bytes) + encryptor.finalize()

    return base64.b64encode(salt + iv + encrypted).decode()


def decrypt_des_cipher(msg: str, secret: str) -> str:
    data = base64.b64decode(msg.encode())

    salt = data[:8]
    iv = data[8:16]
    encrypted = data[16:]

    key = _derive_key(secret, salt, 24)

    cipher = Cipher(decrepit_algorithms.TripleDES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    msg_bytes = decryptor.update(encrypted) + decryptor.finalize()
    padding_length = msg_bytes[-1]
    msg_bytes = msg_bytes[:-padding_length]

    return msg_bytes.decode()


clear = "\x1b[0m"
green = "\x1b[32m"
yellow = "\x1b[33m"

encryptions = {
    "aes_cipher": {
        "encrypt_func": encrypt_aes_cipher,
        "decrypt_func": decrypt_aes_cipher,
    },
    "des_cipher": {
        "encrypt_func": encrypt_des_cipher,
        "decrypt_func": decrypt_des_cipher,
    },
}

if __name__ == "__main__":
    text = "hide the gold in the tree stump"
    secret = "example"

    for encryption in encryptions:
        encrypt = encryptions[encryption]["encrypt_func"]
        decrypt = encryptions[encryption]["decrypt_func"]

        hashed_msg = encrypt(text, secret)
        restored_msg = decrypt(hashed_msg, secret)

        print("\n" + yellow + "=" * 5 + " " + encryption + " " + "=" * 5 + clear)
        print(f"{green}original : {clear}{text}")
        print(f"{green}encrypted: {clear}{hashed_msg}")
        print(f"{green}decrypted: {clear}{restored_msg}")

    print()
