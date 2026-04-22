import hashlib

def hex_to_bin(hex_string):
    return bin(int(hex_string, 16))[2:].zfill(256)

def bit_difference(hash1, hash2):
    bin1 = hex_to_bin(hash1)
    bin2 = hex_to_bin(hash2)

    diff = 0
    for b1, b2 in zip(bin1, bin2):
        if b1 != b2:
            diff += 1

    percent = diff * 100 / 256
    return diff, percent

if __name__ == "__main__":

    msg1 = "hello"
    msg2 = "wassup"

    hash1 = hashlib.sha256(msg1.encode()).hexdigest()
    hash2 = hashlib.sha256(msg2.encode()).hexdigest()

    diff_bits, percent = bit_difference(hash1, hash2)

    print(f"")
    print(f"msg1: {msg1}")
    print(f"msg2: {msg2}")
    print(f"")
    print(f"hash1: {hash1}")
    print(f"hash2: {hash2}")
    print(f"")
    print(f"diff_bits: {diff_bits}")
    print(f"percent: {percent}")
    print(f"")
