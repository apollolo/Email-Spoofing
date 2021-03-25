from config import *

test_list = {
    "Normal1": {
        "ehlo": b'EHLO NOTREALDOMAIN\r\n',
        "mailfrom": b'mail from: <'+sender_email.encode() +b'>\r\n',
        "rcptto": b'rcpt to: <'+receiver_email.encode() +b'>\r\n',
        #"dkim" : {"d":b"attack.com", "s":b"selector", "sign_header": [b"To",b"From", b"Subject"]},
         "data": {
            "from_header": b"From: FAKE NAME <fake@fake.com>\r\n",
            "to_header": b"To: <victim@victim.com>\r\n",
            "subject_header": b"Subject: New Subjects\r\n",
            "body": b"This is a test message.\r\n",
            "html": b"",
        },
         "starttls": True,
    },
    "attack1": {
        "ehlo": b'EHLO pujanpaudel.net\r\n',
        "mailfrom": b'mail from: <test@pujanpaudel.net>\r\n',
        "rcptto": b'rcpt to: <'+receiver_email.encode() +b'>\r\n',
        "dkim" : {"d":b"pujanpaudel.net", "s":b"postal-J2v2Mw", "sign_header": b"From: <admin@legitimate.com>"},
         "data": {
            "from_header": b"From: FAKE NAME <fake@fake.com>\r\n",
            "to_header": b"To: <victim@victim.com>\r\n",
            "subject_header": b"Subject: New Subjects\r\n",
            "body": b"This is a test message.\r\n",
        },
         "starttls": True
    },
   
}


