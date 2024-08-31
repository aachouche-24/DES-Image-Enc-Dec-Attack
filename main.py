import argparse
import os
import services.key as Key
import services.mode as Mode
from services.image import get_pixels, put_pixels


def main():
    parser = argparse.ArgumentParser(
        description="A Python-based image encryption application that enables users to encrypt image files using the Data Encryption Standard DES algorithm. This tool supports five different encryption modes: ECB, CBC, CFB, OFB, and CTR.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("input", type=str, help="The relative path to the image file you wish to encrypt.")
    parser.add_argument("mode", type=str, choices=["ECB", "CBC", "CFB", "OFB", "CTR"], help="The encryption mode to use.")
    parser.add_argument("key", type=int, help="A 64-bit integer representing the key to encrypt/decrypt the image with.")

    args = parser.parse_args()

    try:
        pixels = get_pixels(args.input)
    except ValueError:
        raise

    key = Key.generate_key(args.key)
    subkeys = Key.generate_subkeys(key)

    match args.mode:
        case "ECB":
            pixels_padded = Mode.pad_text(pixels)
            encrypted_data = Mode.ecb(pixels_padded, subkeys)
            encrypted_data = Mode.unpad_text(encrypted_data, len(pixels_padded) - len(pixels))
        case "CBC":
            pixels_padded = Mode.pad_text(pixels)
            encrypted_data = Mode.cbc(pixels_padded, subkeys)
            encrypted_data = Mode.unpad_text(encrypted_data, len(pixels_padded) - len(pixels))
        case "CFB":
            encrypted_data = Mode.cfb(pixels, subkeys)
        case "OFB":
            encrypted_data = Mode.ofb(pixels, subkeys)
        case "CTR":
            encrypted_data = Mode.ctr(pixels, subkeys)

    directory, file = os.path.split(args.input)
    filename, extension = file.split(".")

    output_file = f"{directory}/{filename}-{args.mode}_ENCRYPTION.{extension}"
        
    put_pixels(args.input, output_file, encrypted_data)
    print(f"Image written to {output_file}.")


if __name__ == "__main__":
    main()