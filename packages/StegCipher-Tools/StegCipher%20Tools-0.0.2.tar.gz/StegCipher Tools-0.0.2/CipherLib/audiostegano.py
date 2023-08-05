from CipherLib.stegano import dataToBin
import os
import wave
import sys
import itertools

def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return round(size, 2), power_labels[n]+'B'

def framebytes_from_wave(filename):
    music = wave.open(filename, mode='rb')
    frame_bytes = bytearray(list(music.readframes(music.getnframes())))
    print(f'Number of Frames : {len(frame_bytes)}')
    fsize, label = format_bytes(len(frame_bytes)//9)
    print(f'Maximum Data Size To Embed : {fsize} {label}')
    musicparams = music.getparams()
    music.close()
    return musicparams, frame_bytes

def embed_data_to_frame(frame_bytes, data):
    datalen = len(data)
    size, label = format_bytes(datalen)
    print(f'Embedding Data of size {size} {label}')
    if datalen < len(frame_bytes)//9:
        modified_frames = modFrame(frame_bytes, data)
        return modified_frames + frame_bytes[len(modified_frames):]
    else:
        print('Data too large to embed. Aborting')
        return None

def framebytes_to_file(filename, musicparams, frame_bytes):
    with wave.open(filename, 'wb') as fd:
        fd.setparams(musicparams)
        fd.writeframes(frame_bytes)

def embed_file_to_wave(wavefilepath, filepath, ofilename):
    wdir = os.path.dirname(wavefilepath)
    basename = os.path.basename(wavefilepath)
    params, framebytes = framebytes_from_wave(wavefilepath)
    f = open(filepath, 'rb')
    data = f.read()
    f.close()
    modified_frames = embed_data_to_frame(framebytes, data)
    if modified_frames is not None:
        framebytes_to_file(os.path.join(wdir, ofilename), params, modified_frames)

def extract_data_from_wave(wavefilepath):
    wdir = os.path.dirname(wavefilepath)
    params, framebytes = framebytes_from_wave(wavefilepath)
    data = extractDataFromFrame(framebytes)
    return data

def extract_file_from_wave(wavefilepath, ofilename):
    wdir = os.path.dirname(wavefilepath)
    params, framebytes = framebytes_from_wave(wavefilepath)
    data = extractDataFromFrame(framebytes)
    f = open(os.path.join(wdir, ofilename), 'wb+')
    f.write(data)
    f.close()



def modFrame(frame_bytes, data):
    datalist = dataToBin(data)
    lendata = len(datalist)
    frames = iter(frame_bytes)
    lenframebytes = len(frame_bytes)
    embedded_bytes = 0
    sys.stdout.write('Embedded:           ')
    sys.stdout.flush()
    sys.stdout.write('\b'*10)
    modframes = []
    for i in range(lendata):
        embedded_bytes += 1
        size, label = format_bytes(embedded_bytes)
        showbytes = f'{size:7.2f} {label}'
        sys.stdout.write("%s" % (showbytes))
        sys.stdout.flush()
        sys.stdout.write('\b'*len(showbytes))
        for j in range(0, 9):
            if j != 8:
                frame = (frames.__next__() & 254) | int(datalist[i][j])
                modframes.append(frame)
            else:
                frame = frames.__next__()
                if (i == lendata - 1):
                    frame = frame & 254 | 1

                else:
                    frame = frame & 254
                modframes.append(frame)
    return bytearray(modframes)

def extractDataFromFrame(frame_bytes):
    frames = iter(frame_bytes)
    data = b''
    extracted_bytes = 0
    sys.stdout.write('Extracted:           ')
    sys.stdout.flush()
    sys.stdout.write('\b'*10)
    while True:
        last_bits = itertools.islice(frames, 0, 9)
        binstr = ''
        extracted_bytes+=1
        size, label = format_bytes(extracted_bytes)
        showbytes = f'{size:7.2f} {label}'
        sys.stdout.write("%s" % (showbytes))
        sys.stdout.flush()
        for i, b in zip(range(0, 8), last_bits):
            binval = str(b&1)
            binstr+=binval

        data += bytes([int(binstr, 2)])
        last_bit = last_bits.__next__()
        if last_bit == 1:
            sys.stdout.write('\n')
            return data
        sys.stdout.write('\b'*len(showbytes))


