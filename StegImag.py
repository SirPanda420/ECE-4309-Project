from PIL import Image

# Convert encoding data into 8-bit binary form using ASCII value of characters
def genData(data):
    return [format(ord(i), '08b') for i in data]

# Modify pixels based on the binary data
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        # Extract 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                               imdata.__next__()[:3] +
                               imdata.__next__()[:3]]

        # Modify pixel values to hex 
        for j in range(8):
            if datalist[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1
            elif datalist[i][j] == '1' and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1

        # Use the last pixel to indicate the end of the message
        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                pix[-1] += 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        yield tuple(pix[:3])
        yield tuple(pix[3:6])
        yield tuple(pix[6:9])

# Encode data into a copy of the image
def encode_enc(newimg, data):
    w = newimg.size[0]
    x, y = 0, 0

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

# Encode function
def encode():
    img = input("Enter image name (with extension): ")
    try:
        image = Image.open(img, 'r')
        # Ensure the image is in RGB mode
        image = image.convert("RGB")
    except FileNotFoundError:
        print("Error: Image not found. Please check the file name and try again.")
        return

    data = input("Enter data to be encoded: ")
    if len(data) == 0:
        raise ValueError("Data to encode cannot be empty.")

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Enter the name of the new image (with extension): ")
    try:
        newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
        print(f"Data successfully encoded into {new_img_name}")
    except Exception as e:
        print(f"Error saving image: {e}")


# Decode function
def decode():
    img = input("Enter image name (with extension): ")
    try:
        image = Image.open(img, 'r')
    except FileNotFoundError:
        print("Error: Image not found. Please check the file name and try again.")
        return

    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                               imgdata.__next__()[:3] +
                               imgdata.__next__()[:3]]

        # Convert pixel data to binary string
        binstr = ''.join('0' if i % 2 == 0 else '1' for i in pixels[:8])
        data += chr(int(binstr, 2))

        # Check for end of message
        if pixels[-1] % 2 != 0:
            return data

# Main function
def main():
    print(":: Welcome to Steganography ::")
    choice = input("1. Encode\n2. Decode\nChoose an option: ")

    if choice == '1':
        encode()
    elif choice == '2':
        print("Decoded Message: " + decode())
    else:
        print("Invalid choice. Please select 1 or 2.")

#Running Main
if __name__ == '__main__':
    main()
