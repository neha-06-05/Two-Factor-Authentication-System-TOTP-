from flask import Flask, render_template, request, redirect, session
import pyotp
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random value in production

# In-memory user store (replace with a database for real applications)
users = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        secret = pyotp.random_base32()
        users[username] = {'secret': secret}
        session['username'] = username

        # Generate TOTP URI and QR code
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name="MySecureApp"
        )
        qr = qrcode.make(totp_uri)
        img = BytesIO()
        qr.save(img)
        img_b64 = base64.b64encode(img.getvalue()).decode()

        return render_template('register.html', qr_code=img_b64, username=username)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            session['username'] = username
            return redirect('/verify')
        else:
            return "User not found. Please register."
    return render_template('login.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        otp = request.form['otp']
        username = session.get('username')
        if username and username in users:
            totp = pyotp.TOTP(users[username]['secret'])
            if totp.verify(otp):
                return "✅ Login Successful!"
            else:
                return "❌ Invalid OTP. Try again."
        else:
            return "Session expired or user not found."
    return render_template('verify.html')

if __name__ == '__main__':
    app.run(debug=True)
