from PIL import Image
import random

# Encryption function
def encrypt():
    # Input image file names
    img1_name = input("Enter the name of the first image (with extension): ")
    img2_name = input("Enter the name of the second image (with extension): ")

    try:
        img1 = Image.open(img1_name).convert("RGB")
        img2 = Image.open(img2_name).convert("RGB")
    except FileNotFoundError:
        print("Error: One or both images were not found. Please check the file names.")
        return

    if img1.size != img2.size:
        print("Error: Both images must have the same dimensions.")
        return

    width, height = img1.size
    img1_pixels = img1.load()
    img2_pixels = img2.load()

    # Create a new encrypted image
    encrypted_img = Image.new("RGB", (width, height))
    encrypted_pixels = encrypted_img.load()

    for i in range(width):
        for j in range(height):
            r1, g1, b1 = img1_pixels[i, j]
            r2, g2, b2 = img2_pixels[i, j]

            # Take 4 MSBs from each image
            r_enc = int(format(r1, '08b')[:4] + format(r2, '08b')[:4], 2)
            g_enc = int(format(g1, '08b')[:4] + format(g2, '08b')[:4], 2)
            b_enc = int(format(b1, '08b')[:4] + format(b2, '08b')[:4], 2)

            encrypted_pixels[i, j] = (r_enc, g_enc, b_enc)

    output_name = input("Enter the name for the encrypted image (with extension): ")
    encrypted_img.save(output_name)
    print(f"Encrypted image saved as {output_name}")

# Decryption function
def decrypt():
    # Input encrypted image file name
    encrypted_img_name = input("Enter the name of the encrypted image (with extension): ")

    try:
        encrypted_img = Image.open(encrypted_img_name).convert("RGB")
    except FileNotFoundError:
        print("Error: Encrypted image not found. Please check the file name.")
        return

    width, height = encrypted_img.size
    encrypted_pixels = encrypted_img.load()

    # Create blank images for the two decrypted outputs
    img1 = Image.new("RGB", (width, height))
    img2 = Image.new("RGB", (width, height))
    img1_pixels = img1.load()
    img2_pixels = img2.load()

    for i in range(width):
        for j in range(height):
            r, g, b = encrypted_pixels[i, j]

            # Extract 4 MSBs for each channel
            r1 = int(format(r, '08b')[:4] + "0000", 2)
            r2 = int(format(r, '08b')[4:] + "0000", 2)
            g1 = int(format(g, '08b')[:4] + "0000", 2)
            g2 = int(format(g, '08b')[4:] + "0000", 2)
            b1 = int(format(b, '08b')[:4] + "0000", 2)
            b2 = int(format(b, '08b')[4:] + "0000", 2)

            img1_pixels[i, j] = (r1, g1, b1)
            img2_pixels[i, j] = (r2, g2, b2)

    output_name1 = input("Enter the name for the first decrypted image (with extension): ")
    output_name2 = input("Enter the name for the second decrypted image (with extension): ")
    img1.save(output_name1)
    img2.save(output_name2)
    print(f"Decrypted images saved as {output_name1} and {output_name2}")

# Main function with menu
def main():
    while True:
        print("\n:: Image Encryption & Decryption ::")
        choice = input("1. Encrypt\n2. Decrypt\n3. Exit\nChoose an option: ")

        if choice == '1':
            encrypt()
        elif choice == '2':
            decrypt()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please choose again.")

# Driver code
if __name__ == "__main__":
    main()
