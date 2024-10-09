from django.shortcuts import render
from django.conf import settings
import os
from PIL import Image
import cv2
import numpy as np


# Create your views here.
def encrypt(request):
    return render(request, 'img_encryption.html')

def decrypt(request):
    return render(request, 'img_decryption.html')




def result(request, plain_text, image_path):
    return render(request, 'result.html', {'plain_text': plain_text,'ciphertext':ciphertext, 'image_path': image_path})

def dec_result(request, plain_text, image_path):
    return render(request, 'dec_result.html', {'plain_text': plain_text})
      

################## Handle PlainText  and image for enc ########################
def encresult(request):
    text = request.POST.get('text')
    key = request.POST.get('key')
    print(text)
    image = request.FILES.get('image')
    if image:
        saved_image_path = handle_uploaded_file(image)
        print("Uploaded image filename:", image.name)
        CT = pt_enc(text, key)
        print(CT)
        encrypted_img_path = stegano_enc(CT, saved_image_path, image)
        return render(request, 'img_enc_result.html', {'plain_text': text, 'ciphertext': CT, 'image_path': encrypted_img_path})

####################################################################

################## Handle PlainText  and image for dec ########################
def decresult(request):
    key = request.POST.get('key')
    image = request.FILES.get('imaged')
    if image:
        # Do something with the image file (e.g., save it to the server)
        # For demonstration purposes, just print the filename
        saved_image_path = handle_uploaded_file(image)
        print("Uploaded image filename:", image.name)
    DT_enc = stegano_dec(saved_image_path,image)
    DT = ct_dec(DT_enc,key)
    return render(request, 'img_dec_result.html', {'plain_text': DT})
##########################################################################


########################### Plain Text -TO- Cipher Text###############
def pt_enc(plaintext, key):
    S = KSA(key)
    keystream = np.array(PRGA(S, len(plaintext)))
    plaintext = np.array([ord(i) for i in plaintext])
    cipher = keystream ^ plaintext
    ctext = ''.join([chr(c) for c in cipher])
    return ctext
#####################################################################
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

########################## Cipher Text -TO- Plain Text#################
def ct_dec(ciphertext, key):
    S = KSA(key)
    keystream = np.array(PRGA(S, len(ciphertext)))
    ciphertext = np.array([ord(i) for i in ciphertext])
    decoded = keystream ^ ciphertext
    dtext = ''.join([chr(c) for c in decoded])
    return dtext
#######################################################################


############################ Steganography encryption ############################
def stegano_enc(ciphertext, img_name, file):
    img = cv2.imread(img_name)

    print("The shape of the image is: ", img.shape)
    # print("The original image is as shown below: ")
    # resizedImg = cv2.resize(img, (500, 500))
    # cv2.imshow("Original Image", resizedImg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    data = ciphertext
    if len(data) == 0:
        raise ValueError('Data is Empty')

    file_name, extension = os.path.splitext(file.name)
    if extension != '.png':
        file_name += '.png'

    encodedImage = hide_data(img, data)

    encoded_file_path = os.path.join(settings.BASE_DIR, 'static', 'updated',file_name)
    cv2.imwrite(encoded_file_path, encodedImage)
    return file_name

#######################################################################
def msg_to_bin(msg):
    if type(msg) == str:
        return ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(msg) == np.ndarray:
        return [format(i, "08b") for i in msg]
    elif type(msg) == int or type(msg) == np.uint8:
        return format(msg, "08b")
    else:
        raise TypeError("Input type not supported")

def hide_data(img, secret_msg):
    nBytes = img.shape[0] * img.shape[1] * 3 // 8
    print("Maximum Bytes for encoding:", nBytes)

    if len(secret_msg) > nBytes:
        raise ValueError("Error encountered insufficient bytes, need a bigger image or less data!!")
    secret_msg += '#####'
    dataIndex = 0
    bin_secret_msg = msg_to_bin(secret_msg)

    dataLen = len(bin_secret_msg)
    for values in img:
        for pixels in values:
            r, g, b = msg_to_bin(pixels)
            if dataIndex < dataLen:
                pixels[0] = int(r[:-1] + bin_secret_msg[dataIndex], 2)
                dataIndex += 1
            if dataIndex < dataLen:
                pixels[1] = int(g[:-1] + bin_secret_msg[dataIndex], 2)
                dataIndex += 1
            if dataIndex < dataLen:
                pixels[2] = int(b[:-1] + bin_secret_msg[dataIndex], 2)
                dataIndex += 1
            if dataIndex >= dataLen:
                break

    return img


def show_data(img):
    bin_data = ""
    for values in img:
        for pixels in values:
            r, g, b = msg_to_bin(pixels)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]
    allBytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]
    decodedData = ""
    for byte in allBytes:
        decodedData += chr(int(byte, 2))
        if decodedData[-5:] == "#####":
            break
    return decodedData[:-5]

################## Steganography Decryption ###########################
def stegano_dec(img_name,file):
    img = cv2.imread(img_name)
    text = show_data(img)
    return text
#######################################################################


################# Upload image to server ###########################
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
############################################################