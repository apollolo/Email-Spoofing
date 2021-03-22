from config import *

test_list = {
    "attack1": {
        "ehlo": b'EHLO NOTREALDOMAIN\r\n',
        "mailfrom": b'mail from: <'+sender_email.encode() +b'>\r\n',
        "rcptto": b'rcpt to: <'+receiver_email.encode() +b'>\r\n',
         "data": {
            "from_header": b"From: FAKE NAME <fake@fake.com>\r\nFrom: <admin@legitimate.com>\r\n",
            "to_header": b"To: <victim@victim.com>\r\n",
            "subject_header": b"Subject: This is a test Subject\r\n",
            "message": b"This is a test message.\r\n",
        },
    },
   
}


