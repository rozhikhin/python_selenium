from selenium import webdriver
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
import time


GOOGLE_EMAIL = "proxima963@gmail.com"
GOOGLE_PASSWORD = "<tntkmutqpt300#"
EMAIL_TO_SEMD_INVAIT = 'rozhihin@mail.ru, rozhihin@gmail.com'
MESSAGE_FOR_INVAIT = 'Добро пожаловать в группу'
GROUP_NAME = 'my_fine_test_group'
ANTICAPTCHA_ID= '3d6788ccf7b8ec387e76ff60898d00d8'
SITE_KEY = '6LctgAgUAAAAACsC7CsLr_jgOWQ2ul2vC_ndi8o2'  # grab from site


def insert_anticaptcha_solution(driver):
    try:
        driver.find_element_by_id("g-recaptcha-response")
        api_key = ANTICAPTCHA_ID
        site_key = SITE_KEY
        url = 'https://groups.google.com/forum/#!managemembers/{}/invite'.format(GROUP_NAME)
        print('Вычисляем антикапчу')
        client = AnticaptchaClient(api_key)
        task = NoCaptchaTaskProxylessTask(url, site_key)
        job = client.createTask(task)
        job.join()

        response = job.get_solution_response()
        print("Received solution", response)
        time.sleep(2)

        driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response)
        time.sleep(2)
        driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response)
        time.sleep(2)

        capchaButton = driver.find_element_by_xpath('//div[@aria-disabled]')
        capchaButton.click()
        print('Все приглашения отправлены')
    except:
        print('Все приглашения отправлены')


def send_invait(list_of_emails):
    driver = webdriver.Firefox()
    driver.get("https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    print(driver.title)
    time.sleep(2)
    driver.find_element_by_id("identifierId").send_keys(GOOGLE_EMAIL)
    driver.find_element_by_id("identifierNext").click()
    time.sleep(2)
    passwordElement = driver.find_element_by_name('password')
    time.sleep(2)
    passwordElement.send_keys(GOOGLE_PASSWORD)
    time.sleep(3)
    driver.find_element_by_id("passwordNext").click()
    driver.get("https://groups.google.com/forum/#!managemembers/my_fine_test_group/invite")
    time.sleep(3)
    areaForEmails = driver.find_element_by_xpath('//textarea[@role="combobox"]')
    areaForEmails.send_keys(EMAIL_TO_SEMD_INVAIT)
    time.sleep(3)
    areaForEmails = driver.find_element_by_xpath('//textarea[@rows="10"]')
    areaForEmails.send_keys(MESSAGE_FOR_INVAIT)
    time.sleep(3)

    sendButton = driver.find_element_by_xpath('//div[@data-title="Отправить приглашения"]')
    sendButton.click()
    time.sleep(3)

    insert_anticaptcha_solution(driver)
################################################################


if __name__ == '__main__':
    send_invait(EMAIL_TO_SEMD_INVAIT)