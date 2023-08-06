from PIL import Image
import os
import sys
def dataToBin(data):
    binlist = []
    if isinstance(data, bytes):
        binlist = [format(i, '08b') for i in data]
    else:
        binlist = [format(ord(i), '08b') for i in data]

    return binlist

def modPix(pix, data):
    datalist = dataToBin(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]]
        for j in range(0, 8):
            pix[j] = (pix[j] & 254) | int(datalist[i][j])
            #bump = int(datalist[i][j])^(pix[j]%2)
            #pix[j] -= bump
            #pix[j] = abs(pix[j])
        if (i == lendata - 1):
            pix[-1] = pix[-1] & 254 | 1
#            if (pix[-1] % 2 == 0):
#                if(pix[-1] != 0):
#                    pix[-1] -= 1
#                else:
#                    pix[-1] += 1

        else:
            pix[-1] = pix[-1] & 254
#            if (pix[-1] % 2 != 0):
#                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def embed_data(imgfile, data):
    output_img = imgfile.copy()
    w = output_img.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(output_img.getdata(), data):
        output_img.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
    return output_img

def embed_data_from_file(ifilepath, filepath, ofilename):
    imgfile = Image.open(ifilepath, 'r')
    wdir = os.path.dirname(ifilepath)
    filesize = os.path.getsize(filepath)
    width, height = imgfile.size
    pixels = width*height
    print(f'File Size : {filesize}')
    print(f'Pixels : {pixels}')
    if filesize > pixels /3:
        print('File is too large')
        sys.exit()
    f = open(filepath, 'rb')
    data = f.read()
    #print(f'Data : {data}')
    f.close()
    oimage = embed_data(imgfile, data)
    oimage.save(os.path.join(wdir, ofilename), 'PNG')
    print(f'Data Embedded to {ofilename}')



def extract_data(imgfile):
    data = b''
    imgdata = iter(imgfile.getdata())
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += bytes([int(binstr, 2)])
        if (pixels[-1] % 2 != 0):
            return data

def extract_data_from_image(ifilepath):
    imgfile = Image.open(ifilepath, 'r')
    wdir = os.path.dirname(ifilepath)
    data = extract_data(imgfile)
    return data
def extract_data_from_file(ifilepath, ofilename):
    imgfile = Image.open(ifilepath, 'r')
    wdir = os.path.dirname(ifilepath)
    data = extract_data(imgfile)
    #print(f'Data : {data}')
    f = open(os.path.join(wdir, ofilename), 'wb+')
    f.write(data)
    print(f'Data Extracted to {ofilename}')


def main():
    wdir = input('Please enter your working directory : ')
    wdir = os.path.expanduser(wdir)
    imgname = input('Please enter your image file name : ')
    filename = input('Please enter your data file name : ')
    imgfile = Image.open(os.path.join(wdir, imgname), 'r')
    filepath = os.path.join(wdir, filename)
    print('-'*60)
    print('''
    1. Embed Data
    2. Extract Data
    ''')
    choice = input('Please choose from above option : ')
    print('-'*60)
    if choice == '1':
        f = open(filepath, 'rb')
        data = f.read()
        f.close()
        oimage = imgfile.copy()
        embed_data(oimage, data)
        print(f'embedding data into image file {imgname}')
        print(f'Data : {data}')
        outname = imgname.split('.')[0]+'_1'+'.png'
        oimage.save(os.path.join(wdir, outname), 'PNG')
        print(f'data embedded into file {outname}')
    elif choice == '2':
        print(f'Extracting Data From {imgname}')
        extracted = extract_data(imgfile)
        print(f'Extracted {extracted}')
        f = open(filepath, 'wb+')
        f.write(extracted)

if __name__ == '__main__' :
    main()

