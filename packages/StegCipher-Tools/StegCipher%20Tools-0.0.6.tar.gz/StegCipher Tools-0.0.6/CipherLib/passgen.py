from Crypto.Random import random

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

if __name__ == '__main__':
    password = generate_password()
    print(password)
