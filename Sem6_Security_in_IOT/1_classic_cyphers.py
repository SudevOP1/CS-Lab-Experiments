def _caesar_shift_from_secret(secret: str) -> int:
    return sum(ord(c) for c in secret) % 26


def encrypt_caesar_cipher(msg: str, secret: str) -> str:
    shift = _caesar_shift_from_secret(secret)
    result = []

    for ch in msg:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)

    return "".join(result)


def decrypt_caesar_cipher(msg: str, secret: str) -> str:
    shift = _caesar_shift_from_secret(secret)
    result = []

    for ch in msg:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base - shift) % 26 + base))
        else:
            result.append(ch)

    return "".join(result)


def _rails_from_secret(secret: str) -> int:
    return max(2, (sum(ord(c) for c in secret) % 5) + 2)


def encrypt_railfence_cipher(msg: str, secret: str) -> str:
    rails = _rails_from_secret(secret)
    fence = [[] for _ in range(rails)]

    rail = 0
    direction = 1

    for ch in msg:
        fence[rail].append(ch)
        rail += direction

        if rail == 0 or rail == rails - 1:
            direction *= -1

    return "".join("".join(r) for r in fence)


def decrypt_railfence_cipher(msg: str, secret: str) -> str:
    rails = _rails_from_secret(secret)
    pattern = []
    rail = 0
    direction = 1

    for _ in msg:
        pattern.append(rail)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction *= -1

    rail_lengths = [pattern.count(r) for r in range(rails)]

    fence = []
    idx = 0
    for length in rail_lengths:
        fence.append(list(msg[idx : idx + length]))
        idx += length

    result = []
    rail_indices = [0] * rails
    for r in pattern:
        result.append(fence[r][rail_indices[r]])
        rail_indices[r] += 1

    return "".join(result)


def encrypt_vigenere_cipher(msg: str, secret: str) -> str:
    result = []
    key_index = 0
    key = secret.lower()

    for ch in msg:
        if ch.isalpha():
            shift = ord(key[key_index % len(key)]) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
            key_index += 1
        else:
            result.append(ch)

    return "".join(result)


def decrypt_vigenere_cipher(msg: str, secret: str) -> str:
    result = []
    key_index = 0
    key = secret.lower()

    for ch in msg:
        if ch.isalpha():
            shift = ord(key[key_index % len(key)]) - ord("a")
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            key_index += 1
        else:
            result.append(ch)

    return "".join(result)


encryptions = {
    "caesar_cipher": {
        "encrypt_func": encrypt_caesar_cipher,
        "decrypt_func": decrypt_caesar_cipher,
    },
    "railfence_cipher": {
        "encrypt_func": encrypt_railfence_cipher,
        "decrypt_func": decrypt_railfence_cipher,
    },
    "vigenere_cipher": {
        "encrypt_func": encrypt_vigenere_cipher,
        "decrypt_func": decrypt_vigenere_cipher,
    },
}

clear = "\x1b[0m"
green = "\x1b[32m"
yellow = "\x1b[33m"

if __name__ == "__main__":
    text = "Yo wassup!"
    secret = "something"

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
