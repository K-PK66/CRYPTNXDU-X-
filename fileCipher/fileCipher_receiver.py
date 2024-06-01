# Receiver's Mission:
# √ Use the receiver's own private key to decrypt the sender's symmetric key.
# √ Use the decrypted symmetric key to decrypt the message
# √ Use the public key of the sender to decrypt the encrypted signature in pursuit of the abstract
# √ Calculate the abstract (of the decrypted files) out with the help of hash functions
# √ Make comparisons between the calculated abstract and the decrypted one (transmit success if same)
import math
import os

import time

# 淫趴矩阵（imperative matrix）
# 这些矩阵使用时下标要减一
# IP置换作用于进行16轮f函数作用之前，IP逆置换作用于16轮f函数作用之后
# IP置换表

IP_table = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
            ]
# 逆IP置换表
_IP_table = [40, 8, 48, 16, 56, 24, 64, 32,
             39, 7, 47, 15, 55, 23, 63, 31,
             38, 6, 46, 14, 54, 22, 62, 30,
             37, 5, 45, 13, 53, 21, 61, 29,
             36, 4, 44, 12, 52, 20, 60, 28,
             35, 3, 43, 11, 51, 19, 59, 27,
             34, 2, 42, 10, 50, 18, 58, 26,
             33, 1, 41, 9, 49, 17, 57, 25
             ]
# 每一个S-盒的输入数据是6位，输出数据是4位，但是每个S-盒自身是64位
# 设入的六位为b1,b2,b3,b4,b5,b6，b1、b6位组合得到列号，b2,b3,b4,b5组合得到行号。
# S盒中的S1盒
S1 = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
      0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
      4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
      15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13
      ]
# S盒中的S2盒
S2 = [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
      3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
      0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
      13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9
      ]
# S盒中的S3盒
S3 = [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
      13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
      13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
      1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12
      ]
# S盒中的S4盒
S4 = [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
      13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
      10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
      3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14
      ]
# S盒中的S5盒
S5 = [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
      14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
      4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
      11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3
      ]
# S盒中的S6盒
S6 = [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
      10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
      9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
      4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13
      ]
# S盒中的S7盒
S7 = [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
      13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
      1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
      6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12
      ]
# S盒中的S8盒
S8 = [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
      1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
      7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
      2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
      ]
# S盒；将8个S盒组成一个8行64列的2维数组
S = [S1, S2, S3, S4, S5, S6, S7, S8]
# P盒置换将每一位输入位映射到输出位。任何一位都不能被映射两次，也不能被略去。
# P盒
P_table = [16, 7, 20, 21,
           29, 12, 28, 17,
           1, 15, 23, 26,
           5, 18, 31, 10,
           2, 8, 24, 14,
           32, 27, 3, 9,
           19, 13, 30, 6,
           22, 11, 4, 25
           ]
# 压缩置换表1，不考虑每字节的第8位，将64位密钥减至56位。然后进行一次密钥置换。
# 忽略第8位奇偶校验的同时，进行置换，
compressed_table1 = [57, 49, 41, 33, 25, 17, 9,
                     1, 58, 50, 42, 34, 26, 18,
                     10, 2, 59, 51, 43, 35, 27,
                     19, 11, 3, 60, 52, 44, 36,
                     63, 55, 47, 39, 31, 23, 15,
                     7, 62, 54, 46, 38, 30, 22,
                     14, 6, 61, 53, 45, 37, 29,
                     21, 13, 5, 28, 20, 12, 4
                     ]

# 压缩置换表2，用于将循环左移和右移后的56bit密钥压缩为48bit
# 完成左移和右移后
# 去掉第9、18、22、25、35、38、43、54位，从56位变成48位，再按表的位置置换。
compressed_table2 = [14, 17, 11, 24, 1, 5,
                     3, 28, 15, 6, 21, 10,
                     23, 19, 12, 4, 26, 8,
                     16, 7, 27, 20, 13, 2,
                     41, 52, 31, 37, 47, 55,
                     30, 40, 51, 45, 33, 48,
                     44, 49, 39, 56, 34, 53,
                     46, 42, 50, 36, 29, 32
                     ]

