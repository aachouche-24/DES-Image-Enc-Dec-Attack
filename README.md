# DES Image Encryption

## Overview

A Python CLI that enables users to encrypt image files using the Data Encryption Standard (DES) algorithm. This tool supports five different encryption modes: ECB, CBC, CFB, OFB, and CTR. The DES algorithm, as implemented in this project, follows the detailed guidelines provided in [The DES Algorithm Illustrated](https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm) by J. Orlin Grabbe.

&nbsp; | &nbsp; | <img src="./assets/panda.png" alt="Panda" /> | &nbsp; | &nbsp;
:---: | :---: | :---: | :---: | :---:
ECB | CBC | CFB | OFB | CTR
<img src="./assets/panda-ECB_ENCRYPTION.png" alt="ECB Encryption" /> | <img src="./assets/panda-CBC_ENCRYPTION.png" alt="CBC Encryption" /> | <img src="./assets/panda-CFB_ENCRYPTION.png" alt="CFB Encryption" /> | <img src="./assets/panda-OFB_ENCRYPTION.png" alt="OFB Encryption" /> | <img src="./assets/panda-CTR_ENCRYPTION.png" alt="CTR Encryption" />

## Features

- **Command-Line Interface:** Easily encrypt and decrypt images directly from the command line.
- **Multiple Encryption Modes:** Choose from five different modes of DES encryption.
- **Image File Support:** Specifically designed to work with images that use the RGB or RGBA mode.
- **Python Virtual Environment:** Utilizes a Python virtual environment to manage dependencies and ensure a consistent runtime environment.

## Notes

This tool currently only supports images that use the RGB or RGBA mode. In its current state, this tool is unable to decrypt images that were encrypted using the ECB or CBC mode (unless the original image size perfectly divides into 64-bit blocks).

## Prerequisites

Before using this application, ensure you have Python installed on your machine. You will also need to set up a [virtual environment](https://docs.python.org/3/library/venv.html). After setting up your virtual environment, run

```bash
python -m pip install -r requirements.txt
```

to install all necessary dependencies.

## Usage

```bash
python main.py [-h] input {ECB,CBC,CFB,OFB,CTR} key
```

positional arguments:

- `input`: The relative path to the image file you wish to encrypt.
- `{ECB,CBC,CFB,OFB,CTR}`: The encryption mode to use.
- `key`: A 64-bit integer representing the key to encrypt/decrypt the image with.

options:

- `-h, --help`: show this help message and exit

## Example

The following would encrypt an image named `panda.png` on my desktop using the `CTR` mode and the key `512`.

```bash
python main.py ../Desktop/panda.png CTR 512
```
