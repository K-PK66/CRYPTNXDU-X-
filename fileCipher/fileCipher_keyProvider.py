# The program MUST RUN IN ADVANCE to provide key for clients!!!
# Finished May 31 3:01 a.m.

import math
from random import randint


def extend_gcd(e, m):
    if m == 0:
        return 1, 0, e
    else:
        x, y, gcd = extend_gcd(m, e % m)
        x, y = y, x - (e // m) * y
        return x, y, gcd


def generate_key_pair(p, q):
    n = p * q  # n
    L = (p - 1) * (q - 1)
    prvkey = randint(2, L - 1)  # e
    pubkey = 0  # d

    while pubkey == 0:
        if math.gcd(prvkey, L) == 1:
            pubkey = extend_gcd(prvkey, L)[0]
            pubkey = pubkey % L
        else:
            prvkey = randint(2, L - 1)
    return (n, prvkey), (n, pubkey)


def is_Prime(n):
    if (n <= 1):
        return False
    for i in range(2, int(n / 2 + 1)):
        if n % i == 0:
            return False
    return True


def random_prime(x, y):
    sample = randint(x, y)
    if is_Prime(sample):
        return sample
    else:
        return random_prime(x, y)


def individualized_key_pair_generator(client):
    p = random_prime(100, 200)
    q = random_prime(200, 300)
    private_rsa_key_pair, public_rsa_key_pair = generate_key_pair(p, q)
    with open('public_key_{}.txt'.format(client), 'w') as client_pub_key:
        client_pub_key.write(str(public_rsa_key_pair))
    with open("sandbox_{}/private_key_{}.txt".format(client, client), 'w') as client_private_key:
        client_private_key.write(str(private_rsa_key_pair))
    print("Key pair for {} generated. <<p = {}, q = {}>>".format(client, p, q))


individualized_key_pair_generator('sender')
individualized_key_pair_generator('receiver')
