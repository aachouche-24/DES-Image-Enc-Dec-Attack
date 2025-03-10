# DES Image Encryption & Brute-Force Attack

This project implements **Data Encryption Standard (DES) encryption** for images and demonstrates a **brute-force attack (key exhaustion)** to decrypt an image encrypted using **DES-ECB mode**.

## 🔥 Features
- Encrypt and decrypt images using the **DES algorithm**.
- Support for **ECB, CBC, CFB, OFB, and CTR** encryption modes.
- Perform a **brute-force attack** to find the correct DES key and reconstruct the original image.
- Compare the decrypted image with the original.

---

## 🚀 Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/DES-Image-Cracker.git
cd DES-Image-Cracker
```

### 2️⃣ Install Dependencies
Make sure you have **Python 3.x** installed, then install the required packages:
```sh
pip install -r requirements.txt
```

### 3️⃣ Run Encryption
To encrypt an image using DES:
```sh
python encrypt_image.py input_image.png ECB 0x133457799BBCDFF1
```
This generates an encrypted image.

### 4️⃣ Run Decryption
To decrypt an encrypted image:
```sh
python decrypt_image.py encrypted_image.png ECB 0x133457799BBCDFF1
```

### 5️⃣ Run Brute-Force Attack
If the decryption key is unknown, use brute-force:
```sh
python brute_force.py encrypted_image.png ECB
```
Once the key is found, the script reconstructs the original image.

---

## 🔐 How Brute-Force Works
Brute-force attacks systematically try all possible **56-bit DES keys** until the correct one is found. The process:
1. Load the encrypted image.
2. Try different keys.
3. Check if the decrypted image makes sense.
4. Stop when a valid key is found.

---

## 📜 License
This project is open-source under the **MIT License**.

---

## 🙌 Contributing
Feel free to fork this repository, improve the implementation, and submit pull requests!

---

## 📧 Contact
For any questions, reach out via **GitHub Issues** or email me at `your.email@example.com`.

