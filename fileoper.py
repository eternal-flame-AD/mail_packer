import os
import random
import string


def randname():
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))


def _get_ready_to_write(fn):
    if '/' not in fn:
        return
    fn = fn[0:fn.rindex('/')]
    os.makedirs(fn, exist_ok=True)


def delete_file_folder(src):
    '''delete files and folders'''
    if os.path.isfile(src):
        os.remove(src)
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_file_folder(itemsrc)
        os.rmdir(src)


def delete_file(fn):
    if os.path.exists(fn):
        os.remove(fn)


def write_file(fn, data):
    _get_ready_to_write(fn)
    with open(fn, mode="wb") as f:
        f.write(data)
        f.close()
