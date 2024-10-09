from django.shortcuts import render
from django.conf import settings
import numpy as np
# Create your views here.


def encrypt(request):
    text = ""  # Initialize the variable
    morse_code=""
    display="none"
    if request.method == 'POST':
        # Handle form submission
        text = request.POST.get('text', '')  # Get the value of the 'text' field from the form
        key = request.POST.get('key', '')
        enc_text= encryption(text,key)
        binary_msg=""
        for i in enc_text:
            binary_msg += format(ord(i), '08b')
        # print("Binary : ",binary_msg)

        #convert Binary to morse code
        binary_msg = binary_msg.replace("0",".")
        morse_code = binary_msg.replace("1","-")
        # print("mascode : ",morsecode_msg)
        if(morse_code != ""):
            display="block"

    
    # Pass the 'gajanand' variable to the template
    return render(request, 'morse_enc.html' ,{'display':display,'text':text, 'morsecode':morse_code})


def decrypt(request):
    dec_msg = ""  # Initialize the variable
    morsecode_input=""
    display="none"
    
    if request.method == 'POST':
        morsecode_input = request.POST.get('morsecode', '') 
        key = request.POST.get('key', '')

        #convert morse code to binary then character
        if (len(morsecode_input)%8 == 0):

            drc_bin = morsecode_input.replace("-","1")
            drc_bin = drc_bin.replace(".","0")

            dec_msg=""
            for i in range(0, len(drc_bin), 8):
                substring = drc_bin[i:i+8]
                dec_msg += chr(int(substring, 2)) 
            dec_msg = decryption(dec_msg,key)
            print(dec_msg)
        
            display="block"
    return render(request, 'morse_dec.html', {'display': display, 'morsecode':morsecode_input,'dec_msg':dec_msg})

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
