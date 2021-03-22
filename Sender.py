import smtplib
from socket import *
import base64
import ssl
from config import *
import test_cases


def mail_sender(attack_case):
    print("Connecting to mail server")
    clientSocket = socket(AF_INET, SOCK_STREAM)
    print("Connecting to mail server")
    clientSocket.connect(receiving_mail_server)
    print_receiving_msg("connection", "220", clientSocket)

    # Send HELO command and print server response.
    ehlo = attack_case["ehlo"].decode()
    clientSocket.send(ehlo.encode())
    print_receiving_msg("EHLO", "250", clientSocket)

    #gmail needs to use TLS to start connection
    clientSocket.send(b'STARTTLS\r\n')
    print_receiving_msg("STARTTLS", "220", clientSocket)

    tlsSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLS)

    #Login for attacker, not needed when we have email server
    auth_msg = b'AUTH PLAIN '+base64.b64encode(b'\x00'+ sender_email.encode() +b'\x00'+password.encode())+b'\r\n'
    print(auth_msg.decode())
    tlsSocket.send(auth_msg)
    print_receiving_msg_tls("Authentication", "235",tlsSocket)

    #SMTP MAIL FROM
    MAIL_FROM = attack_case["mailfrom"]
    print(MAIL_FROM)
    tlsSocket.send(MAIL_FROM)
    print_receiving_msg_tls("mail from", "250", tlsSocket)


    #SMTP RCPT TO
    RCPT_TO = attack_case["rcptto"]
    print(RCPT_TO)
    tlsSocket.send(RCPT_TO)
    print_receiving_msg_tls("rcpt to", "250", tlsSocket)

    #DATA command
    tlsSocket.send(b'DATA\r\n')
    print_receiving_msg_tls("data", "354", tlsSocket)

    #Message shown to user on UI
    fakefrom = attack_case["data"]["from_header"]
    print(fakefrom)
    tlsSocket.send(fakefrom)
    TO = attack_case["data"]["to_header"]
    print(TO)
    tlsSocket.send(TO)
    subject = attack_case["data"]["subject_header"]
    print(subject)
    tlsSocket.send(subject)
    message = attack_case["data"]["message"]
    endmsg = "\r\n.\r\n"
    print(message)
    tlsSocket.send(message)
    print(endmsg)
    tlsSocket.send(endmsg.encode())


    #quit command
    tlsSocket.send(b'quit\r\n')
    print_receiving_msg_tls("quit", "250", tlsSocket)
    tlsSocket.close()



#Read at most 1024 bytes from server and print out the message
def print_receiving_msg(request, exp_code, clientSocket):
    recv = clientSocket.recv(1024).decode()
    print("Message after " + request + " request: " + recv)
    if (recv[0:3] != exp_code):
        print(exp_code + ' reply not received from server.')

def print_receiving_msg_tls(request, exp_code, tlsSocket):
    recv = tlsSocket.recv(1024).decode()
    print("Message after " + request + " request: " + recv)
    if (recv[0:3] != exp_code):
        print(exp_code + ' reply not received from server.')

#server = smtplib.SMTP('smtp.gmail.com', 587)
#server.starttls()
#server.login(sender_email, password)
#print("sending email")
#server.sendmail(sender_email, receiver_email, message)



