import sys
from des import DES
from services.image import get_image_data, put_image_data


def encrypt():
    try:
        image_path = sys.argv[1].lower()
        mode = sys.argv[2].lower()

        if image_path[-3:] != "png":
            print("Invalid image type. Must be a PNG file.")
            return
        
        mode_types = frozenset(["ecb", "cbc", "cfb", "ofb", "ctr"])

        if mode not in mode_types:
            print("Invalid mode. Must be one of the following: ecb, cbc, cfb, ofb, or ctr.")
            return
    except:
        print("Invalid arguments. Usage: `python main.py <image_path> <mode>`")
        return

    image_tokens = image_path.split(".")
    PATH = image_tokens[0]
    EXTENSION = image_tokens[1]

    output_path = f"{PATH}-{mode}_encryption.{EXTENSION}"
    
    pixels = get_image_data(image_path)
    des = DES(pixels)

    match mode:
        case "ecb":
            des.mode.pad_text()
            encrypted_data = des.mode.ecb()
            des.mode.unpad_text()
        case "cbc":
            des.mode.pad_text()
            encrypted_data = des.mode.cbc()
            des.mode.unpad_text()
        case "cfb":
            encrypted_data = des.mode.cfb()
        case "ofb":
            encrypted_data = des.mode.ofb()
        case "ctr":
            encrypted_data = des.mode.ctr()
        
    put_image_data(image_path, output_path, encrypted_data)
    print(f"Image written to {output_path}.")


if __name__ == "__main__":
    encrypt()