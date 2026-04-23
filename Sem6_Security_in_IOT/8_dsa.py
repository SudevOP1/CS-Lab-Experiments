import random, hashlib


def modinv(a: int, m: int) -> int:
    return pow(a, -1, m)


def sha1_int(msg: str) -> int:
    h = hashlib.sha1(msg.encode()).hexdigest()
    return int(h, 16)


def generate_keys(p: int, q: int, g: int) -> tuple[int, int]:
    x = random.randint(1, q - 1)  # private key
    y = pow(g, x, p)  # public key
    return x, y


def sign_message(
    msg: str,
    p: int,
    q: int,
    g: int,
    x: int,
) -> tuple[int, int]:

    h = sha1_int(msg)

    while True:
        k = random.randint(1, q - 1)
        r = pow(g, k, p) % q
        if r == 0:
            continue

        k_inv = modinv(k, q)
        s = (k_inv * (h + x * r)) % q
        if s != 0:
            break

    return r, s


def verify_signature(
    msg: str,
    r: int,
    s: int,
    p: int,
    q: int,
    g: int,
    y: int,
) -> bool:

    if not (0 < r < q and 0 < s < q):
        return False

    h = sha1_int(msg)

    w = modinv(s, q)
    u1 = (h * w) % q
    u2 = (r * w) % q

    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q

    return v == r


if __name__ == "__main__":

    p = 23
    q = 11
    g = pow(2, (p - 1) // q, p)

    x, y = generate_keys(p, q, g)
    msg = "wassup boiii"
    r, s = sign_message(msg, p, q, g, x)
    is_valid = verify_signature(msg, r, s, p, q, g, y)

    print("")
    print("Private key x:", x)
    print("Public key y:", y)
    print("Signature (r, s):", (r, s))
    print("Valid:", is_valid)
    print("")
