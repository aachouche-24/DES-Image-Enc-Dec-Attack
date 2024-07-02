# DES Image Encryption

## Overview

The DES Image Encryption application enables users to encrypt image files using the Data Encryption Standard (DES) algorithm. This tool supports five different encryption modes: ECB, CBC, CFB, OFB, and CTR. The DES algorithm, as implemented in this project, follows the detailed guidelines provided in [The DES Algorithm Illustrated](https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm) by J. Orlin Grabbe. To use, first create and spin up a [virtual environment](https://docs.python.org/3/library/venv.html) and then run the following command:

## Features

- **Command-Line Interface:** Easily encrypt and decrypt images directly from the command line.
- **Multiple Encryption Modes:** Choose from five different modes of DES encryption to suit your security needs.
- **PNG File Support:** Specifically designed to work with PNG image files.
- **Python Virtual Environment:** Utilizes a Python virtual environment to manage dependencies and ensure a consistent runtime environment.

## Notes

The application currently only supports PNG and JPG image file formats.

## Prerequisites

Before using this application, ensure you have Python installed on your machine. You will also need to set up a [virtual environment](https://docs.python.org/3/library/venv.html). After setting up your virtual environment, run

```bash
python -m pip install -r requirements.txt
```

to install all necessary dependencies.

## Usage

To encrypt a PNG file, run the following command:

```bash
python encrypt.py --input <input_file> --mode <mode>
```

- `<input_file>`: The *relative* path to the image file you wish to encrypt.
- `<mode>`: The encryption mode to use (ECB, CBC, CFB, OFB, or CTR).
