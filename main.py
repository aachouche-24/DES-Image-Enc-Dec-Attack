import argparse
import os
import services.des as DES
import services.key as Key
import services.mode as Mode
from services.image import get_pixels, put_pixels


def main():
    parser = argparse.ArgumentParser(
        description="A Python-based image encryption application that enables users to encrypt PNG files using the Data Encryption Standard DES algorithm. This tool supports five different encryption modes: ECB, CBC, CFB, OFB, and CTR.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("input", type=str, help="The relative path to the image file you wish to encrypt.")
    parser.add_argument("mode", type=str, choices=["ECB", "CBC", "CFB", "OFB", "CTR"], help="The encryption mode to use.")
    parser.add_argument("-k", "--key", type=int, help="A 64-bit integer representing the key to encrypt/decrypt the image with.")

    args = parser.parse_args()

    pixels = get_pixels(args.input)

    if args.key:
        key = Key.generate_key(args.key)
    else:
        key = Key.generate_key()

    subkeys = Key.generate_subkeys(key)

    match args.mode:
        case "ECB":
            padding_length = Mode.pad_text(pixels)
            encrypted_data = Mode.ecb(pixels, subkeys)
            # Mode.unpad_text(pixels, padding_length)
        case "CBC":
            padding_length = Mode.pad_text()
            encrypted_data = Mode.cbc(pixels, subkeys)
            # Mode.unpad_text(pixels, padding_length)
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