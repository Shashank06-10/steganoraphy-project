# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
from PIL import Image
import os

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
# def encode():
#     img = input("Enter image name(with extension) : ")
#     image = Image.open(img, 'r')

#     data = input("Enter data to be encoded : ")
#     if (len(data) == 0):
#         raise ValueError('Data is empty')

#     newimg = image.copy()
#     encode_enc(newimg, data)

#     new_img_name = "shivjii.jpg"
#     newimg.save(new_img_name, str(new_img_name.split(".")[1].lower()))

def encode():
    img = r"C:\vinod\cwhdj\major\practic\ganesh.jpg"
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded : ")
    if len(data) == 0:
        raise ValueError('Data is empty')

    root, ext = os.path.splitext(img)
    new_img_name = "encoded_" + os.path.basename(root) + ext.lower()  # Make the output filename dynamic
    newimg = image.copy()

    encode_enc(newimg, data)

    new_img_path = os.path.join(os.path.dirname(img), new_img_name)
    newimg.save(new_img_path)
    print(f"Encoded image saved as {new_img_path}")

# Decode the data in the image
def decode():
    # img = input("Enter image name(with extension) : ")
    img = r"C:\vinod\cwhdj\major\practic\encoded_ganesh.jpg"  # Use raw string (prefix with 'r')
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            binstr += '0' if i % 2 == 0 else '1'

        data += chr(int(binstr, 2))

        if pixels[-1] % 2 != 0:
            break

    return data

# Main Function
def main():
    a = int(input(":: Welcome to Steganography ::\n"
                  "1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()
    elif (a == 2):
        print("Decoded Word : " + decode())
    else:
        raise Exception("Enter correct input")

# Driver Code
if __name__ == '__main__':
    # Calling the main function
    main()
