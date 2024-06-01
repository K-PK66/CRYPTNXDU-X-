# Python file to initialize the overall progress of the file transmit
# Finished May 31 2:20 p.m.

import os
import shutil


def does_not_exist(directory_path):
    if os.path.exists(directory_path):
        return False
    return True


def not_empty_dir(directory_path):
    if len(os.listdir(directory_path)) == 0:
        return False
    return True


if does_not_exist('inbox'):
    os.mkdir('inbox')
    
if does_not_exist('outbox'):
    os.mkdir('outbox')

if does_not_exist('sent'):
    os.mkdir('sent')

if does_not_exist('sandbox_receiver'):
    os.mkdir('sandbox_receiver')

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
