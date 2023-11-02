from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from get_chrome_driver import GetChromeDriver
from selenium.webdriver.common.by import By
from colorama import Fore, init
from selenium import webdriver
from time import sleep
from io import BytesIO
import win32clipboard
from PIL import Image
import customtkinter
import ctypes
import os
init(autoreset=True)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


### ~~~ Pre-Posting ~~~ ###

def checkFilesExist():
    required_files = ["postText.txt", "groups", "chromedriver.exe"]
    missing_files = [file for file in required_files if not os.path.exists(file)]

    if missing_files:
        message = "\n".join([f"File/Folder Missing: {file}" for file in missing_files])
        ctypes.windll.user32.MessageBoxW(0, f"{message}\n\nPlease make sure the required files/folders are in the same directory as 'MFGP.py'.", "ERROR!", 0)
        exit()


def checkChromeDriver():
    print("Checking Installed ChromeDriver...")
    get_driver = GetChromeDriver()
    get_driver.install(output_path=os.getcwd())
    print("Complete.")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

###########################


def grabData(groupFiles, imageFile):
    postText = ""

    with open('postText.txt', 'r') as file:
        postText = file.read()

    groups = []

    for groupFile in groupFiles:
        with open(f"groups\\{groupFile}", 'r') as fileRead:
            groups.extend([group.strip() for group in fileRead.readlines()])

    if imageFile:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()

        image = Image.open(imageFile)
        output = BytesIO()
        image.convert('RGB').save(output, 'BMP')
        imageFileData = output.getvalue()[14:]
        output.close()

        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, imageFileData)
        win32clipboard.CloseClipboard()

    with open("UP.txt", 'r') as fileRead:
        email, password = map(str.strip, fileRead.readline().split(','))

    return postText, groups, email, password


### ~~~ Posting to Groups ~~~ ###

def waitPageLoad(browser, name):
    while True:
        try:
            WebDriverWait(browser, 1).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, name)))
            sleep(1)
            break
        except TimeoutError:
            continue


def postToGroups(postText, groups, imageFile, emailText, passwordText):
    clear_screen()
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    service = Service(executable_path='./chromedriver.exe')
    browser = webdriver.Chrome(service=service, options=chrome_options)

    browser.get('https://www.facebook.com/')
    browser.implicitly_wait(10)
    browser.maximize_window()

    email = browser.find_element(By.NAME, "email")
    email.send_keys(emailText)
    password = browser.find_element(By.NAME, "pass")
    password.send_keys(passwordText)

    WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.NAME, "login"))).click()
    waitPageLoad(browser, "x3ajldb")

    count = 0
    failCount = 0

    for group in groups:
        group_url = group.strip()
        group_name = os.path.basename(group_url.rstrip('/'))

        try:
            browser.get(group_url)
            waitPageLoad(browser, "x3ajldb")

            writeSomethingElement = WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Write something...')]")))
            writeSomethingElement.click()
            waitPageLoad(browser, "_5rpu")

            writePost = browser.find_element(By.CLASS_NAME, "_5rpu")
            writePost.send_keys(postText)

            if imageFile:
                sleep(1)
                writePost.send_keys(Keys.CONTROL, 'v')

            sleep(1)

            postButtonElement = WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[text()='Post']")))
            browser.execute_script("arguments[0].click();", postButtonElement)

            try:
                alert = browser.switch_to.alert
                alert.accept()
            except:
                pass

            sleep(5)

            count += 1
            print(f"{Fore.GREEN}Posted to Group: {Fore.WHITE}{group_name} {Fore.CYAN}({count}/{len(groups)})")
        except Exception as e:
            with open("Error Logs.log", "a") as file:
                file.write(f"There was an error posting to group '{group_name}', the error has been pasted below.\n")
                file.write(f"{str(e)}\n\n")

            count += 1
            failCount += 1
            print(f"{Fore.RED}Error!: {Fore.WHITE}Failed to post to group '{group_name}', check file 'Error Logs.log' for the reason. {Fore.CYAN}({count}/{len(groups)})")

            pass

    browser.close()

    return failCount, count