# 扩展置换改变了位的次序，重复了某些位
# 用于对数据进行扩展置换，将32bit数据扩展为48bit
# 目的A:产生与秘钥相同长度的数据以进行异或运算，R0是32位，子秘钥是48位，
# 目的B:提供更长的结果，使得在替代运算时能够进行压缩。
extend_table = [32, 1, 2, 3, 4, 5,
                4, 5, 6, 7, 8, 9,
                8, 9, 10, 11, 12, 13,
                12, 13, 14, 15, 16, 17,
                16, 17, 18, 19, 20, 21,
                20, 21, 22, 23, 24, 25,
                24, 25, 26, 27, 28, 29,
                28, 29, 30, 31, 32, 1
                ]


# --------------------------从字符到bit--------------------------
# 将字符转换为对应的Unicode码，中文用2个字节表示
def char2unicode_ascii(toBeProcessed, length):
    result = []
    for i in range(length):
        # ord是chr()的及配对函数，以‘c’“c”做为参数
        # 返回对应的ASCII或Unicode数值，若超出，返回TypeError
        result.append(ord(toBeProcessed[i]))
    return result


# 将Unicode码转为bit
def unicode2bit(toBeProcessed, length):
    resultBit = []
    for i in range(length * 16):
        # 每一位Unicode都是16bit组成
        # 2bProcessed[int(i/16)]length*16:对应待处理文本中的每一个Unicode，进行16次操作
        # 每轮操作右移0,1,2...,15位，然后与1且运算，一次得到16bit
        # ！！！得到的这16位resultBit是个逆序
        resultBit.append(toBeProcessed[int(i / 16)] >> (i % 16) & 1)
    return resultBit


# 将8位ASCII码转为bit
def byte2bit(charToBeProcessed, length):
    resultBit = []
    for i in range(length * 8):
        # 原理同上
        resultBit.append(charToBeProcessed[int(i / 8)] >> (i % 8) & 1)
    return resultBit


# --------------------------从bit到字符--------------------------
# 将bit转为Unicode码
def bit2unicode(bitToBeProcessed, length):
    out = []
    temp = 0
    for i in range(length):
        # 这和上面是同步的，将bit，反着求出，刚刚好
        # 或的运算符在这里相当+，左边是int，右边是int，这里相当于二进制数，妙
        # 每16位bit，对应着一位Unicode，
        # 所以当i对16求模，余数为15时
        # 将append(temp),并且重新设置temp为0
        temp = temp | (bitToBeProcessed[i] << (i % 16))
        if i % 16 == 15:
            out.append(temp)
            temp = 0
    return out


# 将bit转为ascii码
def bit2byte(bitToBeProcessed, length):
    out = []
    temp = 0
    for i in range(length):
        temp = temp | (bitToBeProcessed[i] << (i % 8))
        if i % 8 == 7:
            out.append(temp)
            temp = 0
    return out


# 将unicode码转为字符（中文或英文）
def unicode2char(byteToBeProcessed, length):
    out = ""
    for i in range(length):
        out = out + chr(byteToBeProcessed[i])
    return out


