from django.shortcuts import render
from django.conf import settings
import os
import wave
import numpy as np

def encrypt(request):
    display_up="block"
    display_down="none"
    text = request.POST.get('text')
    key = request.POST.get('key')
    # print(text)
    audio_file = request.FILES.get('audio') 
    audio_file_name=""
    if audio_file:
        saved_audio_path = handle_uploaded_file(audio_file)
        # print("Uploaded audio filename:", audio_file.name)
        audio_file_name=audio_file.name
        ctext = encryption(text,key)
        encode_aud_data(saved_audio_path,ctext)
        display_up="none"
        display_down="block"
    return render(request, 'audio_enc.html',{'audio_file':audio_file_name,'display_up':display_up,'display_down':display_down})

def decrypt(request):
    key = request.POST.get('key')
    audio_file_name=""
    dec_text=""
    display="none"
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        if audio_file:
            saved_audio_path = handle_uploaded_file(audio_file)
            audio_file_name=audio_file.name
            # print("Uploaded audio filename:", audio_file.name)
            text=decode_aud_data(saved_audio_path)
            dec_text = decryption(text,key)
            display="block"
            # print("in:",dec_text)
    return render(request, 'audio_dec.html',{'audio_file':audio_file_name, 'dec_text':dec_text, 'display':display})


def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + int(key[i % key_length])) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S, n):
    i = 0
    j = 0
    key = []
    while n > 0:
        n -= 1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        key.append(K)
    return key

def encryption(plaintext, key):
    S = KSA(key)
    keystream = np.array(PRGA(S, len(plaintext)))
    plaintext = np.array([ord(i) for i in plaintext])
    cipher = keystream ^ plaintext
    ctext = ''.join([chr(c) for c in cipher])
    return ctext

def decryption(ciphertext, key):
    S = KSA(key)
    keystream = np.array(PRGA(S, len(ciphertext)))
    ciphertext = np.array([ord(i) for i in ciphertext])
    decoded = keystream ^ ciphertext
    dtext = ''.join([chr(c) for c in decoded])
    return dtext

#################
def handle_uploaded_file(file):
    # Define the directory where you want to save the uploaded files
    upload_dir = os.path.join(settings.BASE_DIR, 'static', 'uploads')
    
    # Ensure the directory exists
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Construct the file path
    file_path = os.path.join(upload_dir, file.name)

    # Save the file to the server
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return file_path

####################
def encode_aud_data(nameoffile,data):
    # import wave

    # nameoffile=input("Enter name of the file (with extension) :- ")
    song = wave.open(nameoffile, mode='rb')

    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    res = ''.join(format(i, '08b') for i in bytearray(data, encoding ='utf-8'))     
    print("\nThe string after binary conversion :- " + (res))   
    length = len(res)
    print("\nLength of binary after conversion :- ",length)

    data = data + '*^*^*'

    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0
    for i in range(0,len(result),1): 
        res = bin(frame_bytes[j])[2:].zfill(8)
        if res[len(res)-4]== result[i]:
            frame_bytes[j] = (frame_bytes[j] & 253)      #253: 11111101
        else:
            frame_bytes[j] = (frame_bytes[j] & 253) | 2
            frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j = j + 1
    
    frame_modified = bytes(frame_bytes)
    file_name = os.path.basename(nameoffile)
    stegofile = os.path.join(settings.BASE_DIR, 'static', 'updated', file_name)

    # Save the stego audio file
    with wave.open(stegofile, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)

    print("\nEncoded the data successfully in the audio file.")
    song.close()



######################
def decode_aud_data(nameoffile):
    # import wave

    # nameoffile=input("Enter name of the file to be decoded :- ")
    song = wave.open(nameoffile, mode='rb')

    nframes=song.getnframes()
    frames=song.readframes(nframes)
    frame_list=list(frames)
    frame_bytes=bytearray(frame_list)

    extracted = ""
    p=0
    for i in range(len(frame_bytes)):
        if(p==1):
            break
        res = bin(frame_bytes[i])[2:].zfill(8)
        if res[len(res)-2]==0:
            extracted+=res[len(res)-4]
        else:
            extracted+=res[len(res)-1]
    
        all_bytes = [ extracted[i: i+8] for i in range(0, len(extracted), 8) ]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "*^*^*":
                print("The Encoded data was :--",decoded_data[:-5])
                return decoded_data[:-5]
                p=1
                break  
