import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json
import socket
import threading

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = '*************@gmail.com'   #starred for privacy reasons. give any gmail id you want to set up the server on
SMTP_PASSWORD = '****************'          #starred for privacy reasons. set up 2 step verification for the above gmail account and create an "app password". use that here.


def send_email(to_email, subject, message, attachment=None):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment, 'rb') as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(attachment))
        msg.attach(part)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)

def handle_send_email(data):
    to_email = data.get('to_email')
    subject = data.get('subject')
    message = data.get('message')
    attachment = data.get('attachment')

    send_email(to_email, subject, message, attachment)
    return 'Email sent successfully'


def handle_client(client_socket, addr):
    try:
        data = client_socket.recv(1024).decode('utf-8')
        data = json.loads(data)

        if 'action' in data:
            action = data['action']
            if action == 'send_email':
                result = handle_send_email(data)
            else:
                result = 'Invalid action'

            client_socket.send(result.encode('utf-8'))

    except Exception as e:
        print(f"Error handling client {addr}: {str(e)}")

    finally:
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)

    print('Server listening on port 8080...')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')

        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == '__main__':
    main()