# Python file to initialize the overall progress of the file transmit
# Finished May 31 2:20 p.m.

import os
import shutil


def not_empty_dir(directory_path):
    if len(os.listdir(directory_path)) == 0:
        return False
    return True


if not_empty_dir('inbox'):
    shutil.rmtree(r'inbox')
    os.mkdir(r'inbox')

if not_empty_dir('sent'):
    shutil.rmtree(r'sent')
    os.mkdir(r'sent')

if not_empty_dir('outbox'):
    shutil.rmtree(r'outbox')
    os.mkdir(r'outbox')

os.unlink('public_key_sender.txt')
os.unlink('public_key_receiver.txt')
os.unlink('sandbox_sender/private_key_sender.txt')
os.unlink('sandbox_receiver/private_key_receiver.txt')

print('Initialization Complete')