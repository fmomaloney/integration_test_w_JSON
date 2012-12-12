package com.Crsf.Verify2;

import org.apache.log4j.Logger;
import java.util.regex.Pattern;
import org.junit.*;
import static org.junit.Assert.*;
import java.util.concurrent.TimeUnit;
import java.util.*; // allows iterator, map
import java.util.NoSuchElementException;
import java.io.*; // allows FileReader
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;
//import org.json.simple.JSONArray;
//import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.openqa.selenium.JavascriptExecutor;

public class NewNonPomTest {

                private WebDriver driver;
                private String baseUrl;
                private StringBuffer verificationErrors = new StringBuffer();
                private static Logger logger = Logger.getLogger(com.Crsf.Verify2.NewNonPomTest.class);
                private Object jobj;

                @Before
                public void setUp() throws Exception {
                                // set up webdriver
                                driver = new FirefoxDriver();
                                baseUrl = "http://scheduling.XXXXXXXXcorp.com/";
                                driver.manage().timeouts().implicitlyWait(20, TimeUnit.SECONDS);
                                // Read my JSON data into jobj, before block seems best
                                String myJson = "C:\\Selenium\\json_data.json";
                                JSONParser parser = new JSONParser();
                                try {
                                                // get our JSONObject from file, extends HashMap
                                    jobj = parser.parse(new FileReader(myJson));
                                  } catch (IOException e) {
                                    System.out.println("IO error " + e);
                          } catch (ParseException e) {
                                    System.out.println("parsing error " + e);
                          } catch (Exception e ) {
                                    System.out.println("unexpected error? " + e);
                          }
                }

                @Test
                public void crsfFirefoxJava() throws Exception {
                                driver.get(baseUrl + "SANDBOX-LTRDev/COUNTRYfinancial-DEV/index.html");
                                logger.info("go to " + baseUrl + "SANDBOX-LTRDev/COUNTRYfinancial-DEV/index.html");
                                logger.info("page title is " + driver.getTitle());
                                assertEquals("Schedule a Deposition - Country Financial [DEV]", driver.getTitle());
                                //assertEquals("berfo!", driver.getTitle());
                                // edit hidden field and change email address to my gmail
                                ((JavascriptExecutor) driver).executeScript( "document.getElementsByName('recipient')[0].value='fmomaloneytest@gmail.com';");

                                // use hashmap to populate all text elements on CRSF
                                Iterator i = ((HashMap) jobj).entrySet().iterator();
                                while (i.hasNext()) {
                                   Map.Entry e = (Map.Entry)i.next();
                                                   String mykey = e.getKey().toString();
                                                   String myval = e.getValue().toString();
                                                   driver.findElement(By.id(mykey)).clear();
                                                   driver.findElement(By.id(mykey)).sendKeys(myval);
                                                  }

                                // click datepicker done button, as date last data in JSON file
                                driver.findElement(By.xpath("//*[@id='ui-datepicker-div']/div[3]/button[2]")).click();
                                driver.findElement(By.name("Full_Name")).clear();
                                driver.findElement(By.name("Full_Name")).sendKeys("frank b. maloney!");
                                driver.findElement(By.id("atty")).click();
                                // JQuery ui.dropdown elements, initially hidden. Use arrows to select
                                driver.findElement(By.xpath("//div[@id='rowNoticingFirm']/span/a/span")).click();
                                driver.findElement(By.xpath("//div[@id='rowNoticingFirm']/span/input[2]")).sendKeys("wunder");
                                driver.findElement(By.xpath("//div[@id='rowNoticingFirm']/span/input[2]")).sendKeys(Keys.ARROW_DOWN);
                                driver.findElement(By.xpath("//div[@id='rowNoticingFirm']/span/input[2]")).sendKeys(Keys.TAB);
                                driver.findElement(By.xpath("/html/body/form/div/div[3]/div/div[1]/fieldset/div[12]/span/a/span[1]")).click();
                                driver.findElement(By.xpath("/html/body/form/div/div[3]/div/div[1]/fieldset/div[12]/span/input[2]")).sendKeys("florida");
                                driver.findElement(By.xpath("/html/body/form/div/div[3]/div/div[1]/fieldset/div[12]/span/input[2]")).sendKeys(Keys.ARROW_DOWN);
                                driver.findElement(By.xpath("/html/body/form/div/div[3]/div/div[1]/fieldset/div[12]/span/input[2]")).sendKeys(Keys.TAB);
                                driver.findElement(By.xpath("//div[@id='rowclaimsatty']/span/a/span[1]")).click();
                                driver.findElement(By.xpath(".//*[@id='rowclaimsatty']/span/input[2]")).clear();
                                driver.findElement(By.xpath(".//*[@id='rowclaimsatty']/span/input[2]")).sendKeys("james");
                                driver.findElement(By.xpath(".//*[@id='rowclaimsatty']/span/input[2]")).sendKeys(Keys.ARROW_DOWN);
                                driver.findElement(By.xpath(".//*[@id='rowclaimsatty']/span/input[2]")).sendKeys(Keys.TAB);
                                // File upload from windows desktop
                                driver.findElement(By.id("txtUploadFile")).sendKeys("C:\\Users\\fmalone\\Desktop\\notice-of-depositions.pdf");
                                // click a couple checkboxes
                                driver.findElement(By.id("chkProvVideoConf")).click();
                                driver.findElement(By.id("transTurnaround-STD")).click();
                                // add notes with a current timestamp
                                Date now = new Date();
                                //Long myNow = date.getTime();
                                driver.findElement(By.id("tbNotes")).clear();
                                driver.findElement(By.id("tbNotes")).sendKeys("JSON demo via firefox submitted " + now.toString());
                                // Submit the form
                                driver.findElement(By.id("btnSubmit")).click();
                                driver.findElement(By.xpath("//*span[@class = 'ui-button-text' and . = 'Yes, Save']")).click();
                }

                @After
                public void tearDown() throws Exception {
                                driver.close();
                                driver.quit();
                                String verificationErrorString = verificationErrors.toString();
                                if (!"".equals(verificationErrorString)) {
                                                fail(verificationErrorString);
                                }
                }

                private boolean isElementPresent(By by) {
                                try {
                                                driver.findElement(by);
                                                return true;
                                } catch (NoSuchElementException e) {
                                                return false;
                                }
                }

}
