# README file for "integration test with JSON" project
------------------------------------------------------

The purpose of this project is to demonstrate some simple integrations tests supported by common data using   
JSON as an interchange format. The idea is to get test scripts in different languages to work together. 

This example is from a work project and has the following components:
1. Populate an online order form using a selenium script. This script reads JSON data and writes it to the form.
2. Verify and email notification against the JSON data. I am using imaplib and just verifying that the data strings appear in the email body.
3. Verify that submitted form info is saved to a database table. Script reads the JSON data and looks for same in database.

View log files for the test output. Note that some names, hosts, URL are changed to protect the innocent.

