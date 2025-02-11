from django.shortcuts import render
from django.conf import settings
import os
import numpy as np
import cv2

def encrypt(request):
    display_up="block"
    display_down="none"
    if request.method == 'POST':
        text = request.POST.get('text')
        key = request.POST.get('key')
        print(key)
        video_file = request.FILES.get('video')

        if video_file:
            saved_video_path = handle_uploaded_file(video_file)
            video_file_name = video_file.name
            print(video_file_name)
            encode_vid_data(video_file_name,text,key)
    return render(request, 'video_enc.html', {'display_up': display_up, 'display_down': display_down})


def encode_vid_data(video_file_name,text,key):
    video_path = os.path.join(settings.BASE_DIR, 'static', 'uploads',video_file_name )
    cap = cv2.VideoCapture(video_path)

    vidcap = cv2.VideoCapture(video_path) 
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))

    size = (frame_width, frame_height)
    output_folder = os.path.join(settings.BASE_DIR, 'static', 'updated')
    output_video_path = os.path.join(output_folder, video_file_name)

    # Update the VideoWriter initialization
    out = cv2.VideoWriter(output_video_path, fourcc, 25.0, size)

    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    cap.release()
    print("Total number of Frame in selected Video :",max_frame)
    # print("Enter the frame number where you want to embed data : ")
    # n=int(input())
    n=1
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:    
            change_frame_with = embed(frame, text, key)
            frame_ = change_frame_with
            frame = change_frame_with
        out.write(frame)
    
    print("\nEncoded the data successfully in the video file.")
    # return frame_



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

def msgtobinary(msg):
    if type(msg) == str:
        result= ''.join([ format(ord(i), "08b") for i in msg ])
    
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result= [ format(i, "08b") for i in msg ]
    
    elif type(msg) == int or type(msg) == np.uint8:
        result=format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    
    return result

def KSA(key):
    key_length = len(key)
    S=list(range(256)) 
    j=0
    for i in range(256):
        j=(j+S[i]+key[i % key_length]) % 256
        S[i],S[j]=S[j],S[i]
    return S

def PRGA(S,n):
    i=0
    j=0
    key=[]
    while n>0:
        n=n-1
        i=(i+1)%256
        j=(j+S[i])%256
        S[i],S[j]=S[j],S[i]
        K=S[(S[i]+S[j])%256]
        key.append(K)
    return key

def preparing_key_array(s):
    return [ord(c) for c in s]

def encryption(plaintext,key):
    # print("Enter the key : ")
    # key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(plaintext)))
    plaintext=np.array([ord(i) for i in plaintext])

    cipher=keystream^plaintext
    ctext=''
    for c in cipher:
        ctext=ctext+chr(c)
    return ctext

def decryption(ciphertext):
    print("Enter the key : ")
    key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(ciphertext)))
    ciphertext=np.array([ord(i) for i in ciphertext])

    decoded=keystream^ciphertext
    dtext=''
    for c in decoded:
        dtext=dtext+chr(c)
    return dtext


def embed(frame,data,key):
    # data=input("\nEnter the data to be Encoded in Video :") 
    data=encryption(data,key)
    # print("The encrypted data is : ",data)
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')

    data +='*^*^*'
    
    binary_data=msgtobinary(data)
    length_data = len(binary_data)
    
    index_data = 0
    
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
        return frame


def extract(frame):
    data_binary = ""
    final_decoded_msg = ""
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*": 
                    for i in range(0,len(decoded_data)-5):
                        final_decoded_msg += decoded_data[i]
                    final_decoded_msg = decryption(final_decoded_msg)
                    print("\n\nThe Encoded data which was hidden in the Video was :--\n",final_decoded_msg)
                    return 




def decode_vid_data(frame_):
    cap = cv2.VideoCapture('stego_video.mp4')
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    print("Total number of Frame in selected Video :",max_frame)
    print("Enter the secret frame number from where you want to extract data")
    n=int(input())
    vidcap = cv2.VideoCapture('stego_video.mp4')
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:
            extract(frame_)
            return


# def vid_steg():
#     while True:
#         print("\n\t\tVIDEO STEGANOGRAPHY OPERATIONS") 
#         print("1. Encode the Text message")  
#         print("2. Decode the Text message")  
#         print("3. Exit")  
#         choice1 = int(input("Enter the Choice:"))   
#         if choice1 == 1:
#             a=encode_vid_data()
#         elif choice1 == 2:
#             decode_vid_data(a)
#         elif choice1 == 3:
#             break
#         else:
#             print("Incorrect Choice")
#         print("\n")