# ------------------生成每一轮的key------------------
def createKeys(keyToBeProcessed):
    keyResult = []
    # 将char型秘钥转化为bit型
    key_ascii_ver = char2unicode_ascii(keyToBeProcessed, len(keyToBeProcessed))
    initialKey = byte2bit(key_ascii_ver, len(key_ascii_ver))
    # print("initialKey = ", end = '')
    # print(initialKey)
    # 用0初始化列表key0，key1,
    key0 = [0 for i in range(56)]
    key1 = [0 for i in range(48)]
    # 进行密码压缩置换1，
    # 用压缩置换表1，不考虑每字节的第8位，
    # 将64位密码压缩为56位
    for i in range(56):
        key0[i] = initialKey[compressed_table1[i] - 1]

    # 进行16轮的密码生成
    for i in range(16):
        # ---------------确定左移的次数---------------
        if i == 0 or i == 1 or i == 8 or i == 15:
            movestep = 1
        else:
            movestep = 2
        # --------------------------------------------

        # -----分两部分，每28bit位一部分，进行循环左移-----
        # 因为每次循环左移就是第28个移动至第1个
        for j in range(movestep):
            # 以行为单位
            # 移动2位就是，移动一位进行2次操作
            '''
            for k in range(8):
                #以行为单位左移
                #除去最后一位，每一行都左移一位，操作前保留第一位
                temp = key0[k*7]
                for m in range(7*k, 7*k + 6):
                    key0[m] = key0[m+1]
                key0[7*k + 6] = temp
            '''
            # 以组为单位左移
            temp = key0[0]
            for k in range(27):
                key0[k] = key0[k + 1]
            key0[27] = temp
            temp = key0[28]
            for k in range(28, 55):
                key0[k] = key0[k + 1]
            key0[55] = temp
        # -----------------------------------------------

        # -------对56位密钥进行压缩置换，压缩为48位--------
        # 置换选择表2(PC-2)，得到子密匙K1
        for k in range(48):
            key1[k] = key0[compressed_table2[k] - 1]
        # keyResult为16行48列的二维数组
        keyResult.extend(key1)
        # -------------------------------------------------

    return keyResult


'''
# 用来检验代码
key0 = [57,49,41,33,25,17,9,
        1,58,50,42,34,26,18,
        10,2,59,51,43,35,27,
        19,11,3,60,52,44,36,
        63,55,47,39,31,23,15,
        7,62,54,46,38,30,22,
        14,6,61,53,45,37,29,
        21,13,5,28,20,12,4]


# 以组为单位左移
temp = key0[0]
for k in range(27):
    key0[k] = key0[k+1]
key0[27] = temp
temp = key0[28]
for k in range(28, 55):
    key0[k] = key0[k+1]
key0[55] = temp
key0
'''


