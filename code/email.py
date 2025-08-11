import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Hello from Python!")
msg["Subject"] = "Test Email"
msg["From"] = "you@example.com"
msg["To"] = "friend@example.com"

with smtplib.SMTP("smtp.example.com", 587) as server:
    server.starttls()
    server.login("you@example.com", "password")
    server.send_message(msg)
