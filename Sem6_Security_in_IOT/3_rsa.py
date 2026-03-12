
def _power(base, expo, m):
    result = 1
    base = base % m
    while expo > 0:
        if expo & 1:
            result = (result * base) % m
        base = (base * base) % m
        expo = expo // 2
    return result


def _mod_inverse(euler_totient, phi):
    for d in range(2, phi):
        if (euler_totient * d) % phi == 1:
            return d
    return -1


def _generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    euler_totient = 0
    for euler_totient in range(2, phi):
        if _gcd(euler_totient, phi) == 1:
            break

    d = _mod_inverse(euler_totient, phi)
    return euler_totient, d, n


def _gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def encrypt_rsa(msg, euler_totient, n):
    return _power(msg, euler_totient, n)


def decrypt_rsa(hash, private_key, n):
    return _power(hash, private_key, n)


if __name__ == "__main__":

    msg = 69
    euler_totient, private_key, n = _generate_keys(7919, 1009)
    hashed_msg = encrypt_rsa(msg, euler_totient, n)
    restored_msg = decrypt_rsa(hashed_msg, private_key, n)

    print()
    print(f"(e, n): ({euler_totient}, {n})")
    print(f"(d, n): ({private_key}, {n})")
    print(f"original : {msg}")
    print(f"encrypted: {hashed_msg}")
    print(f"decrypted: {restored_msg}")
    print()
