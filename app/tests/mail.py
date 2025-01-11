import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Initiates the TLS handshake
    server.login('melead2024@gmail.com', '*******************')  # Use your credentials
    print("Connection successful!")
    server.quit()
except Exception as e:
    print(f"Error: {e}")