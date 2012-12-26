#!/usr/bin/python
'''
This is a DB connect example using our python 2.6.6. Writing this as unittest.
Plan is to read JSON test data into a dictionary, then read DB output data into
another, then compare. Note that in this situation, the keys in the dictionaries
will not match (form element names vs. database columns). Therefore I am only
looking at the values, and overlap between sets of values constitutes passing test.
'''

from pprint import pprint
from time import localtime, strftime
import logging, unittest, json
import MySQLdb as mydb

class CRSF_db_verify(unittest.TestCase):

    def setUp(self):
        # set up the logging
        logging.basicConfig(filename='crsf_db.log',
                            level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%m/%d/%y %I:%M:%S%p ')
        self.current = strftime("%Y-%m-%d %H:%M:%S", localtime())
        logging.info("=======================================")
        logging.info("Starting logger at %s!" % (self.current))
        # Open the data file and put into dictionary
        #JSONFILE = 'blurch.json'
        JSONFILE = 'json_data.json'
        try:
            self.mydata = json.load(open(JSONFILE))
            logging.info("Read %i values from the data file", len(self.mydata))
        except IOError as openerr:
            logging.error("Could not find or open file %s: %s!" % (JSONFILE, openerr))
            sys.exit(1)
        # Connect to the database and return handle
        try:
            self.con = mydb.connect(host='a_db_host.com',
                       user='fmaloney',
                       passwd='gkjgfaifiaoh',
                       db='CRSF');
            self.curser = self.con.cursor(mydb.cursors.DictCursor)
            logging.info("Connected to database, got a cursor.")
        except mydb.Error, e:
            logging.error("DB Connect Error %d: %s!" % (e.args[0],e.args[1]))
            sys.exit(1)
        #return self.mydata,self.curser - works w/o a return

    def tearDown(self):
        self.mydata = {}
        self.con.close()

    def test_crsf_database(self):
        # some debug for test JSON
        if (logging.DEBUG):
            for keys in self.mydata:
                logging.debug("data key is %s and value is %s." % (keys, self.mydata[keys]))
        # Now I want to read from deposition table into my dictionary cursor.
        # I will look at the most recent deposition record in this select. Select * might make test less brittle.
        select_string = "select * from deposition order by id desc limit 1;"
        self.curser.execute(select_string)
        data = self.curser.fetchone()
        logging.info("Read %i record from the database type %s!" % (len(data), type(data)))
        #pprint(data) - this is debug for read from database
        if (logging.DEBUG):
            for keyz in data:
                logging.debug("db data key is %s and value is %s." % (keyz, data[keyz]))
	    # Now I want to compare values from self.mydata with data{}. There are a lot of ways to do this,
        # but it seems that the simplest method is to create a couple sets from the dictionary values,
        # and then use set operations to find difference and overlap. This is good enough for my purposes.
        # Note that I'd like this to still work when the number of values in the 2 dictionaries differs.
        mydataset = set(self.mydata.values())
        dataset = set(data.values())
        setmatches = mydataset.intersection(dataset)
        setdifference = mydataset.difference(dataset)
        logging.info("There are %i terms that matched: %s" % (len(setmatches), setmatches))
        logging.info("There are %i terms that did not match: %s" % (len(setdifference), setdifference))
        # assert to make test pass or fail. In this case I am satisfied that 5 matches passes.
        self.assertTrue(len(setmatches) >= 5)

if __name__ == '__main__':
    unittest.main()

# the end