def DES(text, key, optionType):
    keyResult = createKeys(key)
    # 初始化最终得到的结果
    finalTextOfBit = [0 for i in range(64)]
    finalTextOfUnicode = [0 for i in range(4)]

    # 打印出来检验一下
    # print(keyResult)

    if optionType == 0:
        # 初始化
        # 用于临时盛放IP拟置换前，将L部分和R部分合成64的结果
        tempText = [0 for i in range(64)]

        # 初始化
        # 用于盛放R部分的扩展到48位的结果
        extendR = [0 for i in range(48)]

        # char型向bit型转化
        unicodeText = char2unicode_ascii(text, len(text))
        # print(unicodeText)
        bitText = unicode2bit(unicodeText, len(unicodeText))
        # print(bitText)

        # 初始化
        # 用于存放IP置换之后的结果
        initTrans = [0 for i in range(64)]

        # ---------------进行初始IP置换---------------
        for i in range(64):
            initTrans[i] = bitText[IP_table[i] - 1]
        # 将64位明文分为左右两部分

        L = initTrans[:32]
        R = initTrans[32:]

        # 开始进行16轮运算
        for i in range(16):
            # 临时存放R
            tempR = R

            # -------对R进行扩展，将32位扩展为48位-------
            for j in range(48):
                extendR[j] = R[extend_table[j] - 1]
            # print(len(keyResult))

            # 第i轮的秘钥，从keyResult中取出
            key_i = [keyResult[j] for j in range(i * 48, i * 48 + 48)]
            # print(i,key_i)
            # ---------与key进行异或运算--------
            # 初始化
            XORResult = [0 for j in range(48)]
            for j in range(48):
                if key_i[j] != extendR[j]:
                    XORResult[j] = 1
            # ----------------------------------

            # ---------开始进行盒运算----------
            # 初始化
            SResult = [0 for k in range(32)]
            for k in range(8):
                # 此处使用移位转进制
                row = ((XORResult[k * 6]) << 1) | (XORResult[k * 6 + 5])
                column = 0
                for j in range(1, 5):
                    column = column | (XORResult[k * 6 + j] << (4 - j))
                temp = S[k][row * 16 + column]
                for m in range(4):
                    SResult[k * 4 + m] = (temp >> m) & 1
            # ---------------------------------
            # if i == 0:
            #    print('PResult is :;；：',PResult)

            # -------------开始进行P盒置换-------------
            # 初始化
            PResult = [0 for k in range(32)]
            for k in range(32):
                PResult[k] = SResult[P_table[k] - 1]
            # -----------------------------------------
            # if i == 0:
            # print('PRsult is :;；：',PResult)
            # --------------与L部分的数据进行异或------------
            XORWithL = [0 for k in range(32)]
            for k in range(32):
                if L[k] != PResult[k]:
                    XORWithL[k] = 1
            # ----------------------------------------------

            # 将临时保存的R部分值，即tempR复制给L
            L = tempR
            R = XORWithL

            # print("当前i为%d",(i))
            # print("当前L,R为",L,R)
            # -----------------循环结束-----------------

        # 交换左右两部分
        L, R = R, L
        # if i == 0:
        #    print('LRis :;；：',L,R)
        # 合并为一部分
        tempText = L
        tempText.extend(R)

        # IP逆置换
        for k in range(64):
            finalTextOfBit[k] = tempText[_IP_table[k] - 1]

        # bit型转化为char型
        finalTextOfUnicode = bit2byte(finalTextOfBit, len(finalTextOfBit))
        # print("finalTextOfUnicode", finalTextOfUnicode)
        finalTextOfChar = unicode2char(finalTextOfUnicode, len(finalTextOfUnicode))
        # print("finalTextOfChar",finalTextOfChar)
        return finalTextOfChar
    else:
        # 初始化
        # 用于临时盛放IP拟置换前，将L部分和R部分合成64的结果
        tempText = [0 for i in range(64)]

        # 初始化
        # 用于盛放R部分的扩展到48位的结果
        extendR = [0 for i in range(48)]

        # char型向bit型转化
        unicodeText = char2unicode_ascii(text, len(text))
        # print(unicodeText)
        bitText = byte2bit(unicodeText, len(unicodeText))
        # print(bitText)

        # 初始化
        # 用于存放IP置换之后的结果
        initTrans = [0 for i in range(64)]

        # ---------------进行初始IP置换---------------
        for i in range(64):
            initTrans[i] = bitText[IP_table[i] - 1]
        # 将64位明文分为左右两部分
        L = [initTrans[i] for i in range(32)]
        R = [initTrans[i] for i in range(32, 64)]

        # 开始进行16轮运算
        for i in range(15, -1, -1):
            # 临时存放R
            tempR = R

            # -------对R进行扩展，将32位扩展为48位-------
            for j in range(48):
                extendR[j] = R[extend_table[j] - 1]
            # print(len(keyResult))

            # 第i轮的秘钥，从keyResult中取出
            key_i = [keyResult[j] for j in range(i * 48, i * 48 + 48)]
            # ---------与key进行异或运算--------
            # 初始化
            XORResult = [0 for j in range(48)]
            for j in range(48):
                if key_i[j] != extendR[j]:
                    XORResult[j] = 1
            # ----------------------------------

            # ---------开始进行S盒运算----------
            # 初始化
            SResult = [0 for k in range(32)]

            for k in range(8):
                # 此处使用移位转进制
                row = (XORResult[k * 6] << 1) | (XORResult[k * 6 + 5])
                column = 0
                for j in range(1, 5):
                    column = column | (XORResult[k * 6 + j] << (4 - j))
                temp = S[k][row * 16 + column]
                for m in range(4):
                    SResult[k * 4 + m] = (temp >> m) & 1
            # ---------------------------------
            # print('SResult',SResult)
            # -------------开始进行P盒置换-------------
            # 初始化
            PResult = [0 for k in range(32)]
            for k in range(32):
                PResult[k] = SResult[P_table[k] - 1]
            # -----------------------------------------

            # --------------与L部分的数据进行异或------------
            XORWithL = [0 for k in range(32)]
            for k in range(32):
                if L[k] != PResult[k]:
                    XORWithL[k] = 1
            # ----------------------------------------------

            # 将临时保存的R部分值，即tempR复制给L
            L = tempR
            R = XORWithL
            # print("L, R在第%d轮",(i, L,R))
        # 交换左右两部分
        L, R = R, L
        # print("L, R",(L,R))
        # 合并为一部分
        tempText = L
        tempText.extend(R)
        # ----------------------IP逆置换----------------------
        for k in range(64):
            finalTextOfBit[k] = tempText[_IP_table[k] - 1]

        # bit型转化为char型
        finalTextOfUnicode = bit2unicode(finalTextOfBit, len(finalTextOfBit))
        # print(finalTextOfUnicode)
        finalTextOfChar = unicode2char(finalTextOfUnicode, len(finalTextOfUnicode))
        # print(finalTextOfChar)
        return finalTextOfChar


