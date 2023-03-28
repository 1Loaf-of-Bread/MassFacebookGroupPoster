from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from colorama import Fore, init
from time import sleep
import os
init(autoreset=True)


def checkFilesExist():
    fileMissing = False

    if not os.path.isfile("postText.txt"):
        print("ERROR! File Missing: postText.txt")
        fileMissing = True

    if not os.path.isdir("groups"):
        print("ERROR! Folder Missing: groups")
        fileMissing = True
    
    if not os.path.isfile("chromedriver.exe"):
        print("ERROR! File Missing: chromedriver.exe")
        fileMissing = True

    if fileMissing:
        print()
        print("Please make sure 'groups' folder, 'postText.txt' file, and 'chromedriver.exe' file are all in the same dir as 'MFGP.py'. ")
        print()
        input("Press ENTER to Exit...")

        exit()

    return
    

def mainMenu():
    groupFiles = []

    for file in os.listdir("Groups"):
        if os.path.isfile(os.path.join("Groups", file)):
            if os.path.splitext(file)[1] == ".list":
                groupFiles.append(file)

    if groupFiles == []:
        os.system('cls')

        print(f"{Fore.RED}ERROR!: {Fore.WHITE}There are no group.list files provided.")
        print()
        print("Please add files such as 'facebook_groups.list' in the 'Groups' folder.")
        print()

        input("Press ENTER Key to Exit...")

        exit()

    postingGroups = []

    while True:
        groupFiles.sort()
        postingGroups.sort()

        os.system('cls')

        print("Available Group Files to Pick: ")
        print()

        for groupFile in groupFiles:
            print(f"    {groupFiles.index(groupFile)+1}. {groupFile}")

        print()

        if postingGroups != []:
            print("Posting to Groups:")
            print()

            for groupFile in postingGroups:
                print(f"    {postingGroups.index(groupFile)+1}. {groupFile}")

            print()

        numChoice = input("--> ")

        if numChoice.lower() == ":p":
            return postingGroups
        if numChoice.lower() == ":a":
            postingGroups = groupFiles
            groupFiles = []
            
            continue

        if numChoice[0:2].lower() == ":r":
            if postingGroups == []:
                print(f"{Fore.RED}ERROR!: {Fore.WHITE}You currently have no posting groups selected.")
                sleep(1.5)

                continue
            elif len(numChoice) < 3 or numChoice[2:].isdigit() == False:
                print(f"\n{Fore.RED}ERROR!: {Fore.WHITE}Please enter one of the numbers shown above for removal.")
                sleep(1.5)

                continue
            else:
                removalNum = int(numChoice[2:])

                if removalNum > len(postingGroups) or removalNum <= -1:
                    print(f"\n{Fore.RED}ERROR!: {Fore.WHITE}Please enter one of the numbers shown above.")
                    sleep(1.5)

                    continue

                groupFiles.append(postingGroups[removalNum-1])
                postingGroups.remove(postingGroups[removalNum-1])

                continue
        elif not numChoice.isdigit():
            print(f"\n{Fore.RED}ERROR!: {Fore.WHITE}Please enter a numerical value.")
            sleep(1.5)

            continue
        
        numChoice = int(numChoice) - 1

        if numChoice > len(groupFiles) or numChoice <= -1:
            print(f"\n{Fore.RED}ERROR!: {Fore.WHITE}Please enter one of the numbers shown above.")
            sleep(1.5)

            continue
        elif groupFiles[numChoice] not in postingGroups:
            if groupFiles[numChoice] in groupFiles:
                postingGroups.append(groupFiles[numChoice])

                groupFiles.remove(groupFiles[numChoice])
            else:
                print(f"\n{Fore.RED}ERROR!: {Fore.WHITE}Group file '{groupFiles[numChoice]}' not in listed group files above.")
                sleep(1.5)

                continue
        else:
            print(f"\n{Fore.RED}ERROR!: {Fore.WHITE}Group file '{groupFiles[numChoice]}' already added.")
            sleep(1.5)

            continue


def grabData(groupFiles):
    postText = ""

    with open('postText.txt', 'r') as file:
        postLines = file.readlines()
        file.close()

    for i in postLines:
        postText += i

    groups = []

    for groupFile in groupFiles:
        with open(f"groups\\{groupFile}", 'r') as fileRead:
            fileLines = fileRead.readlines()
            fileRead.close()

        for group in fileLines:
            groups.append(group[0:-1])

    return postText, groups


def waitPageLoad(browser, name):            
    while True:
        try:
            WebDriverWait(browser, 1).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, name)))

            sleep(1)

            break
        except TimeoutError:
            continue



def sendToGroups(postText, groups):
    os.system('cls')

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get('https://www.facebook.com/')
    browser.implicitly_wait(5)
    browser.maximize_window()
    
    emailText = "email"
    passwordText = "pass"

    email = browser.find_element(By.NAME, "email")
    email.send_keys(emailText)
    password = browser.find_element(By.NAME, "pass")
    password.send_keys(passwordText)

    browser.find_element(By.NAME, "login").click()

    waitPageLoad(browser, "x3ajldb")

    count = 0

    for group in groups:
        groupName = group[32:]

        if groupName[-1] == "/":
            groupName = groupName[0:-1]

        try:
            browser.get(group)

            waitPageLoad(browser, "x3ajldb")

            browser.find_element(By.XPATH, "//*[contains(text(), 'Write something...')]").click()

            waitPageLoad(browser, "_5rpu")

            writePost = browser.find_element(By.CLASS_NAME, "_5rpu")
            writePost.send_keys(postText)

            sleep(1)

            browser.find_element(By.XPATH, "//span[text()='Post']").click()

            try:
                alert = browser.switch_to.alert()
                alert.accept()
            except:
                a=0

            sleep(5)

            count += 1
            print(f"{Fore.GREEN}Posted to Group: {Fore.WHITE}{groupName} {Fore.CYAN}({count}/{len(groups)})")
        except Exception as e:
            with open("Error Logs.log", "a") as file:
                file.write(f"There was an error posting to group '{groupName}', the error has been pasted below.\n")
                file.write(f"{str(e)}\n\n")

                file.close()

            count += 1
            print(f"{Fore.RED}Error!: {Fore.WHITE}Unable to post to group '{groupName}', check 'Error Logs.log'. {Fore.CYAN}({count}/{len(groups)})")

            pass
    
    browser.close()

    return


if __name__ == "__main__":
    checkFilesExist()

    groupFiles = mainMenu()
    postText, groups = grabData(groupFiles)

    sendToGroups(postText, groups)

    print()
    print()
    print("Posting to Groups Complete.")
    print()

    input("Press ENTER Key to Exit...")

    exit()
