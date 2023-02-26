# MassFacebookGroupPoster

Mass Facebook group poster is a program that will post any message you want to any amount of groups you wish to post too.

This program will run in the open background, allowing you to do anything while the program is running.

## How to use

### MUST KNOW FIX:
If you launch the program, and it closes right away after trying to open chrome, and you know 100% that everything was inputted correctly, the file 'chromedriver.exe' may be out of date. Go to https://chromedriver.chromium.org/downloads, and select your chrome version (To find: Three Dots -> Help -> About Google Chrome), then download the chromedriver for your operating system.

### Before Launching Program:
Make sure you use the command `pip install -r requirements.txt` in terminal first.

Before launching the program, you must change the emailText and passwordText values in the program, to allow the program to login on the Facebook website with your email and password.

The emailText variable is located on line 74, and you must input your email inbetween the double quotation marks.

The passwordText variable is located on line 75, and you must input your password inbetween the double quotation marks.

### How to Add Groups:
You add Facebook groups by pasting them into the file called 'groups.list', if your computer asks what to open the file with, choose notepad.exe, as the file is just a text file.

### How to Edit Post Message:
To edit your post message, type what you want to post into the file 'postText.txt'. Spaces, special chars, newlines are all okay, write the message as your normally would on Facebook.

### How to Launch Program:
Make sure 'groups.list', 'postText.txt', and 'chromedriver.exe' are all in the same dir as 'MFGP.py'. To launch the program, just double click 'MFGP.py' or use the command `python MFGP.py` in terminal.