### ~~~ GUI ~~~ ###

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.getGroupsList()

        self.geometry("350x455")
        self.title("MassFacebookGroupPoster v2.0.0")
        self.resizable(False, False)

        self.postingGroupsString = ""
        self.imagePath = ""

        groupSelectionLabel = customtkinter.CTkLabel(self, text="Please select the group files you wish to post to.")
        groupSelectionLabel.grid(row=0, padx=15, pady=5, sticky="nsew")

        self.groupSelectionBox = customtkinter.CTkComboBox(self, values=self.groupsList, width=2)
        self.groupSelectionBox.set("Select Group Files")
        self.groupSelectionBox.grid(row=1, padx=15, pady=5, sticky="nsew")

        refreshSelectionBoxButton = customtkinter.CTkButton(self, width=2, height=2, text="Refresh Group File Selection List", command=self.refreshGroupList)
        refreshSelectionBoxButton.grid(row=2, padx=15, pady=5, sticky="nsew")

        buttonsFrame = customtkinter.CTkFrame(self)
        buttonsFrame.grid(row=3, padx=15, pady=5, sticky="nsew")

        addGroupButton = customtkinter.CTkButton(buttonsFrame, text="Add Group", height=2, width=2, command=self.addGroup)
        addGroupButton.grid(row=0, column=0, padx=30, pady=5, sticky="nsew")
        addAllGroupsButton = customtkinter.CTkButton(buttonsFrame, text="Add All Groups", height=2, width=2, command=self.addAllGroups)
        addAllGroupsButton.grid(row=1, column=0, padx=30, pady=5, sticky="nsew")

        removeGroupButton = customtkinter.CTkButton(buttonsFrame, text="Remove Group", height=2, width=2, command=self.removeGroup)
        removeGroupButton.grid(row=0, column=1, padx=30, pady=5, sticky="nsew")
        removeAllGroupsButton = customtkinter.CTkButton(buttonsFrame, text="Remove All Groups", height=2, width=2, command=self.removeAllGroups)
        removeAllGroupsButton.grid(row=1, column=1, padx=30, pady=5, sticky="nsew")

        addImageButton = customtkinter.CTkButton(buttonsFrame, text="Add Image", height=2, width=2, command=self.addImage)
        addImageButton.grid(row=2, column=0, padx=30, pady=5, sticky="nsew")
        removeImageButton = customtkinter.CTkButton(buttonsFrame, text="Remove Image", height=2, width=2, command=self.removeImage)
        removeImageButton.grid(row=2, column=1, padx=30, pady=5, sticky="nsew")

        self.textBox = customtkinter.CTkTextbox(self, width=250)
        self.textBox.configure(state="disabled")
        self.textBox.grid(row=5, padx=15, pady=5, sticky="nsew")

        self.imageFrame = customtkinter.CTkFrame(self)
        self.imageFrameLabel = customtkinter.CTkLabel(self.imageFrame, width=200)
        self.imageFrameLabel.grid_forget()

        startPostingButton = customtkinter.CTkButton(self, height=2, width=2, text="Start Posting", command=self.startPosting)
        startPostingButton.grid(row=6, padx=100, pady=5, sticky="nsew")


    def getGroupsList(self):
        self.groupsList = [file.name for file in os.scandir("groups") if file.is_file() and file.name.endswith('.list')]


    def refreshGroupList(self):
        self.getGroupsList()
        self.groupSelectionBox.configure(values=self.groupsList)


    def addGroup(self):
        selected_group = self.groupSelectionBox.get()
        if selected_group not in self.postingGroupsString and selected_group in self.groupsList:
            self.postingGroupsString += f"{selected_group}\n"
            self.update_groups_text()


    def addAllGroups(self):
        for group in self.groupsList:
            if group not in self.postingGroupsString:
                self.postingGroupsString += f"{group}\n"
        self.update_groups_text()


    def removeGroup(self):
        selected_group = self.groupSelectionBox.get()
        if selected_group in self.postingGroupsString:
            self.postingGroupsString = self.postingGroupsString.replace(f"{selected_group}\n", "")
            self.update_groups_text()


    def removeAllGroups(self):
        self.postingGroupsString = ""
        self.update_groups_text()


    def addImage(self):
        self.imagePath = customtkinter.filedialog.askopenfile(initialdir="%homepath%\Desktop", title="Select an Image File", filetypes=(("Image Files", "*.jpg *.png"), ("all files", "*.*")))
        self.imagePath = self.imagePath.name

        self.imageFrame.grid_forget()
        self.imageFrameLabel.grid_forget()

        self.imageFrame.grid(row=4, padx=15, pady=5, sticky="nsew")
        self.imageFrameLabel = customtkinter.CTkLabel(self.imageFrame, width=200, text=os.path.basename(self.imagePath))
        self.imageFrameLabel.grid(padx=20, pady=5, sticky="w")

        self.geometry("350x505")


    def removeImage(self):
        self.imagePath = ""
        self.imageFrame.grid_forget()
        self.imageFrameLabel.grid_forget()
        self.geometry("350x455")


    def startPosting(self):
        postText, groups, email, password = grabData(self.groupsList, self.imagePath)
        postToGroups(postText, groups, self.imagePath, email, password)


    def update_groups_text(self):
        self.textBox.configure(state="normal")
        self.textBox.delete("0.0", customtkinter.END)
        self.textBox.insert("0.0", self.postingGroupsString)
        self.textBox.configure(state="disabled")


if __name__ == "__main__":
    checkChromeDriver()
    checkFilesExist()

    app = App()
    app.mainloop()
