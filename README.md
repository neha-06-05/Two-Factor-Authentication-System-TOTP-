# Two-Factor Authentication System (TOTP)

This is a simple Python web application that demonstrates Two-Factor Authentication using **TOTP (Time-based One-Time Passwords)**, compatible with apps like Google Authenticator. It allows users to register and log in securely using both a password and a time-sensitive OTP.

---

## Features

* Register user and generate a TOTP secret
* Generate QR code to scan in Google Authenticator
* Login with username
* Verify time-based OTP from authenticator app

---

## How to Use

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
python app.py
```

3. Open `http://localhost:5000` in your browser and:

* Register a user — it will generate a QR code
* Scan the QR code using Google Authenticator
* Use the generated 6-digit code to log in

---

## Requirements

* Python 3.x
* Flask
* pyotp
* qrcode
* pillow

---

## How It Works

* A unique secret key is generated using `pyotp.random_base32()` during registration
* A QR code is generated from a TOTP provisioning URI
* The user scans the QR code in Google Authenticator (or any TOTP app)
* On login, the app verifies the current TOTP code with the saved secret
