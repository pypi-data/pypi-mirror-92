from Crypto.Random import random
import re

strong = re.compile(r'^(?=.{6,})((?=.*[a-zA-Z])(?=.*[\W_])(?=.*[0-9])).*$')
medium = re.compile(r'^(?=.{6,})((?=.*[a-zA-Z])(?=.*[0-9])|(?=.*[a-zA-Z])(?=.*[\W_])|(?=.*[0-9])(?=.*[\W_])).*$')
weak = re.compile(r'(?=.{6,}).*$')

def generate_password(passlen=16, exclude = '%'):
    p = ''
    for i in range(passlen):
        while True:
            l = chr(random.randint(33, 123))
            if l not in exclude:
                p += l
                break
            else:
                continue
    return p

def get_pass_strength(password):
    m = strong.match(password)
    if m is not None:
        return 2
    else:
        m = medium.match(password)
        if m is not None:
            return 1
        else:
            m = weak.match(password)
            if m is not None:
                return 0
            else:
                return -1

if __name__ == '__main__':
    password = generate_password()
    print(password)
