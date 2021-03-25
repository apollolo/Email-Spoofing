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

class MailSender(object):
    def __init__(self):
        self.EHLO = "" #SMTP envelope
        self.MAIL_FROM =""
        self.RCPT_TO = ""

        self.from_header = "" #headers in UI
        self.to_header = ""
        self.subject_header = ""
        self.body = ""
        self.message_html = ""
        self.endmsg = b'\r\n.\r\n'

        self.starttls = False
        self.clientSocket = None #socket choices
        self.tlsSocket = None

        self.currentSocket = None #swap between TLS and regular
        
        self.dkim_para = None
        


    def set_parameter(self, attack_case):
        self.EHLO = attack_case["ehlo"]
        self.MAIL_FROM = attack_case["mailfrom"]
        self.RCPT_TO = attack_case["rcptto"]

        self.from_header = attack_case["data"]["from_header"]
        self.to_header = attack_case["data"]["to_header"]
        self.subject_header = attack_case["data"]["subject_header"]
        self.body = attack_case["data"]["body"]
        self.message_html = attack_case["data"]["html"]

        self.starttls = attack_case["starttls"]

        #if there's DKIM attack
        if 'dkim' in attack_case.keys():
            self.dkim_para = attack_case["dkim"]


    def mail_sender(self):
        #connect to the SMTP server
        self.socket_connection()

        # Send HELO command and print server response.
        self.currentSocket.send(self.EHLO)
        self.print_receiving_msg("EHLO", "250")

        #gmail needs to use TLS to start connection
        self.currentSocket.send(b'STARTTLS\r\n')
        self.print_receiving_msg("STARTTLS", "220")

        if (self.starttls):
            self.tlsSocket = ssl.wrap_socket(self.clientSocket, ssl_version=ssl.PROTOCOL_TLS)
            self.currentSocket = self.tlsSocket

        #Login for attacker
        auth_msg = b'AUTH PLAIN '+base64.b64encode(b'\x00'+ sender_email.encode() +b'\x00'+password.encode())+b'\r\n'
        print(auth_msg.decode())
        self.currentSocket.send(auth_msg)
        self.print_receiving_msg("Authentication", "235")

        #SMTP MAIL FROM
        print(self.MAIL_FROM)
        self.currentSocket.send(self.MAIL_FROM)
        self.print_receiving_msg("mail from", "250")


        #SMTP RCPT TO
        print(self.RCPT_TO)
        self.currentSocket.send(self.RCPT_TO)
        self.print_receiving_msg("rcpt to", "250")

        #DATA command
        self.currentSocket.send(b'DATA\r\n')
        self.print_receiving_msg("data", "354")

        
           
        #If there's DKIM, add to data of email, else send regular email
        if (self.dkim_para != None):
            self.create_DKIM_sig()
        else:
            #Message shown to user on UI
            print(self.from_header)
            self.currentSocket.send(self.from_header)
            print(self.to_header)
            self.currentSocket.send(self.to_header)
            print(self.subject_header)
            self.currentSocket.send(self.subject_header)
        
            print(self.body)
            self.currentSocket.send(self.body)
            

            print(self.endmsg)
            self.currentSocket.send(self.endmsg) 

        #quit command
        self.currentSocket.send(b'quit\r\n')
        self.print_receiving_msg("quit", "250")
        self.currentSocket.close()

    def create_DKIM_sig(self):
        print("preparing DKIM signature")
        f = open("dkimkey","r")
        pkey = f.read()
        print(pkey)
        
        #configure MIME to allow DKIM signature
        MIMEmessage = MIMEMultipart("alternative")
        MIMEmessage.attach(MIMEText(self.body.decode(), "plain"))
        MIMEmessage.attach(MIMEText(self.message_html, "html"))
        MIMEmessage["To"] = self.to_header.decode()
        MIMEmessage["From"] = self.from_header.decode()
        MIMEmessage["Subject"] = self.subject_header.decode()


        #inspecting dkim sign function
        #lines = inspect.getsource(dkim.sign)
        #print(lines)

        sig = dkim.sign(
            message = MIMEmessage.as_string().encode(),
            selector=self.dkim_para["s"],
            domain=self.dkim_para["d"],
            privkey=pkey.encode(),
            canonicalize=(b'simple',b'relaxed'),
            include_headers=self.dkim_para["sign_header"],
        )

        print(sig)
        self.currentSocket.send(sig+b"\r\n.\r\n")
        self.print_receiving_msg("dkim", "250")


        
    #Estabilish connection with attacker's SMTP server
    def socket_connection(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.currentSocket = self.clientSocket

        print("Connecting to mail server")
        self.currentSocket.connect(sender_mail_server)
        self.print_receiving_msg("connection", "220")


    #Read at most 1024 bytes from server and print out the message
    def print_receiving_msg(self, request, exp_code):
            recv = self.currentSocket.recv(1024).decode()
            print("message after " + request + " request: " + recv)
            if (recv[0:3] != exp_code):
                print(exp_code + ' reply not received from server.')