import random


class ECC:

    def __init__(self, a: int, b: int, p: int, G: tuple[int, int]):
        self.a = a
        self.b = b
        self.p = p
        self.G = G

        if not self.is_on_curve(G):
            raise ValueError("Base point is not on the curve")

    def inv_mod(self, x: int) -> int:
        return pow(x, -1, self.p)

    def is_on_curve(self, P):
        if P is None:
            return True
        x, y = P
        return (y * y - (x * x * x + self.a * x + self.b)) % self.p == 0

    def point_add(self, P, Q):

        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        # P + (-P) = infinity
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        # point doubling
        if P == Q:
            if y1 % self.p == 0:
                return None
            m = (3 * x1 * x1 + self.a) * self.inv_mod(2 * y1 % self.p) % self.p
        else:
            m = (y2 - y1) * self.inv_mod((x2 - x1) % self.p) % self.p

        x3 = (m * m - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def scalar_mult(self, k, P):

        result = None
        current = P

        while k > 0:
            if k & 1:
                result = self.point_add(result, current)
            current = self.point_add(current, current)
            k >>= 1

        return result

    def point_order(self, P):
        Q = P
        order = 1

        while Q is not None:
            Q = self.point_add(Q, P)
            order += 1

        return order


def encrypt_ecc(message: str, shared_point):

    key = (shared_point[0] + shared_point[1]) % 256

    return [ord(ch) ^ key for ch in message]


def decrypt_ecc(cipher, shared_point):

    key = (shared_point[0] + shared_point[1]) % 256

    return "".join(chr(val ^ key) for val in cipher)


if __name__ == "__main__":

    ecc = ECC(a=2, b=3, p=97, G=(3, 6))

    # compute order of G
    n = ecc.point_order(ecc.G)
    print("")
    print("order of G:", n)

    # repeat until valid shared secret (not infinity)
    while True:

        priv_A = random.randint(1, n - 1)
        priv_B = random.randint(1, n - 1)

        pub_A = ecc.scalar_mult(priv_A, ecc.G)
        pub_B = ecc.scalar_mult(priv_B, ecc.G)

        # validate points
        if not ecc.is_on_curve(pub_A) or not ecc.is_on_curve(pub_B):
            continue

        shared_A = ecc.scalar_mult(priv_A, pub_B)
        shared_B = ecc.scalar_mult(priv_B, pub_A)

        if shared_A is not None and shared_B is not None:
            break

    print("priv_A:", priv_A)
    print("priv_B:", priv_B)
    print("pub_A :", pub_A)
    print("pub_B :", pub_B)
    print("shared_A:", shared_A)
    print("shared_B:", shared_B)
    print("shared equal:", shared_A == shared_B)

    msg = "hey brooo"

    encrypted_msg = encrypt_ecc(msg, shared_A)
    restored_msg = decrypt_ecc(encrypted_msg, shared_B)

    print()
    print("original :", msg)
    print("encrypted:", encrypted_msg)
    print("decrypted:", restored_msg)
    print()
