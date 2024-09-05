import socket
import json

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost',  8080)
client_socket.connect(server_address)

data = {
    "action": "send_email",
    "to_email": "***********@gmail.com",   #starred for privacy reasons. type the gmail id you want to send an email to. it can be any gmail id.
    "subject": "Test Email",
    "message": "This is a test email.",
    "attachment": "*********************************" ,  #starred for privacy reasons. add the path of the file you want to attach here
}

data_str = json.dumps(data)
data_bytes = data_str.encode('utf-8')
client_socket.send(data_bytes)

response = client_socket.recv(1024).decode('utf-8')
client_socket.close()
print(response)