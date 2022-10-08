from selenium.webdriver.common.by import By
from selenium import webdriver
import time


def getGroups():
    groups = []

    with open("groups.list", 'r') as file:
        groupLines = file.readlines()
        file.close()
    
    for group in groupLines:
        groups.append(group)

    return groups


def getPost():
    post = ""

    with open('postText.txt') as file:
        postLines = file.readlines()
        file.close()

    for i in postLines:
        post += i

    return post


def sendToGroups():
    groups = getGroups()
    post = getPost()

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get('https://www.facebook.com/')
    browser.implicitly_wait(5)
    browser.maximize_window()

    emailText = "email"
    passwordText = "password"

    time.sleep(2)

    email = browser.find_element(By.NAME, "email")
    email.send_keys(emailText)
    password = browser.find_element(By.NAME, "pass")
    password.send_keys(passwordText)

    browser.find_element(By.NAME, "login").click()

    time.sleep(7)

    for group in groups:
        browser.get(group)

        time.sleep(3)

        browser.find_element(By.XPATH, "//*[contains(text(), 'Write something...')]").click()

        time.sleep(2)

        writePost = browser.find_element(By.CLASS_NAME, "_5rpu")
        writePost.send_keys(post)

        time.sleep(4)

        browser.find_element(By.XPATH, "//*[contains(text(), 'Post')]").click()

        time.sleep(8)
    
    browser.close()


if __name__ == "__main__":
    sendToGroups()
    time.sleep(1)
    exit()