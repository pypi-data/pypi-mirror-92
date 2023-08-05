import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
def encode(msg):
    if not isinstance(msg, bytes):
        msg = msg.encode('utf-8')
    return msg
def decode(msg):
    if isinstance(msg, bytes):
        msg = msg.decode('utf-8')
    return msg

def encrypt(key, source, b64encode=True):
    key = encode(key)
    source = encode(source)
    key = SHA256.new(key).digest()  
    IV = Random.new().read(AES.block_size)  
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  
    source += bytes([padding]) * padding  
    data = IV + encryptor.encrypt(source)  
    return base64.b64encode(data) if b64encode else data


def decrypt(key, source, b64decode=True):
    if b64decode:
        source = base64.b64decode(source)
    key = encode(key)
    key = SHA256.new(key).digest()  
    IV = source[:AES.block_size]  
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  
    padding = data[-1]  
    if data[-padding:] != bytes([padding]) * padding:  
        raise ValueError("Invalid padding...")
    return data[:-padding]  

def encryptfile(key, filein, fileout):
    f = open(filein, 'rb')
    source = f.read()
    f.close()
    data = encrypt(key, source)
    f = open(fileout, 'wb+')
    f.write(data)
    f.close()
    
def decryptfile(key, filein, fileout):
    f = open(filein, 'rb')
    source = f.read()
    f.close()
    data = decrypt(key, source)
    #data = decode(data)
    #print(f'Data Decrypted : \n {data}')
    f = open(fileout, 'wb+')
    f.write(data)
    f.close()

def main():
    key = input('Enter your key : ')
    encryptfile(key, 'test.tar.gz', 'enc_test.tar.gz')
    decryptfile(key, 'enc_test.tar.gz', 'dec_tet.tar.gz')
if __name__ == '__main__':
    main()

