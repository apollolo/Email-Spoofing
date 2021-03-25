from Sender import *
import test_cases


if __name__ == '__main__':
	print("Sending spoof emails based on test cases")
	
	#Loop through all test cases
	for x in test_cases.test_list:
		print("keys: " + x)
		print ("Victim's email address: " + test_cases.test_list[x]["rcptto"].decode())
	newmail = MailSender()
	newmail.set_parameter(test_cases.test_list["Normal1"])
	newmail.mail_sender()

