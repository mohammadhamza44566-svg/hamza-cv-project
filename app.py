import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = ("Your Website", os.getenv("MAIL_USERNAME"))

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('desktop'))
    return render_template('login.html')

@app.route('/desktop')
def desktop():
    return render_template('desktop.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    sender_email = request.form.get('email')
    message = request.form.get('message')

    try:
        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            recipients=[os.getenv("MAIL_USERNAME")],
            body=f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}"
        )
        mail.send(msg)

        print("---- New Email Sent ----")
        print(f"To: {os.getenv('MAIL_USERNAME')}")
        print(f"From: {sender_email}")
        print(f"Name: {name}")
        print(f"Message:\n{message}")
        print("------------------------")

        flash("✅ Message sent successfully!", "success")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        flash("❌ Error sending message. Try again later.", "danger")

    return redirect(url_for('desktop'))

if __name__ == '__main__':
    app.run(debug=True)