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


class RSA:
    def __init__(self, keyPair):
        self.n = keyPair[0]
        self.key = keyPair[1]

    def Encrypt(self, M):
        if isinstance(M, (tuple, list)):
            return [s ** self.key % self.n for s in M]
        elif isinstance(M, int):
            return M ** self.key % self.n

    def Decrypt(self, E):
        if isinstance(E, (tuple, list)):
            return [s ** self.key % self.n for s in E]
        elif isinstance(E, int):
            return E ** self.key % self.n

    def PrintKeyInfo(self):
        print(f"n: {self.n} key:{self.key}")
        pass

def Encode2int(S):
    int_list = []
    for i in range(len(S)):
        int_list.append(ord(S[i]))
    return int_list


def Decode2chr(L):
    chr_list = []
    for i in range(len(L)):
        chr_list.append(chr(L[i]))
    return "".join(chr_list)


def main():
    
    p, q = 181, 281

    ### 产生密钥对
    prvKeyPair, pubKeyPair = generate_key_pair(p, q)

    ### 公钥公开给Encrypter
    Encrypter = RSA(prvKeyPair)

    ### 私钥保存
    Decrypter = RSA(pubKeyPair)

    ### 待加密信息
    M = input("输入待处理文本：")  # 保证明文中的每个字符 ASCII 值小于 p*q
    print(f"明  文: {M}")

    ### 加密
    #### 转码为整数列
    M_encode = Encode2int(M)
    print(f"转码后：{M_encode}")
    #### 加密整数列
    E_ = Encrypter.Encrypt(M_encode)
    print(f"加密后：{E_}")
    #### 密文
    E = Decode2chr(E_)
    print(f"密  文：{E}")

    ### 解密
    #### 转码为整数列
    E_encode = Encode2int(E)
    #### 解密整数列
    E_encode_decrypt = Decrypter.Decrypt(E_encode)
    print(f"解密后：{E_encode_decrypt}")
    M_ = Decode2chr(E_encode_decrypt)

    print(f"解密文：{M_}")

    print(f"prvKeyPair: {prvKeyPair}  pubKeyPair: {pubKeyPair}")
    pass


if __name__ == "__main__":
    main()
