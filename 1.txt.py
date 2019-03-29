from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions
import pickle
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask

import time

mail_address = "proxima963@gmail.com"
password = "<tntkmutqpt300#"


# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# go to the google home page
driver.get("https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin")

# the page is ajaxy so the title is originally this:
print(driver.title)


# loginElement = driver.find_element_by_id("identifierId")
# loginElement.send_keys("proxima963@gmail.com")


# nextButton = driver.find_element_by_id("identifierNext")
# nextButton.send_keys(Keys.RETURN)
#
#
# # passwordElement = driver.find_element_by_id("password")
# passwordElement = driver.find_element_by_class_name("whsOnd")
# passwordElement.send_keys("<tntkmutqpt300#")
#
# # nextButton = driver.find_element_by_id("passwordNext");
# # nextButton.send_keys(Keys.RETURN)
#
# try:
#     # we have to wait for the page to refresh, the last thing that seems to be updated is the title
#     WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))
#
#     # You should see "cheese! - Google Search"
#     print(driver.title)
#
# finally:
#     # driver.quit()
#
#     pass


time.sleep(2)

driver.find_element_by_id("identifierId").send_keys(mail_address)
driver.find_element_by_id("identifierNext").click()

time.sleep(2)

passwordElement = driver.find_element_by_name('password')
time.sleep(2)

passwordElement.send_keys(password)
time.sleep(3)

driver.find_element_by_id("passwordNext").click()

driver.get("https://groups.google.com/forum/#!managemembers/my_fine_test_group/invite")


# areaForEmails = driver.find_element_by_id("gwt-uid-144")
time.sleep(3)
areaForEmails = driver.find_element_by_xpath('//textarea[@role="combobox"]')
areaForEmails.send_keys('79032018796@ya.ru')
time.sleep(3)
areaForEmails = driver.find_element_by_xpath('//textarea[@rows="10"]')
areaForEmails.send_keys('sdfsdfsd')

time.sleep(3)

# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
# cookies = pickle.load(open("cookies.pkl", "rb"))
# for cookie in cookies:
#     driver.add_cookie(cookie)

sendButton = driver.find_element_by_xpath('//div[@data-title="Отправить приглашения"]')
sendButton.click()

################################################################

api_key = '3d6788ccf7b8ec387e76ff60898d00d8'
# site_key = '6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'  # grab from site
site_key = '6LctgAgUAAAAACsC7CsLr_jgOWQ2ul2vC_ndi8o2'  # grab from site
url = 'https://groups.google.com/forum/#!managemembers/my_fine_test_group/invite'

client = AnticaptchaClient(api_key)
task = NoCaptchaTaskProxylessTask(url, site_key)
job = client.createTask(task)
print("Waiting to solution by Anticaptcha workers")
job.join()
# Receive response
response = job.get_solution_response()
print("Received solution", response)
time.sleep(3)
# Inject response in webpage
driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response)
time.sleep(2)
driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response)
# driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "INNER_HTML"')
time.sleep(2)
# driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "INNER_HTML"')

# Wait a moment to execute the script (just in case).
# time.sleep(3)

# Press submit button
# capchaButton = driver.find_element_by_xpath('//div[@role="dialog"]').find_element_by_xpath('//div[@role="button"]')
capchaButton = driver.find_element_by_xpath('//div[@aria-disabled]')
capchaButton.click()