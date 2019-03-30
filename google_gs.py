# Для работы с Google groups нужно установить пакеты
# pip install selenium
# pip install anticaptcha
# pip install webdriver-manager
# и установить последний forefox (chrome ругается)

import pickle
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from selenium import webdriver
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
from webdriver_manager.firefox import GeckoDriverManager

# Данные для работы с google groups
GOOGLE_EMAIL = "ewewewew@gmail.com"
GOOGLE_PASSWORD = "asdasdasdasd"
# EMAIL_TO_SEMD_INVAIT = 'sdsdsd@mail.ru, sdsdds2@gmail.com'
MESSAGE_FOR_INVAIT = 'Добро пожаловать в группу'
# GROUP_NAME = 'my_fine_test_group'
# Ключ с сервиса https://anti-captcha.com - там за тысячу капч - 1 доллар - этот ключ рабочий
ANTICAPTCHA_ID= '3d6788ccf7b8ec387e76ff60898d00d8'
# https://www.google.com/recaptcha/api.js?render=reCAPTCHA_site_key"
SITE_KEY = '6LctgAgUAAAAACsC7CsLr_jgOWQ2ul2vC_ndi8o2'  # grab from site


# Данные для работы с google tables
GOOGLE_SHEET_JSON = 'google_table.json' # указать свой
GOOGLE_SHEET_TOKEN = 'google_table_token.pickle'
GOOGLE_SHEET_SCOPES =  ['https://www.googleapis.com/auth/spreadsheets']
GOOGLE_SPREADSHEET_ID = '1H_E8me__UR40m_mzRqZZioZdeX6sY7AaUphotexeVbg' # указать свой
SHEET_NAME = "Лист1"
RANGE_NAME = "{}!A:K".format(SHEET_NAME)

# Данные для работы с google directory
GOOGLE_DIRECTORY_JSON = 'directory.json'
GOOGLE_DIRECTORY_TOKEN = 'directory_token.pickle'
GOOGLE_DIRECTORY_SCOPES = ['https://www.googleapis.com/auth/admin.directory.group.member',
                           'https://www.googleapis.com/auth/admin.directory.group',
                           'https://www.googleapis.com/auth/admin.directory.user']

def get_cred(json_file, token_file, scopes):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                json_file, scopes)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(token_file,'wb') as token:
            pickle.dump(creds, token)

    return creds

def add_user_to_directory(user):
    creds = get_cred(GOOGLE_DIRECTORY_JSON, GOOGLE_DIRECTORY_TOKEN, GOOGLE_DIRECTORY_SCOPES)

    service = build('admin', 'directory_v1', credentials=creds)

    user_results = service.users().insert(
        body={
            "name": {
                "givenName": user['firstname'],
                "familyName": user['lastname']
            },
            "password": user['password'],
            "primaryEmail": user['email']
        # "changePasswordAtNextLogin": False,  # менять ли пароль при первом входе в аккаунт, закоментировано,  нет надобности
        }).execute()

    group_result = service.members().insert(groupKey = user['group_key1'], body={
         # group key
        'email': user['email'] # user email who need to insert in google groups
    }).execute()

def insert_anticaptcha_solution(driver, group_name):
    try:
        driver.find_element_by_id("g-recaptcha-response")
        api_key = ANTICAPTCHA_ID
        site_key = SITE_KEY
        url = 'https://groups.google.com/forum/#!managemembers/{}/invite'.format(group_name)
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
        error = driver.find_element_by_class_name('F0XO1GC-Nb-f').text
        print(error)


def send_invait(list_of_emails, group_name):
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
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
    driver.get("https://groups.google.com/forum/#!managemembers/{}/invite".format(group_name))
    time.sleep(3)
    areaForEmails = driver.find_element_by_xpath('//textarea[@role="combobox"]')
    areaForEmails.send_keys(list_of_emails)
    time.sleep(3)
    areaForEmails = driver.find_element_by_xpath('//textarea[@rows="10"]')
    areaForEmails.send_keys(MESSAGE_FOR_INVAIT)
    time.sleep(3)

    sendButton = driver.find_element_by_xpath('//div[@data-title="Отправить приглашения"]')
    sendButton.click()
    time.sleep(3)

    insert_anticaptcha_solution(driver, group_name)

def main():
    LIST_OF_EMAIL_TO_INVAIT = []
    creds = get_cred(GOOGLE_SHEET_JSON, GOOGLE_SHEET_TOKEN, GOOGLE_SHEET_SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=GOOGLE_SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    for i in range(1, len(values)):
        if (values[i][8]) == 'done':
            continue
        # print(values[i])

        user_data = {
            'firstname': values[i][0],
            'lastname': values[i][1],
            'email': values[i][2],
            'password': values[i][5],
            'group_key1': values[i][6],
            'group_key2': values[i][7],
            'invait': values[i][7]
        }

        if not user_data['invait'] == 'invated':
            LIST_OF_EMAIL_TO_INVAIT.append(user_data['email'])
            print()

        try:
            add_user_to_directory(user_data)
            cell_to_update = '{}!I'.format(SHEET_NAME) + str(i+1)
            sheet.values().update(spreadsheetId=GOOGLE_SPREADSHEET_ID, range=cell_to_update, valueInputOption="USER_ENTERED", body={"values": [['done']]}).execute()
        except Exception as e:
            print(e)

    GROUP_NAME_TO_SEND_INVAIT = values[2][7]
    if LIST_OF_EMAIL_TO_INVAIT:
        try:
            send_invait(', '.join(LIST_OF_EMAIL_TO_INVAIT), GROUP_NAME_TO_SEND_INVAIT)
            for i in range (2, len(LIST_OF_EMAIL_TO_INVAIT) + 1) :
                cell_to_update_invate = '{}!J'.format(SHEET_NAME) + str(i + 1)
                sheet.values().update(spreadsheetId=GOOGLE_SPREADSHEET_ID, range=cell_to_update_invate,
                                  valueInputOption="USER_ENTERED", body={"values": [['invated']]}).execute()
        except Exception as e:
            print(e)



if __name__ == '__main__':
    main()
