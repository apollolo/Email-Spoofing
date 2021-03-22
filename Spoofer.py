import Sender
import test_cases


if __name__ == '__main__':
	print("Sending spoof emails based on test cases")
	print (test_cases.test_list["attack1"]["mailfrom"].decode())
	Sender.mail_sender(test_cases.test_list["attack1"])

	#Sender()