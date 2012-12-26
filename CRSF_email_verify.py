#!C:/Python3/bin/python.exe

'''
Script to verify email message against some JSON data. This one is Python3 w/ PyDev.
I am looking at my Gmail account for a notification email, and logging matches against
body text as success or failure. Script written as unittest.
'''

#from pprint import pprint
import email, json, sys
import imaplib, ssl
import logging, unittest, socket
from time import localtime, strftime

class CRSF_verify_email_refactor(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(filename='/home/fmaloney/github/integration_test_w_json/py_crsf.log',
                            level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%y %I:%M:%S%p ')
        self.current = strftime("%Y-%m-%d %H:%M:%S", localtime())
        logging.info("=======================================")
        logging.info("Starting logger at %s!" % (self.current))
        # get test data from JSON into dictionary
        JSONFILE = '/home/fmaloney/github/integration_test_w_json/json_data.json'
        #JSONFILE = 'C:\Selenium\json_data.json'
        try:
            self.mydata =  json.load(open(JSONFILE))
            logging.info("Read %i values from the data file", len(self.mydata))
        except IOError as openerr:
            logging.error("Could not find or open file %s: %s!" % (JSONFILE, openerr))
            sys.exit(1)
        # connect to gmail inbox
        try:
            self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
            self.mail.login('fmomey@gmail.com', 'xxxxxxxxx')
            self.mail.select("Inbox")
            logging.info("Connected to Gmail Inbox.")
        except socket.error as connecterr:
            logging.error("could not reach gmail inbox: ".format(connecterr))

    def tearDown(self):
        self.mydata = {}
        self.mail.close()
        self.mail.logout()

    def test_email_body(self):
        foundcount = 0
        # find the notification message in inbox. I should raise error if no match
        status,notificationmsg  = self.mail.search(None, '(SUBJECT "Scheduling Request")')
        #status,notificationmsg  = self.mail.search(None, '(SUBJECT "bberfo")')
        mymsg = notificationmsg[0]
        mymsgstr = str(mymsg, "utf-8")
        if (len(mymsgstr) == 0):
            logging.error("Notification email was not in the inbox! Quitting...")
            raise NameError("Notification Email not in Inbox!")
            sys.exit(1)
        typz, detailz = self.mail.fetch(mymsgstr,'(RFC822)')
        # this is email flattened to string
        email_string = str(detailz[0][1], "utf-8")
        email_message = email.message_from_string(email_string)
        hdrinfo = "From: " + email_message["From"] + "  Subject: " + email_message["Subject"] + "  Date: " + email_message["Date"]
        logging.info(hdrinfo)

        for part in email_message.walk():
            # our emails may be multipart, as file attachment allowed. But there will always be plaintext payload
            if part.get_content_type() == 'text/plain':
                txtpayload = part.get_payload()
        logging.debug("this is the message body\n{}".format(txtpayload))
        # now loop through dict and look for values in email body
        for keys in self.mydata:
            try:
                myindex =  txtpayload.index(self.mydata[keys])
                logging.debug("OK: found term %s in email" % (self.mydata[keys]))
                foundcount = foundcount + 1
            except ValueError as valerr:
                logging.error("did not find term \"%s\" anywhere in email!  err: %s." % (self.mydata[keys],valerr))
        # test summary
        logging.info("Found %i out of %i terms in email notification!" % (foundcount, len(self.mydata)))
        # assert to pass or fail test
        self.assertTrue(foundcount >= 5)

if __name__ == '__main__':
    unittest.main()
