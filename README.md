# Email Spoofing
**Boston University EC700 Epoch2 Project:** 

**Authors: Pujan Paudel and Apollo Lo**

Our project involves exploring ability to create spoofed emailed through the vulnerabilities in Email's authentication protocol


## Email Flow

<div align="center"><a href="url"><img src="https://github.com/apollolo/Email-Spoofing/blob/main/pictures/Email%20flow.PNG" align="center"></a>
  
  *Source: Composition Kills: A Case Study of Email Sender Authentication on https://www.usenix.org/system/files/sec20-chen-jianjun.pdf*</div>

### SMTP (Simple Mail Transfer Protocol)
SMTP, defined in [RFC5321](https://tools.ietf.org/html/rfc5321), is the most common use of protocol to transmit emails between two users. When user A wants to send an email to another user B, user A will first draft up the email in MUA(Mail User Agent), which is the application users interact with. The email will be transmitted to the Sending service via SMTP protocol on port 25 or 587, which will then be transmitted to the Receiving server using SMTP again. When user B logs into his/her email account, the receiving server will transmit all emails received by the account to User B, which will show up on user B's MUA. 

During SMTP, the client will send with EHLO command to identify itself with the domain name. Then it will send "MAIL FROM" and "RCPT TO" to identify the sender and receiver for the email. Each command will have a OK reply code from the server as the respond. The next command is the data command, which indicates the start of the email message contents. These message contents are the contents that shows up to user in their MUA. After the message has been crafted and sent to the server, the quit command is sent to indicate the end of the conversation.

### MIME (Multipurpose Internet Mail Extension)
MIME is an extension of the email message content sent through SMTP. It allows messages to send in a different languages and attach files or videos in the email, which could not be done by SMTP. According to [RFC4021](https://tools.ietf.org/html/rfc4021), there are multiple headers that are defined by MIME, however our project will focus on from header, sender header, to header, and subject header as these are the headers a user will typically see in their email.

## Authentication 
Since there is no authentication mechanism in SMTP, the receiving server will have implement its own authentication methods to combat email spoofing. Email spoofing is a technique of creating email messages with forged sender address, in order to trick the receiver of the email. It is most commonly used for Phishing or other types of Malware injection to the victim's computer. Users typically rely on the email server to do the filtering in order to block fraudulent emails or separate spam emails from legitimate emails. SPF, DKIM, and DMARC are the three most widely adopted protocols for email authentication. These three protocols are combined together to verify different parts of an email and ensure email authenticity.

### SPF (Sender Policy Framework)
[RFC 7208](https://tools.ietf.org/html/rfc7208) stated that since there are no restrictions on what can be placed EHLO command and "MAIL FROM" in the SMTP protocol, SPF will verify if the email is indeed sent from these domains. receiving mail server will query the domain from "MAIL FROM" for SPF record, which is a DNS record that was added to the domain by the sending mail server. The SPF record will specify which IP address or hostnames are authorized to send email on their behalf. SPF will have different policies for different scenarios. If the email IP address doesn't match the IP address from SPF record, then a "fail" result is given, otherwise a "pass" result for matching IP address. "Permerror" result shows up when SPF could not verify the domain, either by missing "MAIL FROM" or non-existing domain name. 

### DKIM (DomainKeys Identified Mail)
DKIM is an authentication mechanism that attach a digital signature to the email. The idea is that sender of the email will create hashes of the different message headers to ensure data integrity. DKIM includes d tag for the domain and s tag for a "selector", selector is used to identify which DKIM signature amongst multiple signatures in the same domain. The receiver of the email will query "{s tag}r.\_domainkey{d tag}" for the public key and use it to ensure that the headers that are encrypted are not modified. 
The architecture of DKIM is defined in [RFC 6376](https://tools.ietf.org/html/rfc6376)

### DMARC (Domain-based Message Authentication, Reporting and Conformance)
DMARC is the last step of the authentication process and depends on the results from the previous two which is explained in [RFC7489](https://tools.ietf.org/html/rfc7489). The receiver will conduct alignment test of the domain in "from header" with domains in DKIM and SPF. It will query the domain in "from header" in the data message for DMARC record published by the sender. The sender will specify what to do with emails that failed SPF and DKIM, which the receiver will follow. This ensures that no other brand can pretend to be the sender, and if the receiver got an email that pretends to the be a company, the receiver will notify the company with information in DMARC record.  

## Project Attempts 
- python script with smtplib
- python script using socket and SMTP commands
- 
## Projct Progress
- SMTP server created with Digital Ocean with email funcitionality
- APIs created to connect json test cases with portal email functionality 
- SPF/DMARC protocol established for SMTP server

### Found Vulnerbiity 
- From header author name can be an specified with email
- comma can be use as next line feed
- SPF and DMARC checks attacker email address, author name is shown to user

-DMARC = pass even when header.d has comments inside, outlook dmarc may not be doing alignment correctly
-DKIM, hasing from header incorrectly, signature verification failed when from header is modified
-multiple d tags in DKIM will force the authentication process to ignore DKIM
