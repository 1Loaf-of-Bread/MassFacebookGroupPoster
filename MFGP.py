from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import os


def checkFilesExist():
    fileMissing = False

    if not os.path.isfile("postText.txt"):
        print("ERROR! File Missing: postText.txt")
        fileMissing = True

    if not os.path.isfile("groups.list"):
        print("ERROR! File Missing: groups.list")
        fileMissing = True
    
    if not os.path.isfile("chromedriver.exe"):
        print("ERROR! File Missing: chromedriver.exe")
        fileMissing = True

    if fileMissing:
        print()
        print("Please make sure 'groups.list', 'postText.txt', and 'chromedriver.exe' are all in the same dir as 'MFGP.py'. ")
        print()
        input("Press ENTER to Exit...")

        exit()

    return


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

    with open('postText.txt', 'r') as file:
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
        groupName = group[32:-1]

        if groupName[-1] == "/":
            groupName = groupName[0:-1]

        try:
            browser.get(group)

            time.sleep(3)

            browser.find_element(By.XPATH, "//*[contains(text(), 'Write something...')]").click()

            time.sleep(2)

            writePost = browser.find_element(By.CLASS_NAME, "_5rpu")
            writePost.send_keys(post)

            time.sleep(4)

            browser.find_element(By.XPATH, "//span[text()='Post']").click()

            time.sleep(8)
        except Exception as e:
            with open("Error Logs.log", "a") as file:
                file.write(f"There was an error posting to group '{groupName}', the error has been pasted below.\n")
                file.write(f"{str(e)}\n\n")

                file.close()

            pass
    
    browser.close()

    return


if __name__ == "__main__":
    checkFilesExist()
    sendToGroups()

    os.system('cls')

    print("Posting to Groups Complete.")
    print()

    input("Press ENTER Key to Exit...")

    exit()
