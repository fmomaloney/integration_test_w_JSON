#!C:/Python3/bin/python.exe

'''
script to verify email from json file
To Do: read email verify terms from JSON. Write as unittest. Add logging.
'''

#from pprint import pprint
import email, json
import imaplib, ssl
import logging, unittest, socket
from time import localtime, strftime

class CRSF_verify_email_refactor(unittest.TestCase):

    def setUp(self):
        # set up logger
        #logging.basicConfig(filename='/home/fmaloney/Selenium/email_verify.log',format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
        logging.basicConfig(filename='C:\loggingResults\py_crsf.log',level=logging.DEBUG)
        #logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.current = strftime("%Y-%m-%d %H:%M:%S", localtime())
        logging.info('========================\nStarting the logger at {}!'.format(self.current))
        # get test data from JSON into dictionary
        JSONFILE = 'C:\Selenium\json_data.json'
        try:
            self.mydata =  json.load(open(JSONFILE))
            print("reading {} values from JSON".format(len(self.mydata)))
        except IOError as openerr:
            print("Could not open {} for writing!{}\n".format(JSONFILE, openerr))
            return
        # connect to gmail inbox
        try:
            self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
            self.mail.login('fmomaloneytest@gmail.com', 'XXXXXX')
            self.mail.select("Inbox")
        except socket.error as connecterr:
            print("could not connect to inbox. ", connecterr)
            logging.error("could not reach gmail inbox: ".format(connecterr))

    def tearDown(self):
        self.mydata = {}
        self.mail.close()
        self.mail.logout()

    def test_email_body(self):
        foundcount = 0
        # find the notification message in inbox
        status,notificationmsg  = self.mail.search(None, '(SUBJECT "Scheduling Request")')
        mymsg = notificationmsg[0]
        #print("status {} and mail id {}!".format(status,notificationmsg))
        mymsgstr = str(mymsg, "utf-8")
        typz, detailz = self.mail.fetch(mymsgstr,'(RFC822)')
        raw_email = detailz[0][1]
        # this is email flattened to string
        email_string = str(raw_email, "utf-8")
        logging.debug("this is raw email\n{}".format(email_string))
        email_message = email.message_from_string(email_string)
        hdrinfo = "From: " + email_message["From"] + "\n"
        hdrinfo += "Subject: " + email_message["Subject"] + "\n"
        hdrinfo += "Date: " + email_message["Date"] + "\n"
        print(hdrinfo)
        logging.info(hdrinfo)

        # now loop through dict and look for values in email
        for keys in self.mydata:
            try:
                myindex =  email_string.index(self.mydata[keys])
                # now assert something
                print("OK: found term \"{}\" in email".format(self.mydata[keys]))
                foundcount = foundcount + 1
            except ValueError as valerr:
                print("did not find term \"{}\" anywhere in email!  err: {} ".format(self.mydata[keys],valerr))

        print("test complete")
        logging.info("Found {} of {} terms in email notification at {}".format(foundcount, len(self.mydata), self.current))

if __name__ == '__main__':
    unittest.main()
