import requests
import json
from config import *
url="http://167.99.0.42:3000/sendemail"

headers = ["from", "to", "subject", "message", "sender", "dkim_d", "dkim_s", "mail_from", "resentsender"]
defaults={
"helo":"postal.pujanpaudel.net",
"dkim_domain":"pujanpaudel.net",
"dkim_subdomain":"postal-IZOG0a",
"smtp_mailfrom":"omlkfo@rp.postal.pujanpaudel.net"
}



for i in range(33,500,5): #increment by 5
	attackbody={
	"from": chr(i) + chr(i+1) + chr(i+2) + chr(i+3) + chr(i+4) + "@pujanpaudel.net",
	"to": "EC700emailtesting@gmail.com",	
	"subject":"This is a test subject " + str(i),
	"message":"Just a regular message " + str(i),
	"sender":"",
	"dkim_d":defaults["dkim_domain"],
	"dkim_s":defaults["dkim_subdomain"],
	"mail_from":"spoof@pujanpaudel.net",
	"resentsender":"resent_sender"
	}
	print(attackbody)
	req = urllib.request.Request(url)
	req.add_header('Content-Type', 'application/json; charset=utf-8')
	jsondata = json.dumps(attackbody)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	response = urllib.request.urlopen(req, jsondataasbytes)
	break
