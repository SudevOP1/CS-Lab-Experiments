def _generate_playfair_matrix(secret: str) -> list[str]:

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    secret = secret.upper().replace("J", "I").replace(" ", "")

    playfair_matrix = []
    for char in secret:
        if char not in playfair_matrix:
            playfair_matrix.append(char)

    for char in alphabet:
        if char not in playfair_matrix:
            playfair_matrix.append(char)

    return playfair_matrix


def _print_playfair_matrix(secret: str) -> None:
    playfair_matrix = _generate_playfair_matrix(secret)
    print(len(playfair_matrix))
    for i in range(5):
        for j in range(5):
            print(f"{playfair_matrix[i*5 + j]} ", end="")
        print("")


def encrypt_playfair_cipher(msg: str, secret: str) -> str:

    def _encrypt_pair(pair: str, matrix: list[str]) -> str:
        a, b = pair

        i1 = matrix.index(a)
        i2 = matrix.index(b)

        r1, c1 = divmod(i1, 5)
        r2, c2 = divmod(i2, 5)

        # same row
        if r1 == r2:
            return matrix[r1 * 5 + (c1 + 1) % 5] + matrix[r2 * 5 + (c2 + 1) % 5]

        # same column
        if c1 == c2:
            return matrix[((r1 + 1) % 5) * 5 + c1] + matrix[((r2 + 1) % 5) * 5 + c2]

        # rectangle
        return matrix[r1 * 5 + c2] + matrix[r2 * 5 + c1]

    def _create_pairs(msg: str) -> list[str]:
        msg_pairs = []
        i = 0

        while i < len(msg):
            char1 = msg[i]

            if i + 1 < len(msg):
                char2 = msg[i + 1]

                if char1 == char2:
                    msg_pairs.append(char1 + "X")
                    i += 1
                else:
                    msg_pairs.append(char1 + char2)
                    i += 2
            else:
                msg_pairs.append(char1 + "X")
                i += 1

        return msg_pairs

    msg = msg.upper().replace("J", "I").replace(" ", "")
    secret = secret.upper().replace("J", "I").replace(" ", "")
    playfair_matrix = _generate_playfair_matrix(secret)

    msg_pairs = _create_pairs(msg)
    hashed_msg = ""

    for pair in msg_pairs:
        hashed_msg += _encrypt_pair(pair, playfair_matrix)

    return hashed_msg


def decrypt_playfair_cipher(msg: str, secret: str) -> str:

    def _decrypt_pair(pair: str, matrix: list[str]) -> str:
        a, b = pair

        i1 = matrix.index(a)
        i2 = matrix.index(b)

        r1, c1 = divmod(i1, 5)
        r2, c2 = divmod(i2, 5)

        # same row
        if r1 == r2:
            return matrix[r1 * 5 + (c1 - 1) % 5] + matrix[r2 * 5 + (c2 - 1) % 5]

        # same column
        if c1 == c2:
            return matrix[((r1 - 1) % 5) * 5 + c1] + matrix[((r2 - 1) % 5) * 5 + c2]

        # rectangle
        return matrix[r1 * 5 + c2] + matrix[r2 * 5 + c1]

    playfair_matrix = _generate_playfair_matrix(secret)
    msg_pairs = [msg[i : i + 2] for i in range(0, len(msg), 2)]

    restored = ""
    for pair in msg_pairs:
        restored += _decrypt_pair(pair, playfair_matrix)

    return restored


clear = "\x1b[0m"
green = "\x1b[32m"
yellow = "\x1b[33m"

encryptions = {
    "playfair_cipher": {
        "encrypt_func": encrypt_playfair_cipher,
        "decrypt_func": decrypt_playfair_cipher,
    },
}

if __name__ == "__main__":
    text = "hide the gold in the tree stump"
    secret = "playfair example"

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
