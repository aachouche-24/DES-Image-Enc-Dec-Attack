import argparse
from PIL import Image
from des import DES
from services.image import get_image_data, put_image_data


def encrypt():
    parser = argparse.ArgumentParser(description="Encrypt an image file using the DES algorithm.")
    parser.add_argument("--input", type=str, required=True, help="The relative path to the image file you wish to encrypt.")
    parser.add_argument("--mode", type=str, required=True, choices=["ECB", "CBC", "CFB", "OFB", "CTR"], help="The encryption mode to use (ECB, CBC, CFB, OFB, or CTR).")

    args = parser.parse_args()
    pixels = get_image_data(args.input)
    des = DES(pixels)

    match args.mode:
        case "ECB":
            des.mode.pad_text()
            encrypted_data = des.mode.ecb()
            des.mode.unpad_text()
        case "CBC":
            des.mode.pad_text()
            encrypted_data = des.mode.cbc()
            des.mode.unpad_text()
        case "CFB":
            encrypted_data = des.mode.cfb()
        case "OFB":
            encrypted_data = des.mode.ofb()
        case "CTR":
            encrypted_data = des.mode.ctr()

    with Image.open(args.input) as image:
        path, extension = image.filename.split(".")

    output_path = f"{path}-{args.mode}_ENCRYPTION.{extension}"
        
    put_image_data(args.input, output_path, encrypted_data)
    print(f"Image written to {output_path}.")


if __name__ == "__main__":
    encrypt()