# The function is for decryption of encrypted message from sender.
# The function will generate and write the decrypted version of the inbox message.
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


# -- Beginning of MD5 Cipher --
def int2bin(n, count=24):
    # returns the binary of integer n, using count number of digits
    return "".join([str((n >> y) & 1) for y in range(count - 1, -1, -1)])


class MD5(object):
    # cipher text initialization
    def __init__(self, message):
        self.message = message
        self.ciphertext = ""

        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476
        self.init_A = 0x67452301
        self.init_B = 0xEFCDAB89
        self.init_C = 0x98BADCFE
        self.init_D = 0x10325476

        self.T = [0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE, 0xF57C0FAF, 0x4787C62A, 0xA8304613, 0xFD469501,
                  0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE, 0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821,
                  0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA, 0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
                  0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED, 0xA9E3E905, 0xFCEFA3F8, 0x676F02D9, 0x8D2A4C8A,
                  0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C, 0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
                  0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05, 0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665,
                  0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039, 0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
                  0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1, 0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391]
        self.s = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
        self.m = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                  1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12,
                  5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2,
                  0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]

    # 附加填充位
    def fill_text(self):
        for i in range(len(self.message)):
            c = int2bin(ord(self.message[i]), 8)
            self.ciphertext += c

        if (len(self.ciphertext) % 512 != 448):
            if ((len(self.ciphertext) + 1) % 512 != 448):
                self.ciphertext += '1'
            while (len(self.ciphertext) % 512 != 448):
                self.ciphertext += '0'

        length = len(self.message) * 8
        if (length <= 255):
            length = int2bin(length, 8)
        else:
            length = int2bin(length, 16)
            temp = length[8:12] + length[12:16] + length[0:4] + length[4:8]
            length = temp

        self.ciphertext += length
        while (len(self.ciphertext) % 512 != 0):
            self.ciphertext += '0'

    # 分组处理（迭代压缩）
    def circuit_shift(self, x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    def change_pos(self):
        a = self.A
        b = self.B
        c = self.C
        d = self.D
        self.A = d
        self.B = a
        self.C = b
        self.D = c

    def FF(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.F(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp) % pow(2, 32)
        self.change_pos()

    def GG(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.G(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp) % pow(2, 32)
        self.change_pos()

    def HH(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.H(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp) % pow(2, 32)
        self.change_pos()

    def II(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.I(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp) % pow(2, 32)
        self.change_pos()

    def F(self, X, Y, Z):
        return (X & Y) | ((~X) & Z)

    def G(self, X, Y, Z):
        return (X & Z) | (Y & (~Z))

    def H(self, X, Y, Z):
        return X ^ Y ^ Z

    def I(self, X, Y, Z):
        return Y ^ (X | (~Z))

    def group_processing(self):
        M = []
        for i in range(0, 512, 32):
            num = ""
            # Get hex form of every single section
            for j in range(0, len(self.ciphertext[i:i + 32]), 4):
                temp = self.ciphertext[i:i + 32][j:j + 4]
                temp = hex(int(temp, 2))
                num += temp[2]
            # Sort the hex values
            num_tmp = ""
            for j in range(8, 0, -2):
                temp = num[j - 2:j]
                num_tmp += temp

            num = ""
            for i in range(len(num_tmp)):
                num += int2bin(int(num_tmp[i], 16), 4)
            M.append(num)

        # print(M)

        for j in range(0, 16, 4):
            self.FF(M[self.m[j]], self.s[j], self.T[j])
            self.FF(M[self.m[j + 1]], self.s[j + 1], self.T[j + 1])
            self.FF(M[self.m[j + 2]], self.s[j + 2], self.T[j + 2])
            self.FF(M[self.m[j + 3]], self.s[j + 3], self.T[j + 3])

        for j in range(0, 16, 4):
            self.GG(M[self.m[16 + j]], self.s[16 + j], self.T[16 + j])
            self.GG(M[self.m[16 + j + 1]], self.s[16 + j + 1], self.T[16 + j + 1])
            self.GG(M[self.m[16 + j + 2]], self.s[16 + j + 2], self.T[16 + j + 2])
            self.GG(M[self.m[16 + j + 3]], self.s[16 + j + 3], self.T[16 + j + 3])

        for j in range(0, 16, 4):
            self.HH(M[self.m[32 + j]], self.s[32 + j], self.T[32 + j])
            self.HH(M[self.m[32 + j + 1]], self.s[32 + j + 1], self.T[32 + j + 1])
            self.HH(M[self.m[32 + j + 2]], self.s[32 + j + 2], self.T[32 + j + 2])
            self.HH(M[self.m[32 + j + 3]], self.s[32 + j + 3], self.T[32 + j + 3])

        for j in range(0, 16, 4):
            self.II(M[self.m[48 + j]], self.s[48 + j], self.T[48 + j])
            self.II(M[self.m[48 + j + 1]], self.s[48 + j + 1], self.T[48 + j + 1])
            self.II(M[self.m[48 + j + 2]], self.s[48 + j + 2], self.T[48 + j + 2])
            self.II(M[self.m[48 + j + 3]], self.s[48 + j + 3], self.T[48 + j + 3])

        self.A = (self.A + self.init_A) % pow(2, 32)
        self.B = (self.B + self.init_B) % pow(2, 32)
        self.C = (self.C + self.init_C) % pow(2, 32)
        self.D = (self.D + self.init_D) % pow(2, 32)
        '''
        print("A:{}".format(hex(self.A)))
        print("B:{}".format(hex(self.B)))
        print("C:{}".format(hex(self.C)))
        print("D:{}".format(hex(self.D)))
        '''
        answer = ""
        for register in [self.A, self.B, self.C, self.D]:
            register = hex(register)[2:]
            for i in range(8, 0, -2):
                answer += str(register[i - 2:i])

        return answer


# The function to decrypt the password from the sender (finished May 31 12:12 a.m.)
def des_pwd_decrypt():
    with open('sent/encrypted_pwd_des.txt', 'r') as des_pwd_container:
        des_pwd_encrypted = des_pwd_container.readline()
    with open('sandbox_receiver/private_key_receiver.txt', 'r') as prv_key_radio:
        private_key_pair_string = prv_key_radio.readline()
    private_key_pair_string2pair_step_1 = private_key_pair_string.split(', ')
    private_key_pair_string2pair_step_2_a = private_key_pair_string2pair_step_1[0].removeprefix('(')
    private_key_pair_string2pair_step_2_b = private_key_pair_string2pair_step_1[1].removesuffix(')')
    private_key_pair = int(private_key_pair_string2pair_step_2_a), int(private_key_pair_string2pair_step_2_b)
    # print(public_key_pair_string2pair_step_2_a)
    # print(public_key_pair_string2pair_step_2_b)
    rsa_decrypt_service = RSA(private_key_pair)
    encoded_encrypted_des_pwd = Encode2int(des_pwd_encrypted)
    decrypted_encoded_des_pwd = rsa_decrypt_service.Decrypt(encoded_encrypted_des_pwd)
    return str(Decode2chr(decrypted_encoded_des_pwd))


# The function to decrypt the message basing on the symmetric password decrypted (finished May 31 12:13 a.m.)
def message_decrypt():
    decrypted_lines = ""
    with open('sandbox_sender/desPassword.txt', 'r') as des_password_gotcha:
        des_pwd = des_pwd_decrypt()
    with open('sent/encrypted_msg.txt', 'r') as encrypted_message_container:
        encrypted_message = encrypted_message_container.readline()
    for i in range(int(len(encrypted_message) / 8)):
        newTempText = [encrypted_message[j] for j in range(i * 8, i * 8 + 8)]
        decrypted_lines = "".join([decrypted_lines, DES(newTempText, des_pwd, 1)])
    # print(decrypted_lines)
    with open('inbox/decrypted_msg.txt', 'w') as container_of_decrypted_contents:
        container_of_decrypted_contents.write(decrypted_lines)
    print("Message Decrypted.")


def hash_decrypt():
    with open('sent/encrypted_hash.txt', 'r') as hash_receipt:
        encrypted_hash = hash_receipt.readline()
    with open('public_key_sender.txt', 'r') as public_key_sender:
        public_key_sender_string = public_key_sender.readline()
    public_key_pair_string2pair_step_1 = public_key_sender_string.split(', ')
    public_key_pair_string2pair_step_2_a = public_key_pair_string2pair_step_1[0].removeprefix('(')
    public_key_pair_string2pair_step_2_b = public_key_pair_string2pair_step_1[1].removesuffix(')')
    public_rsa_key_pair = int(public_key_pair_string2pair_step_2_a), int(public_key_pair_string2pair_step_2_b)
    rsa_decrypt_service = RSA(public_rsa_key_pair)
    encoded_hash = Encode2int(encrypted_hash)
    encrypted_hash = rsa_decrypt_service.Decrypt(encoded_hash)
    encrypted_hash_chr = Decode2chr(encrypted_hash)
    with open('inbox/hash_decrypted.txt', 'w') as decrypted_hash:
        decrypted_hash.write(str(encrypted_hash_chr))
    print("Hash Decrypted.")


def hash_check():
    with open('inbox/hash_decrypted.txt', 'r') as hash_decrypted:
        hash_received = hash_decrypted.readline()
        hash_received_list = hash_received.split(" ")
    hash_received_1 = hash_received_list[0]
    hash_received_2 = hash_received_list[1]
    with open('sent/encrypted_msg.txt', 'r') as sample:
        message = sample.read()
    with open('sent/encrypted_pwd_des.txt', 'r') as encrypted_pwd:
        password = encrypted_pwd.readline()
    message_hash = MD5(message)
    message_hash.fill_text()
    message_hash_str = message_hash.group_processing()
    if hash_received_1 != message_hash_str:
        print(message_hash_str)
        print("FATAL: Message has been modified half way.")
    password_hash = MD5(password)
    password_hash.fill_text()
    password_hash_str = password_hash.group_processing()
    if hash_received_2 != password_hash_str:
        print("FATAL: Symmetric password has been modified half way.")
    if hash_received_1 == message_hash_str and hash_received_2 == password_hash_str:
        print("Message not vandalized. Transmit success.")


message_decrypt()
hash_decrypt()
hash_check()
os.unlink('sent/encrypted_msg.txt')
os.unlink('sent/encrypted_hash.txt')
os.unlink('sent/encrypted_pwd_des.txt')