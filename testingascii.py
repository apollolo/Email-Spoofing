from Sender import *
import test_cases
import time


if __name__ == '__main__':
	print("Sending spoof emails based on test cases")
	
	for i in range(9,12,1): #increment by 10
	attack_case = test_cases.test_list["Normal1"]
	#temp = chr(i) + chr(i+1) + chr(i+2) + chr(i+3) + chr(i+4) + chr(i+5) + chr(i+6) + chr(i+7) + chr(i+8) + chr(i+9)
	temp = chr(i) + chr(i+1) +chr(i) + chr(i+1) +chr(i) + chr(i+1) +chr(i) + chr(i+1)
	attack_case["data"]["from_header"] = b"From: " + temp.encode() + b" <fake@fake.com>\r\n"
	
	message = str(i) + " ~ " + str(i+1)
	#message = str(i) + " ~ " + str(i+9)
	attack_case["data"]["subject_header"] = b"Subject: New Subject " + message.encode() + b"\r\n"
	attack_case["data"]["body"] = message.encode()

	newmail = MailSender()
	newmail.set_parameter(attack_case)

	time.sleep(0.5)
	newmail.mail_sender()

	