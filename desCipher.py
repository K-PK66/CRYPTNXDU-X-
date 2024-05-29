# 淫趴矩阵（imperative matrix）
# 这些矩阵使用时下标要减一
# IP置换作用于进行16轮f函数作用之前，IP逆置换作用于16轮f函数作用之后
# IP置换表
import time

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
yasuo1_table = [57, 49, 41, 33, 25, 17, 9,
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
yasuo2_table = [14, 17, 11, 24, 1, 5,
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
def char2unicode_ascii(intext, length):
    outtext = []
    for i in range(length):
        # ord是chr()的及配对函数，以‘c’“c”做为参数
        # 返回对应的ASCII或Unicode数值，若超出，返回TypeError
        outtext.append(ord(intext[i]))
    return outtext


# 将Unicode码转为bit
def unicode2bit(intext, length):
    outbit = []
    for i in range(length * 16):
        # 每一位Unicode都是16bit组成
        # intext[int(i/16)]length*16:对应intext中的每一个Unicode，进行16次操作
        # 每轮操作右移0,1,2...,15位，然后与1且运算，一次得到16bit
        # ！！！得到的这16位bit是个逆序
        outbit.append(intext[int(i / 16)] >> (i % 16) & 1)
    return outbit


# 将8位ASCII码转为bit
def byte2bit(inchar, length):
    outbit = []
    for i in range(length * 8):
        # 原理同上
        outbit.append(inchar[int(i / 8)] >> (i % 8) & 1)
    return outbit


# --------------------------从bit到字符--------------------------
# 将bit转为Unicode码
def bit2unicode(inbit, length):
    out = []
    temp = 0
    for i in range(length):
        # 这和上面是同步的，将bit，反着求出，刚刚好
        # 或的运算符在这里相当+，左边是int，右边是int，这里相当于二进制数，妙
        # 每16位bit，对应着一位Unicode，
        # 所以当i对16求模，余数为15时
        # 将append(temp),并且重新设置temp为0
        temp = temp | (inbit[i] << (i % 16))
        if i % 16 == 15:
            out.append(temp)
            temp = 0
    return out


# 将bit转为ascii码
def bit2byte(inbit, length):
    out = []
    temp = 0
    for i in range(length):
        temp = temp | (inbit[i] << (i % 8))
        if i % 8 == 7:
            out.append(temp)
            temp = 0
    return out


# 将unicode码转为字符（中文或英文）
def unicode2char(inbyte, length):
    out = ""
    for i in range(length):
        out = out + chr(inbyte[i])
    return out


# ------------------生成每一轮的key------------------
def createKeys(inkeys):
    keyResult = []
    # 将char型秘钥转化为bit型
    asciikey = char2unicode_ascii(inkeys, len(inkeys))
    keyinit = byte2bit(asciikey, len(asciikey))
    # print("keyinit = ", end = '')
    # print(keyinit)
    # 用0初始化列表key0，key1,
    key0 = [0 for i in range(56)]
    key1 = [0 for i in range(48)]
    # 进行密码压缩置换1，
    # 用压缩置换表1，不考虑每字节的第8位，
    # 将64位密码压缩为56位
    for i in range(56):
        key0[i] = keyinit[yasuo1_table[i] - 1]

    # 进行16轮的密码生成
    for i in range(16):
        # ---------------确定左移的次数---------------
        if (i == 0 or i == 1 or i == 8 or i == 15):
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
            key1[k] = key0[yasuo2_table[k] - 1]
        # keyResult为16行48列的二维数组
        keyResult.extend(key1)
        # -------------------------------------------------

    return keyResult


'''
#用来检验代码
key0 = [57,49,41,33,25,17,9,
        1,58,50,42,34,26,18,
        10,2,59,51,43,35,27,
        19,11,3,60,52,44,36,
        63,55,47,39,31,23,15,
        7,62,54,46,38,30,22,
        14,6,61,53,45,37,29,
        21,13,5,28,20,12,4]


#以组为单位左移
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
        # print("lkasdjfklsjdflksdfj")
        # print("L and R",L,R)
        # print('initTrans:',initTrans)
        # print("bittext:",bitText)
        # 开始进行16轮运算
        for i in range(16):
            # 临时存放R
            tempR = R

            # -------对R进行扩展，将32位扩展为48位-------
            for j in range(48):
                extendR[j] = R[extend_table[j] - 1]
            # print(len(keyResult))

            # 第i轮的秘钥，从keyResult中取出
            keyi = [keyResult[j] for j in range(i * 48, i * 48 + 48)]
            # print(i,keyi)
            # ---------与key进行异或运算--------
            # 初始化
            XORResult = [0 for j in range(48)]
            for j in range(48):
                if keyi[j] != extendR[j]:
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
            #    print('PRsult is :;；：',PResult)

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
            keyi = [keyResult[j] for j in range(i * 48, i * 48 + 48)]
            # ---------与key进行异或运算--------
            # 初始化
            XORResult = [0 for j in range(48)]
            for j in range(48):
                if keyi[j] != extendR[j]:
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


def main():
    text = input("MSG>>>>>>>>>> ")
    # str0.join([str1,str2])
    print(" ".join(["GOT>>>>>>>>>>", text]))
    length = len(text)
    key = input("PWD>>>>>>>>>> ")
    while len(key) != 8:
        print("FATAL: Password not 8-digit")
        key = input("REENTER PWD>> ")
    encResult = ""
    decResult = ""
    # optionType = input("MODE(EN0/DE1)>> ")
    
    # 若输入文本的长度不是4的整数倍（即不是64字节的整数倍）则需用用空格补全。
    # 此处为了加密中文，用的是unicode编码，即用16字节表示一个字符。
    # if optionType == "0":
    text = text + int(4 - (length % 4)) * " "
    length = len(text)

    print("ENCRYPTED>>>>", end=" ")
    # 字符每四个为一组
    for i in range(int(length / 4)):
        # [text[j] for j in range()]
        tempText = [text[j] for j in range(i * 4, i * 4 + 4)]
        encResult = "".join([encResult, DES(tempText, key, 0)])
        # f.write(Result)
    print(encResult)
    time.sleep(1)
    print("DECRYPTING", end=".")
    time.sleep(1)
    for i in range(2):
        print(".", end="")
        time.sleep(1)
    print("", end="\r")
  
    # else:
    # 若输入文本的长度不是8的整数倍（即不是64字节的整数倍）则需要用空格补全。
    # 此处解密出来的密文用的是每8bit转换为一个ascii码，所以生成的是用八位表示的字符

    newText = encResult + int(8 - (len(encResult) % 8)) * " "
    print("DECRYPTED>>>>", end=" ")
    for i in range(int(len(encResult) / 8)):
        newTempText = [encResult[j] for j in range(i * 8, i * 8 + 8)]
        decResult = "".join([decResult, DES(newTempText, key, 1)])
    print(decResult)
    print("RESULT>>>>>>> " + str(decResult == text))


main()
