import os
import shutil
import time

shutil.rmtree(r'inbox')
os.makedirs('inbox')
willingness = input("Are you sure to send all files in the outbox?\nNO(0)/YES(1)>>> ")
if willingness == "1":
    print("Sending", end=">")
    time.sleep(1)
    for i in range(10):
        print(">", end="")
        time.sleep(0.2)
    shutil.move('outbox/encrypted_hash.txt', r'sent/encrypted_hash.txt')
    shutil.move('outbox/encrypted_msg.txt', r'sent/encrypted_msg.txt')
    shutil.move('outbox/encrypted_pwd_des.txt', r'sent/encrypted_pwd_des.txt')
    print("\rPack sent.")
else:
    os.unlink(r'outbox/encrypted_hash.txt')
    os.unlink(r'outbox/encrypted_msg.txt')
    os.unlink(r'outbox/encrypted_pwd_des.txt')


